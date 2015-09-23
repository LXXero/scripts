#!/usr/bin/ruby

require 'serialport'
require 'timeout'

#params for serial port
port_str = '/dev/ttyUSB0'  #may be different for you
baud_rate = 9600
data_bits = 8
stop_bits = 1
parity = SerialPort::NONE
 
sp = SerialPort.new(port_str, baud_rate, data_bits, stop_bits, parity)
sp.read_timeout = 50

while true
  begin
    Timeout::timeout(1) do
      time = Time.new
      #date = time.strftime("%Y-%m-%dT%H:%M:%S:%L")
      date = time.strftime("%m-%d-%yT%H:%M:%S")
 
      sp.write "L3200C5"
      ppv = sp.read
      ppv.gsub!(/L3240020*([0-9]+)\w{2}/,'\1')
 
      sp.write "L3201532E"
      pmv = sp.read
      pmv.gsub!(/L3210*([0-9]+)\w{2}/,'\1').insert(-2, '.')
 
      sp.write "L32010026"
      psv = sp.read
      psv.gsub!(/L32020*([0-9]+)\w{2}/,'\1')
 
      puts "#{date} PV: #{ppv} SV: #{psv} MV: #{pmv}"

      File.open('/home/xero/pidout.csv', 'a') do |f|
        f.puts "#{date},#{ppv},#{psv},#{pmv}"
      end

      sleep
    end
  rescue
    next
  end
end
sp.close
