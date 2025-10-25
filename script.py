import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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
    dataset = pd.read_csv('raportVanzari.csv', encoding = 'utf-8', encoding_errors = 'ignore')
    if dataset.empty:
        print("Excelul de date este gol, eroare la incarcare.")
        return
    data_check = dataset.head()
    print("\nVerificarea incarcarii datelor...", data_check)
    model = dataset['MODEL']
    versiune  = dataset['VERSIUNE']
    an_fabricatie = dataset['AN FABRICATIE']
    print("\nVerificare model...\n", model)
    print("\nVerificare versiune...\n", versiune)
    print("\nVerificare an fabricatie...\n", an_fabricatie)
    #Curatare de date, coloana cu vanzari
    dataset['MODEL'] = dataset['MODEL'].str.replace(' ','', regex = False)
    dataset['VANZARE'] = dataset['VANZARE'].str.replace(',','', regex=False).str.replace('?','', regex=False).str.replace('lei', '', regex = False).str.strip().astype(float)
    #convert la tip float dupa eliminarea caracterelor nedorite
    median = dataset['VANZARE'].median()
    dataset['VANZARE'].fillna(median, inplace = True)
    nr_valori_lipsa = dataset['VANZARE'].isnull().sum()
    if nr_valori_lipsa > 0:
        print("\nEroare la completarea cu mediana!")
        return
    #Incerc sa combin marca si echiparea pentru vizualizare
    matrice_echipare = np.column_stack((model, versiune))
    print("\nVerificare matrice...\n", matrice_echipare)

    #Grupare dupa fiecare model, pentru a putea accesa fiecare coloana din fiecare masina in parte
    #Creează un dicționar cu modelele ca chei și datele lor ca valori
    grupare_modele = {model: dataset[dataset['MODEL'] == model] for model in dataset['MODEL'].unique()}
    grupare_versiune = {versiune: dataset[dataset['VERSIUNE'] == versiune] for versiune in dataset['VERSIUNE'].unique()}
    grupare_an_fabricatie = {an_fabricatie: dataset[dataset['AN FABRICATIE']==an_fabricatie] for an_fabricatie in dataset['AN FABRICATIE'].unique()}

    #Initializarea unor vectori pentru stocarea mediilor fiecarui model/an de fabricatie/versiune pentru a observa diferentele dintre date
    medii_vanzare_model= []
    medii_vanzare_an_fabricatie = []
    medii_vanzare_versiune = []

    for model in grupare_modele:
        media = grupare_modele[model]['VANZARE'].mean()
        medii_vanzare_model.append(media)
        print(f"Pentru modelul {model}, media de vanzare este: {media:.2f}.")

    print("\n")
    for an_fabricatie in grupare_an_fabricatie:
        media = grupare_an_fabricatie[an_fabricatie]['VANZARE'].mean()
        medii_vanzare_an_fabricatie.append(media)
        print(f"Pentru anul de fabricatie {an_fabricatie}, media de vanzare este: {media:.2f}.")

    print("\n")
    for versiune in grupare_versiune:
        media = grupare_versiune[versiune]['VANZARE'].mean()
        medii_vanzare_versiune.append(media)
        print(f"Pentru varianta de echipare {versiune}, media de vanzare este: {media:.2f}.")


if(__name__ == "__main__"):
    main()