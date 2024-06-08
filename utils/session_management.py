#session_management

import streamlit as st

def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "show_create_user_form" not in st.session_state:
        st.session_state.show_create_user_form = False
    if "stock_file" not in st.session_state:
        st.session_state.stock_file = None
    if "markup_stock_file" not in st.session_state:
        st.session_state.markup_stock_file = None
    if "markup_sales_file" not in st.session_state:
        st.session_state.markup_sales_file = None
    if "sales_file" not in st.session_state:
        st.session_state.sales_file = None
    if "vencimiento_stock_file" not in st.session_state:
        st.session_state.vencimiento_stock_file = None
    if "vencimiento_vencimientos_file" not in st.session_state:
        st.session_state.vencimiento_vencimientos_file = None

def delete_file(file_type):
    st.session_state[f"{file_type}_file"] = None
    st.session_state[f"df_{file_type}"] = None
