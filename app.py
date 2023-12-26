import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import tabs
from utils import get_google_sheet_titles_and_url, get_worksheet 

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="📈",
    layout="wide",
)
st.title('Expense Tracker')

google_sheets_titles_and_url = get_google_sheet_titles_and_url()
if google_sheets_titles_and_url:
    s_title, w_title, url = google_sheets_titles_and_url
    title = f"{s_title} ({w_title})" if w_title else f"{s_title}"
    st.link_button(f"📝{title}", url, help="Google Sheets link")

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

summary_tab, breakdown_tab, monthly_trends_tab, expense_heatmap_tab, add_transaction_tab, df_tab = st.tabs([
    "Summary", "Breakdown", "Monthly Trends", "Expense Heatmap", "Add Transaction", "Data"])

with summary_tab:
    tabs.render_summary_tab(filtered_df.copy())

with breakdown_tab:
    tabs.render_breakdown_tab(filtered_df.copy())

with monthly_trends_tab:
    tabs.render_monthly_trends_tab(filtered_df.copy())

with expense_heatmap_tab:
    tabs.render_expense_heatmap_tab(filtered_df.copy())

with add_transaction_tab:
    tabs.render_add_transaction_tab()

with df_tab:
    tabs.render_df_tab(filtered_df.copy())
