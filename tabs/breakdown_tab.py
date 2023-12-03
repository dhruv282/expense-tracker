import pandas as pd
import plotly.express as px
import streamlit as st
from styling import get_owner_color_map

def breakdown_tab(df):
    df= df.loc[df["Category"] != "Income", :]
    histogram = px.histogram(df, x="Category", y="Price", color="Owner", barmode="group",
                             text_auto='.2s', color_discrete_map=get_owner_color_map())
    histogram.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False,
                            hovertemplate="%{x} <br> %{y:$,.2f}")
    histogram.update_layout(bargroupgap=0.15)
    st.plotly_chart(histogram, use_container_width=True)