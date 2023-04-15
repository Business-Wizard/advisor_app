import pandas as pd
import finviz
from finvizfinance.quote import finvizfinance
from finviz import get_analyst_price_targets, get_news, get_stock
import streamlit as st

import src.tools.functions as f0



class Single_Asset_Analysis(object):


    def __init__(self):
        self.ticker = st.sidebar.text_input(label='[3] Enter Stock', value='AAPL')


    def run(self):

        st.sidebar.write('*'*25)
        if st.sidebar.button('Run'):
            stock = finvizfinance(self.ticker)        

            try:
                company_name = f0.company_longName(self.ticker)
                x = f"{company_name} [{self.ticker}]"
            except Exception as e:
                pass            

            try:
                st.subheader(f"𝄖𝄗𝄘𝄙𝄚 Asset · Overview · {x} 𝄚𝄙𝄘𝄗𝄖")
                st.write('*'*25)
            except Exception as e:
                pass

            try:
                stock_description = stock.ticker_description()
                st.subheader('𝄖𝄗𝄘𝄙 Description')
                st.caption(stock_description)
                st.write(' '*25)
            except Exception as e:
                pass

            try:
                st.subheader('𝄖𝄗𝄘𝄙 Stock Information')
                st.dataframe(pd.DataFrame.from_dict(get_stock(self.ticker), orient='index'))
                st.write(' '*25)
            except Exception as e:
                pass

            try:
                stock_chart = stock.ticker_charts()
                st.subheader('𝄖𝄗𝄘𝄙 Stock Chart')
                st.image(stock_chart)
                st.write(' '*25)
            except Exception as e:
                pass

            try:
                st.subheader('𝄖𝄗𝄘𝄙 Analyst Ratings')
                outer_ratings_df = stock.ticker_outer_ratings()
                st.dataframe(outer_ratings_df.head().set_index('Date'))
                st.write(' '*25)
            except Exception as e:
                pass

            try:
                st.subheader('𝄖𝄗𝄘𝄙 Stock News')
                from bs4 import BeautifulSoup
                from urllib.request import urlopen, Request
                from nltk.sentiment.vader import SentimentIntensityAnalyzer
                from newspaper import Article, Config
                user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
                config = Config()
                config.browser_user_agent = user_agent
                config.request_timeout = 10
                parsed_news=[]
                pull_list=[]
                bad_stocks=[]
                n=14
                url = 'https://finviz.com/quote.ashx?t=' + self.ticker
                req = Request(url=url,headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'})
                resp = urlopen(req)
                html = BeautifulSoup(resp, features="lxml")
                news_table = html.find(id='news-table')
                news_tables = {self.ticker: news_table}
                new_stock_list = [self.ticker]
                for file_name, news_table in news_tables.items():
                    try:
                        rows = news_table.findAll("tr")
                        rows = rows[:n]
                        for row in rows:
                            cols = row.findAll("td")
                            try:
                                ticker = file_name.split('_')[0]
                                date = cols[0].text.split()[0]
                                title = cols[1].get_text()
                                link = cols[1].a['href']
                                source = link.split("/")[2]          
                                if source == "feedproxy.google.com":
                                    source = link.split("/")[4]
                                info_dict = {
                                    "Ticker": ticker,
                                    "Date": date, 
                                    "Title": title, 
                                    "Source": source, 
                                    "Link": link
                                    }
                                parsed_news.append(info_dict)
                            except Exception:
                                pass
                    except Exception as e:
                        print(e)
                parsed_news_df = pd.DataFrame(parsed_news)
                parsed_news_df.columns = [x.lower() for x in parsed_news_df.columns]
                parsed_news_df['date'] = pd.to_datetime(parsed_news_df['date'])
                parsed_news_df = parsed_news_df[parsed_news_df['date'] >= pd.Timestamp('2022-06-01')]
                st.dataframe(parsed_news_df)
            except Exception as e:
                pass

            try:
                inside_trader_df = stock.ticker_inside_trader()
                st.subheader('𝄖𝄗𝄘𝄙 Stock Insider Trading')
                st.dataframe(inside_trader_df.head())
                st.dataframe(pd.DataFrame.from_records(finviz.get_insider(self.ticker)))
                st.write(' '*25)
            except Exception as e:
                pass

            try:
                stock_fundamentals = stock.ticker_fundament()
                st.subheader('𝄖𝄗𝄘𝄙 Stock Fundamentals')
                st.dataframe(pd.DataFrame.from_dict(stock_fundamentals, orient='index'))
                st.write(' '*25)
            except Exception as e:
                pass

            try:
                stock_signal = stock.ticker_signal()
                st.subheader('𝄖𝄗𝄘𝄙 Stock Signals')
                st.dataframe(stock_signal)
            except Exception as e:
                pass
