#plot_util

import streamlit as st

def mostrar_en_pestanas(df, fig, option):
    tab1, tab2 = st.tabs(["DataFrame", "Gráfico"])
    with tab1:
        st.write(option)
        st.dataframe(df)
    with tab2:
        if fig is not None:
            st.write(option)
            st.plotly_chart(fig)
