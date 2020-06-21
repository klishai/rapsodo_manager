# frozen_string_literal: true

require 'cgi'
require 'cgi/session'
require 'sqlite3'

# http://capm-network.com/?tag=Ruby-CGI%E3%82%BB%E3%83%83%E3%82%B7%E3%83%A7%E3%83%B3

# ログイン処理
class Login
  # イニシャライザ
  def initialize(cgi, session)
    @cgi = cgi
    @session = session
    @db = SQLite3::Database.new('./data/data.db')
    @id = ''
    @message = ''
    @tname = ''
  end

  attr_reader :message

  def login_process
    login_id = @cgi['username']
    login_pw = @cgi['password']

    # セッションが確立済み
    return true if @session['id']

    # 新規セッションの作成
    if !check_id_pass(login_id, login_pw)
      false
    elsif !check_auth(login_id, login_pw)
      false
    else
      @session['username'] = login_id
      @session['id'] = @id
      @session['tname'] = @tname
      @session.close
      true
    end
  end

  # 入力されたパスワードと名前のバリデーション
  def check_id_pass(name, pass)
    # 英数字3~8文字
    if name == '' || pass == ''
      return false
    elsif name !~ /\A[0-9a-zA-Z]{3,8}\z/i
      @message = '名前は英数字3~8文字です.'
      return false
    elsif pass !~ %r{^(?=.*?[a-z])(?=.*?\d)
                    (?=.*[?!#$%&'()*+-.
                     /:;<=>?@[\\]^_`{|}~])
                    [a-z\d!#$%&'()*+-.
                     /:;<=>?@[\\]^_`{|}~]{8,16}$}ix
      @message = 'パスワードは英数記号8~16文字です.'
      return false
    end

    true
  end

  # ログイン情報のチェック
  def check_auth(name, pass)
    data = []
    name = CGI.escapeHTML(name)
    sql = 'select id,password,teamname from user where user.username = ?;'
    @db.execute(sql, name).each do |row|
      data << row
    end
    if data == []
      @message = '名前が間違っているか, 登録されていません.'
      false
    elsif data[0][1] != pass
      @message = 'パスワードが間違っています.'
      false
    else
      @id = data[0][0]
      @tname = data[0][2]
      true
    end
  end
end
