import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, Boolean, Date, BigInteger,text
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import patoolib
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from time import sleep

def perform_action(engine, connection,option1, option2,start,end):
    # Perform some action based on the selected options
    query = text(f"select SecuritiesCode from stock_list where Name = '{option1}';")
    r = connection.execute(query)
    i = r.fetchall()[0][0]
    query = text(f"select * from stock_prices where SecuritiesCode = {i};")
    r = connection.execute(query)
    data = pd.DataFrame(r.fetchall())
    if(len(data)!=0):
        if start_date > end_date:
            st.error('start date can not be less than end date')
        else:
            data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]
            if(len(data)!=0):
                st.subheader(f"graph of {option1}")
                if option2 == 'ALL':
                    fig = go.Figure()
                    y_columns = ['Open', 'Close', 'High','Low']
                    for col in y_columns:
                        fig.add_trace(go.Scatter(x=data['Date'], y=data[col], mode='lines', name=col))
                    
                    st.plotly_chart(fig)
                else:
                    plot_data = data[['Date',option2]]
                    fig = px.line(plot_data, x='Date', y=option2, title='Stock Values Over Time')
                    st.plotly_chart(fig)
            else:
                st.error('no data for this date range')
    else:
        st.write('no data available')


def download_data_and_create_db(engine,connection,database_name):
    api = KaggleApi()
    api.authenticate()
    kaggle.api.competition_download_files('jpx-tokyo-stock-exchange-prediction', path='datasets/')
    patoolib.extract_archive("datasets/jpx-tokyo-stock-exchange-prediction.zip", outdir="datasets")
    query = text(f"CREATE DATABASE IF NOT EXISTS {database_name};")
    connection.execute(query)


def db_engine():
    # MySQL connection parameters
    username = 'root'
    password = '123456'
    host = 'localhost'
    port = 3306
    database_name = 'financialdata'

    # Database connection string
    connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/'

    # Connect to the MySQL server
    engine = create_engine(connection_string)
    connection = engine.connect()
    query = text('SHOW DATABASES;')
    result = connection.execute(query)
    databases = [i[0] for i in result.fetchall()]

    if database_name.lower() not in databases:
        download_data_and_create_db(engine,connection,database_name)
        engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}')
        stocks = pd.read_csv('datasets/stock_list.csv')
        stock_prices = pd.read_csv('datasets/train_files/stock_prices.csv')
        stock_prices['Date'] = pd.to_datetime(stock_prices['Date'])
        stock_prices.to_sql('stock_prices',con=engine)
        stocks['EffectiveDate'] = pd.to_datetime(stocks['EffectiveDate'].astype(str))
        stocks.to_sql('stock_list',con=engine)

    use = text(f"USE {database_name};")
    connection.execute(use)

    # Reconnect to the newly created database
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}')
    return engine


engine = db_engine()
connection = engine.connect()
query = text('select Name from stock_list;')
r = connection.execute(query)
stock_codes = np.unique([i[0] for i in r.fetchall()])
prices = ['Open', 'Close', 'High','Low','ALL']

# Streamlit app
st.title('STOCKS')

code_selected = st.selectbox('Select stock code', stock_codes)
price_selected = st.selectbox('Select price option', prices)
col1,col2 = st.columns(2)
with col1:
    start_date = st.date_input('start date')
with col2:
    end_date = st.date_input('end date')

if st.button('Plot'):
    perform_action(engine,connection,code_selected, price_selected,start_date,end_date)