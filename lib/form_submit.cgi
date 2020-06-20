#!/usr/bin/ruby
# frozen_string_literal: true

require 'cgi'
require 'cgi/session'
require 'sqlite3'

cgi = CGI.new
session = CGI::Session.new(cgi)
redirect_flag = false
redirect = lambda { |message, loc|
  puts cgi.header({ 'status' => 'REDIRECT', 'Location' => '../' + loc + '?id=' +
                      session['id'].to_s + '&message=' + CGI.escape(message) })
}
messages = []
if cgi['delete'] == '削除'
  sql = 'delete from pitcher_data where id = ? and data_id = ?;'
  begin
    SQLite3::Database.new('../data/data.db').execute(
      sql, session['id'], cgi['id']
    )
    puts cgi.header({ 'status' => 'REDIRECT', 'Location' => '../edit.cgi' })
  rescue StandardError => e
    redirect.call("DBエラー: #{e.message}", 'edit.cgi')
  end
else

  begin
    unless cgi['name'] =~ /^[\p{Hiragana}\p{Katakana}\p{Han}ー]+$/
      redirect_flag = true
      messages << '名前はすべて漢字、カタカナ、ひらがなです'
    end
    unless cgi['date'] =~ /^\d{8}+$/
      redirect_flag = true
      messages << '日付はYYYYMMDD(例: 20190101)の形式です'
    end
    unless cgi['pitch_type'] =~ /
        ^(
        ストレート|スライダー|チェンジアップ|フォーク|
        ツーシーム|カーブ|カットボール|スライダー2|スプリット
        )$
        /x
      redirect_flag = true
      messages << '名前はすべて漢字、カタカナ、ひらがなです'
    end
    unless cgi['pitch_speed'] =~ /^\d+\.\d+$/
      redirect_flag = true
      messages << '球速は小数です'
    end
    unless cgi['rotations'] =~ /^\d+$/
      redirect_flag = true
      messages << '回転数は整数です'
    end
    unless cgi['efficiency'] =~ /^\d+$/
      redirect_flag = true
      messages << '回転効率は整数です'
    end
    unless cgi['v_change'] =~ /^\d+\.\d+$/
      redirect_flag = true
      messages << '縦の変化量は小数です'
    end
    unless cgi['h_change'] =~ /^\d+\.\d+$/
      redirect_flag = true
      messages << '横の変化量は小数です'
    end
  rescue StandardError
    redirect_flag = true
    messages << 'エラーが発生しました'
  end

  if redirect_flag
    redirect.call(messages.join('br'), cgi['add'] ? 'add.cgi' : 'edit_s.cgi')
  elsif cgi['add'] == '1'
    sql = <<-SQL
    insert into
    pitcher_data(
        data_id,
        pitcher_name,
        day,
        pitch_type,
        pitch_speed,
        rotations,
        r_efficiency,
        v_change,
        h_change,
        id
    )
    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    SQL
    begin
      SQLite3::Database.new('../data/data.db').execute(
        sql, cgi['data_id'], cgi['name'], cgi['date'], cgi['pitch_type'],
        cgi['pitch_speed'], cgi['rotations'], cgi['efficiency'],
        cgi['v_change'], cgi['h_change'], session['id']
      )
      puts cgi.header({ 'status' => 'REDIRECT', 'Location' => '../add.cgi?message=追加しました' })
    rescue StandardError => e
      redirect.call("DBエラー: #{e.message}", 'add.cgi')
    end
  else
    sql = <<-SQL
    update pitcher_data
    set
        pitcher_name = ?,
        day = ?,
        pitch_type = ?,
        pitch_speed = ?,
        rotations = ?,
        r_efficiency = ?,
        v_change = ?,
        h_change = ?
    where id = ? and data_id = ?;
    SQL
    begin
      SQLite3::Database.new('../data/data.db').execute(
        sql, cgi['name'], cgi['date'], cgi['pitch_type'],
        cgi['pitch_speed'], cgi['rotations'], cgi['efficiency'],
        cgi['v_change'], cgi['h_change'], session['id'], cgi['id']
      )
      puts cgi.header({ 'status' => 'REDIRECT', 'Location' => '../edit.cgi' })
    rescue StandardError => e
      redirect.call("DBエラー: #{e.message}", 'edit_s.cgi')
    end
  end
end
