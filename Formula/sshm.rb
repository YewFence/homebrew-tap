# typed: false
# frozen_string_literal: true

# CLI to manage ~/.ssh/config easily
class Sshm < Formula
  desc "CLI to manage ~/.ssh/config easily"
  homepage "https://github.com/YewFence/ssh-config-manager"
  version "0.1.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-arm64.zip"
      sha256 "c9bced14f320304fad1160df4be82705b404e5e57c7719c276bbd8e3bc30564a"

      define_method(:install) do
        bin.install "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-amd64.zip"
      sha256 "2aaabe8f4e016db16904b6350c4f7c0d0404b75402103e653f2b34aed8ba6eeb"

      define_method(:install) do
        bin.install "sshm"
      end
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-arm64.zip"
      sha256 "92512205ff05e525fe1c24feb76a8fed49b59199845e65560aee182c3aa02fb0"

      define_method(:install) do
        bin.install "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-amd64.zip"
      sha256 "ede98971be1e8ee8fba5a8a920bbdb02a8cef714fa98082d4f838cf27890d6ca"

      define_method(:install) do
        bin.install "sshm"
      end
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin} --version")
  end
end
