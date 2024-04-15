import streamlit as st
from hasura import read_by_subject
import pandas as pd

st.set_page_config(
    page_title="学習指導要領コード", layout="wide", initial_sidebar_state="expanded"
)

st.title("学習指導要領コード 検索")

st.sidebar.title("検索条件")

subject = st.sidebar.selectbox(
    "どの教科？",
    ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"),
    index=1,
    placeholder="教科を選択してください",
)

goal = st.sidebar.multiselect(
    "目標区分",
    ["0", "1", "2", "3", "4", "5", "6", "7"],
    default=["0", "1", "2", "3", "4", "5", "6", "7"],
)

limit = st.sidebar.number_input("表示件数", min_value=1, max_value=100, value=10)

data = read_by_subject(subject, goal=goal, limit=limit)
# st.write(data)
df = pd.DataFrame(data["data"]["codes"])
st.table(df)
