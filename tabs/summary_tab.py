import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from styling import category_color_map, get_owner_color_map

def summary_tab(df: pd.DataFrame) -> None:
    owners = df['Owner'].unique()
    if len(owners) > 1:
        savings_expenses_column, expenses_breakdown_column, shared_expenses_column = st.columns(3)
    else:
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
                                                    annotations=[dict(text=f'Income:<br>${income_total:,.2f}',
                                                                    font_size=20,
                                                                    showarrow=False)])
        savings_expenses_pie_chart.update_traces(textinfo="percent+label")
        savings_expenses_pie_chart.update_traces(hovertemplate="%{label} (%{percent}) <br> %{value:$,.2f}")
        st.plotly_chart(savings_expenses_pie_chart, theme=None, use_container_width=True)
    
    with expenses_breakdown_column:
        total_expenses = expenses.loc[:, 'Price'].sum(numeric_only=True)
        expenses_breakdown_pie_chart: go.Figure = px.pie(expenses, values="Price", names="Category", hole=0.75,
                            color="Category", color_discrete_map=category_color_map,
                            title="Expense Breakdown")
        expenses_breakdown_pie_chart.update_layout(showlegend=False,
                                                    annotations=[dict(text=f'Total:<br>${total_expenses:,.2f}',
                                                                    font_size=20,
                                                                    showarrow=False)])
        expenses_breakdown_pie_chart.update_traces(textinfo="percent+label")
        expenses_breakdown_pie_chart.update_traces(hovertemplate="%{label} (%{percent}) <br> %{value:$,.2f}")
        st.plotly_chart(expenses_breakdown_pie_chart, theme=None, use_container_width=True)

    if len(owners) > 1:
        with shared_expenses_column:
            shared_expenses = df.loc[
                (df['Shared'] == 'Yes') &
                (df['Category'] != 'Income'), :]
            o_grouped_data = shared_expenses.groupby([
                shared_expenses['Owner'],
            ], as_index=False).sum(numeric_only=True)
            total_expenses = o_grouped_data.loc[:, 'Price'].sum(numeric_only=True)
            shared_expenses_pie_chart: go.Figure = px.pie(o_grouped_data, values="Price", names="Owner", hole=0.75,
                                color="Owner", color_discrete_map=get_owner_color_map(),
                                title="Shared Expenses")
            shared_expenses_pie_chart.update_layout(showlegend=False,
                                                        annotations=[dict(text=f'Total:<br>${total_expenses:,.2f}',
                                                                        font_size=20,
                                                                        showarrow=False)])
            shared_expenses_pie_chart.update_traces(textinfo="percent+label")
            shared_expenses_pie_chart.update_traces(hovertemplate="%{label} (%{percent}) <br> %{value:$,.2f}")
            st.plotly_chart(shared_expenses_pie_chart, theme=None, use_container_width=True)