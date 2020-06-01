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
    @db = SQLite3::Database.new("./data/data.db")
    @cgi_p = @cgi.instance_variable_get(:@params).map{|a,b|[a, CGI.escapeHTML(b.to_s)]}.to_h
    @data = lookup
    
  end
  
  def confirm_get_param
    @cgi_p
  end
    
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
     選手名検索
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
     球種検索
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
     <input type="text" name="ps" value="" list="case-numbers2" placeholder="1ページの表示件数:">
       <datalist id="case-numbers2">
         <option value="20">けっこう少ない</option>
         <option value="50">少ない</option>
         <option value="100">ちょっと少ない</option>
         <option value="200">ちょうどいい</option>
         <option value="500">ちょっと多い</option>
       </datalist>
     </p>
     <input type="hidden" name="p" value="0">

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
      data << row[0,row.size-1]
    }
    return data
  end

  def create_paging_link
    @cgi["ps"]=["20"] if @cgi["ps"]==[""]
    @cgi["ps"]=["20"] if @cgi["ps"][0]=~/[^0-9]/
    # par["ps"]||=["20"]
    # par["ps"]=["20"] if par["ps"][0].to_i<0
    p_now,p_size,hits=@cgi["p"][0].to_i,@cgi["ps"][0].to_i,@data.size
    begin
    hmp=hits%p_size!=0&&hits!=0? (hits/p_size)+1 : hits/p_size
    rescue ZeroDivisionError
      hmp=0
    end
    pagelinks="<table><tr>\n"
    hmp.times{|i|
        link="http://160.16.75.206/~irizon/rapsodo_manager/show.cgi?"
      @cgi["p"]= i
      @cgi.each{|k,v|link+="#{k}=#{v[0]}&"}
      pagelinks+="<td><a href=\"#{link.chop}\"><b>#{i+1}</b></a></td>\n"
      pagelinks+="</tr>\n<tr>" if i%30==0&&i!=0
    }
    pagelinks+="</tr></table>\n"
    return pagelinks
  end

  
  def show_table
     puts
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
