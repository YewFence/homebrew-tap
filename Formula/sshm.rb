# typed: false
# frozen_string_literal: true

# CLI to manage ~/.ssh/config easily
class Sshm < Formula
  desc "CLI to manage ~/.ssh/config easily"
  homepage "https://github.com/YewFence/ssh-config-manager"
  version "0.0.6"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-arm64.zip"
      sha256 "3125056af7f775077d62e506cb5ba4a094bccb9bff525e0e8214f6b3d9a04552"

      define_method(:install) do
        bin.install "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-amd64.zip"
      sha256 "8e857513a6f5ae923eaa75947b88f46134f8cf7396bc13cf5ce83634ade8ff30"

      define_method(:install) do
        bin.install "sshm"
      end
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-arm64.zip"
      sha256 "84fb2fbc4b937af4b1111abda25916173c7d17f9bda8b3c85958bdcf2e010759"

      define_method(:install) do
        bin.install "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-amd64.zip"
      sha256 "face1ddc9b13356f53484bb95127c0857e6b514c07866b49b1dc0926e819a844"

      define_method(:install) do
        bin.install "sshm"
      end
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin} --version")
  end
end
