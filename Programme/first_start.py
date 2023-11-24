import pandas as pd
import file_handling as fh
import datetime
import shutil
import sys
import os
from openpyxl import load_workbook
import numpy as np

# grundpfad = 'G:/Drive/Pythonprojects/Budgettracker/'
grundpfad = sys.argv[1]
venvpfad = grundpfad + '\\venv\\Scripts\\python.exe'


file_path = '../Haushaltsbuch.xlsm'
grundpfad = os.path.dirname(grundpfad.rstrip("\\")) + "\\Daten\\"

print(grundpfad)
print(venvpfad)


# x = input('Drücke Enter...')

# Heutiger Tag
today = datetime.date.today()
# dd/mm/YY
d1 = today.strftime("%d-%m-%Y")
aktueller_zeitpunkt = datetime.datetime.now()

# Das Datum und die Uhrzeit formatieren und ausgeben
formatierter_zeitpunkt = aktueller_zeitpunkt.strftime("%Y-%m-%d %H:%M:%S")

importpath = fh.get_path()
ing = fh.data_import_ing(importpath)
# Verschiebe die InputDatei in das Importverzeichniss
try:    
    shutil.move(importpath, grundpfad + '\\Import')
except:
    print("Datei ist schon im Importverzeichniss")
# Df invertieren, da das aktuellste Datum ganz oben steht
ing = ing.iloc[::-1].reset_index(drop=True)
# Konvertieren Sie die Spalte 'datum' in das gewünschte Format
ing['Buchung'] = pd.to_datetime(ing['Buchung'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
ing['Valuta'] = pd.to_datetime(ing['Valuta'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
ing['Kategorie'] = np.nan
fh.append_to_excel(grundpfad + '\\Data.xlsx', ing, 'Data')


# Logeintrag in Data.xlsx
excel_datei_pfad = grundpfad + '\\Data.xlsx'
df_date = pd.read_excel(excel_datei_pfad, sheet_name='Log')
df_date.loc[len(df_date)] = [d1]
# df_date.head()
fh.append_to_excel(grundpfad + '\\Data.xlsx', df_date, 'Log')

# # SPeichere die Pfade in Excel, damit dort die Programme funktionieren
# workbook = load_workbook(filename=file_path, keep_vba=True)

# # Zugriff auf das Tabellenblatt "Pfade"
# sheet = workbook['Pfade']

# # Ändern des Werts in Zelle B2
# sheet['B2'] = venvpfad
# sheet['B3'] = grundpfad
# sheet['B4'] = grundpfad + '\\Data.xlsx'

# # Speichern der Änderungen in der Datei
# workbook.save(filename=file_path)'


info = input("Drücke Enter zum fortfahren...")