from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.graph_objects as go
from flask import request

app = Flask(__name__)
app.debug = True




@app.route('/')


def new():

   return render_template('hero.html')



@app.route('/dash')

def notdash():
   
   def timechange(time):
      """changes unix format to datetime format

      Args:
        time (int): time
      """
      from datetime import datetime
      # if you encounter a "year is out of range" error the timestamp
      # may be in milliseconds, try `ts /= 1000` in that case
      # return(datetime.utcfromtimestamp(time).strftime('%d-%m-%Y'))
      return(datetime.utcfromtimestamp(time))

   import pandas as pd
   k = pd.read_csv('./Crypto_analysis_dashboard/Analysis/Spot.csv')


   totalpairlist = k.Pair.tolist()


   pairlist = []

   for i in totalpairlist:
      if i in pairlist:
         continue
      else:
        pairlist.append(i)

  

   from requests import Request, Session
   from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
   import json

   url = ' https://api.cryptowat.ch/markets/binance/adausdt/ohlc?periods=86400'
   parameters = {
  'exchange' : 'binance',
  'pair' : ' '
    
   }

   headers = {
   'Accepts': 'application/json',
   }

   session = Session()
   #session.headers.update(headers)

   try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
   except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

   a = len(data['result']['86400'])
   Date = []
   for i in range (0,a,1):
      Date.append(timechange(data['result']['86400'][i][0]))

   openprice = []
   for i in range (0,a,1):
      openprice.append(data['result']['86400'][i][1])

   highprice = []
   for i in range (0,a,1):
      highprice.append(data['result']['86400'][i][2])

   lowprice = []
   for i in range (0,a,1):
      lowprice.append(data['result']['86400'][i][3])

   closeprice = []
   for i in range (0,a,1):
      closeprice.append(data['result']['86400'][i][4])

   volume = []
   for i in range (0,a,1):
      volume.append(data['result']['86400'][i][5])




   fig = go.Figure(data=[go.Candlestick(x=Date,
                open=openprice, high=highprice,
                low=lowprice, close=closeprice)
                     ])

   fig.update_layout(xaxis_rangeslider_visible=False)
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

   return render_template('notdash.html', graphJSON=graphJSON,pairlist=pairlist)






@app.route('/dash/graph',methods = ["get","post"]) 

