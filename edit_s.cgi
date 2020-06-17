#!/usr/bin/ruby
#encoding:UTF-8
require 'cgi'
require 'cgi/session'
require './lib/edit.rb'

cgi = CGI.new
session = CGI::Session.new(cgi)
# session["id"] = 1
unless session["id"]
  puts cgi.header({'status' => 'REDIRECT', 'Location' => 'login.cgi'})
else
  l = Edit.new(cgi, session)
  table = l.show_only_table(cgi["id"])
end

puts <<-EOS if session["id"]
Content-type: text/html

<!DOCTYPE HTML>
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>詳細編集 | Rapsodo Manager</title>
<link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico">
</head>
<body>

<p>ようこそ#{session["username"]}さん<br>
   チーム: #{session["tname"]}</p>
<h1>データ詳細編集</h1>
<input type="button" onClick="location.href='edit.cgi'" value="戻る">
<div class="container">
<p class="message">#{cgi["message"].gsub('br', '<br>')}</p>
<form
        class="row"
        method="post"
        action="lib/form_submit.cgi">
#{table}
<table>
<tr>
  <td colspan="3">
  <input type="reset" value="元の値に戻す">
  <input type="submit" value="更新">
  <input type="submit" name="delete" value="削除">
  </td>
</tr>
</table>
</form>
</div>
</body>
</html>
EOS
