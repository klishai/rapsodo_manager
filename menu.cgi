#!/usr/bin/ruby
require 'cgi'
require 'cgi/session'

cgi = CGI.new
session = CGI::Session.new(cgi)
if ! session["id"]
  puts cgi.header({'status' => 'REDIRECT',
                   'Location' => 'login.cgi'})
end

puts <<-EOS if session["id"]
Content-type: text/html

<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>メニュー | Rapsodo Manager</title>
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
    
    <link rel="stylesheet" href="css/menu.css">
  </head>
  　
<body>
  <div class="cover">
    <header>
      <h1 class="text-center">#{session["username"]}さん、ようこそ！</h1>
    </header>
  <main>
  </div>
    <div class="container text-center">
     <div class="row">
      <div class="col-sm-8 col-sm-offset-2">
       <a href="edit.cgi" role="button" class="btn btn-primary btn-lg" id="a1" >データを編集</a>
      </div>
      <div class="col-sm-8 col-sm-offset-2">
       <a href="show.cgi" role="button" class="btn btn-success btn-lg" id="a2" >データを閲覧</a>
      </div>
      <div class="col-sm-8 col-sm-offset-2">
       <a href="logout.cgi" role="button" class="btn btn-danger btn-lg ">ログアウト</a> 
      </div>
    </div>
  </div>
 </main>
</body>

</html>

EOS
