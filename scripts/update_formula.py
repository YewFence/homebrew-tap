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
import sys
import urllib.error
import urllib.request


def load_config(config_file: str, formula_name: str) -> dict:
    result = subprocess.run(
        ["yq", "-o=json", f'.formulas[] | select(.name == "{formula_name}")', config_file],
        capture_output=True, text=True, check=True,
    )
    if not result.stdout.strip():
        print(f"ERROR: formula '{formula_name}' not found in {config_file}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def gh_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_latest_version(repo: str, tag_prefix: str) -> str:
    data = gh_get(f"https://api.github.com/repos/{repo}/releases/latest")
    tag = data.get("tag_name", "")
    if not tag:
        print(f"ERROR: no tag_name in latest release for {repo}", file=sys.stderr)
        sys.exit(1)
    return tag.removeprefix(tag_prefix)


def get_current_version(formula_file: str) -> str:
    with open(formula_file) as f:
        for line in f:
            m = re.search(r'version "([^"]+)"', line)
            if m:
                return m.group(1)
    print(f"ERROR: version field not found in {formula_file}", file=sys.stderr)
    sys.exit(1)


def download_and_sha256(url: str) -> str:
    print(f"  Downloading {url}")
    req = urllib.request.Request(url)
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} for {url}", file=sys.stderr)
        sys.exit(1)
    if not data:
        print(f"ERROR: empty response from {url}", file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(data).hexdigest()
    print(f"  sha256={digest}")
    return digest


def patch_formula(formula_file: str, rb_os: str, rb_cpu: str, new_url: str, new_sha256: str):
    """替换 rb 文件里指定 on_{os}/Hardware::CPU.{cpu}? 块的 url 和 sha256"""
    with open(formula_file) as f:
        content = f.read()

    os_m = re.search(rf"(  on_{rb_os}\s+do\b.*?^  end\b)", content, re.DOTALL | re.MULTILINE)
    if not os_m:
        print(f"ERROR: on_{rb_os} block not found in {formula_file}", file=sys.stderr)
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

    with open(formula_file, "w") as f:
        f.write(content)
    print(f"  Patched on_{rb_os}/CPU.{rb_cpu}?")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--formula", required=True)
    parser.add_argument("--version", default="")
    args = parser.parse_args()

    cfg           = load_config(args.config, args.formula)
    repo          = cfg["repo"]
    formula_file  = cfg["formula_file"]
    asset_pattern = cfg["asset_pattern"]
    tag_prefix    = cfg.get("tag_prefix", "v")
    platforms     = cfg["platforms"]

    current = get_current_version(formula_file)
    new_ver = args.version or get_latest_version(repo, tag_prefix)

    print(f"{args.formula}: current={current}  latest={new_ver}")
    if current == new_ver:
        print(f"{args.formula}: already up to date, skipping.")
        sys.exit(0)

    for p in platforms:
        pattern = p.get("asset_pattern", asset_pattern)  # platform 级别可覆盖默认值
        asset = (pattern
                 .replace("{version}", new_ver)
                 .replace("{os}", p["os"])
                 .replace("{arch}", p["arch"]))
        url = f"https://github.com/{repo}/releases/download/{tag_prefix}{new_ver}/{asset}"
        sha256 = download_and_sha256(url)
        patch_formula(formula_file, p["rb_os_block"], p["rb_cpu"], url, sha256)

    # 更新顶层 version 字段
    with open(formula_file) as f:
        content = f.read()
    content = re.sub(r'version "[^"]*"', f'version "{new_ver}"', content)
    with open(formula_file, "w") as f:
        f.write(content)

    print(f"{args.formula}: updated to {new_ver}")


if __name__ == "__main__":
    main()
