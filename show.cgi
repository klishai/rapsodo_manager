#!/usr/bin/ruby
#encoding:UTF-8
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
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
<p>データ表示</p>
EOS
l.searchform
l.lookup
l.show_table
puts <<-EOS
</body>
</html>
EOS
