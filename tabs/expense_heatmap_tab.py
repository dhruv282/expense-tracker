import pandas as pd
import plotly.express as px
import streamlit as st
from utils import month_labels

def expense_heatmap_tab(df: pd.DataFrame):
    df['Month'] = df['Date'].dt.month
    df = df.sort_values(by='Month')
    m_grouped_data = df.groupby([
            df['Category'],
            df['Month'],
        ], as_index=False).sum(numeric_only=True)
    m_grouped_data = m_grouped_data.loc[(m_grouped_data['Category'] != 'Income'), :]
    categories = sorted(m_grouped_data['Category'].unique())
    months = sorted(m_grouped_data['Month'].unique())
    category_index = {c: i for i, c in enumerate(categories)}
    data = [[0 for _ in categories]
            for _ in months]
    first_month = months[0]
    for _, row in m_grouped_data.iterrows():
        data[row['Month'] - first_month][category_index[row['Category']]] = row['Price']
    heatmap = px.imshow(data, x=categories, y=months, labels=dict(color='Total Expenses'), text_auto='.2s')
    heatmap.update_yaxes(labelalias=month_labels, tickmode='linear')
    heatmap.update_traces(hovertemplate="Category: %{x}<br>Month: %{y}<br>Total: %{z:$,.2f}<extra></extra>")
    st.plotly_chart(heatmap, use_container_width=True)
