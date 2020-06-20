#!/usr/bin/ruby
# frozen_string_literal: true

require 'cgi'
require 'cgi/session'

cgi = CGI.new
session = CGI::Session.new(cgi)
session.delete

puts cgi.header({ 'status' => 'REDIRECT',
                  'Location' => 'login.cgi' })
