# frozen_string_literal: true

require 'cgi'
require 'cgi/session'
require 'sqlite3'

class Edit
  # イニシャライザ
  def initialize(cgi, session)
    @cgi = cgi
    @session = session
    @id = session['id']
    @tname = session['tname']
    @db = SQLite3::Database.new('./data/data.db')
    @cgi_p = @cgi.instance_variable_get(:@params).map { |a, b| [a, CGI.escapeHTML(b.to_s)] }.to_h
    @data = lookup
  end

  def confirm_get_param
    @cgi_p
  end

  def searchform
    datasrc = []
    sqlsrc = "select * from pitcher_data where pitcher_data.id = #{@id};"
    @db.execute(sqlsrc).each do |row|
      datasrc << row[0, row.size - 1]
    end
    puts <<-EOS
    <details class="ml-3 mt-2 mb-2">
      <summary>検索フォーム</summary>
      <form method="get" action="">
      <p>
      選手名検索 <span class="message"></span>
      <select name="team_pitcher">
      <option value = ""> -- </opition>
    EOS

    datasrc.map { |row| row[1] }.uniq.each do |a|
      puts "<option value = #{a}>" + CGI.escapeHTML(a.to_s) + '</option>'
    end
    puts <<-EOS
     </select>
     </p>                                                                                                                                                                                    
     <p>
     球種検索
     <select name ="pitch_type">
     <option value = ""> -- </opition>
    EOS

    datasrc.map { |row| row[3] }.uniq.each do |t|
      puts "<option value = #{t}>" + CGI.escapeHTML(t.to_s) + '</option>'
    end
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
     <input type="submit" class="btn btn-outline-secondary" value="送信"></p>
     </p>
     </form>
     </details>
    EOS
    puts
    puts
  end

  def lookup
    data = []
    # teams
    sql =  "select * from pitcher_data where pitcher_data.id = #{@session['id']}"
    unless @cgi['team_pitcher'].nil? || @cgi['team_pitcher'].empty?
      sql += " and pitcher_data.pitcher_name = '#{@cgi['team_pitcher']}'"
    end
    unless @cgi['pitch_type'].nil? || @cgi['pitch_type'].empty?
      sql += " and pitcher_data.pitch_type = '#{@cgi['pitch_type']}'"
    end
    unless @cgi['day1'].nil? || @cgi['day1'].empty?
      day1 = @cgi['day1'].delete!('-').to_i
      sql += " and pitcher_data.day >= #{day1} "
    end

    unless @cgi['day2'].nil? || @cgi['day2'].empty?
      day2 = @cgi['day2'].delete!('-').to_i
      sql += " and pitcher_data.day <= #{day2} "
    end

    @db.execute(sql).each do |row|
      data << row
    end
    data
  end

  def show_table
    cond = []
    cond << '選手名:' +  @cgi['team_pitcher'] unless @cgi['team_pitcher'].empty?
    cond << '球種名:' +  @cgi['pitch_type'] unless @cgi['pitch_type'].empty?
    cond << 'From:' +  @cgi['day1'] unless @cgi['day1'].empty?
    cond << 'Till:' +  @cgi['day2'] unless @cgi['day2'].empty?
    puts "<h2>「#{cond.empty? ? '(条件なし)' : cond.join(',' + "\s")}」の検索結果: #{@data.size}件HIT</h2>"
    unless @data.empty?
      unless @cgi['team_pitcher'].empty? || @cgi['pitch_type'].empty?
        puts '<section><div class="highchart-container"></div></section>'
      end
      puts <<-EOS
    <section> 
    <table id="showtable" class="highchart table table-hover table table-striped table-active">
      <thead class="thead-dark table-bordered">
      <tr>
        <th>ID</th>
        <th>名前</th>
        <th>日付</th>
        <th>球種</th>
        <th>球速</th>
        <th>回転数</th>
        <th>回転効率(%)</th>
        <th>縦の変化量(cm)</th>
        <th>横の変化量(cm)</th>
        <th>編集</th>
      </tr>
      </thead>
      EOS
      puts '<tbody>'
      @data.each do |r|
        puts '<tr>'
        r[0, r.size - 1].each do |d|
          puts '<td>' + CGI.escapeHTML(d.to_s) + '</td>'
        end
        # 編集ボタン
        puts '<td><a class="btn btn-primary" href="' \
             "edit_s.cgi?id=#{r[0]}" \
             '" role="button">編集</a></td>'
        puts '</tr>'
      end
      puts '</tbody>'
      puts '</table></section>'
    end
  end

  def show_only_table(id)
    data = []
    sql = 'select * from pitcher_data where data_id = ?'
    @db.execute(sql, id)[0].each do |row|
      data << CGI.escapeHTML(row.to_s)
    end
    <<-EOS
    <input type="hidden" name="id" value="#{data[0]}">
    <table>
    <tr>
      <th>データID</th>
      <td>#{data[0]}</td>
    </tr>
    <tr>
      <th>名前</th>
      <td><input name="name" type="text" value="#{data[1]}" required></td>
    </tr>
    <tr>
      <th>日付</th>
      <td><input name="date" type="text" value="#{data[2]}" required></td>
    </tr>
    <tr>
      <th>球種</th>
      <td>
        <select name="pitch_type" required>
        <option value="#{data[3]}">#{data[3]}</opition>
        <option value="ストレート">ストレート</option>
        <option value="スライダー">スライダー</option>
        <option value="チェンジアップ">チェンジアップ</option>
        <option value="フォーク">フォーク</option>
        <option value="ツーシーム">ツーシーム</option>
        <option value="カーブ">カーブ</option>
        <option value="カットボール">カットボール</option>
        <option value="スライダー2">スライダー2</option>
        <option value="スプリット">スプリット</option>
        </select>
      </td>
    </tr>
    <tr>
      <th>球速(km/h)</th>
      <td><input name="pitch_speed" type="text" value="#{data[4]}" required>km/h</td>
    </tr>
    <tr>
      <th>回転数</th>
      <td><input name="rotations" type="text" value="#{data[5]}" required>回</td>
    </tr>
    <tr>
      <th>回転効率(%)</th>
      <td><input name="efficiency" type="text" value="#{data[6]}" required>%</td>
    </tr>
    <tr>
      <th>縦の変化量(cm)</th>
      <td><input name="v_change" type="text" value="#{data[7]}" required>cm</td>
    </tr>
    <tr>
      <th>横の変化量(cm)</th>
      <td><input name="h_change" type="text" value="#{data[8]}" required>cm</td>
    </tr>
    </table>
    EOS
  end

  def show_adddata_table
    data = []
    sql = 'select data_id from pitcher_data order by data_id desc limit 1;'
    @db.execute(sql)[0].each do |row|
      data << row
    end
    data_id = data[0] + 1
    <<-EOS
    <input type="hidden" name="add" value="1">
    <input type="hidden" name="data_id" value="#{data_id}">
    <table>
    <tr>
      <th>データID</th>
      <td>#{data_id}</td>
    </tr>
    <tr>
      <th>名前</th>
      <td><input name="name" type="text" placeholder="例: 手簀戸" required></td>
    </tr>
    <tr>
      <th>日付</th>
      <td><input name="date" type="text" placeholder="例: 20200101" required></td>
    </tr>
    <tr>
      <th>球種</th>
      <td>
        <select name="pitch_type" required>
        <option value="ストレート">ストレート</option>
        <option value="スライダー">スライダー</option>
        <option value="チェンジアップ">チェンジアップ</option>
        <option value="フォーク">フォーク</option>
        <option value="ツーシーム">ツーシーム</option>
        <option value="カーブ">カーブ</option>
        <option value="カットボール">カットボール</option>
        <option value="スライダー2">スライダー2</option>
        <option value="スプリット">スプリット</option>
        </select>
      </td>
    </tr>
    <tr>
      <th>球速(km/h)</th>
      <td><input name="pitch_speed" type="text" placeholder="例: 120.0" required>km/h</td>
    </tr>
    <tr>
      <th>回転数</th>
      <td><input name="rotations" type="text" placeholder="例: 1966" required>回</td>
    </tr>
    <tr>
      <th>回転効率(%)</th>
      <td><input name="efficiency" type="text" placeholder="例: 77" required>%</td>
    </tr>
    <tr>
      <th>縦の変化量(cm)</th>
      <td><input name="v_change" type="text" placeholder="例: 32.3" required>cm</td>
    </tr>
    <tr>
      <th>横の変化量(cm)</th>
      <td><input name="h_change" type="text" placeholder="例: 26.4" required>cm</td>
    </tr>
    </table>
    EOS
  end
end
