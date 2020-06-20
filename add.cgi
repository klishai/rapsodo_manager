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
  table = l.show_adddata_table
end

puts <<-EOS if session["id"]
Content-type: text/html

<!DOCTYPE HTML>
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>データ新規追加 | Rapsodo Manager</title>
<link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico">
<link rel="icon" href="img/favicon.ico">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
<link rel="stylesheet" href="css/add.css">
</head>
<body>
<header>
   <div class="container-fluid">
    <div class="row">
      <div class="col-sm-1">
       <img src ="img/logo.png" width="100" hight="50" id="b2">
       </div>
       <div class="row">
        <div class="col-sm-5 offset-sm-2">
       <h1 id="b1">Rapsodo&nbsp;Manager</h1>
     </div>
 </header>
<div class="container-fluid mt-2 mb-2">
<p>ようこそ#{session["username"]}さん<br>
   チーム: #{session["tname"]}</p>
<h1>データ詳細編集</h1>
<input type="button" onClick="location.href='edit.cgi'" value="戻る">
</div>
<div class="container">
 <div class="row">
  <div class="col-sm-3">
<p class="message">#{cgi["message"].gsub('br', '<br>')}</p>
<form
        class="row"
        method="post"
        action="lib/form_submit.cgi">
#{table}
<table>
<tr>
  <td colspan="2">
  <input type="reset" value="リセット">
  <input type="submit" value="追加">
  </td>
</tr>
</table>
</form>
</div>
</body>
</html>
EOS
