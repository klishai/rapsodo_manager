#!/usr/bin/ruby
# frozen_string_literal: true

require 'cgi'
require 'cgi/session'
require './lib/login_cert.rb'

cgi = CGI.new
session = CGI::Session.new(cgi)
l = Login.new(cgi, session)
l.login_process
m = CGI.escapeHTML(l.message)
if session['id']
  puts cgi.header({ 'status' => 'REDIRECT',
                    'Location' => 'menu.cgi' })
end

puts <<~EOS unless session['id']
  Content-type: text/html
  
  <!DOCTYPE html>
  <html lang="ja">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <title>ログイン | Rapsodo Manager</title>
      <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
      <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
      <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
      
    <link rel="stylesheet" href="css/login.css">
    <link rel="icon" href="img/favicon.ico">
    </head>
    <body>
    <header>
      <div cover>
        <h1 id="b1"><img src ="img/logo.png" width="100" hight="50" id="b2">Rapsodo&nbsp;Manager</h1>
      </div>
    </header>
    <main class="login-form">
      <div class="container">
        <form action=""  method="post" class="row" >
          <div class="col-sm-8 col-sm-offset-2">
            <p class="new text-center">ログイン</p>
            <p class="text-danger">#{m}</p>
            <div class="form-group">
              <label for="username"id="a1" >Username (英数字3~8文字) <span class="label label-danger">必須</span></label>
              <input type="text" id="username" class="form-control" name="username" required autofocus>             
              <label for="password"id="a2" >Password (英数記号全て含む8~16文字) <span class="label label-danger">必須</span></label>
              <input type="password" id="password" class="form-control" name="password" required>
            </div>             
            <div class="text-center">             
              <button type="submit" class="btn btn-primary"> ログイン </button> 	
            </div>
          </div>
        </form>
      </div>
    </main>
        
    <footer class="text-center">
      <a href="register.cgi" class="btn btn-link">新規登録ページへ</a>
      <a href="index.html" class="btn btn-link">ホームへ戻る</a>
    </footer>
     
    </body>
  </html>
EOS
