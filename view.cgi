#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require("sqlite3")
require("cgi")
c = CGI.new
k = c["key"]
i = 0

print("Content-Type: text/html; charset=utf-8\n")
print("\n")
print("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML .01//EN\"\n")
print("\"http://www.w3.org/TR/html4/strit.dtd\">\n")
print("<html>\n")
print("  <head>\n")
print("    <title>検索結果</title>\n")
print("  </head>\n")
print("  <body>\n")
print("    <h2>検索結果</h2>\n")
db = SQLite3::Database.new("data.db")
db.transaction{
  db.execute("select * from pitcher_data where pitcher_data.id = 1;"){|row|
      i = i + 1
      if i == 1
        print("<table>")
      end
          print("<tr>")
          　print("<td>",i,"</td>")
            print("<td>",row[0],"</td>")
            print("<td>",row[1],"</td>")
            print("<td>",row[2],"</td>")
            print("<td>",row[3],"</td>")
            print("<td>",row[4],"</td>")
            print("<td>",row[5],"</td>")
            print("<td>",row[6],"</td>")
          print("</tr>")
}
  }
  if i == 0
    print("ご希望のデータは見つかりませんでした。")
  else
    print("</table>")
    print(i,"件ヒットしました。")
  end
print("  </body>\n")
print("</html>\n")
db.close

