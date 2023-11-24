import pandas as pd
import tkinter as tk
from tkinter import filedialog
import sys

# grundpfad = 'G:/Drive/Pythonprojects/Budgettracker/'
grundpfad = sys.argv[1]

def data_import_ing(path: str) -> pd.DataFrame:
    bankdata = pd.read_csv(path, skiprows=12, header=0, sep=';', encoding='ISO-8859-1')
    return bankdata

def data_import_paypal(path: str) -> pd.DataFrame:
    bankdata = pd.read_csv(path, header=0, sep=',')
    return bankdata

def read_data_file(all: bool = True, training: bool = False) -> pd.DataFrame:
    # path = "G:\Drive\Pythonprojects\Budgettracker\Daten\Data.xlsm"
    # data = pd.read_excel(path, engine='openpyxl')
    if training is False:
        # path = "G:/Drive/Pythonprojects/Budgettracker/Daten/Data.csv"
        excel_datei_pfad = grundpfad + '..\\Daten\\Data.xlsx'
        data = pd.read_excel(excel_datei_pfad, sheet_name='Data')
    else:
        path = grundpfad + "../Daten/Trainingsdata.csv"
        data = pd.read_csv(path)

    if all is False:
        data = data[['Auftraggeber/Empfänger', 'Verwendungszweck', 'Buchungstext', 'Kategorie']]
    return data

def prepare_data_for_model(data):
    # Konvertieren Sie beide Spalten in Strings, bevor Sie sie kombinieren
    data['Auftraggeber/Empfänger'] = data['Auftraggeber/Empfänger'].astype(str)
    data['Verwendungszweck'] = data['Verwendungszweck'].astype(str)
    # data['Kategorie'] = data['Kategorie'].astype(str)

    # Jetzt kombinieren Sie die beiden Spalten zu einer einzigen Textspalte
    data['text'] = data['Auftraggeber/Empfänger'] + " " + data['Verwendungszweck']

def append_to_excel(filename, df, sheet_name):
    # Die aktualisierten Daten in die Excel-Datei schreiben
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
        if sheet_name in writer.sheets:
            # Wenn das Blatt bereits existiert, löschen Sie es
            writer.book.remove(writer.sheets[sheet_name])
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def get_path() -> str:
# Ein Tkinter-Fenster erstellen (es wird nicht angezeigt)
    root = tk.Tk()
    root.withdraw()

    # Dateiauswahldialog öffnen
    dateipfad = filedialog.askopenfilename()

    # Überprüfe, ob ein Dateipfad ausgewählt wurde
    if dateipfad:
        print(f'Datei ausgewählt: {dateipfad}')
        return dateipfad
    else:
        print('Keine Datei ausgewählt')

# data = read_data_file()
# print(data.head())

#create_trainings_data()