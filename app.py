import streamlit as st
import pandas as pd
from PIL import Image
from script1 import functieGestiuneDate


# functie pentru schimbarea paginilor in on_click
def switch_page(nume_pagina):
    st.session_state.page = nume_pagina


@st.cache_data
def get_data(nume_fisier):
    if nume_fisier is not None:
        try:
            if nume_fisier.name.endswith('.csv'):
                dataset = pd.read_csv(nume_fisier)
            elif nume_fisier.name.endswith(('.xlsx', '.xls')):
                dataset = pd.read_excel(nume_fisier)
            if nume_fisier.name.endswith(('.csv', 'xlsx', 'xls')):
                coloane_necesare = ['NR. CRT.', 'VIN', 'DATA INTRARE VO', 'TIP AUTOVEHICUL', 'MARCA',
                                    'MODEL', 'VERSIUNE', 'CULOARE', 'AN FABRICATIE', 'KM',
                                    'CAPACITATE CILINDRICA', 'PUTERE', 'DATA PRIMEI INMATRICULARI',
                                    'FURNIZOR', 'PROVENIENTA', 'Tip', 'LOCATIA', 'PRET CUMPARARE HT LEI',
                                    'PRET EVALUARE TTC EURO', 'Data validare pret evaluare', 'REZERVARI',
                                    'NR NIR', 'OBSERVATII', 'Serie caroserie', 'Nr inmatriculare vehicul',
                                    'Discount', 'VANZARE', 'Curs € Dacia', 'Pret vanzare lei TTC',
                                    'Pret vanzare lei HT', 'tva', 'Data aviz plata', 'Nr factura',
                                    'Data factura', 'Nume cumparator', 'Conditie interioara',
                                    'Conditie exterioara', 'Pret evaluare DVS (TVA inclus)',
                                    'Pret evaluare Retail (TVA inclus)', 'Pret Trade-in (TVA inclus)',
                                    'Stare', 'Data evaluare', 'FREVO', 'Data final garantie',
                                    'Data actuala', 'Zile ramase garantie', 'Rate facturate',
                                    'Perioada contract', 'CIV', 'IESIRE ROL', 'LIVRATE LA CLIENT',
                                    'DATA OFERTA ANGAJATI', 'Data evaluare.1', 'Zile stoc / data evaluare',
                                    'Zile stoc / data intrare', 'Viteza rotatie']
                if all(col in dataset.columns for col in coloane_necesare):
                    st.success("Excelul a fost introdus corect!")
                    
            dataset_procesat = functieGestiuneDate(dataset)
            return dataset_procesat

        except Exception as e:
            return "Eroare_citire"


def main_page():
    st.title("Home")
    st.text("Pentru a incarca fisierul excel foloseste butonul de mai jos. Se va genera automat un fisier excel cu rezultate" \
    "referitoare la masinile vandute, numarul de kilometri si alti factori care influenteaza media de vanzare. Fisierul se va salva automat " \
    "la descarcari in calculator fiind pregatit de gestiune.")
    st.button("Incarca fisierul Excel", on_click=lambda: switch_page('upload'))
    

def upload_page():
    st.title("Upload page")
    st.session_state.page = 'upload'
    st.button("Back", on_click=lambda: switch_page('main'))
    uploaded_file = st.file_uploader("Incarca fisierul Excel (CSV)/(EXCEL): ")
    #initializez cu none variabila dataset pentru ca ea sa existe indiferent de upload
    dataset = None
    if uploaded_file is not None:
        with st.spinner('Uploading...'):
         dataset = get_data(uploaded_file)
    if isinstance(dataset, pd.DataFrame):  # verifica daca dataset este un pd.DataFrame
        st.success("Fisier incarcat corect si format valid!")
        st.dataframe(dataset.head())

        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine = 'xlsxwriter') as writer:
            dataset.to_excel(writer, index = False, sheet_name = 'MediiVanzari')

        st.download_button(
            label = "Descarca Rezultate",
            data = output.getvalue(),
            file_name = "Rezultate_Vanzari.xlsx",
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Numar randuri", len(dataset))
        with col2:
            st.metric("Numar coloane", len(dataset.columns))
        with col3:
            st.metric("Memorie(MB)", f"{dataset.memory_usage(deep=True).sum()/1024**2:.2f}")


    elif dataset == "Eroare citire":
        st.error("S-a produs o eroare la citirea fisierului. Verificati structura acestuia (XLSX/XLS/CSV)!")

    

def main():
    st.set_page_config(layout="wide", page_title="Statistici Vanzari - Excel")
    if 'page' not in st.session_state:
        st.session_state.page = 'main'

    if st.session_state.page == 'main':
        main_page()
    elif st.session_state.page == 'upload':
        upload_page()


if (__name__ == '__main__'):
    main()