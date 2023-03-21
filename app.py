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
   

   return render_template('notdash.html')






@app.route('/dash/graph',methods = ["get","post"]) 

def change():

   default_coin = "ADAUPUSDT"
   default_type = "Price History"
   default_movingav  =  5



   coin = request.form.get("coins")
   print(coin)
   option = request.form.get("type")
   temp = request.form.get("movingav")

   print(temp)
   if (temp != None):
      movingav = int(temp)
   else:
      movingav = None


   if ((coin == None) or (option == None)):
      coin = default_coin
      option = default_type
   
   if (movingav == None):
      movingav = default_movingav


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

   closeprice_series = pd.Series(closeprice)
   rolling_window = closeprice_series.rolling(window=movingav*7)
   rolling_mean = rolling_window.mean()
   rolling_mean_list = rolling_mean.tolist()

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
            pop[i] = pop[i].replace(',', '')
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
   previousdayprice = closeprice[l-2]

   changeprice = (currentprice-previousdayprice)/(previousdayprice)*100
   changeprice = round(changeprice,2)
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
                low=lowprice, close=closeprice)])

      fig.add_trace(go.Scatter(
        x=Date,
        y=rolling_mean,
        mode='lines',
        line=dict(color='blue', width=2),
        name=f"{movingav}-week Moving Average"
    ))
                     

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
                name = "Candlestick")])

      fig.add_trace(go.Scatter(
        x=Date,
        y=rolling_mean,
        mode='lines',
        line=dict(color='blue', width=2),
        name=f"{movingav}-week Moving Average"
    ))

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
                name = "Candlestick")
                ])
         
      fig.add_trace(go.Scatter(
        x=Date,
        y=rolling_mean,
        mode='lines',
        line=dict(color='blue', width=2),
        name=f"{movingav}-week Moving Average"
    ))
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
   

   return render_template('graph.html', graphJSON=graphJSON,pairlist=pairlist,coin=coin,option=option,totalamount = totalamount,totalcoins=totalcoins,currentprice=currentprice,changeprice=changeprice,movingav=movingav)


@app.route('/dash/trade',methods = ["get","post"]) 


def trade():


   default_coin = "ADAUPUSDT"
   
   temp_sdate = request.form.get("sdate")
   temp_edate = request.form.get("edate")
   coin = request.form.get("coins")

   print(coin)
   




   if ((coin == None)):
      coin = default_coin

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



   def datetounix(a):
      import calendar, time;
      return(calendar.timegm(time.strptime(a, '%d-%m-%Y')))

   def datetimetostring(b):
      import datetime
      return(b.strftime('%d-%m-%Y'))




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

   Datetemp = []
   for i in range (len(Date)):
      Datetemp.append(datetimetostring(Date[i]))

   date_len = len(Datetemp)
   startdate_default = Datetemp[0]
   enddate_default = Datetemp[date_len - 1]
   
   print(startdate_default)
   print(enddate_default)

   def datetounix(a):
      import calendar, time;
      return(calendar.timegm(time.strptime(a, '%d-%m-%Y')))

   
   for i in range (0,len(date)):
      date[i] = datetounix(date[i])


   for i in range (0,len(date)):
      date[i] = timechange(date[i])

  


   if ((temp_edate and temp_sdate) == None):
      sdate = startdate_default
      edate = enddate_default
   elif((temp_edate) == None):
      edate = enddate_default
      sdate = temp_sdate
   elif((sdate) == None):
      edate = temp_edate
      sdate = startdate_default
   
   sdate = datetounix(sdate)
   edate = datetounix(edate)

   sdate = timechange(sdate)
   edate = timechange(edate)

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
            pop[i] = pop[i].replace(',', '')
            buy_date.append(date[i])
            buy_price.append(float(pop[i]))
            vol_buy.append(float(vol[i]))
            spent.append(float(spent_gain[i]))

         elif (mode[i] =="SELL"):
            sell_date.append(date[i])
            sell_price.append(float(pop[i]))
            vol_sell.append(float(vol[i]))
            gain.append(float(spent_gain[i]))




   sum_volbuy = round(sum(vol_buy),4)
   sum_volsell = round(sum(vol_sell),4)
   sum_amountbuy = round(sum(spent),4)
   sum_amountsell = round(sum(gain),4)

   if ((sum_amountsell or sum_volsell) == 0):
      average_buy = round(sum_volbuy/sum_amountbuy,4)
      average_sell =  "-"
   else:
      average_buy = round(sum_volbuy/sum_amountbuy,4)
      average_sell = round(sum_volsell/sum_amountsell,4)

      

   



   totalamount = abs(sum_amountbuy - sum_amountsell)
   totalcoins = abs(sum_volbuy - sum_volsell)
   totalamount = round(totalamount,4)
   totalcoins = round(totalcoins,4)

   current_position = round(sum_volbuy - sum_volsell,4)
   total_position_cost = round(sum_amountbuy - sum_amountsell,4)
   average_postion = round(current_position/total_position_cost,4)




   l = len(closeprice)

   currentprice = closeprice[l-1]
   previousdayprice = closeprice[l-2]

   changeprice = (currentprice-previousdayprice)/(previousdayprice)*100
   changeprice = round(changeprice,2)
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


      

   return render_template('Trade_analysis.html',pairlist=pairlist,coin=coin,sum_volbuy = sum_volbuy,sum_volsell = sum_volsell,sum_amountsell = sum_amountsell,sum_amountbuy = sum_amountbuy,average_buy = average_buy,average_sell=average_sell,current_position=current_position,total_position_cost=total_position_cost,average_postion=average_postion,edate=edate,sdate=sdate)
      



if __name__ == '__main__':
    app.run()