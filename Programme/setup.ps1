Add-Type -AssemblyName System.Windows.Forms
# Funktion um auf Enter zu warten
function Pause ($Message="Press any key to continue...")  
{
  Write-Host -NoNewLine $Message
  $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")  
  Write-Host ""  
}

# Funktion zum Öffnen eines Dialogs zur Ordnerauswahl
function Select-Folder($message) {
    $folderBrowserDialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowserDialog.Description = $message
    $result = $folderBrowserDialog.ShowDialog()
    if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
        return $folderBrowserDialog.SelectedPath
    } else {
        return $null
    }
}

# Funktion zum Öffnen eines Dialogs zur Dateiauswahl
function Select-File($message, $initialDirectory) {
    $fileDialog = New-Object System.Windows.Forms.OpenFileDialog
    $fileDialog.InitialDirectory = $initialDirectory
    $fileDialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*"
    $fileDialog.Title = $message
    $result = $fileDialog.ShowDialog()
    if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
        return $fileDialog.FileName
    } else {
        return $null
    }
}

# Benutzer auffordern, den Pfad zur Python-Installation auszuwählen
$pythonPath = Select-Folder -message "Python.exe -> \AppData\Local\Programs\Python\Python311"
if (-not $pythonPath) {
    Write-Host "Kein Pfad ausgewählt. Skript wird beendet."
    exit
}

# Benutzer auffordern, den Pfad für das Virtual Environment auszuwählen
#$venvPath = Select-Folder -message "Bitte waehlen Sie den Pfad für das Virtual Environment aus"
#if (-not $venvPath) {
#    Write-Host "Kein Pfad ausgewählt. Skript wird beendet."
#    exit
#}

# Benutzer auffordern, den Pfad zur requirements.txt-Datei auszuwählen
$reqPath = Select-Folder -message "Bitte waehlen Sie den Ordner Programme aus, wo die Datei requirements.txt enthalten ist."
if (-not $reqPath) {
    Write-Host "Kein Pfad ausgewählt. Skript wird beendet."
    exit
}
#$reqPath = Select-File -message "Bitte wählen Sie die requirements.txt-Datei aus" -initialDirectory $venvPath
#if (-not $reqPath) {
#    Write-Host "Kein Pfad ausgewählt. Skript wird beendet."
#    exit
#}

# Erstellen des Virtual Environments
Write-Host "Erstelle Virtual Environment..."
& "$pythonPath\python.exe" -m venv "$reqPath\venv\"

# Aktivieren des Virtual Environments
Write-Host "Aktiviere Virtual Environment..."
. "$reqPath\venv\Scripts\activate.ps1"

# Installieren von Modulen aus der requirements.txt
Write-Host "Installiere Module aus requirements.txt..."
pip install -r $reqPath\requirements.txt

# Führe den ersten Import von der csv durch mit first_start.Python-Installation
Write-Host "Lade den ersten Umsatzreport von deiner Bank herunter und drücke enter sobald du die Datei herunter geladen hast. (csv und Kontosaldo vom Export ausschließen wählen."
Pause
python "$reqPath\first_start.py" $reqPath

# Deaktivieren des Virtual Environments
Write-Host "Deaktiviere Virtual Environment..."
deactivate

Write-Host "Fertig!"
