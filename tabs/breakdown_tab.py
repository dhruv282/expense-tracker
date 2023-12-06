import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from styling import get_owner_color_map, category_color_map
from typing import Callable

def process_data(df: pd.DataFrame,
                 get_savings_df: Callable[[int], pd.DataFrame],
                 hide_savings: bool) -> pd.DataFrame:
    income: list[int] = df.loc[(df['Category'] == 'Income'), 'Price'].values
    if income:
        income_total = income[0]
        df = df.drop(df[(df['Category'] == 'Income')].index)
    else:
        income_total = 0
    if not hide_savings:
        expenses = df.loc[(df['Category'] != 'Income'), :]
        expenses_total = expenses.loc[:, 'Price'].sum(numeric_only=True)
        if not expenses_total:
            expenses_total = 0
        savings = income_total - expenses_total
        df = pd.concat([df, get_savings_df(savings)], axis=0)
    return df.copy()

def breakdown_tab(df: pd.DataFrame) -> None:
    owners = df['Owner'].unique()
    if len(owners) > 1:
        combined_breakdown = st.checkbox('Show combined breakdown', value=False)
    savings_toggle = st.checkbox('Hide Savings', value=False)
    if len(owners) == 1 or combined_breakdown:
        c_grouped_data = df.groupby([
            df['Category'],
        ], as_index=False).sum(numeric_only=True)
        data = process_data(c_grouped_data,
                            lambda s: pd.DataFrame({
                                'Category': ['Savings'],
                                'Price': [s],
                            }),
                            savings_toggle)
        histogram: go.Figure = px.histogram(data, x="Category", y="Price", color="Category",
                                            text_auto='.2s', color_discrete_map=category_color_map)
    else:
        c_o_grouped_data = df.groupby([
            df['Owner'],
            df['Category'],
        ], as_index=False).sum(numeric_only=True)
        o_grouped_data = df.groupby([
            df['Owner'],
        ], as_index=False).sum(numeric_only=True)
        data = pd.DataFrame()
        for _, row in o_grouped_data.iterrows():
            data = pd.concat([data, 
                              process_data(c_o_grouped_data.loc[c_o_grouped_data['Owner'] == row['Owner']],
                                           lambda s: pd.DataFrame({
                                               'Owner': [row['Owner']],
                                               'Category': ['Savings'],
                                               'Price': [s],
                                               }),
                                               savings_toggle)
                            ], axis=0)

        histogram: go.Figure = px.histogram(data, x="Category", y="Price", color="Owner", barmode="group",
                                            text_auto='.2s', color_discrete_map=get_owner_color_map())
    histogram.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False,
                            hovertemplate="%{x} <br> %{y:$,.2f}")
    histogram.update_layout(bargroupgap=0.15, xaxis={'categoryorder':'total descending'})
    st.plotly_chart(histogram, use_container_width=True)