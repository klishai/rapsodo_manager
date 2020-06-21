#!/usr/bin/ruby
# frozen_string_literal: true

require 'cgi'
require 'cgi/session'
require './lib/show.rb'

cgi = CGI.new
session = CGI::Session.new(cgi)
# session["id"] = 1
if session['id']
  l = Show.new(cgi, session)
else
  puts cgi.header({ 'status' => 'REDIRECT', 'Location' => 'login.cgi' })
end

puts <<~HTML if session['id']
  Content-type: text/html
  
  <!DOCTYPE HTML>
  <html lang="ja">
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <script type="text/javascript" src="libjs/jquery-1.10.1.min.js"></script>
  <script 
   type="text/javascript"
   src="libjs/query.tablePagination.0.5.js"
  ></script>
  <link rel="stylesheet" href="css/styletable.css" />
  <script src="libjs/highcharts.src.js"></script>
  <script src="libjs/jquery.highchartTable.js"></script>
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
    <h1>データ表示</h1>
    <p>
      ようこそ#{session['username']}さん<br>
      チーム: #{session['tname']}
    </p>
    <input type="button" onClick="location.href='menu.cgi'" class="btn btn-outline-secondary"  value="戻る">
  </div>
HTML
l.searchform
l.lookup
l.show_table
puts <<~HTML
  <script type="text/javascript">
    $(document).ready(function () {
      var options = {
        currPage: 1,
        optionsForRows: [20, 50, 100],
        rowsPerPage: 20,
      };
      $("table#showtable").tablePagination(options);
      $("table.highchart").highchartTable();
    });
  </script>
  </body>
  </html>
HTML
