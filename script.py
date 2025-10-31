import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
import os
import tarfile
import urllib
#github raw url format
#https://raw.githubusercontent.com/username/repo/branch/path/to/file.xlsx

#Valoarea medie de vanzare per model, per an fabricatie, per varianta echipare
#La numar de km in medie din 30 .000 in 30.000
#Raport la luna
#ttc - pret cu tva
#VANZARE

def main():
    workbook = xlsxwriter.Workbook('ExcelRezultateVanzari.xlsx', {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet()
    headers = ['Modele', 'Medie vanzare/Model', 'Abatere standard/MedieModel',
               'An de fabricatie', 'Medie vanzare/An de fabricatie', 'Abatere standard/MedieAnFabricatie',
               'Echipare', 'Medie vanzare/Echipare', 'Abatere standard/Echipare']
    worksheet.write_row('A1', headers)
    dataset = pd.read_csv('raportVanzari.csv', encoding = 'utf-8', encoding_errors = 'ignore')
    if dataset.empty:
        print("Excelul de date este gol, eroare la incarcare.")
        return
    data_check = dataset.head()
    print("\nVerificarea incarcarii datelor...", data_check)

    model = dataset['MODEL']
    versiune  = dataset['VERSIUNE']
    an_fabricatie = dataset['AN FABRICATIE']

    #Curatare de date, coloana cu vanzari
    dataset['MODEL'] = dataset['MODEL'].str.replace(' ','', regex = False)
    dataset['VANZARE'] = dataset['VANZARE'].str.replace(',','', regex=False).str.replace('?','', regex=False).str.replace('lei', '', regex = False).str.strip().astype(float)

    median = dataset['VANZARE'].median()
    dataset['VANZARE'].fillna(median, inplace = True)
    nr_valori_lipsa = dataset['VANZARE'].isnull().sum()
    if nr_valori_lipsa > 0:
        print("\nEroare la completarea cu mediana!")
        return


    #Grupare dupa fiecare model, pentru a putea accesa fiecare coloana din fiecare masina in parte
    #Creează un dicționar cu modelele chei și datele lor ca valori
    grupare_modele = {model: dataset[dataset['MODEL'] == model] for model in dataset['MODEL'].unique()}
    grupare_versiune = {versiune: dataset[dataset['VERSIUNE'] == versiune] for versiune in dataset['VERSIUNE'].unique()}
    grupare_an_fabricatie = {an_fabricatie: dataset[dataset['AN FABRICATIE']==an_fabricatie] for an_fabricatie in dataset['AN FABRICATIE'].unique()}

    #Initializarea unor vectori pentru stocarea mediilor fiecarui model/an de fabricatie/versiune pentru a observa diferentele dintre date
    medii_vanzare_model= []
    medii_vanzare_an_fabricatie = []
    medii_vanzare_versiune = []
    #Vectori de abatere standard
    std_vanzare_model = []
    std_vanzare_an_fabricatie = []
    std_vanzare_versiune = []
    #Liste pentru modele pentru ca sus avem dictionare
    lista_modele = []
    lista_an_fabricatie = []
    lista_versiune = []

    for model in grupare_modele:
        media = grupare_modele[model]['VANZARE'].mean()
        abatere_standard_model = grupare_modele[model]['VANZARE'].std()
        medii_vanzare_model.append(media)
        std_vanzare_model.append(abatere_standard_model)
        lista_modele.append(model)
        print(f"Pentru modelul {model}, media de vanzare este: {media:.2f}.")

    for row, values in enumerate(lista_modele, start = 1):
        worksheet.write(row, 0, values)
    for row, values in enumerate(medii_vanzare_model, start = 1):
        worksheet.write(row, 1, values)
    for row, values in enumerate(std_vanzare_model, start = 1):
        worksheet.write(row, 2, values)

    print("\n")
    for an_fabricatie in grupare_an_fabricatie:
        media = grupare_an_fabricatie[an_fabricatie]['VANZARE'].mean()
        abatere_standard_an = grupare_an_fabricatie[an_fabricatie]['VANZARE'].std()
        medii_vanzare_an_fabricatie.append(media)
        std_vanzare_an_fabricatie.append(abatere_standard_an)
        lista_an_fabricatie.append(an_fabricatie)
        print(f"Pentru anul de fabricatie {an_fabricatie}, media de vanzare este: {media:.2f}.")

    for row, values in enumerate(lista_an_fabricatie, start = 1):
        worksheet.write(row, 3, values)
    for row, values in enumerate(medii_vanzare_an_fabricatie, start = 1):
        worksheet.write(row, 4, values)
    for row, values in enumerate(std_vanzare_an_fabricatie, start = 1):
        worksheet.write(row, 5, values)

    print("\n")
    for versiune in grupare_versiune:
        media = grupare_versiune[versiune]['VANZARE'].mean()
        abatere_standard_echipare = grupare_versiune[versiune]['VANZARE'].std()
        medii_vanzare_versiune.append(media)
        std_vanzare_versiune.append(abatere_standard_echipare)
        lista_versiune.append(versiune)
        print(f"Pentru varianta de echipare {versiune}, media de vanzare este: {media:.2f}.")

    for row, values in enumerate(lista_versiune, start = 1):
        worksheet.write(row, 6, values)
    for row, values in enumerate(medii_vanzare_versiune,start = 1):
        worksheet.write(row, 7, values)
    for row, values in enumerate(std_vanzare_versiune, start = 1):
        worksheet.write(row, 8, values)


    workbook.close()
if(__name__ == "__main__"):
    main()