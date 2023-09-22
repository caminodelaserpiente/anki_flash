import streamlit as st


def css(): 
    # Ocultar pie de página
    st.markdown(
        """
        <style>
        footer {
            visibility: hidden;
        }
        </style>

        <style>
            .st-emotion-cache-ki0vs3 p:nth-child(2) {
                display: none;
            }
        </style>

        """,
        unsafe_allow_html=True
    )
