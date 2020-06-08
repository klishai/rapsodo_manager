#!/usr/bin/ruby
require 'cgi'
require 'cgi/session'
require "./lib/register_cert.rb"

cgi = CGI.new
r = Register.new(cgi)

f = r.register?

if f
  puts cgi.header({'status' => 'REDIRECT',
                 'Location' => 'login.cgi'})
end

m = CGI.escapeHTML(r.message)

puts <<-EOS if ! f
Content-type: text/html

<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>新規作成 | Rapsodo Manager</title>
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
    <link rel="stylesheet" href="css/register.css">
    <link rel="icon" href="img/favicon.ico">
  </head>
 
  <body>
   <header>
    <div class="row">
      <div class="col-sm-8 col-sm-offset-2 text-center">
       <img src ="img/logo.png">
     </div>
    </header>
     
     <main class="register-form">
       <div class="container">
        <form action="" method="post" class="row">
          <div class="col-sm-8 col-sm-offset-2">
　　　　　 <p class="new text-center">新規登録</p>             
         　 <p>#{m}</p>
            <div class="form-group">
              <label for="username id="a1">Username (英数字3~8文字) <span class="label label-danger">必須</span></label>
                <input type="text" id="username" class="form-control" name="username" required autofocus>          
              <label for="team" id="a2">Teamname (1文字以上) <span class="label label-danger">必須</span></label>
                <input type="text" id="teamname" class="form-control" name="teamname" required>
              <label for="password" id="a3">Password (英数記号全て含む8~16文字) <span class="label label-danger">必須</span></label>
                <input type="password" id="password" class="form-control" name="password" required>
             </div>                                
               
              <div class="text-center">    
                <button type="submit" class="btn btn-primary text-center">新規登録 </button>
              </div>        
          </div>
        </form>
        </div>
       
          <footer class="text-center">
          　<p><a href="login.cgi" class="btn btn-link">ログインへ戻る</a>
               <a href="index.html" class="btn btn-link">ホームへ戻る</a></p>
          </footer>
                     
  </main>
 </body>
</html>

EOS
