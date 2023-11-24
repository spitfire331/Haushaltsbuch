import file_handling
import pandas as pd
import sys

# grundpfad = 'G:/Drive/Pythonprojects/Budgettracker/'
grundpfad = sys.argv[1]

data = file_handling.read_data_file(False, training=False)
# data.head()

# Importieren Sie die erforderlichen Bibliotheken
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump
import shutil

# Konvertieren Sie beide Spalten in Strings, bevor Sie sie kombinieren
data['Auftraggeber/Empfänger'] = data['Auftraggeber/Empfänger'].astype(str)
data['Verwendungszweck'] = data['Verwendungszweck'].astype(str)
data['Buchungstext'] = data['Buchungstext'].astype(str)
data['Kategorie'] = data['Kategorie'].astype(str)

# Jetzt kombinieren Sie die beiden Spalten zu einer einzigen Textspalte
data['text'] = data['Auftraggeber/Empfänger'] + " " + data['Verwendungszweck'] + " " + data['Buchungstext']



# Teilen Sie die Daten in Trainings- und Testsets auf
X = data['text']
Y = data['Kategorie']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=123)

# Erstellen Sie eine Pipeline mit CountVectorizer und LogisticRegression
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', LogisticRegression(max_iter=10000))  # Erhöhen Sie max_iter, falls die Konvergenz nicht erreicht wird
])

# Trainieren Sie das Modell
pipeline.fit(X_train, y_train)

# Vorhersagen für das Testset
y_pred = pipeline.predict(X_test)

# Auswerten des Modells
accuracy = accuracy_score(y_test, y_pred)


# Detaillierterer Bericht
report = classification_report(y_test, y_pred)
print(report)

# Backup des vorherigen Modells speichern
try:
    shutil.copy(grundpfad + '..\\Daten\\trained_model.joblib', grundpfad + '..\\Daten\\trained_model.bak')
except:
    print("Keine Datei vorhanden!")
# Modell speichern
dump(pipeline, grundpfad + '..\\Daten\\trained_model.joblib')


print(f"Genauigkeit des Modells: {accuracy:.2f}")
info = input("Drücke Enter zum fortfahren...")

