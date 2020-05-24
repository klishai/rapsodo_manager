#!/usr/bin/ruby
require 'cgi'
require 'cgi/session'
require './login_cert.rb'

cgi = CGI.new
session = CGI::Session.new(cgi)
l=Login.new(cgi, session)
l.login_process()
m = CGI.escapeHTML(l.message)
if session["id"]
  puts cgi.header({'status' => 'REDIRECT',
                   'Location' => 'menu.cgi'})
end

puts <<-EOS
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
  </head>
  <body>
    <main class="login-form">
      <div class="cotainer">
        <div class="row justify-content-center">
            <div class="col-md-8">
		<p>#{m}</p>
                <div class="card">
                    <div class="card-header">ログイン</div>
                    <div class="card-body">
                        <form action="" method="post">
                            <div class="form-group row">
                                <label for="username" class="col-md-4 col-form-label text-md-right">Username (英数字3~8文字)</label>
                                <div class="col-md-6">
                                    <input type="text" id="username" class="form-control" name="username" required autofocus>
                                </div>
                            </div>

                            <div class="form-group row">
                                <label for="password" class="col-md-4 col-form-label text-md-right">Password (英数記号全て含む8~16文字)</label>
                                <div class="col-md-6">
                                    <input type="password" id="password" class="form-control" name="password" required>
                                </div>
                            </div>

                            
                            <div class="col-md-6 offset-md-4">
                                <button type="submit" class="btn btn-primary">
                                    ログイン
                                </button>
                                <a href="register.cgi" class="btn btn-link">
                                    新規登録
                                </a>
                            </div>
                    </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    </div>

</main>
  </body>
</html>

EOS
