#ライブラリのインポート
import pandas as pd
import streamlit as st
import plotly.express as px
import os

# アプリケーションのルートディレクトリを取得
current_dir = os.path.dirname(__file__)

# ファイルパスの絶対パスを生成
file_path = os.path.join(current_dir, '../app_step2/hotel.csv')

# DataFrame として CSV を読み込む
df = pd.read_csv(file_path)

# 複数のホテル名を選択できるマルチセレクトボックスをサイドバーに作成
hotelNames = st.sidebar.multiselect('ホテルを選択してください', df['hotelName'].unique())

# 価格レンジのスライダーをサイドバーに作成
min_price, max_price = st.sidebar.slider(
    '価格レンジを選択してください',
    min_value=int(df['hotelMinCharge'].min()),
    max_value=int(df['hotelMinCharge'].max()),
    value=(int(df['hotelMinCharge'].min()), int(df['hotelMinCharge'].max()))
)

# フィルタリングされたデータを作成
filtered_df = df[(df['hotelName'].isin(hotelNames)) &
                 (df['hotelMinCharge'] >= min_price) &
                 (df['hotelMinCharge'] <= max_price)]

# フィルタリングされたホテルのテーブル表示
st.write("選択された価格レンジ内のホテル一覧")
st.dataframe(filtered_df[['hotelName', 'hotelMinCharge', 'reviewAverage']])

# フィルタリングされたデータを用いて棒グラフを作成
fig_bar = px.bar(
    filtered_df,
    x='hotelName',
    y='hotelMinCharge',
    color='reviewAverage',
    hover_name='hotelName',
    title='選択されたホテルの価格とレビュー評価',
    labels={'hotelMinCharge': '価格', 'reviewAverage': 'レビュー評価'}
)

# フィルタリングされたデータを用いて散布図を作成
fig_filtered = px.scatter(
    filtered_df,
    x='hotelMinCharge',
    y='reviewAverage',
    size='reviewAverage',
    color='hotelName',
    hover_name='hotelName',
    title='選択したホテルのレビューと価格の関係'
)

# フィルタリングされていないグラフを表示
fig_unfiltered = px.scatter(
    df,
    x='hotelMinCharge',
    y='reviewAverage',
    size='reviewAverage',
    color='hotelName',
    hover_name='hotelName',
    title='すべてのホテルのレビューと価格の関係'
)

# テーブル表示
st.plotly_chart(fig_unfiltered)
st.plotly_chart(fig_filtered)
st.plotly_chart(fig_bar)