#!/usr/bin/ruby

require "cgi"
require "cgi/session"
require "sqlite3"


# http://capm-network.com/?tag=Ruby-CGI%E3%82%BB%E3%83%83%E3%82%B7%E3%83%A7%E3%83%B3

# ログイン処理
class login_cert

# イニシャライザ
def initialize(cgi)
  @cgi = cgi
  @session = CGI::Session.new(cgi)
end

def login_process()
  login_id = @cgi["username"]
  login_pw = @cgi["password"]

  # セッションが確立済み
  if( @session != nil )
    return true
  end

  # 新規セッションの作成
  if check_auth(login_id, login_pw)
    @session = CGI::Session.new( @cgi, {"new_session"=>true,
                                      "tmpdir"=>"tmp/." } )
    @session['account'] = 1
    @session['id'] = login_id
    @session.close
    return true
  else
    return false
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

  # セッションの終了
  @session['account'] = 0
  @session.close
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

def check_auth(name, pass)
  data = []
  db.execute(sql).each{|row|
    data<<row[0]
  }


end

def register
