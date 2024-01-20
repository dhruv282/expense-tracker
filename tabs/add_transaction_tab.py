import datetime
import streamlit as st
from styling import category_color_map, payment_method_color_map, get_owner_color_map, payment_method_label_prefix
from utils import get_worksheet_client, get_transaction_tab_shared_default, get_transaction_tab_presets

def transaction_tab() -> None:
    worksheet_client = get_worksheet_client()
    memo_default = ''
    category_options = [c for c in category_color_map.keys() if c != 'Savings']
    category_default = 0
    owner_options = list(get_owner_color_map().keys())
    owner_default = 0
    price_default = 0.0
    payment_options = list(payment_method_color_map.keys())
    payment_method_default = payment_options.index('Credit')
    shared_default = get_transaction_tab_shared_default()
    shared_value = shared_default
    if worksheet_client:
        presets = get_transaction_tab_presets()
        if presets:
            preset = st.selectbox('Preset', ['New transaction'] + list(presets.keys()), key='preset')
            if preset:
                if preset == 'New transaction':
                    memo_default = ''
                    price_default = 0.0
                    payment_method_default = payment_options.index('Credit')
                else:
                    preset_val = presets[preset]
                    if 'memo' in preset_val:
                        memo_default = preset_val['memo']
                    if 'category' in preset_val:
                        category_default = category_options.index(preset_val['category'])
                    if 'owner' in preset_val:
                        owner_default = owner_options.index(preset_val['owner'])
                    if 'price' in preset_val:
                        price_default = float(preset_val['price'])
                    if 'payment_method' in preset_val:
                        payment_method_default = payment_options.index(preset_val['payment_method'])
                    if 'shared' in preset_val:
                        shared_value = bool(preset_val['shared'])

        with st.form('add_transaction_form', clear_on_submit=False, border=False):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input('Date', value='today', format='MM/DD/YYYY', key='date')
                memo = st.text_input('Memo', value=memo_default, key='memo')
                category = st.selectbox('Category',
                                        category_options,
                                        index=category_default, key='category')
            with col2:
                owner = st.selectbox('Owner', owner_options,
                                     index=owner_default, key='owner')
                price = st.number_input('Price', value=price_default, key='price')
                payment_method = st.selectbox('Payment Method', payment_options,
                                            format_func=lambda p: f'{payment_method_label_prefix[p]} {p}',
                                            index=payment_method_default, key='payment_method')
                shared = st.checkbox('Shared Expense?',
                                     value=shared_value, key='shared')
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
                        res = worksheet_client.append_row(values, value_input_option = 'USER_ENTERED')
                        if res:
                            st.toast(':green[Transaction added successfully!]', icon='🎉')
                        else:
                            st.toast(':red[Something went wrong]', icon='😢')
            with submit_col2:
                def clear():
                    st.session_state['preset'] = 'New transaction'
                    st.session_state['date'] = datetime.date.today()
                    st.session_state['memo'] = ''
                    st.session_state['price'] = 0.0
                    st.session_state['payment_method'] = 'Credit'
                    st.session_state['shared'] = shared_default
                if st.form_submit_button('Clear', type='secondary', on_click=clear, use_container_width=True):
                    st.toast(':green[Form cleared!]', icon='✔️')
    else:
        st.error('Service account not setup with write permissions')
