require "cgi"
require "cgi/session"
require "sqlite3"
#encoding: UTF-8

# 情報表示
class Show

  # イニシャライザ
  def initialize(cgi, session)
    @cgi = cgi
    @session = session
    @id = session["id"]
    @tname = session["tname"]
    @db = SQLite3::Database.new("./data/data.db")
    @cgi_p = @cgi.instance_variable_get(:@params).map{|a,b|[a, CGI.escapeHTML(b.to_s)]}.to_h
    @data = lookup    
  end

  def confirm_get_param
    @cgi_p
  end
    
  #検索フォームを作る
  def searchform
    datasrc = []
    sqlsrc = "select * from pitcher_data where pitcher_data.id = #{@id};"

    @db.execute(sqlsrc).each{|row|
      datasrc << row[0,row.size-1]
    }
    
    puts <<-EOS
     <details>
       <summary>検索フォーム</summary>
        <form method="get" action="">
         <p>
           選手名検索 <span class="message">(※グラフ)</span>
           <select name="team_pitcher">
            <option value = ""> -- </opition>
            EOS

            datasrc.map{|row|row[1]}.uniq.each{|a|
            puts "<option value = #{a.to_s}>" + CGI.escapeHTML(a.to_s) + "</option>"
            }
    
            puts <<-EOS
           </select>
         </p>                                                                                                                                                                                    
    
         <p>
           球種検索<span class="message">(※グラフ)</span>     
           <select name ="pitch_type">
            <option value = ""> -- </opition>
            EOS

             datasrc.map{|row| row[3]}.uniq.each{|t|
              puts "<option value = #{t.to_s}>" + CGI.escapeHTML(t.to_s) + "</option>"
             }
              puts <<-EOS
            </select>
          </p>

          <p>
            期間検索
          </p>
          
          <p>
            <input type="date" name="day1"> ～　<input type ="date" name ="day2" >
          </p>

          <p>
            <input type="submit" value="送信"></p>
          </p>

       </form>
     </details>
     EOS
     
  end

  def lookup
    data = []
    sql = "select * from pitcher_data where pitcher_data.id = #{@id}"
    sql += " and pitcher_data.pitcher_name = '#{@cgi["team_pitcher"]}'" unless @cgi["team_pitcher"].nil? || @cgi["team_pitcher"].empty?
    sql += " and pitcher_data.pitch_type = '#{@cgi["pitch_type"]}'" unless @cgi["pitch_type"].nil? || @cgi["pitch_type"].empty?

    unless @cgi["day1"].nil? || @cgi["day1"].empty? 
      day1 = @cgi["day1"].delete!("-").to_i
      sql += " and pitcher_data.day >= #{day1} "
    end

    unless @cgi["day2"].nil? || @cgi["day2"].empty?   
      day2 = @cgi["day2"].delete!("-").to_i      
      sql += " and pitcher_data.day <= #{day2} "
    end
 
    sql += ";"
    @db.execute(sql).each{|row|
      data << row[1,row.size-2]
    }

    return data
  end
  
  def show_table

     cond = []
      cond << "選手名:" +  @cgi['team_pitcher'] unless @cgi['team_pitcher'].empty?
      cond << "球種名:" +  @cgi['pitch_type'] unless @cgi['pitch_type'].empty?
      cond << "From:" +  @cgi['day1'] unless @cgi['day1'].empty?
      cond << "Till:" +  @cgi['day2'] unless @cgi['day2'].empty?
     puts "<h2>「#{cond.join(?, + ?\s)}」の検索結果: #{@data.size}件HIT</h2>"
    
     if @data.size != 0
       unless @cgi["team_pitcher"].empty? || @cgi["pitch_type"].empty?
         puts '<section><div class="highchart-container"></div></section>' 
       end
       puts <<-EOS

       <section> 
         <table id="showtable" class="highchart"
               graph-container-before="1"
               data-graph-container=".highchart-container"
               data-graph-type="line"
          >
      
           <thead>
             <tr>
               <th>日付</th>
               <th data-graph-skip="1">名前</th>
               <th data-graph-skip="1">球種</th>
               <th>球速</th>
               <th data-graph-hidden="1">回転数</th>
               <th data-graph-hidden="1">回転効率(%)</th>
               <th data-graph-hidden="1">縦の変化量(cm)</th>
               <th data-graph-hidden="1">横の変化量(cm)</th>
             </tr>
           </thead>
         
          EOS

           puts"<tbody>"
         
           @data.each{|r|
            puts "<tr>"
            r[0], r[1] = r[1], r[0]
            r.each{|d|
            puts "<td>" + CGI.escapeHTML(d.to_s) + "</td>"
            }
           puts "</tr>"
           }

         puts "</tbody>"
         puts "</table></section>"
     end
   end

   

end
