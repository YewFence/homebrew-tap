#!/usr/bin/env python3
"""
update_formula.py — 从 GitHub Releases 更新 Homebrew formula 文件

用法：
  python3 scripts/update_formula.py --config formulas.yml --formula infisical
  python3 scripts/update_formula.py --config formulas.yml --formula infisical --version 1.2.3
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import socket
import sys
import urllib.error
import urllib.request

# Try to use PyYAML, fallback to yq if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def load_config(config_file: str, formula_name: str) -> dict:
    """加载 formulas.yml 中指定 formula 的配置。"""
    if not re.match(r'^[a-zA-Z0-9_-]+$', formula_name):
        print(f"ERROR: invalid formula name '{formula_name}'", file=sys.stderr)
        sys.exit(1)

    if HAS_YAML:
        # Use PyYAML for safer parsing
        with open(config_file) as f:
            data = yaml.safe_load(f)
        for formula in data.get("formulas", []):
            if formula.get("name") == formula_name:
                return formula
        print(f"ERROR: formula '{formula_name}' not found in {config_file}", file=sys.stderr)
        sys.exit(1)
    else:
        # Fallback to yq with safe --arg usage
        result = subprocess.run(
            ["yq", "--arg", "name", formula_name, "-o=json", ".formulas[] | select(.name == $name)", config_file],
            capture_output=True, text=True, check=True,
        )
        if not result.stdout.strip():
            print(f"ERROR: formula '{formula_name}' not found in {config_file}", file=sys.stderr)
            sys.exit(1)
        return json.loads(result.stdout)


def gh_get(url: str) -> dict:
    """带认证的 GitHub API GET 请求。"""
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} for {url}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except (urllib.error.URLError, socket.timeout, socket.error) as e:
        print(f"ERROR: network error for {url}: {e}", file=sys.stderr)
        sys.exit(1)


def get_latest_version(repo: str, tag_prefix: str) -> str:
    """从 GitHub Releases API 获取最新版本号，并去掉 tag 前缀。"""
    data = gh_get(f"https://api.github.com/repos/{repo}/releases/latest")
    tag = data.get("tag_name", "")
    if not tag:
        print(f"ERROR: no tag_name in latest release for {repo}", file=sys.stderr)
        sys.exit(1)
    return tag.removeprefix(tag_prefix)


def get_current_version(formula_file: str) -> str:
    """从 formula 文件中读取当前版本，文件不存在则返回空字符串。"""
    if not os.path.exists(formula_file):
        return ""
    with open(formula_file) as f:
        for line in f:
            m = re.match(r'^  version "([^"]+)"', line)
            if m:
                return m.group(1)
    return ""


def create_formula_skeleton(formula_file: str, formula_name: str, repo: str, platforms: list, tag_prefix: str) -> str:
    """当 formula 文件不存在时，创建一个骨架文件。"""
    class_name = "".join(part.capitalize() for part in re.split(r"[-_]", formula_name))

    # 生成每个平台的块
    platform_blocks = []
    os_groups = {}

    # 按 os 分组
    for p in platforms:
        os_key = p["rb_os_block"]
        if os_key not in os_groups:
            os_groups[os_key] = []
        os_groups[os_key].append(p)

    for os_name, os_platforms in os_groups.items():
        cpu_blocks = []
        for p in os_platforms:
            cpu = p["rb_cpu"]
            cpu_blocks.append(f"""    if Hardware::CPU.{cpu}?
      url "PLACEHOLDER_URL"
      sha256 "PLACEHOLDER_SHA256"
    end""")

        cpu_block_str = "\n".join(cpu_blocks)
        platform_blocks.append(f"""  on_{os_name} do
{cpu_block_str}
  end""")

    platform_str = "\n\n".join(platform_blocks)

    skeleton = f'''class {class_name} < Formula
  desc "Auto-generated formula for {formula_name}"
  homepage "https://github.com/{repo}"
  version "0.0.0"
  license "MIT"

{platform_str}

  def install
    bin.install "{formula_name}"
  end

  test do
    system "#{{bin}}/{formula_name}", "--version"
  end
end
'''
    # 确保目录存在
    os.makedirs(os.path.dirname(formula_file), exist_ok=True)
    with open(formula_file, "w") as f:
        f.write(skeleton)
    print(f"Created formula skeleton: {formula_file}")
    return skeleton


def download_and_sha256(url: str) -> str:
    """下载文件并计算 SHA256 哈希值。"""
    print(f"  Downloading {url}")
    req = urllib.request.Request(url)
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:  # longer timeout for asset downloads
            data = resp.read()
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} for {url}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except (urllib.error.URLError, socket.timeout, socket.error) as e:
        print(f"ERROR: network error for {url}: {e}", file=sys.stderr)
        sys.exit(1)
    if not data:
        print(f"ERROR: empty response from {url}", file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(data).hexdigest()
    print(f"  sha256={digest}")
    return digest


def patch_formula(content: str, rb_os: str, rb_cpu: str, new_url: str, new_sha256: str) -> str:
    """在内存中替换 rb 文件里指定 on_{os}/Hardware::CPU.{cpu}? 块的 url 和 sha256，返回修改后的内容。"""
    os_m = re.search(rf"(  on_{rb_os}\s+do\b.*?^  end\b)", content, re.DOTALL | re.MULTILINE)
    if not os_m:
        print(f"ERROR: on_{rb_os} block not found in formula", file=sys.stderr)
        sys.exit(1)

    os_block = os_m.group(0)
    cpu_m = re.search(
        rf"(if Hardware::CPU\.{rb_cpu}\?.*?)(?=\n    if Hardware::CPU|\n  end\b)",
        os_block, re.DOTALL,
    )
    if not cpu_m:
        print(f"ERROR: Hardware::CPU.{rb_cpu}? not found in on_{rb_os}", file=sys.stderr)
        sys.exit(1)

    patched = cpu_m.group(0)
    patched = re.sub(r'url "[^"]*"', f'url "{new_url}"', patched)
    patched = re.sub(r'sha256 "[^"]*"', f'sha256 "{new_sha256}"', patched)

    new_os_block = os_block[:cpu_m.start()] + patched + os_block[cpu_m.end():]
    content = content[:os_m.start()] + new_os_block + content[os_m.end():]
    print(f"  Patched on_{rb_os}/CPU.{rb_cpu}?")
    return content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--formula", required=True)
    parser.add_argument("--version", default="")
    args = parser.parse_args()

    cfg           = load_config(args.config, args.formula)
    required = ["repo", "formula_file", "asset_pattern", "platforms"]
    missing = [k for k in required if k not in cfg]
    if missing:
        print(f"ERROR: missing required fields in config: {missing}", file=sys.stderr)
        sys.exit(1)
    repo          = cfg["repo"]
    formula_file  = cfg["formula_file"]
    asset_pattern = cfg["asset_pattern"]
    tag_prefix    = cfg.get("tag_prefix", "v")
    platforms     = cfg["platforms"]

    # 校验每个平台的必需字段
    required_platform_keys = ["os", "arch", "rb_os_block", "rb_cpu"]
    for i, p in enumerate(platforms):
        p_missing = [k for k in required_platform_keys if k not in p]
        if p_missing:
            print(f"ERROR: platform[{i}] missing required fields: {p_missing}", file=sys.stderr)
            sys.exit(1)

    # 如果 formula 文件不存在，创建骨架
    if not os.path.exists(formula_file):
        create_formula_skeleton(formula_file, args.formula, repo, platforms, tag_prefix)

    current = get_current_version(formula_file)
    new_ver = args.version or get_latest_version(repo, tag_prefix)

    print(f"{args.formula}: current={current}  latest={new_ver}")
    if current == new_ver:
        print(f"{args.formula}: already up to date, skipping.")
        sys.exit(0)

    # 读取 formula 文件内容，在内存中完成所有修改后再一次写入，避免部分写入
    with open(formula_file) as f:
        content = f.read()

    for p in platforms:
        pattern = p.get("asset_pattern", asset_pattern)  # platform 级别可覆盖默认值
        asset = (pattern
                 .replace("{version}", new_ver)
                 .replace("{os}", p["os"])
                 .replace("{arch}", p["arch"]))
        url = f"https://github.com/{repo}/releases/download/{tag_prefix}{new_ver}/{asset}"
        sha256 = download_and_sha256(url)
        content = patch_formula(content, p["rb_os_block"], p["rb_cpu"], url, sha256)

    # 更新顶层 version 字段（只匹配类级别的 version，即行首有2空格缩进）
    content = re.sub(r'^  version "[^"]*"', f'  version "{new_ver}"', content, flags=re.MULTILINE)

    with open(formula_file, "w") as f:
        f.write(content)

    print(f"{args.formula}: updated to {new_ver}")


if __name__ == "__main__":
    main()
