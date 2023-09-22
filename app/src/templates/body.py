import pandas as pd
import streamlit as st
import os

from app.src.modules import load_files as load
from app.src.modules import filters as menu


def body():
    with st.sidebar:
        path_csv = load.load_csv()

    with st.container():
        tab1, tab2 = st.tabs(["DataFrame", "Anki Files"])

        with tab1:
            df = load.select_df(path_csv)
            if df is not None:
                try:
                    df = st.data_editor(df, use_container_width=False,)
                except:
                    st.warning("The CSV file does not adhere to the expected format.")

        with tab2:
            col1, col2 = st.columns([3, 1.5])
            with col1:
                if df is not None:
                    with col2:
                        if df is not None and isinstance(df, pd.DataFrame):
                            path_files = menu.mkdir_temp()
                            (anki_csv, path_zip) = menu.generate_files(path_files, df)
                            col1.dataframe(anki_csv, use_container_width=True)
                            if path_zip is not None:
                                st.download_button(
                                        label="Download .zip file",
                                        data=open(path_zip, 'rb').read(),
                                        file_name='anki.zip',
                                         mime='application/zip',
                                        disabled=False
                                    )
                        else:
                            col1.warning("The CSV file does not adhere to the expected format.")
                else:
                    st.warning("No CSV files uploaded.")
