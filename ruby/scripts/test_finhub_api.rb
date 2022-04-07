require 'finnhub_ruby'
require 'json'
finhub_key = ENV['FINHUB_API_KEY']
FinnhubRuby.configure do |config|
  config.api_key['api_key'] = finhub_key.to_str
end

finnhub_client = FinnhubRuby::DefaultApi.new
stock = 'AAPL'
rt_price = finnhub_client.quote(stock)
symbols = finnhub_client.symbol_search(stock)
# stock2 = finnhub_client.company_profile2({symbol: 'AAPL'})
# stock3 = finnhub_client.company_basic_financials('AAPL', 'all')
# puts(stock.inspect)
# puts(stock2.inspect)
# buffer = stock3
puts(rt_price.inspect)



# <img src="<%= @profile.logo %>"><br/>
# Company Name : <%= @profile.name %> <br/>
# Price : $ <%= @rtprice.c %> <br/>
# Previous Close : $ <%= @rtprice.pc %> <br/>
# Market Cap : $ <%= @profile.marketCapitalization %> <br/>
# Week52High : $ <%= @financials.metric.52WeekHigh %> <br/>
# Week52Low : $ <%= @financials.metric.52WeekLow %> <br/>
# Beta : <%= @financials.metric.beta %><br/>