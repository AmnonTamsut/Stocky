import yfinance as yf


def get_data(a):
    try:
        return yf.Ticker(a).fast_info
    except:
        print("get data exception")


def get_multiple_data(name, start_date, end_date):
    try:
        df = yf.download(name, start=start_date, end=end_date)
        return df.to_json()
    except:
        print("get data exception")



