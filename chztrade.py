import time
import pyupbit
import datetime

# ticker, k, currency
#total = 100000
ticker = "KRW-CHZ"
currency = "CHZ"
k = 0.1

# 손절, 익절 비율
rate_minus = 0.95    #손절 비율
rate_plus = 1.37      #익절 비율

access = 
secret = 

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma10(ticker):
    """10일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=10)
    ma10 = df['close'].rolling(10).mean().iloc[-1]
    return ma10

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def get_buy_average(currency):
    """평균매수가 조회"""                      
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == currency:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("Autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(ticker)
        end_time = start_time + datetime.timedelta(days=1)
        chz = get_balance("CHZ")

        if chz > 0 :
            current_price = get_current_price(ticker)
            buy_price = get_buy_average(currency)
            if current_price < buy_price*rate_minus or buy_price*rate_plus < current_price:
                upbit.sell_market_order(ticker, chz)
                print("sell ok")

        else:
            print("There is no coin")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)