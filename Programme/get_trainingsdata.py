import pandas as pd


excel_datei_pfad = 'G:/Drive/Pythonprojects/Budgettracker/Daten/Data.xlsx'

# Lade die Excel-Datei in ein Pandas DataFrame
df = pd.read_excel(excel_datei_pfad, sheet_name='Data')

# Pfad zur CSV-Datei für die Ausgabe
csv_datei_pfad = 'G:/Drive/Pythonprojects/Budgettracker/Daten/Trainingsdata.csv'

# Daten als CSV-Datei speichern mit Komma als Separator
# df.to_csv(csv_datei_pfad, index=False, sep=',', encoding='utf-8')
df.to_csv(csv_datei_pfad, index=False, sep=',')

info = input("Drücke Enter zum fortfahren...")