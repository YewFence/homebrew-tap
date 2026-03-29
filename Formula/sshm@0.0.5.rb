# typed: false
# frozen_string_literal: true

# CLI to manage ~/.ssh/config easily
class SshmAT005 < Formula
  desc "CLI to manage ~/.ssh/config easily"
  homepage "https://github.com/YewFence/ssh-config-manager"
  version "0.0.5"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-arm64"
      sha256 "15aa8dbf6cd959969e00a501dbc3fe9111ed6083256ddb8849a8e5e42be37608"

      define_method(:install) do
        bin.install "sshm-v#{version}-macos-arm64" => "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-amd64"
      sha256 "3ea79579250098e3d36567d2346bacd15d29a2054a397620c54737a557608611"

      define_method(:install) do
        bin.install "sshm-v#{version}-macos-amd64" => "sshm"
      end
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-arm64"
      sha256 "e8bb68c708bb841cbc0eac42cd3f9ad182f0bbde74939ec5f1a4bc1fab7f4b81"

      define_method(:install) do
        bin.install "sshm-v#{version}-linux-arm64" => "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-amd64"
      sha256 "54198f8e7e0b7482e753e69311aa016ffaf05ffb6871606da98cdc58ed932d03"

      define_method(:install) do
        bin.install "sshm-v#{version}-linux-amd64" => "sshm"
      end
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin} --version")
  end
end
