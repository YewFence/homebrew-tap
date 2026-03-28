# typed: false
# frozen_string_literal: true

class Sshm < Formula
  desc "CLI to manage ~/.ssh/config easily"
  homepage "https://github.com/YewFence/ssh-config-manager"
  version "0.0.2"
  license "MIT"


  test do
    assert_match version.to_s, shell_output("#{bin} --version")
  end
end
