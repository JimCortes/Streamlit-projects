import pandas as pd
import streamlit as st
import yfinance as yf
import streamlit.components.v1 as stc 
import matplotlib.pyplot as plt
import numpy as np
# getting tickers

companies = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
companies = companies[0]
symbols = companies["Symbol"].tolist()
indicators = {
    "Market Cap": "marketCap",
    "Book Value": "bookValue",
    "Fiscal year":"lastFiscalYearEnd",
    "Regular Market Price" : "regularMarketPrice",
    "Enterprice Value":"enterpriseValue",
    }


title = """
<div style="font-size:60px;font-weight:bolder;background-color:#fff;text-align:center;">
		<span style='color:Green'>SP 500</span>
		
</div>

"""

def MACD(ticker):
    df = yf.Ticker(ticker).history(period="2y")
    df["MA_Fast"]=df["Close"].ewm(span=12,min_periods=12).mean()
    df["MA_Slow"]=df["Close"].ewm(span=26,min_periods=26).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=9,min_periods=9).mean()   
    df.dropna(inplace=True)
    return df

def bollinger(ticker):
    dfb = yf.Ticker(ticker).history(period="6mo")
    dfb = dfb[["High","Low","Close"]]
    dfb['H-L']=abs(dfb['High']-dfb['Low'])
    dfb['H-PC']=abs(dfb['High']-dfb['Close'].shift(1))
    dfb['L-PC']=abs(dfb['Low']-dfb['Close'].shift(1))
    dfb['TR']=dfb[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    dfb['ATR'] = dfb['TR'].rolling(12).mean()
    dfb = dfb.drop(['H-L','H-PC','L-PC'],axis=1)
    return dfb

def OBV(ticker):
    df = yf.Ticker(ticker).history(period="6mo")
    df['dailychange'] = df['Close'].pct_change()
    df['direction'] = np.where(df['dailychange']>=0,1,-1)
    df['direction'][0] = 0
    df['vol_adj'] = df['Volume'] * df['direction']
    df['obv'] = df['vol_adj'].cumsum()
    return df
 



stc.html(title)
st.sidebar.subheader("Menu")
tickers = symbols
st.sidebar.subheader("Tickers")
choice = st.sidebar.multiselect("",tickers)

st.sidebar.subheader("Indicator")
choice1 = st.sidebar.selectbox("",list(indicators.keys()))

def main ():
    try:

        title_left_column, title_center_column, title_right_column = st.beta_columns(3)
        title_left_column.write("Symbol")
        title_center_column.write("Industry")
        title_right_column.write(choice1)
        st.markdown("___")

        left_column, center_column, right_column = st.beta_columns(3)
        if choice == "":
            pass
        else:
            i = 0
            while  i < len(choice):
                ticker = yf.Ticker(choice[i])
                left_column.write(choice[i])
                center_column.write(ticker.info["industry"])
                right_column.write("${:,.2f}".format(ticker.info[indicators[choice1]]))
                i += 1

        

        expander = st.beta_expander("More Analysis")

        ticker = expander.radio("Select a stock",list(choice))

        tecnicalindica = expander.selectbox("Select Tecinical Indicator :",("OBV",'MCDA', 'ATR'))
        
        
        if  tecnicalindica == "MCDA":
            a = MACD(ticker)
            fig, (ax0, ax1) = plt.subplots(nrows=2,ncols=1, sharex=True, sharey=False, figsize=(11, 5), gridspec_kw = {'height_ratios':[3.5,1 ]})
            grafico1 = a[["Close","MA_Fast","MA_Slow"]]
            grafico1[-150:].plot(ax=ax0)

            graph2 = a[["MACD","Signal"]]  
            graph2[-150:].plot(ax=ax1)

            expander.pyplot(fig)
        elif tecnicalindica == "ATR":
            a = bollinger(ticker)
            fig, (ax0,ax1)= plt.subplots(nrows=2,ncols=1, sharex=True, sharey=False, figsize=(11, 5), gridspec_kw = {'height_ratios':[3.5,1 ]})

            grafico1 = a[["High","Low","Close"]]
            grafico1[-150:].plot(ax=ax1)
            
            graph2 = a[["TR","ATR"]]  
            graph2[-150:].plot(ax=ax0)


            expander.pyplot(fig)
        elif tecnicalindica == "OBV":
            df = OBV(ticker)

            fig, ax= plt.subplots()
            df['obv'].plot(ax=ax)

            expander.pyplot(fig)
        else:
            pass
    except:
        pass

if __name__ == "__main__":
    main()

