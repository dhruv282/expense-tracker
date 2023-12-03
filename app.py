import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import tabs

st.set_page_config(page_title="Budget Tracker", page_icon="📈",)
st.title('Budget Tracker DashBoard')

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    worksheet="History",
    ttl="10m",
)

# Prep dataframe
df.columns = df.iloc[0]
df = df[1:]
df = df.dropna()
df["Price"] = pd.to_numeric(df['Price'])
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
df.sort_values(by="Date", ascending=False, inplace=True)

year_col, owner_col = st.columns(2)

year_options = df["Date"].dt.strftime('%Y').drop_duplicates().tolist()
year_options.sort(reverse=True)
selected_year = year_col.selectbox("📆 Year", ["All"] + year_options, index=1)
filtered_df = df
if selected_year != "All":
    filtered_df = df[df['Date'].dt.year == int(selected_year)]

owner_options = ["All"] + df["Owner"].drop_duplicates().tolist()
selected_owner = owner_col.selectbox("👤 Owner", owner_options, index=0)
if selected_owner != "All":
    filtered_df = filtered_df[filtered_df['Owner'] == selected_owner]

dashboard_tab, df_tab = st.tabs(["Dashboard", "Data"])

with dashboard_tab:
    tabs.render_dashboard_tab(filtered_df.copy())

with df_tab:
    tabs.render_df_tab(filtered_df.copy())
