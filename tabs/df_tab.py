import pandas as pd
import streamlit as st
from styling import category_color_map, payment_method_color_map, payment_method_label_prefix, get_owner_color_map

def df_tab(df):
    # Temporarily turning off false positive warning
    # https://www.dataquest.io/blog/settingwithcopywarning/#falsepositives
    with pd.option_context('mode.chained_assignment', None):
        df.loc[:,"Payment Method"] = df["Payment Method"].map(lambda x: f"{payment_method_label_prefix[x]} {x}")

    styled_df = df.style \
                .format({
                    "Date": "{:%m/%d/%Y}",
                    "Price": "${:,.2f}",
                }) \
                .applymap(lambda x: f"color: {category_color_map[x]}", subset=["Category"]) \
                .applymap(lambda x: f"color: {payment_method_color_map[x.split()[-1]]}", subset=["Payment Method"])
    owner_color_map = get_owner_color_map()
    if owner_color_map:
        styled_df = styled_df.applymap(lambda x: f"color: {owner_color_map[x]}", subset=["Owner"])
    st.dataframe(styled_df, column_config={
        "Shared": st.column_config.CheckboxColumn(),
    }, hide_index=True, use_container_width=True)