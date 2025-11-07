import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
import seaborn as sns

#github raw url format
#https://raw.githubusercontent.com/username/repo/branch/path/to/file.xlsx

#Valoarea medie de vanzare per model, per an fabricatie, per varianta echipare
#La numar de km in medie din 30 .000 in 30.000
#Raport la luna
#ttc - pret cu tva
#VANZARE

def main():

    workbook = xlsxwriter.Workbook('ExcelRezultateVanzari.xlsx', {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet('Gestionare - Date')
    headers = ['Modele', 'Echipare', 'An de fabricatie', 'Medie de vanzare', 'Abatere standard', 'Coeficient de variatie', 'Observatii(Total vanzari)']
    worksheet.write_row('A1', headers)
    dataset = pd.read_csv('raportVanzari.csv', encoding = 'utf-8', encoding_errors = 'ignore')
    if dataset.empty:
        print("Excelul de date este gol, eroare la incarcare.")
        return
    data_check = dataset.head()
    print("\nVerificarea incarcarii datelor...", data_check)

     #Curatare de date, coloana cu vanzari
    dataset['MODEL'] = dataset['MODEL'].str.replace(' ','', regex = False)
    dataset['VANZARE'] = dataset['VANZARE'].str.replace(',','', regex=False).str.replace('?','', regex=False).str.replace('lei', '', regex = False).str.strip().astype(float)


    dataset = dataset.dropna(subset = ['VANZARE'])
    nr_valori_lipsa = dataset['VANZARE'].isnull().sum()
    if nr_valori_lipsa > 0:
        print("\nEroare la stergerea coloanelor goale.")
        return
    rezultate_combinate = dataset.groupby(['MODEL', 'VERSIUNE', 'AN FABRICATIE'])['VANZARE'].agg(
        ['mean', 'std', 'count']).reset_index()

    current_row = 1
    for index, row in rezultate_combinate.iterrows():
        worksheet.write(current_row, 0, row['MODEL'])
        worksheet.write(current_row, 1, row['VERSIUNE'])
        worksheet.write(current_row, 2, row['AN FABRICATIE'])
        worksheet.write(current_row, 3, row['mean'])  # Medie Vanzare Combi
        worksheet.write(current_row, 4, row['std'])  # Abatere Std Combi
        worksheet.write(current_row, 6, row['count'])  #numarul de observatii non-nule
        current_row += 1


    worksheet_plot = workbook.add_worksheet('Vizualizari')

    grupare_modele_df = dataset.groupby('MODEL')['VANZARE'].mean().reset_index()
    modele_array = rezultate_combinate['MODEL'].to_numpy()
    medii_vanzare_array = rezultate_combinate['mean'].to_numpy()
    grupare_sortata =grupare_modele_df.sort_values(by = 'MODEL', ascending = True)
    nume_modele_sortate = grupare_sortata['MODEL'].to_numpy()
    medii_sortate = grupare_sortata['VANZARE'].to_numpy()

    #1.--Salvarea si generarea Box_plot-ului--

    plt.figure(figsize=(16, 12))
    sns.boxplot(x='MODEL', y='mean', data=rezultate_combinate)
    plt.xticks(rotation=90, ha='right', fontsize=8)
    plt.title('Distributia Mediei Vanzarilor per Model')
    plt.ylabel('Medie Vanzare')
    plt.xlabel('Model')

    #--Salvare
    boxplot_filename = 'boxplot.vanzari.png'
    plt.savefig(boxplot_filename, bbox_inches = 'tight')
    plt.close()
    #--Inserarea imaginii in excel
    worksheet_plot.insert_image('A2', boxplot_filename)

    #2.--Salvarea si generarea Bar Plot-ului
    plt.figure(figsize = (10,12))
    plt.barh(modele_array, medii_vanzare_array, label = 'Modele')
    plt.title("Plot pentru vizualizarea mediilor in functie de model")
    plt.ylabel("|  Modele  |")
    plt.xlabel("|  Medii de vanzare  |")
    plt.legend()

    barplot_filename = 'barplot.vanzari.png'
    plt.savefig(barplot_filename, bbox_inches = 'tight')
    plt.close()

    worksheet_plot.insert_image('A40', barplot_filename)

    #3.Salvarea si generarea BarPlot-ului - ordonat
    plt.figure(figsize=(10, 12))
    plt.barh(nume_modele_sortate, medii_sortate, label='Modele')
    plt.title("Plot pentru vizualizarea mediilor in functie de model")
    plt.ylabel("|  Modele  |")
    plt.xlabel("|  Medii de vanzare  |")
    plt.legend()

    barplot_ordonat_filename = 'barplot2.vanzari.png'
    plt.savefig(barplot_ordonat_filename, bbox_inches = 'tight')
    plt.close()

    worksheet_plot.insert_image('A60', barplot_ordonat_filename)

    workbook.close()






if(__name__ == "__main__"):
    main()
