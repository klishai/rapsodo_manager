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
else
  puts cgi.header({ 'status' => 'REDIRECT', 'Location' => 'login.cgi' })
end
puts <<~EOS if session['id']
  Content-type: text/html
  
  <!DOCTYPE HTML>
  <html lang="ja">
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <title>データ編集 | Rapsodo Manager</title>
  <script type="text/javascript" src="libjs/jquery-1.10.1.min.js"></script>
  <script 
    type="text/javascript"
    src="libjs/query.tablePagination.0.5.js"
  ></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pace/1.0.2/pace.min.js"></script>
  <link rel="stylesheet" href="css/styletable.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pace/1.0.2/themes/black/pace-theme-center-circle.min.css" />
  <link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
  <link rel="icon" href="img/favicon.ico">
  </head>
  <body>
  <header>
  <div cover class="mb-3 ml-3 mt-3">
    <h1 id="b1"><img src ="img/logo.png" width="100" hight="50" id="b2">Rapsodo&nbsp;Manager</h1>
  </div>
  </header>
  <div class="cover ml-3">
  <h1>データ編集</h1>
    <p>ようこそ#{session['username']}さん<br>
      チーム: #{session['tname']}</p>
    <input type="button" onClick="location.href='menu.cgi'" class="btn btn-outline-secondary" value="戻る">
    <input type="button" onClick="location.href='add.cgi'" class="btn btn-outline-secondary" value="データ新規追加">
  </div>
  
EOS
l.searchform
l.lookup
l.show_table
puts <<~EOS
  <script type="text/javascript">
    $(document).ready(function () {
      var options = {
        currPage: 1,
        optionsForRows: [20, 50, 100],
        rowsPerPage: 20,
      };
    $("table#showtable").tablePagination(options);
    });
  </script>
  </body>
  </html>
EOS
