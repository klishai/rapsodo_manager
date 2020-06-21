# frozen_string_literal: true

require 'cgi'
require 'cgi/session'
require 'sqlite3'
# encoding: UTF-8
# show informations
class Show
  # init
  def initialize(cgi, session)
    @cgi = cgi
    @session = session
    @id = session['id']
    @tname = session['tname']
    @db = SQLite3::Database.new('./data/data.db')
    @cgi_p = @cgi.instance_variable_get(:@params).map { |a, b|
      [a, CGI.escapeHTML(b.to_s)]
    }.to_h
    @data = lookup
  end

  def confirm_get_param
    @cgi_p
  end

  def searchform
    datasrc = []
    sqlsrc = 'select * from pitcher_data where pitcher_data.id in ' \
             '(select id from user where teamname == ?)'
    @db.execute(sqlsrc, @tname).each do |row|
      datasrc << row[0, row.size - 1]
    end
    puts <<-HTML
    <details class="ml-3 mt-2 mb-2 h5">
      <summary>検索フォーム</summary>
      <form method="get" action="">
      <p class="mt-3 mb-3 h5">
      選手名検索 <span class="message">(※グラフ)</span>
      <select name="team_pitcher">
      <option value=""> -- </opition>
    HTML

    datasrc.map { |row| row[1] }.uniq.each do |a|
      puts "<option value=#{a}>" + CGI.escapeHTML(a.to_s) + '</option>'
    end
    puts <<-HTML
      </select>
      </p>                                                                                                                                                                                    
      <p class="mb-3 h5">
      球種検索<span class="message">(※グラフ)</span> 
      <select name="pitch_type">
      <option value=""> -- </opition>
    HTML

    datasrc.map { |row| row[3] }.uniq.each do |t|
      puts "<option value=\"#{t}\">" + CGI.escapeHTML(t.to_s) + '</option>'
    end
    puts <<-HTML
      </select>
      </p>

     <p class="mb-3 h5">
     期間検索
      </p>
      <p class="mb-3 h5">
      <input type="date" name="day1"> ～　<input type="date" name="day2" >
      </p>

      <p>
      <input type="submit" class="btn btn-outline-secondary" value="検索">
      <a class="btn btn-outline-secondary" href="show.cgi" role="button">条件なしに戻る</a>
      </p>

      </form>
    </details>
    HTML
    puts
    puts
  end

  def lookup
    data = []
    sqlargs = [@session['tname']]
    # teams
    sql = 'select * from pitcher_data where pitcher_data.id in ' \
          '(select id from user where teamname == ?)'
    unless @cgi['team_pitcher'].nil? || @cgi['team_pitcher'].empty?
      sql += ' and pitcher_data.pitcher_name = ? '
      sqlargs << @cgi['team_pitcher']
    end
    unless @cgi['pitch_type'].nil? || @cgi['pitch_type'].empty?
      sql += ' and pitcher_data.pitch_type = ? '
      sqlargs << @cgi['pitch_type']
    end
    unless @cgi['day1'].nil? || @cgi['day1'].empty?
      day1 = @cgi['day1'].delete!('-').to_i
      sql += ' and pitcher_data.day >= ? '
      sqlargs << day1
    end

    unless @cgi['day2'].nil? || @cgi['day2'].empty?
      day2 = @cgi['day2'].delete!('-').to_i
      sql += ' and pitcher_data.day <= ? '
      sqlargs << day2
    end

    sql += ';'
    @db.execute(sql, *sqlargs).each do |row|
      data << row[1, row.size - 2]
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
      puts <<-HTML
      <section> 
      <table id="showtable" class="highchart table table-hover table table-striped table-active"
        graph-container-before="1"
        data-graph-container=".highchart-container"
        data-graph-type="line"
      >
      <thead class="thead-dark table-bordered">
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
      HTML
      puts '<tbody>'
      @data.each do |r|
        puts '<tr>'
        r[0], r[1] = r[1], r[0]
        r.each do |d|
          puts '<td>' + CGI.escapeHTML(d.to_s) + '</td>'
        end
        puts '</tr>'
      end
      puts '</tbody>'
      puts '</table></section>'
    end
  end
end
