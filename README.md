# Sudoku-Löser mit Kamera

Ein Python-Projekt, das ein Foto eines gedruckten Sudokus einliest, das Gitter und die Zahlen per OCR erkennt, das Rätsel mathematisch löst und das Ergebnis anzeigt.

## Projektstruktur

```
sudoku_solver/
├── image_processing.py   # Modul 1: Bildverarbeitung (OpenCV)
├── grid_extraction.py    # Modul 2: Gitter-Extraktion & OCR
├── sudoku_solver.py      # Modul 3: Backtracking-Algorithmus
├── main.py               # Modul 4: Pipeline & Main-Skript
├── README.md             # Diese Datei
└── requirements.txt      # Python-Abhängigkeiten
```

## Installation

### 1. Python-Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 2. Tesseract OCR installieren

Tesseract ist ein separates Programm, das zusätzlich installiert werden muss.

#### Windows

1. **Download:** Lade den Installer von https://github.com/UB-Mannheim/tesseract/wiki herunter
   - Empfohlen: `tesseract-ocr-w64-setup-5.x.x.exe` (64-Bit)
2. **Installation:** Führe den Installer aus und **merke dir den Installationspfad** (standardmäßig `C:\Program Files\Tesseract-OCR\`)
3. **Sprachpaket:** Während der Installation kannst du zusätzliche Sprachen auswählen. Für Ziffern reicht die Standard-Installation (Englisch).
4. **Umgebungsvariable (optional, aber empfohlen):**
   - Füge `C:\Program Files\Tesseract-OCR\` zur Systemvariablen `PATH` hinzu
   - Oder: Öffne Systemsteuerung → System → Erweiterte Systemeinstellungen → Umgebungsvariablen
   - Bearbeite `Path` und füge den Tesseract-Installationspfad hinzu

**Alternativ (falls PATH nicht gesetzt werden kann):**
Öffne `grid_extraction.py` und füge ganz oben (vor `import pytesseract`) folgende Zeile ein:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
(Passe den Pfad ggf. an deine Installation an.)

#### macOS

```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install tesseract-ocr
```

### 3. Installation überprüfen

```bash
tesseract --version
```

Sollte die Versionsnummer ausgeben. Falls nicht, wurde Tesseract nicht zum PATH hinzugefügt.

## Verwendung

### 1. Testbild bereitstellen

Lege ein Foto eines gedruckten Sudokus (z. B. `test_sudoku.jpg`) im Projektordner ab.
**Wichtig:** Das Sudoku sollte möglichst gut ausgeleuchtet und frontal fotografiert sein.

### 2. Pipeline starten

```bash
python main.py test_sudoku.jpg
```

### 3. Ablauf

1. Das Programm zeigt nacheinander:
   - Das Originalbild
   - Das transformierte Sudoku (von oben)
   - Das Binärbild des Sudokus
2. Drücke eine Taste, um die OCR-Erkennung zu starten
3. Das erkannte und das gelöste Sudoku werden in der Konsole ausgegeben
4. Ein Fenster zeigt das Sudoku mit den gelösten Zahlen (rot eingetragen)
5. Drücke eine Taste zum Beenden

## Module im Überblick

### Modul 1: `image_processing.py` (Bildverarbeitung)
- Lädt ein Bild mit OpenCV
- Wendet Graustufen, Gaußschen Weichzeichner und adaptive Thresholding an
- Findet die größte viereckige Kontur (das Sudoku-Quadrat)
- Führt eine Perspektiventransformation durch

### Modul 2: `grid_extraction.py` (Gitter-Extraktion & OCR)
- Unterteilt das transformierte Bild in 9x9 Zellen
- Schneidet Ränder ab, um Gitterlinien zu entfernen
- Erkennt leere Zellen anhand des Pixelanteils
- Führt OCR mit Tesseract auf jeder Zelle durch
- Gibt ein 9x9-Array zurück (0 = leer)

### Modul 3: `sudoku_solver.py` (Backtracking-Algorithmus)
- Validiert die Ausgangskonfiguration
- Löst das Sudoku mit Backtracking (in Millisekunden)
- Prüft auf eindeutige Lösbarkeit

### Modul 4: `main.py` (Pipeline)
- Verbindet alle Module
- Zeichnet die Lösung in das transformierte Bild ein
- Gibt formatierte Konsolenausgabe

## Fehlerbehebung

### "TesseractOCR wurde nicht gefunden!"
→ Tesseract ist nicht installiert oder nicht im PATH. Siehe Installationsanleitung oben.

### "Kein Sudoku-Quadrat im Bild gefunden!"
→ Das Sudoku ist zu klein, zu schräg oder zu schlecht ausgeleuchtet. Fotografiere es neu.

### OCR erkennt falsche Ziffern
→ Die Bildqualität ist entscheidend. Achte auf:
- Gute Ausleuchtung (keine Schatten)
- Gerade Aufnahme (nicht zu schräg)
- Ausreichende Auflösung
- Sauberer Druck (keine verwischten Zahlen)

## Beispiel

```bash
python main.py mein_sudoku.jpg
```

Ausgabe:
```
==================================================
  SUDOKU-LÖSER MIT KAMERA
==================================================

[1/4] Bild wird geladen und Sudoku-Quadrat wird gesucht...
      ✓ Sudoku-Quadrat gefunden und transformiert!

[2/4] Gitter wird extrahiert und Ziffern werden erkannt (OCR)...
      ✓ Erkennung abgeschlossen!

   Erkanntes Sudoku:
   ╔═══════╤═══════╤═══════╗
   ║ 5 3 . │ . 7 . │ . . . ║
   ║ 6 . . │ 1 9 5 │ . . . ║
   ║ . 9 8 │ . . . │ . 6 . ║
   ╟───────┼───────┼───────╢
   ║ 8 . . │ . 6 . │ . . 3 ║
   ║ 4 . . │ 8 . 3 │ . . 1 ║
   ║ 7 . . │ . 2 . │ . . 6 ║
   ╟───────┼───────┼───────╢
   ║ . 6 . │ . . . │ 2 8 . ║
   ║ . . . │ 4 1 9 │ . . 5 ║
   ║ . . . │ . 8 . │ . 7 9 ║
   ╚═══════╧═══════╧═══════╝

[3/4] Sudoku wird gelöst...
      ✓ Sudoku erfolgreich gelöst!

   Gelöstes Sudoku:
   ╔═══════╤═══════╤═══════╗
   ║ 5 3 4 │ 6 7 8 │ 9 1 2 ║
   ║ 6 7 2 │ 1 9 5 │ 3 4 8 ║
   ║ 1 9 8 │ 3 4 2 │ 5 6 7 ║
   ╟───────┼───────┼───────╢
   ║ 8 5 9 │ 7 6 1 │ 4 2 3 ║
   ║ 4 2 6 │ 8 5 3 │ 7 9 1 ║
   ║ 7 1 3 │ 9 2 4 │ 8 5 6 ║
   ╟───────┼───────┼───────╢
   ║ 9 6 1 │ 5 3 7 │ 2 8 4 ║
   ║ 2 8 7 │ 4 1 9 │ 6 3 5 ║
   ║ 3 4 5 │ 2 8 6 │ 1 7 9 ║
   ╚═══════╧═══════╧═══════╝

[4/4] Ergebnis wird visualisiert...
   ...