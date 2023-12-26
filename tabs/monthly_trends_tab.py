import pandas as pd
import plotly.express as px
import streamlit as st
from styling import category_color_map
from utils import month_labels

def monthly_trends_tab(df: pd.DataFrame):
    df['Month'] = df['Date'].dt.month
    df = df.sort_values(by='Month')
    m_grouped_data = df.groupby([
            df['Category'],
            df['Month'],
        ], as_index=False).sum(numeric_only=True)
    expenses = m_grouped_data.loc[(m_grouped_data['Category'] != 'Income'), :]
    expenses = expenses.groupby([expenses['Month']], as_index=False).sum(numeric_only=True)
    line_chart = px.line(m_grouped_data[m_grouped_data['Category'] == 'Income'], x='Month',
                         y='Price', color='Category', color_discrete_map=category_color_map,
                         markers=True)
    line_chart.add_bar(x=expenses['Month'], y=expenses['Price'], marker={'color': '#fc0000'},
                       name = 'Expenses', hovertemplate="%{y:$,.2f}",
                       textfont_size=12, textangle=0, textposition="outside")
    line_chart.update_yaxes(title='')
    line_chart.update_xaxes(title='', labelalias=month_labels, tickmode='linear')
    line_chart.update_layout(hovermode='x unified')
    line_chart.update_traces(hovertemplate="%{y:$,.2f}")
    st.plotly_chart(line_chart, use_container_width=True)
