#!/usr/bin/ruby
require "cgi"
require "cgi/session"

cgi = CGI.new
session = CGI::Session.new(cgi)
if ! session["id"]
  # セッション破棄してログイン画面へ
  session.delete
end

puts cgi.header({'status' => 'REDIRECT',
                 'Location' => 'login.cgi'}
