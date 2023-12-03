import pandas as pd
import plotly.express as px
import streamlit as st
from styling import category_color_map

def dashboard_tab(df):
    # Temporarily turning off false positive warning
    # https://www.dataquest.io/blog/settingwithcopywarning/#falsepositives
    with pd.option_context('mode.chained_assignment', None):
        df.loc[:,'Year'] = df['Date'].dt.year
        df.loc[:,'Month'] = df['Date'].dt.month

    y_m_c_grouped_data = df.groupby([
        df['Year'],
        df['Month'],
        df['Category'],
    ], as_index=False).sum(numeric_only=True)

    y_m_grouped_data = df.groupby([
        df['Year'],
        df['Month'],
    ], as_index=False).sum(numeric_only=True)

    for i, row in y_m_grouped_data.iterrows():
        income = y_m_c_grouped_data.loc[
            (y_m_c_grouped_data['Year'] == row['Year']) &
            (y_m_c_grouped_data['Month'] == row['Month']) &
            (y_m_c_grouped_data['Category'] == 'Income'), 'Price'
        ].values[0]
        
        y_m_c_grouped_data.loc[
            (y_m_c_grouped_data['Year'] == row['Year']) &
            (y_m_c_grouped_data['Month'] == row['Month']) &
            (y_m_c_grouped_data['Category'] == 'Income'), 'Category'
        ] = 'Savings'
        
        y_m_c_grouped_data.loc[
            (y_m_c_grouped_data['Year'] == row['Year']) &
            (y_m_c_grouped_data['Month'] == row['Month']) &
            (y_m_c_grouped_data['Category'] == 'Savings'), 'Price'
        ] = income - (row['Price'] - income)

    pie_chart = px.pie(y_m_c_grouped_data, values="Price", names="Category", hole=0.75,
                      color="Category", color_discrete_map=category_color_map)
    pie_chart.update_traces(textinfo="percent+label")
    pie_chart.update_traces(hovertemplate="%{label} (%{percent}) <br> %{value:$,.2f} </br>")
    st.plotly_chart(pie_chart, theme=None, use_container_width=True)