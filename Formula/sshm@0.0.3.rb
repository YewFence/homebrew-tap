# typed: false
# frozen_string_literal: true

class SshmAT003 < Formula
  desc "CLI to manage ~/.ssh/config easily"
  homepage "https://github.com/YewFence/ssh-config-manager"
  version "0.0.3"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-arm64"
      sha256 "cebae480473a4219e942a5f0be19bcf4defa388e06ebe0f2ec526594499939be"

      def install
        bin.install "sshm-v#{version}-macos-arm64" => "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-amd64"
      sha256 "b9dcb29ee7356e1da3e05841c2a7ab4bd0ffdf91753a1565d30eeb024f698c0e"

      def install
        bin.install "sshm-v#{version}-macos-amd64" => "sshm"
      end
    end
  end
  on_linux do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-arm64"
      sha256 "2e465e0df23d0654f7b6ae6ea9b37ca9114bd427d5d3031e90bb27daa032c229"

      def install
        bin.install "sshm-v#{version}-linux-arm64" => "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-amd64"
      sha256 "a116b1335c80fca8f2d1ad4282db1e084ddbdad6d73bf7bc7d714fd9d5c1ca1f"

      def install
        bin.install "sshm-v#{version}-linux-amd64" => "sshm"
      end
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin} --version")
  end
end
