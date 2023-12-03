import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import tabs
from utils import get_worksheet 

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="📈",
    layout="wide",
)
st.title('Expense Tracker')

# Create a connection object.
conn: GSheetsConnection = st.connection("gsheets", type=GSheetsConnection)

DATA_TTL_SECONDS = 10 * 60 # 10 mins
df: pd.DataFrame = conn.read(
    worksheet=get_worksheet(),
    ttl=DATA_TTL_SECONDS,
)

# Prep dataframe
df.columns = df.iloc[0]
df = df[1:]
df = df.dropna()
df["Price"] = pd.to_numeric(df['Price'].map(lambda x: str(x).lstrip('$').replace(',','')))
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
df.sort_values(by="Date", ascending=False, inplace=True)

year_col, owner_col = st.columns(2)

year_options: list[str] = df["Date"].dt.strftime('%Y').drop_duplicates().tolist()
year_options.sort(reverse=True)
selected_year: str | None = year_col.selectbox("📆 Year", ["All"] + year_options, index=1)
filtered_df = df
if selected_year and selected_year != "All":
    filtered_df = df[df['Date'].dt.year == int(selected_year)]

owner_options: list[str] = ["All"] + df["Owner"].drop_duplicates().tolist()
selected_owner: str | None = owner_col.selectbox("👤 Owner", owner_options, index=0)
if selected_owner != "All":
    filtered_df = filtered_df[filtered_df['Owner'] == selected_owner]

dashboard_tab, breakdown_tab, df_tab = st.tabs(["Dashboard", "Breakdown", "Data"])

with dashboard_tab:
    tabs.render_dashboard_tab(filtered_df.copy())

with breakdown_tab:
    tabs.render_breakdown_tab(filtered_df.copy())

with df_tab:
    tabs.render_df_tab(filtered_df.copy())
