#!/usr/bin/ruby
# frozen_string_literal: true

require 'cgi'
require 'cgi/session'
require './lib/edit.rb'

cgi = CGI.new
session = CGI::Session.new(cgi)
# session["id"] = 1
if session['id']
  l = Edit.new(cgi, session)
  table = l.show_only_table(cgi['id'])
else
  puts cgi.header({ 'status' => 'REDIRECT', 'Location' => 'login.cgi' })
end

puts <<~EOS if session['id']
  Content-type: text/html
  
  <!DOCTYPE HTML>
  <html lang="ja">
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <title>詳細編集 | Rapsodo Manager</title>
  <link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
  <link rel="icon" href="img/favicon.ico">
  <link rel="stylesheet" href="css/add.css" />
  </head>
  <body>
  <header>
  <div cover class="mb-3 ml-3 mt-3">
    <h1 id="b1"><img src ="img/logo.png" width="100" hight="50" id="b2">Rapsodo&nbsp;Manager</h1>
  </div>
  </header>
  <div class="cover ml-3">
  <p>ようこそ#{session['username']}さん<br>
    チーム: #{session['tname']}</p>
  <h1>データ詳細編集</h1>
  <input type="button" onClick="location.href='edit.cgi'" class="btn btn-outline-secondary" value="戻る">
  </div>
  <div class="container">
    <div class="row">
      <div class="col-sm-4">
        <p class="message">#{cgi['message'].gsub('br', '<br>')}</p>
          <form
              class="row"
              method="post"
              action="lib/form_submit.cgi">
          #{table}
          <table>
          <tr>
            <td colspan="3">
            <input type="reset" class="btn btn-outline-primary mt-2" value="元の値に戻す">
            <input type="submit" class="btn btn-outline-primary mt-2" value="更新">
           <input type="submit" class="btn btn-outline-primary mt-2" name="delete" value="削除">
            </td>
          </tr>
          </table>
          </form>
      </div>
    </div>
  </div>
  </body>
  </html>
EOS
