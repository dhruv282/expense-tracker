import streamlit as st
from styling import category_color_map, payment_method_color_map, get_owner_color_map, payment_method_label_prefix
from utils import get_worksheet_client, get_transaction_tab_shared_default

def transaction_tab():
    worksheet_client = get_worksheet_client()
    if worksheet_client:
        with st.form('add_transaction_form', clear_on_submit=True, border=False):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input('Date', value='today', format='MM/DD/YYYY')
                memo = st.text_input('Memo')
                category = st.selectbox('Category', [c for c in category_color_map.keys() if c != 'Savings'])
            with col2:
                owner = st.selectbox('Owner', get_owner_color_map())
                price = st.number_input('Price')
                payment_method = st.selectbox('Payment Method', payment_method_color_map.keys(), index=0,
                                            format_func=lambda p: f'{payment_method_label_prefix[p]} {p}')
                shared = st.checkbox('Shared Expense?', value=get_transaction_tab_shared_default())
                if shared:
                    shared = 'Yes'
                else:
                    shared = 'No'
            if st.form_submit_button('Submit'):
                values = [date.strftime('%m/%d/%Y'), memo, category, owner, price, payment_method, shared]
                res = worksheet_client.append_row(values)
                if res:
                    st.toast(':green[Transaction added successfully!]', icon='🎉')
                else:
                    st.toast(':red[Something went wrong]', icon='😢')
    else:
        st.error('Service account not setup with write permissions')
