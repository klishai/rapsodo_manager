#!/usr/bin/ruby
require 'cgi'
require 'cgi/session'
require "./lib/Edit.rb"

cgi = CGI.new
session = CGI::Session.new(cgi)
e = Edit.new(cgi, session)
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
    <title>編集 | Rapsodo Manager</title>
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
  </head>
  <body>
   <h1>#{session["username"]}さん、ようこそ！</h1>
   <p>#{e.list}</p>
  </body>
</html>

EOS
