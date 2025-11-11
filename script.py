import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
import seaborn as sns


def main():
    workbook = xlsxwriter.Workbook('Rezultate - Excel.xlsx', {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet('Grupare - Medii de vanzare')
    headers = [
        'MARCA', 'MODEL', 'VERSIUNE', 'AN FABRICATIE', 'CAPACITATE CILINDRICA', 'PUTERE', 'MEDIE DE VANZARE',
        'COUNT'
    ]
    worksheet.write_row('A1', headers)
    dataset = pd.read_csv('raportVanzari.csv', encoding='utf-8', encoding_errors='ignore')
    if dataset.empty:
        print("Excelul de date este gol, eroare la incarcare.")
        return
    data_check = dataset.head()
    print("\nVerificarea incarcarii datelor...", data_check)

    # Curatare de date, coloana cu vanzari
    dataset['MODEL'] = dataset['MODEL'].str.replace(' ', '', regex=False)
    dataset['VANZARE'] = dataset['VANZARE'].str.replace(',', '', regex=False).str.replace('?', '',regex=False).str.replace('lei', '', regex=False).str.strip().astype(float)
    dataset['CULOARE'] = dataset['CULOARE'].astype(str).str.lower().str.strip()


    dataset = dataset.dropna(subset=['VANZARE'])
    nr_valori_lipsa = dataset['VANZARE'].isnull().sum()
    if nr_valori_lipsa > 0:
        print("\nEroare la stergerea coloanelor goale.")
        return
    grupare_marca = {marca: dataset[dataset['MARCA'] == marca] for marca in dataset['MARCA'].unique()}

    current_row = 1
    for marca, df_marca in grupare_marca.items():

        # Grupare pe cele 6 atribute in cadrul marcii curente si calcul 'mean' si 'count'
        rezultate_combinate = df_marca.groupby([
            'MODEL', 'VERSIUNE', 'AN FABRICATIE', 'CAPACITATE CILINDRICA', 'PUTERE'
        ])['VANZARE'].agg(['mean', 'count']).reset_index()
        worksheet.write(current_row, 0, marca)

        for index, row in rezultate_combinate.iterrows():
            worksheet.write(current_row, 1, row['MODEL'])
            worksheet.write(current_row, 2, row['VERSIUNE'])
            worksheet.write(current_row, 3, row['AN FABRICATIE'])
            worksheet.write(current_row, 4, row['CAPACITATE CILINDRICA'])
            worksheet.write(current_row, 5, row['PUTERE'])
            worksheet.write(current_row, 6, row['mean'])
            worksheet.write(current_row, 7, row['count'])
            current_row += 1


    workbook.close()



if (__name__ == '__main__'):
    main()