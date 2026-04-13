# typed: false
# frozen_string_literal: true

# CLI to manage ~/.ssh/config easily
class SshmAT006 < Formula
  desc "CLI to manage ~/.ssh/config easily"
  homepage "https://github.com/YewFence/ssh-config-manager"
  version "0.0.6"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-arm64.zip"
      sha256 "cf84f33557433d399cc3413311a24bb7748f5d03ba9f3b839c243af4c222221e"

      define_method(:install) do
        bin.install "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-amd64.zip"
      sha256 "211336affdbe9f1f1528498eefffdf2522cdd68a87078df6cac62d68611a8640"

      define_method(:install) do
        bin.install "sshm"
      end
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-arm64.zip"
      sha256 "4e5dcb8afe324239116b222cfbeb3b181ee67c7303e8ef72ff02a84cebfd6e4d"

      define_method(:install) do
        bin.install "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-amd64.zip"
      sha256 "16bcf3195c42775645db8857a1061f01ba0c29c00735738308f5d54c6241005a"

      define_method(:install) do
        bin.install "sshm"
      end
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin} --version")
  end
end
