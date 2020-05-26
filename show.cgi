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
<p>ようこそ！検索ワードを入力してください。</p>
<p>#{CGI.escapeHTML(cgi["key"])}</p>                         
<p>#{l.confirm_get_param}</p>
 
<form method="GET" action="">
キーワード: <input type="text" name="key" size="50"><br>
<input type="submit" value="送信">
<input type="reset" value="リセット">
</form>
EOS
l.show_table
puts <<-EOS
</body>
</html>
EOS
