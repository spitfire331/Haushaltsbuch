from joblib import load
import pandas as pd
import file_handling as fh
from openpyxl import load_workbook
import datetime
import shutil
import sys

# grundpfad = 'G:/Drive/Pythonprojects/Budgettracker/'
grundpfad = sys.argv[1]
print(grundpfad)

# Heutiger Tag
today = datetime.date.today()
# dd/mm/YY
d1 = today.strftime("%d-%m-%Y")
aktueller_zeitpunkt = datetime.datetime.now()

# Das Datum und die Uhrzeit formatieren und ausgeben
formatierter_zeitpunkt = aktueller_zeitpunkt.strftime("%Y-%m-%d %H:%M:%S")

# Modell laden
loaded_pipeline = load(grundpfad + '..\\Daten\\trained_model.joblib')
# Dataset laden
data = fh.read_data_file()
# data.head()

importpath = fh.get_path()
ing = fh.data_import_ing(importpath)
# Verschiebe die InputDatei in das Importverzeichniss
try:    
    shutil.move(importpath, grundpfad + '..\\Daten\\Import')
except:
    print("Datei ist schon im Importverzeichniss")
# Df invertieren, da das aktuellste Datum ganz oben steht
ing = ing.iloc[::-1].reset_index(drop=True)
# Konvertieren Sie die Spalte 'datum' in das gewünschte Format
ing['Buchung'] = pd.to_datetime(ing['Buchung'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
ing['Valuta'] = pd.to_datetime(ing['Valuta'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
# data['Buchung'] = pd.to_datetime(data['Buchung'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
# data['Valuta'] = pd.to_datetime(data['Valuta'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
# Kommazahl in Punkt ändern
# ing['Betrag'] = ing['Betrag'].astype(str).str.replace(',', '.')
# ing.head()

# Liste der Spalten, die Sie berücksichtigen möchten
cols = ['Buchung', 'Valuta', 'Auftraggeber/Empfänger', 'Buchungstext', 'Verwendungszweck', 'Betrag', 'Währung']

# Bestimmen Sie den letzten Eintrag von df1
last_entry = data[cols]
last_entry = data.iloc[-1]
last_entry_betrag = str(last_entry['Betrag'])

# Vergleiche die Einträge mit den vorhanden Daten und behalte nur die neuen Einträge
for index, row in ing.iterrows():
    if row['Verwendungszweck'] == last_entry['Verwendungszweck'] and row['Auftraggeber/Empfänger'] == last_entry['Auftraggeber/Empfänger'] and row['Buchung'] == last_entry['Buchung'] and row['Betrag'] == last_entry_betrag:
        print(index)
        ing = ing.iloc[index + 1:]

# ing.head()


fh.prepare_data_for_model(ing)


X_new_data = ing['text']
predictions = loaded_pipeline.predict(X_new_data)


ing['Kategorie'] = predictions
ing = ing.drop(columns=['text'])

# ing.head()

df = pd.concat([data, ing], ignore_index= True)
# df.head()


df['Betrag'] = df['Betrag'].astype(str).str.replace('.', ',')
# test.head()


# df.to_csv('G:/Drive/Pythonprojects/Budgettracker/Daten/Data.csv', index=False)

fh.append_to_excel(grundpfad + '..\\Daten\\Data.xlsx', df, 'Data')


# Logeintrag in Data.xlsx
excel_datei_pfad = grundpfad + '..\\Daten\\Data.xlsx'
df_date = pd.read_excel(excel_datei_pfad, sheet_name='Log')
df_date.loc[len(df_date)] = [d1]
# df_date.head()
fh.append_to_excel(grundpfad + '..\\Daten\\Data.xlsx', df_date, 'Log')


info = input("Drücke Enter zum fortfahren...")