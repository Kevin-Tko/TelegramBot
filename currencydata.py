import requests
from datetime import datetime, timedelta

API_KEY = 'a5ae81f29d302833d62aabf306f1dc70'
URL = f"http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}"


def search_currency(ccy):
    response = requests.get(url=URL)
    if response.status_code == 200:
        output = response.json()['rates']
        if ccy not in output.keys():
            return False
        else:
            rate = output['KES'] / output[ccy]
            return rate
    else:
        return False


today = datetime.now()
yesterday = today - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y-%m-%d')
past_url = f'http://api.exchangeratesapi.io/v1/{formatted_yesterday}?access_key={API_KEY}'


def trade_check(ccy):
    past_response = requests.get(url=past_url)
    if past_response.status_code == 200:
        past_output = past_response.json()['rates']
        if ccy not in past_output.keys():
            return False
        else:
            past_rate = past_output['KES'] / past_output[ccy]
            today_rate = search_currency(ccy)
            if today_rate > past_rate:
                return (f'Right now {ccy}/KES --> {today_rate}\n\n'
                        f'is higher than yesterday\'s rate --> {past_rate}.\n\n'
                        f' PLEASE SELL {ccy}')
            elif today_rate == past_rate:
                return (f'Right now {ccy}/KES --> {today_rate}\n\n'
                        f'is equal to yesterday\'s rate --> {past_rate}.\n\n'
                        f'Maybe it\'s a weekend or a holiday\n\n'
                        f' PLEASE HOLD{ccy}')
            else:
                return (f'Right now {ccy}/KES --> {today_rate}\n\n'
                        f'is lower than yesterday\'s rate {past_rate}.\n\n'
                        f' PLEASE BUY {ccy}')
    else:
        return False



