# typed: false
# frozen_string_literal: true

# CLI to manage ~/.ssh/config easily
class SshmAT004 < Formula
  desc "CLI to manage ~/.ssh/config easily"
  homepage "https://github.com/YewFence/ssh-config-manager"
  version "0.0.4"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-arm64"
      sha256 "e8465bfb94d661b212fddb01d5fae8f7c9052251976e34c82c131475e17bb593"

      define_method(:install) do
        bin.install "sshm-v#{version}-macos-arm64" => "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-amd64"
      sha256 "03c4d69fd5249448f624b66ab32e8525a5674085353769266c0043959530d507"

      define_method(:install) do
        bin.install "sshm-v#{version}-macos-amd64" => "sshm"
      end
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-arm64"
      sha256 "2c51e81473837562aad5c68f9b10b09534c341f023533bfc5333e59079a0e3e3"

      define_method(:install) do
        bin.install "sshm-v#{version}-linux-arm64" => "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-amd64"
      sha256 "0e88d09b804085304836b1fa5262b9076bdc67f81a1efaf71e3f60638ee27a2a"

      define_method(:install) do
        bin.install "sshm-v#{version}-linux-amd64" => "sshm"
      end
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin} --version")
  end
end
