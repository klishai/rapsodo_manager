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
<p>ようこそ！検索ワードを入力してください。</p>
<p>#{l.confirm_get_param["key"]}</p>                         
<p>#{l.confirm_get_param}</p>
<p>
<form method="GET" action="">
キーワード: <input type="text" name="key" size="50"><br>
</p>
<p>
<input type="submit" value="送信">
<input type="reset" value="リセット">
</p>
</form>
EOS

l.lookup
l.show_table
puts <<-EOS
</body>
</html>
EOS
