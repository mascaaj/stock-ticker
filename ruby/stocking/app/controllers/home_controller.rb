class HomeController < ApplicationController
  def index
    require 'finnhub_ruby'
    finhub_key = ENV['FINHUB_API_KEY']
    FinnhubRuby.configure do |config|
      config.api_key['api_key'] = finhub_key.to_str
    end
    
    finnhub_client = FinnhubRuby::DefaultApi.new
    if params[:ticker] == ""
      @nothing = "Please enter a symbol before searching"
    elsif params[:ticker]
      @symbol_input = params[:ticker]
      @rtprice = finnhub_client.quote(@symbol_input)
      @profile = finnhub_client.company_profile2({symbol: @symbol_input})
      # @financials = finnhub_client.company_basic_financials(@symbol_input, 'all')
      if finnhub_client.symbol_search(@symbol_input).count == 0
        @error = "Please check the symbol that has been entered"
      end
    end
  end

  def about
  end
end
