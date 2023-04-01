from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://api.cryptowat.ch/markets/summaries'
parameters = {
'exchange' : 'binance',
'pair' : ' '

}

headers = {
'Accepts': 'application/json',
}

session1 = Session()
#session.headers.update(headers)

try:
    response = session1.get(url, params=parameters)
    data = json.loads(response.text)
    #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)


data1 = data['result']




key = data1.keys()
value = data1.values()


value = list(value)


values_len = len(value)

percentage_change = []
coin_percentage = {}

for i in range(0,values_len):
    percentage_change.append(value[i]['price']['change']['percentage'])


key_list = list(key)
marketlist = []
coinlist  = []
for i in key_list:
    marketlist.append(i.split(':')[0])
    coinlist.append(i.split(':')[1])


for i in range(values_len):
    temp = coinlist[i].split("-")
    if(len(temp) > 2):
        if (temp[2] == "future"):
            coinlist[i] = temp[0]

    if(len(temp) == 2):
        if(temp[0] == "binance"):
            coinlist[i] = temp[1]

for i in range(0,values_len):
    coin_percentage[(coinlist[i])] = percentage_change[i]





Key_max = max(coin_percentage, key = lambda x: coin_percentage[x])
Key_min = min(coin_percentage, key = lambda x: coin_percentage[x])   

maxcoin_percentage = round(coin_percentage[Key_max],4)
mincoin_percentage = round(coin_percentage[Key_min],4)




