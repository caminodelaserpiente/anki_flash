import os
import tempfile


import pandas as pd
import streamlit as st


def load_csv():
    with st.expander("Load CSV", expanded=True):
        path_files = {'dir': tempfile.mkdtemp(),
                'files': []}
        uploaded_files = st.file_uploader("Choose a CSV file", 
                                    type=['csv'], 
                                    accept_multiple_files=True, 
                                    key="csv_uploader")
        if uploaded_files:
            for uploaded_file in uploaded_files:
                original_filename = uploaded_file.name
                temp_file_path = os.path.join(path_files['dir'], original_filename)
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(uploaded_file.read())
                path_files['files'].append(original_filename)
            st.success("CSV files uploaded successfully!")
            return path_files
        else:
            st.warning("No CSV files uploaded.")
            return None



def select_df(path_files):
    try:
        if path_files is not None and path_files.get('files'):
            selected_file = st.selectbox("Selecciona un archivo CSV:", 
                                        path_files['files']
                                        )
            path_csv = os.path.join(path_files['dir'], selected_file)
            df = pd.read_csv(path_csv, header=None)
            if not df.iloc[0].equals(pd.Series(["front", "back"])):
                df.columns = ["front", "back"]
            else:
                df = df.iloc[1:].reset_index(drop=True)
                df.columns = ["front", "back"]
            return df
        else:
            st.warning("No CSV files uploaded.")
            return None
    except ValueError as error:
        return error
        
