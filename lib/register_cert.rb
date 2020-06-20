# frozen_string_literal: true

require 'cgi'
require 'sqlite3'

# 新規名前とパスワードチェック
# 文字種と重複をみる
# 良ければuserに追加してloginに遷移
class Register
  def initialize(cgi)
    @cgi = cgi
    @db = SQLite3::Database.new('./data/data.db')
    @message = ''
    @pre_id = ''
  end

  attr_reader :message

  def register?
    register_pw = @cgi['password']
    register_un = @cgi['username']
    register_tm = @cgi['teamname']
    if !check_id_pass_team(register_un, register_pw, register_tm)
      return false
    elsif !check_register(register_un)
      return false
    end

    register(register_un, register_pw, register_tm)
    true
  end

  # 入力されたパスワードと名前のバリデーション
  def check_id_pass_team(name, pass, team)
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
    elsif team == ''
      @message = 'チーム名は1文字以上です.'
      return false
    end

    true
  end

  def check_register(name)
    # ログイン情報のチェック
    data = []
    name = CGI.escapeHTML(name)
    sql = "select username from user where user.username = '#{name}';"
    @db.execute(sql).each  do |row|
      data << row
    end
    if !data.empty?
      @message = '名前が登録されています.'
      false
    else
      sql = 'select id from user;'
      data = []
      @db.execute(sql).each do |row|
        data << row[0]
      end
      @pre_id = data[-1]
      true
    end
  end

  def register(name, pass, team)
    data = []
    name = CGI.escapeHTML(name)
    pass = CGI.escapeHTML(pass)
    team = CGI.escapeHTML(team)
    sql = "insert into user values(#{@pre_id + 1}, '#{name}', '#{pass}', '#{team}');"
    @db.execute(sql).each do |row|
      data << row
    end
  end
end
