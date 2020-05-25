#!/usr/bin/ruby
require 'cgi'
require 'cgi/session'
require './lib/show.rb'

cgi = CGI.new
session = CGI::Session.new(cgi)
session["id"] = 1
l = Show.new(cgi, session)
puts <<-EOS
Content-type: text/html

<!DOCTYPE HTML>
<html lang="ja">
<head>
  <meta charset="utf-8">
</head>
<body>
EOS
l.show_table
puts <<-EOS
</body>
</html>
EOS
