#!/usr/bin/ruby
#encoding:UTF-8
require 'cgi'
require 'cgi/session'
require './lib/show.rb'

cgi = CGI.new
session = CGI::Session.new(cgi)
# session["id"] = 1
unless session["id"]
  puts cgi.header({'status' => 'REDIRECT', 'Location' => 'login.cgi'})
else
  l = Show.new(cgi, session)
end

puts <<-EOS if session["id"]
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

</head>
<body>
<h1>データ表示</h1>
<p>ようこそ#{session["username"]}さん<br>
   チーム: #{session["tname"]}</p>

<form>
<input type="button" onClick="location.href='menu.cgi'" value="戻る">
</form>

EOS
l.searchform
l.lookup
l.show_table
puts <<-EOS
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
EOS
