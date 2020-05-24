require 'cgi'
require 'sqlite3'

# 新規名前とパスワードチェック
# 文字種と重複をみる
# 良ければuserに追加してloginに遷移
class Register
  def initialize(cgi)
    @cgi = cgi
    @db = SQLite3::Database.new("./data.db")
    @message = ""
    @pre_id = ""
  end

  def message
    @message
  end

  def register?
    register_pw = @cgi["password"]
    register_un = @cgi["username"]
    register_tm = @cgi["teamname"]
    if ! check_id_pass_team(register_un, register_pw, register_tm)
      return false
    elsif ! check_register(register_un)
      return false
    end
    register(register_un, register_pw, register_tm)
    return true
  end
  # 入力されたパスワードと名前のバリデーション
  def check_id_pass_team(name, pass, team)
    # 英数字3~8文字
    if name == "" || pass == ""
      return false
    elsif name !~ /\A[0-9a-zA-Z]{3,8}\z/i
      @message = "名前は英数字3~8文字です."
      return false
    elsif pass !~ /\A[a-z\d]{8,100}\z/i
      @message = "パスワードは英数字8文字以上です."
      return false
    elsif team == ""
      @message = "チーム名は1文字以上です."
      return false
    end
    return true
  end

  def check_register(name)
    # ログイン情報のチェック
    data = []
    name = CGI.escapeHTML(name)
    sql = "select id, username from user where user.username = '#{name}';"
    @db.execute(sql).each{|row|
      data << row
    }
    if data.size > 0
      @message = "名前が登録されています."
      return false
    else
      @pre_id = data[0][0]
      return true
    end
  end

  def register(name, pass, team)
    data = []
    name = CGI.escapeHTML(name)
    pass = CGI.escapeHTML(pass)
    team = CGI.escapeHTML(team)
    sql = "insert into user values(#{pre_id}, '#{name}', '#{pass}', '#{team}');"
    @db.execute(sql).each{|row|
      data << row
    }
  end
end
