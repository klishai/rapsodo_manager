#!/usr/bin/ruby
#encoding:UTF-8
require 'cgi'
require 'cgi/session'
require './lib/show.rb'

cgi = CGI.new
session = CGI::Session.new(cgi)
session["id"] = 1
l = Show.new(cgi, session)
puts <<-EOS
Content-type: text/html

<!DOCTYPE HTML>
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<script type="text/javascript" src="libjs/jquery-1.3.2.js"></script>
<script 
 type="text/javascript"
 src="libjs/query.tablePagination.0.5.js"
></script>
    <link rel="stylesheet" href="css/styletable.css" />

</head>
<body>

<p>データ表示</p>
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
   $("#showtable").tablePagination(options);
   });
</script>

</body>
</html>
EOS
