require "cgi"
require "cgi/session"
require "sqlite3"


# http://capm-network.com/?tag=Ruby-CGI%E3%82%BB%E3%83%83%E3%82%B7%E3%83%A7%E3%83%B3

# ログイン処理
class Login

  # イニシャライザ
  def initialize(cgi, session)
    @cgi = cgi
    @session = session
    @db = SQLite3::Database.new("./data.db")
    @id= ""
    @message = ""
  end

  def message
    @message
  end

  def login_process()
    login_id = @cgi["username"]
    login_pw = @cgi["password"]

    # セッションが確立済み
    if @session["id"] 
      return true
    end

    # 新規セッションの作成
    if ! check_id_pass(login_id, login_pw)
       return false
    elsif ! check_auth(login_id, login_pw)
       return false
    else
      @session['username'] = login_id
      @session['id'] = @id
      @session.close
      return true
    end
  end

  # ログイン済みか判断する
  def get_existing_session(cgi)
    begin
      session = CGI::Session.new( cgi, {"new_session"=>false,
                                        "tmpdir"=>"tmp/." } )
    rescue ArgumentError
      session = nil
    end
    return( session )
  end

  # ログアウト処理
  def logout_process()
    return if( is_session_auth() == false )

    @session.delete

    # ログアウト完了画面
    login = STW::Login.new( PATH_PASSWD )
    @contents = login.prompt( LOGIN_TEMPLETE )
    put_browser_info()
  end

  def is_session_auth()
    # 編集権限の確認
    if( @session == nil )
      @contents << "<h1>ERROR</h1>"
      @contents << "<p>Invalid Session.</p>"
      @contents << "<p>Session is not enable.</p>"
      return( false )
    end
    return( true )
  end

  # 入力されたパスワードと名前のバリデーション
  def check_id_pass(name, pass)
    # 英数字3~8文字
    if name == "" || pass == ""
      return false
    elsif name !~ /\A[0-9a-zA-Z]{3,8}\z/i 
      @message = "名前は英数字3~8文字です."
      return false
    elsif pass !~ /\A[a-z\d]{8,100}\z/i
      @message = "パスワードは英数字8文字以上です."
      return false
    end
    return true
  end

  # ログイン情報のチェック
  def check_auth(name, pass)
    data = []
    name = CGI.escapeHTML(name)
    sql = "select id,pass_hash from user where user.username = '#{name}';"
    @db.execute(sql).each{|row|
      data << row
    }
    if data == []
      @message = "名前が間違っているか, 登録されていません."
      return false
    elsif data[0][1] != pass
      @message = "パスワードが間違っています."
      return false
    else
      @id = data[0][0]
      return true
    end
  end
end
