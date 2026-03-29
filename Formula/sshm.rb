# typed: false
# frozen_string_literal: true

# CLI to manage ~/.ssh/config easily
class Sshm < Formula
  desc "CLI to manage ~/.ssh/config easily"
  homepage "https://github.com/YewFence/ssh-config-manager"
  version "0.0.5"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-arm64"
      sha256 "a1fc8f8d12229f1f75ba351e1949ed82d977611b508e9e23a2411f0e48c77815"

      define_method(:install) do
        bin.install "sshm-v#{version}-macos-arm64" => "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-macos-amd64"
      sha256 "8ff8f749daf4b947fa71fcfbd5fd16fe435590ff7ac73cf3f532382915e6c27a"

      define_method(:install) do
        bin.install "sshm-v#{version}-macos-amd64" => "sshm"
      end
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-arm64"
      sha256 "fe1ae5fbaeec009e085b058a2f767b6fc7601940dd7f0c868189878ef4ad160b"

      define_method(:install) do
        bin.install "sshm-v#{version}-linux-arm64" => "sshm"
      end
    end
    on_intel do
      url "https://github.com/YewFence/ssh-config-manager/releases/download/v#{version}/sshm-v#{version}-linux-amd64"
      sha256 "47e329f1ab86fca9bbe67a322ee9b4551ac1e8c90b134313f4d4dd22761f36fe"

      define_method(:install) do
        bin.install "sshm-v#{version}-linux-amd64" => "sshm"
      end
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin} --version")
  end
end
