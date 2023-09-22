import os
import tempfile
import time
import zipfile


import pandas as pd
import streamlit as st
from gtts import gTTS


def mkdir_temp():
    if 'path_files' not in st.session_state:
        st.session_state.path_files = {'dir': tempfile.mkdtemp(),
                                       'files': []}
    return st.session_state.path_files


def _filters_column():
    option_column = st.radio(
            "Select column to convert audio",
            ["front", "back"],
            captions = None
            )
    return option_column


def _filters_lang():
    languages = {
        'español': ['es', 'com.mx'],
        'english': ['en', 'us'],
        'française': ['fr', 'fr'],
        'deutsche': ['de', 'de'],
        'italiano': ['it', 'it'],
    }
    option_lang = st.selectbox(
            "Select language",
            list(languages.keys())
            )
    return languages, option_lang


def _generate_csv(path_files, dataframe, option_column):
    df_anki = dataframe.copy()
    # Generate CSV for Anki
    name_csv = 'import_anki.csv'
    temp_file_path = os.path.join(path_files['dir'], 'import_anki.csv')
    df_anki[option_column] = df_anki.apply(lambda row: f"{row[option_column]}<br>[sound:{row[option_column]}.mp3]", axis=1)
    df_anki.to_csv(temp_file_path, index=False, header=False)
    path_files['files'].append(name_csv)
    return df_anki


def _generate_mp3(path_files, dataframe, option_column, languages, option_lang):
    for index, row in dataframe.iterrows():
        text = row[option_column]
        name_mp3 = f"{text}.mp3"
        temp_file_path = os.path.join(path_files['dir'], name_mp3)
        tts = gTTS(text, lang=languages[option_lang][0], tld=languages[option_lang][1])
        tts.save(temp_file_path)
        path_files['files'].append(name_mp3)


def _generate_zip(path_files):
    name_zip = 'anki.zip'
    temp_file_path = os.path.join(path_files['dir'], name_zip)
    progress_text = 'Creating .mp3... Wait a moment'
    my_bar = st.progress(0, text=progress_text)
    with zipfile.ZipFile(temp_file_path, 'w') as zip_file:
        for count, file in enumerate(path_files['files']):
            path_file = os.path.join(path_files['dir'], file)
            zip_file.write(path_file, file)
            time.sleep(0.1)
            my_bar.progress((count + 1) / len(path_files['files']), text=progress_text)
    return temp_file_path


def generate_files(path_files, dataframe):
    # Clean files from /temp/path_files['dir']
    for archivo in os.listdir(path_files['dir']):
        if os.path.exists(os.path.join(path_files['dir'], archivo)):
            os.remove(os.path.join(path_files['dir'], archivo))
    path_files['files'] = []
    # Generate_files
    option_column = _filters_column()
    anki_csv = _generate_csv(path_files, dataframe, option_column)
    (languages, option_lang) = _filters_lang()
    if st.button('Generate files'):
        _generate_mp3(path_files, dataframe, option_column, languages, option_lang)
        path_zip = _generate_zip(path_files)
        return anki_csv, path_zip
    return anki_csv, None
