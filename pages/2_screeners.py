import yahooquery as yq
from yahooquery import Ticker
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from os.path import exists

from src.models.analysis.multivariate_timeSeries_rnn import Multivariate_TimeSeries_RNN
from src.data import yahoo_fin_stock_info as si
import src.data.yahoo_fin_stock_info as SI
from src.tools import functions as f0
from src.tools import lists as l0


class Snapshot(object):


    def __init__(self, today_stamp):
        self.today_stamp = today_stamp
        self.saveMonth = str(datetime.now())[:7]
        self.saveRec = Path(f"data/recommenders/{str(today_stamp)[:4]}/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveRec.exists():
            self.saveRec.mkdir(parents=True)
        self.saveRaw = Path(f"data/raw/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveRaw.exists():
            self.saveRaw.mkdir(parents=True)
        self.saveScreeners = Path(f"data/screeners/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveScreeners.exists():
            self.saveScreeners.mkdir(parents=True)
        self.saveTickers = Path(f"data/tickers/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveTickers.exists():
            self.saveTickers.mkdir(parents=True)


    def get_screener_display(self, screener):
        if screener == "Day_Gainer_Stocks":
            try:
                st.write(" Today's Gainers ")
                st.dataframe(si.get_day_gainers().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Day_Loser_Stocks":
            try:
                st.write(" Today's Losers ")
                st.dataframe(si.get_day_losers().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Most_Active_Stocks":
            try:
                st.write(" Today's Most Active ")
                st.dataframe(si.get_day_most_active().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Trending_Tickers":
            try:
                st.write(" Today's Trending Tickers ")
                st.dataframe(si.get_trending_tickers().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Most_Shorted_Stocks":
            try:
                st.write(" Today's Most Shorted Stocks ")
                st.dataframe(si.get_most_shorted_stocks().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Undervalued_Large_Cap_Stocks":
            try:
                st.write(" Undervalued Large Cap Stocks ")
                st.dataframe(si.get_undervalued_large_caps().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Undervalued_Growth_Stocks":
            try:
                st.write(" Undervalued Growth Stocks ")
                st.dataframe(si.get_undervalued_growth_stocks().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Growth_Technology_Stocks":
            try:
                st.write(" Growth Technology Stocks ")
                st.dataframe(si.get_growth_technology_stocks().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Aggressive_Small_Cap_Stocks":
            try:
                st.write(" Aggressive Small Cap Stocks ")
                st.dataframe(si.get_aggressive_small_caps().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Small_Cap_Gainer_Stocks":
            try:
                st.write(" Small Cap Gainer Stocks ")
                st.dataframe(si.get_small_cap_gainers().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Top_Crypto_Securities":
            try:
                st.write(" Top Crypto Assets ")
                st.dataframe(SI.get_top_crypto())
            except Exception:
                pass

        elif screener == "Top_Mutual_Funds":
            try:
                st.write(" Top Mutual Funds ")
                st.dataframe(si.get_top_mutual_funds().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Portfolio_Anchor_Securities":
            try:
                st.write(" Portfolio Anchors ")
                st.dataframe(si.get_portfolio_anchors().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Solid_Large_Cap_Growth_Funds":
            try:
                st.write(" Solid Large-Cap Growth Funds ")
                st.dataframe(si.get_solid_large_growth_funds().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Solid_Mid_Cap_Growth_Funds":
            try:
                st.write(" Solid Mid-Cap Growth Funds ")
                st.dataframe(si.get_solid_midcap_growth_funds().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "Conservative_Foreign_Funds":
            try:
                st.write(" Conservative Foreign Funds ")
                st.dataframe(si.get_conservative_foreign_funds().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass

        elif screener == "High_Yield_Bond_Funds":
            try:
                st.write(" High Yield Bond funds ")
                st.dataframe(si.get_high_yield_bond().round(2).set_index(["Name", "Symbol"]))
            except Exception:
                pass


    def run_multivariate(self):
        Multivariate_TimeSeries_RNN().multivariate()


    def run_trending(self):
        data = yq.get_trending()
        for keys, values in data.items():
            if keys == "quotes":
                t_lst = values
        res = [sub["symbol"] for sub in t_lst]
        res = sorted(res)
        df = pd.DataFrame(res, columns=["symbol"])
        companyNames = []
        for i in df["symbol"]:
            if x := f0.company_longName(i):
                companyNames.append(x)
            else:
                companyNames.append(i)
        df["companyName"] = companyNames
        currentPrice = []
        targetMeanPrice = []
        recommendationMean = []
        recommendationKey = []

        for i in res:
            tick = i
            fin = Ticker(tick)
            data_fin = fin.financial_data
            try:
                currentPrice.append(data_fin[tick]["currentPrice"])
            except:
                currentPrice.append(0.0)
            try:
                targetMeanPrice.append(data_fin[tick]["targetMeanPrice"])
            except:
                targetMeanPrice.append(0.0)
            try:
                recommendationMean.append(data_fin[tick]["recommendationMean"])
            except:
                recommendationMean.append(6.0)
            try:
                recommendationKey.append(data_fin[tick]["recommendationKey"])
            except:
                recommendationKey.append("-")
        df["currentPrice"] = currentPrice
        df["targetPrice"] = targetMeanPrice
        df["recomMean"] = recommendationMean
        df["recommendation"] = recommendationKey
        st.dataframe(df.set_index("symbol").sort_values(by="recomMean", ascending=True))


    def run_mkt_snap(self):
        self.names_of_screeners = l0.names_of_screeners
        self.stock_name_list = l0.stock_name_list
        self.major_indicies = l0.major_indicies
        self.major_index_names = l0.major_index_names

        st.header("Screeners")
        with st.expander("", expanded=True):
            st.write(" * Select Screener: ")
            screener = st.selectbox("", l0.names_of_screeners)
            if st.button("Source Screeners"):
                self.get_screener_display(screener)

        st.header("Multivariate")
        with st.expander("", expanded=True):
            st.write("- Recurrent Neural Network [RNN] Analysis - Consumer Sentiment vs Industrial Production ")
            if st.button("Source Multivariate"):
                self.run_multivariate()

        st.header("Trending")
        with st.expander("", expanded=True):
            if st.button("Source Trending"):
                self.run_trending()



















import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime


plt.style.use("ggplot")
plt.rcParams["axes.facecolor"] = "silver"


class Screeners(object):


    def __init__(self, today_stamp):
        self.today_stamp = str(today_stamp)[:10]
        self.stage_lst = l0.general_pages
        self.major_indicies = l0.major_indicies
        self.major_index_names = l0.major_index_names
        
        st.header(" ◾ 𝄖𝄗𝄘𝄙𝄚 ·  Screener ·  𝄚𝄙𝄘𝄗𝄖 ◾ ")
        st.header(" ")


    def run_screen(self):
        
        cols = st.columns(2)
        with cols[0]:
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Stock Screeners")
            screener = st.selectbox("", l0.names_of_screeners)
            if screener != "-":
                Snapshot(self.today_stamp).get_screener_display(screener)              
        st.write(f"{'_'*10}")        

        cols = st.columns(1)
        with cols[0]:
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Google Trending Topics")
            if st.button("Source Trending"):
                Snapshot(self.today_stamp).run_trending()    
        st.write(f"{'_'*25}")
                
        cols = st.columns(1)
        with cols[0]:
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Multivariate Market Analysis")       
            if st.button("Source Multivariate"):
                Snapshot(self.today_stamp).run_multivariate()  



















if __name__ == '__main__':
    today_stamp = str(datetime.now())[:10]
    Screeners(today_stamp).run_screen()