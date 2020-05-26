require "cgi"
require "cgi/session"
require "sqlite3"

# 情報表示
class Show

  # イニシャライザ
  def initialize(cgi, session)
    @cgi = cgi
    @session = session
    @id = session["id"]
    @db = SQLite3::Database.new("./data.db")
    @data =[]
    lookup
  end
  def lookup
    sql = "select * from pitcher_data where pitcher_data.id = #{@id};"
    @db.execute(sql).each{|row|
      @data<<row[0,row.size-1]
    }
  end


  def show_table
    puts <<-EOS
    <table border="1">
      <tr>
        <th>data_id</th>
        <th>名前</th>
        <th>日付</th>
        <th>球種</th>
        <th>球速</th>
        <th>回転数</th>
        <th>回転効率(%)</th>
        <th>縦の変化量(cm)</th>
        <th>横の変化量(cm)</th>
      </tr>
    EOS
    @data.each{|r|
      puts "<tr>"
      r.each{|d|
        puts "<td>" + CGI.escapeHTML(d.to_s) + "</td>"
      }
      puts "</tr>"
    }
    puts "</table>" 
  end
end
