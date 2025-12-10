import numpy as np
import pandas as pd
import xlsxwriter

def functieGestiuneDate(dataset):
    workbook = xlsxwriter.Workbook('Rezultate - Excel.xlsx', {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet('Grupare - Medii de vanzare')
    worksheet2 = workbook.add_worksheet('Pagina suplimentara')
    headers = [
        'TIP AUTOVEHICUL', 'MARCA', 'MODEL', 'VERSIUNE', 'AN FABRICATIE', 'CAPACITATE CILINDRICA', 'PUTERE',
        'INTERVAL_KM', 'MEDIE DE VANZARE',
        'COUNT'
    ]
    worksheet.write_row('A1', headers)
    worksheet2.write_row('A1', headers)

    #dataset = pd.read_csv(nume_fisier, encoding='utf-8', encoding_errors='ignore')

    # Curatare de date
    dataset['MODEL'] = dataset['MODEL'].str.replace(' ', '', regex=False)
    dataset['VANZARE'] = dataset['VANZARE'].str.replace(',', '', regex=False).str.replace('?', '',regex=False).str.replace('lei', '', regex=False).str.strip().astype(float)
    dataset['CULOARE'] = dataset['CULOARE'].astype(str).str.lower().str.strip()
    dataset['KM'] = dataset['KM'].fillna(0)
    dataset['CAPACITATE CILINDRICA'] = dataset['CAPACITATE CILINDRICA'].fillna('ELECTRIC')
    dataset['PUTERE'] = dataset['PUTERE'].fillna('uknown')
    median_vanzare = dataset['VANZARE'].median()
    dataset = dataset.fillna(median_vanzare)

    current_row = 1
    previous_marca = None
    max_km = dataset['KM'].max()
    bins = np.arange(0, max_km + 30001, 30000)
    dataset['KM'] = pd.cut(dataset['KM'], bins=bins, right=True, include_lowest=True).astype(str)
    currency_format = workbook.add_format({'num_format': '€#,##0.00'})
    grupare_tip = {tip: dataset[dataset['TIP AUTOVEHICUL'] == tip] for tip in dataset['TIP AUTOVEHICUL'].unique()}

    for tip, df_tip in grupare_tip.items():
        rezultate_combinate = df_tip.groupby([
            'MARCA', 'MODEL', 'VERSIUNE', 'AN FABRICATIE', 'CAPACITATE CILINDRICA', 'PUTERE', 'KM'
        ])['VANZARE'].agg(['mean', 'count']).reset_index()
        worksheet.write(current_row, 0, tip)

        for index, row in rezultate_combinate.iterrows():
            current_marca = row['MARCA']
            if current_marca != previous_marca:
                worksheet.write(current_row, 1, row['MARCA'])
                previous_marca = current_marca
            worksheet.write(current_row, 2, row['MODEL'])
            worksheet.write(current_row, 3, row['VERSIUNE'])
            worksheet.write(current_row, 4, row['AN FABRICATIE'])
            worksheet.write(current_row, 5, row['CAPACITATE CILINDRICA'])
            worksheet.write(current_row, 6, row['PUTERE'])
            worksheet.write(current_row, 7, row['KM'])
            worksheet.write(current_row, 8, row['mean'], currency_format)
            worksheet.write(current_row, 9, row['count'])

            worksheet2.write(current_row, 0, tip)
            worksheet2.write(current_row, 1, row['MARCA'])
            worksheet2.write(current_row, 2, row['MODEL'])
            worksheet2.write(current_row, 3, row['VERSIUNE'])
            worksheet2.write(current_row, 4, row['AN FABRICATIE'])
            worksheet2.write(current_row, 5, row['CAPACITATE CILINDRICA'])
            worksheet2.write(current_row, 6, row['PUTERE'])
            worksheet2.write(current_row, 7, row['KM'])
            worksheet2.write(current_row, 8, row['mean'], currency_format)
            worksheet2.write(current_row, 9, row['count'])
            current_row += 1

    worksheet.set_column("A:XFD", 25)
    worksheet2.set_column("A:XFD", 25)

    workbook.close()