def change():


   coin = request.form.get("coins")
   print(coin)
   option = request.form.get("type")


   def timechange(time):
      """changes unix format to datetime format

      Args:
        time (int): time
      """
      from datetime import datetime
      # if you encounter a "year is out of range" error the timestamp
      # may be in milliseconds, try `ts /= 1000` in that case
      # return(datetime.utcfromtimestamp(time).strftime('%d-%m-%Y'))
      return(datetime.utcfromtimestamp(time))

   import pandas as pd
   k = pd.read_csv('./Crypto_analysis_dashboard/Analysis/Spot.csv')


   totalpairlist = k.Pair.tolist()


   pairlist = []

   for i in totalpairlist:
      if i in pairlist:
         continue
      else:
        pairlist.append(i)

  
   from requests import Request, Session
   from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
   import json

   url = ' https://api.cryptowat.ch/markets/binance/{c}/ohlc?periods=86400'.format(c = coin)
   parameters = {
  'exchange' : 'binance',
  'pair' : ' ' 
    
   }

   headers = {
   'Accepts': 'application/json',
   }

   session = Session()
   #session.headers.update(headers)

   try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
   except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

   datakey = data.keys()
   datakeylist = list(datakey)

   if (datakeylist[0] == 'error'):

      from requests import Request, Session
      from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
      import json

      url = ' https://api.cryptowat.ch/markets/binance/binance-{c}/ohlc?periods=86400'.format(c = coin)
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


   a = len(data['result']['86400'])

   Date = []
   for i in range (0,a,1):
      Date.append(timechange(data['result']['86400'][i][0]))

   openprice = []
   for i in range (0,a,1):
      openprice.append(data['result']['86400'][i][1])

   highprice = []
   for i in range (0,a,1):
      highprice.append(data['result']['86400'][i][2])

   lowprice = []
   for i in range (0,a,1):
      lowprice.append(data['result']['86400'][i][3])

   closeprice = []
   for i in range (0,a,1):
      closeprice.append(data['result']['86400'][i][4])

   volume = []
   for i in range (0,a,1):
      volume.append(data['result']['86400'][i][5])

   dt = pd.read_csv('Spot2.csv')

   date=dt.Date.tolist()

   def datetounix(a):
      import calendar, time;
      return(calendar.timegm(time.strptime(a, '%d-%m-%Y')))

   for i in range (0,len(date)):
      date[i] = datetounix(date[i])


   for i in range (0,len(date)):
      date[i] = timechange(date[i])


   buy_date = []
   buy_price =[]
   sell_date = []
   sell_price = []
   vol_buy=[]
   vol_sell=[]
   spent = []
   gain =[]

   pair = dt.Pair.tolist() 
   mode= dt.Buy_Sell.tolist()
   pop = dt.Price.tolist()
   vol = dt.Volume.tolist()
   spent_gain = dt.Spent_Gain.tolist()

   for i in range(0,len(mode),1):
      if (pair[i] == coin ):
         if (mode[i] == "BUY"):
            buy_date.append(date[i])
            buy_price.append(float(pop[i]))
            vol_buy.append(float(vol[i]))
            spent.append(float(spent_gain[i]))

         elif (mode[i] =="SELL"):
            sell_date.append(date[i])
            sell_price.append(float(pop[i]))
            vol_sell.append(float(vol[i]))
            gain.append(float(spent_gain[i]))



   totalamount = abs(sum(spent) - sum(gain))
   totalcoins = abs(sum(vol_buy) - sum(vol_sell))
   totalamount = round(totalamount,4)
   totalcoins = round(totalcoins,4)


   l = len(closeprice)

   currentprice = closeprice[l-1]

   def listsize(l):
         new = []
         mini = min(l)
         maxi = max(l)
         if (mini == maxi):
            new.append(mini)
            return (new)   
         else:           
            for i in l:
               new.append((i-mini)/(maxi-mini)*50)
            return (new)
      
   
   vol_buysize=listsize(vol_buy)
   if (vol_sell == []):
      vol_sellsize = [0]
      gainsize = [0]
   else:
      vol_sellsize=listsize(vol_sell)
      gainsize =listsize(gain)

   spentsize = listsize(spent)
   

   if (option == "Price History"):

      fig = go.Figure(data=[go.Candlestick(x=Date,
                open=openprice, high=highprice,
                low=lowprice, close=closeprice)
                     ])

      fig.update_layout(
      xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="backward"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        range = (Date[0],Date[-1]),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    )
               )

      graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


   elif (option == "Transaction History"):

      fig = go.Figure(
            [go.Candlestick(x=Date,
                open=openprice, high=highprice,
                low=lowprice, close=closeprice,
                name = "Candlestick")]
      )

      fig.add_trace(

         go.Scatter(x=buy_date,
                y=buy_price,
                mode = "markers",
                name = "buy",
                marker=dict(color="rgba(67, 255, 100, 0.85)",size = 12)
                )
    
         ) 

      fig.add_trace(
         go.Scatter(x=sell_date,
                y=sell_price,
                mode = "markers",
                name = "sell",
                marker = dict(color = "rgba(67, 33, 100, 0.85)",size =12)
                )
    
         )

      fig.update_layout(
         xaxis=dict(
         rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="backward"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        range = (Date[0],Date[-1]),
        rangeslider=dict(
            visible=False
            ),
        type="date"
         )
         )

      graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


   
   if (option == "Transaction Volume"):

      fig = go.Figure(
         [go.Candlestick(x=Date,
                open=openprice, high=highprice,
                low=lowprice, close=closeprice,
                name = "Candlestick")]
         )

      fig.add_trace(

      go.Scatter(x=buy_date,
                y=buy_price,
                mode = "markers",
                name = "buy_volume",
                marker=dict(color="rgba(67, 255, 100, 0.85)",size = (vol_buysize))
                )
    
         )    

      fig.add_trace(
      go.Scatter(x=sell_date,
                y=sell_price,
                mode = "markers",
                name = "sell_volume",
                marker = dict(color = "rgba(67, 33, 100, 0.85)",size =(vol_sellsize))
                )
    
         )
      fig.update_layout(
         xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="backward"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        range = (Date[0],Date[-1]),
        rangeslider=dict(
            visible=False
        ),
        type="date"
      )
         )

      graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   

   return render_template('graph.html', graphJSON=graphJSON,pairlist=pairlist,coin=coin,option=option,totalamount = totalamount,totalcoins=totalcoins,currentprice=currentprice)





if __name__ == '__main__':
    app.run()