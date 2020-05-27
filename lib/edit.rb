#!/usr/bin/ruby
require "sqlite3"
require "cgi"
require "cgi/session"

class Edit

  def initialize(cgi, session)
    @cgi = cgi
    @session = session
    @id = @session["id"]
    @db = SQLite3::Database.new("./data/data.db")
  end

  def id
    @id
  end

  def list
    p @id
    if @id.nil?
      return nil
    else
      data = []
      sql = "select * from pitcher_data where pitcher_data.id = #{@id};"
      @db.execute(sql).each{|row|
        data<<row
      }
      return data
    end
  end
 
end
