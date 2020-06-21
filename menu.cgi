#!/usr/bin/ruby
# frozen_string_literal: true

require 'cgi'
require 'cgi/session'

cgi = CGI.new
session = CGI::Session.new(cgi)
unless session['id']
  puts cgi.header({ 'status' => 'REDIRECT',
                    'Location' => 'login.cgi' })
end

puts <<~EOS if session['id']
  Content-type: text/html
  
  <!DOCTYPE html>
  <html lang="ja">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <title>メニュー | Rapsodo Manager</title>
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
      <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
      
      <link rel="stylesheet" href="css/menu.css">
    </head>
    　
  <body>
  <header>
  <div cover class="mb-3 ml-3">
    <h1 id="b1"><img src ="img/logo.png" width="100" hight="50" id="b2">Rapsodo&nbsp;Manager</h1>
  </div>
  </header>
    <div class="cover">
      <header>
        <h1 class="text-center">#{session['username']}さん、ようこそ！</h1>
      </header>
    </div>
    <main>
      <div class="container text-center">
        <a href="edit.cgi" role="button" class="btn btn-primary btn-lg" id="a1" >データを編集</a>
        <a href="show.cgi" role="button" class="btn btn-success btn-lg" id="a2" >データを閲覧</a>
        <a href="logout.cgi" role="button" class="btn btn-danger btn-lg">ログアウト</a> 
      </div>
    </main>
  </body>
  
  </html>
  
EOS
