import datetime
import streamlit as st
from styling import category_color_map, payment_method_color_map, get_owner_color_map, payment_method_label_prefix
from utils import get_worksheet_client, get_transaction_tab_shared_default

def transaction_tab() -> None:
    worksheet_client = get_worksheet_client()
    shared_default = get_transaction_tab_shared_default()
    st.session_state['shared'] = shared_default
    if worksheet_client:
        with st.form('add_transaction_form', clear_on_submit=False, border=False):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input('Date', value='today', format='MM/DD/YYYY', key='date')
                memo = st.text_input('Memo', key='memo')
                category = st.selectbox('Category',
                                        [c for c in category_color_map.keys() if c != 'Savings'])
            with col2:
                owner = st.selectbox('Owner', get_owner_color_map())
                price = st.number_input('Price', key='price')
                payment_method = st.selectbox('Payment Method', payment_method_color_map.keys(), index=0,
                                            format_func=lambda p: f'{payment_method_label_prefix[p]} {p}',
                                            key='payment_method')
                shared = st.checkbox('Shared Expense?',
                                     key='shared')
                if shared:
                    shared = 'Yes'
                else:
                    shared = 'No'
            submit_col1, submit_col2 = st.columns(2)
            with submit_col1:
                if st.form_submit_button('Submit', type='primary', use_container_width=True):
                    if not memo or price <= 0:
                        if not memo:
                            st.toast(':red[Invalid value for Memo field]', icon='😢')
                        if price <= 0:
                            st.toast(':red[Invalid value for Price field]', icon='😢')
                    else:
                        values = [date.strftime('%m/%d/%Y'), memo, category, owner, price, payment_method, shared]
                        res = worksheet_client.append_row(values)
                        if res:
                            st.toast(':green[Transaction added successfully!]', icon='🎉')
                        else:
                            st.toast(':red[Something went wrong]', icon='😢')
            with submit_col2:
                def clear():
                    st.session_state['date'] = datetime.date.today()
                    st.session_state['memo'] = ''
                    st.session_state['price'] = 0.0
                    st.session_state['payment_method'] = 'Credit'
                    st.session_state['shared'] = shared_default
                if st.form_submit_button('Clear', type='secondary', on_click=clear, use_container_width=True):
                    st.toast(':green[Form cleared!]', icon='✔️')
    else:
        st.error('Service account not setup with write permissions')
