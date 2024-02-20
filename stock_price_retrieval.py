import yfinance as yf

try:
    def get_data(a):
        return yf.Ticker(a).fast_info
except:
    print("get data exception")



