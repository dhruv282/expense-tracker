import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud

def wordcloud_tab(df: pd.DataFrame):
    income_toggle = st.checkbox('Hide Income', value=False)
    if income_toggle:
        df = df.loc[(df['Category'] != 'Income'), :]
    memo_grouped_data = df.groupby([df['Memo']], as_index=False).sum(numeric_only=True)
    weights = pd.Series(memo_grouped_data['Price'].values,
                        index=memo_grouped_data['Memo']).to_dict()
    cloud = WordCloud(background_color='rgba(255, 255, 255, 0)', mode='RGBA', scale=10,
                      colormap='tab20', width=800).generate_from_frequencies(weights)
    pl_cloud = px.imshow(cloud)
    pl_cloud.update_xaxes(visible=False)
    pl_cloud.update_yaxes(visible=False)
    pl_cloud.update_traces(hovertemplate=None, hoverinfo='skip')
    st.plotly_chart(pl_cloud, use_container_width=True)
