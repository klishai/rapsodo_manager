#!/usr/bin/ruby
require 'cgi'
require 'cgi/session'
require './lib/login_cert.rb'

cgi = CGI.new
session = CGI::Session.new(cgi)
l = Login.new(cgi, session)
l.login_process()
m = CGI.escapeHTML(l.message)
if session["id"]
  puts cgi.header({'status' => 'REDIRECT',
                   'Location' => 'menu.cgi'})
end

puts <<-EOS if ! session["id"]
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
     <div class="row">
      <div class="col-sm-8 col-sm-offset-2 text-center">
       <img src ="img/logo.png">
      </div>
    </header>

    <main class="login-form">
      <div class="container">
        <form action=""  method="post" class="row" >
           <div class="col-sm-8 col-sm-offset-2">
             <p>#{m}</p>
             <div class="form-group">
               <label for="username"id="a1" >Username (英数字3~8文字) <span class="label label-danger">必須</span></label>
                 <input type="text" id="username" class="form-control" name="username" required autofocus>             
               <label for="password"id="a2" >Password (英数記号全て含む8~16文字) <span class="label label-danger">必須</span></label>
                 <input type="password" id="password" class="form-control" name="password" required>
             </div>             
                        

                     
              <button type="submit" class="btn btn-primary"> ログイン </button> 	
	     <button type="button" class="btn btn-link"> <a href="register.cgi"> 新規登録 </a></buttom>
         
          </div>
        </form>
       </div>
     </main>
      
   <footer>
     <p class="text-center"><a href="index.html">ホームへ戻る</p>
   </footer>
  </body>
</html>

EOS
