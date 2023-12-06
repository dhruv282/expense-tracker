import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from styling import category_color_map

def summary_tab(df: pd.DataFrame) -> None:
    savings_expenses_column, expenses_breakdown_column = st.columns(2)

    c_grouped_data = df.groupby([
        df['Category'],
    ], as_index=False).sum(numeric_only=True)
    expenses = c_grouped_data.loc[(c_grouped_data['Category'] != 'Income'), :]
    income: list[int] = c_grouped_data.loc[
        (c_grouped_data['Category'] == 'Income'), 'Price'
    ].values
    
    with savings_expenses_column:
        expenses_total = expenses.loc[:, 'Price'].sum(numeric_only=True)
        c_grouped_data_rows = [[ 'Expenses', expenses_total  ]]
        if income:
            income_total = income[0]
            if not expenses_total:
                expenses_total = 0
            savings = income_total - expenses_total
            if savings > 0:
                c_grouped_data_rows.append([ 'Savings', savings  ])
        else:
            income_total = 0
        c_grouped_data = pd.DataFrame(c_grouped_data_rows, columns=['Category', 'Price'])

        savings_expenses_pie_chart: go.Figure = px.pie(c_grouped_data, values="Price", names="Category", hole=0.75,
                        color="Category", color_discrete_map={
                            'Savings': '#7cfc00',
                            'Expenses': '#fc0000'},
                        title="Savings/Expenses Breakdown")
        savings_expenses_pie_chart.update_layout(showlegend=False,
                                                    annotations=[dict(text=f'Income: ${income_total:,.2f}',
                                                                    font_size=20,
                                                                    showarrow=False)])
        savings_expenses_pie_chart.update_traces(textinfo="percent+label")
        savings_expenses_pie_chart.update_traces(hovertemplate="%{label} (%{percent}) <br> %{value:$,.2f}")
        st.plotly_chart(savings_expenses_pie_chart, theme=None, use_container_width=True)
    
    with expenses_breakdown_column:
        expenses_breakdown_pie_chart: go.Figure = px.pie(expenses, values="Price", names="Category", hole=0.75,
                            color="Category", color_discrete_map=category_color_map,
                            title="Expense Breakdown")
        expenses_breakdown_pie_chart.update_layout(showlegend=False)
        expenses_breakdown_pie_chart.update_traces(textinfo="percent+label")
        expenses_breakdown_pie_chart.update_traces(hovertemplate="%{label} (%{percent}) <br> %{value:$,.2f}")
        st.plotly_chart(expenses_breakdown_pie_chart, theme=None, use_container_width=True)