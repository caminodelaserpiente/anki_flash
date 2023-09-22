import streamlit as st


def set_page_config():
    st.set_page_config(
        page_title= "anki_flash",
        page_icon= ":card_index_dividers:",
        layout= "wide",
        initial_sidebar_state= "expanded",
        menu_items= {
            'Get Help': 'mailto:caminodelaserpiente.py@gmail.com',
            'Report a bug': 'https://github.com/caminodelaserpiente/anki_flash',
            'About': 'By. 蛇道 @caminodelaserpiente'
        }
    )


def header():
    with st.container():
        st.subheader("Create FlashCards for Anki :card_index_dividers:", anchor=False)
        st.markdown('[![GitHub](https://badgen.net/badge/icon/GitHub?icon=github&color=black&label)](https://github.com/caminodelaserpiente/anki_flash)')
        st.title(":speaking_head_in_silhouette:", anchor=False)
        st.write("---")
