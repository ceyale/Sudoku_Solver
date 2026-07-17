"""
Modul 2: Gitter-Extraktion & Texterkennung (OCR)
=================================================
Unterteilt das transformierte Sudoku-Bild in 81 Zellen,
führt OCR auf jeder Zelle durch und erstellt ein 9x9-Array.
"""

import cv2
import numpy as np
from typing import List, Optional
import pytesseract


def extract_cells(warped_bin: np.ndarray, grid_size: int = 9) -> List[List[np.ndarray]]:
    """
    Unterteilt das transformierte Sudoku-Bild in ein 9x9-Gitter von Zellen.

    Args:
        warped_bin: Binäres, transformiertes Sudoku-Bild.
        grid_size: Größe des Gitters (Standard: 9x9).

    Returns:
        ​​Eine 9x9-Liste von Zellen-Bildern (jeweils als numpy-Array).
    """
    height, width = warped_bin.shape
    cell_h = height // grid_size
    cell_w = width // grid_size

    cells: List[List[np.ndarray]] = []

    for row in range(grid_size):
        row_cells: List[np.ndarray] = []
        for col in range(grid_size):
            # Zellenkoordinaten berechnen
            y1 = row * cell_h
            y2 = (row + 1) * cell_h
            x1 = col * cell_w
            x2 = (col + 1) * cell_w

            cell = warped_bin[y1:y2, x1:x2]

            # Ränder leicht abschneiden (10% pro Seite), um Gitterlinien zu entfernen
            margin_h = int(cell_h * 0.1)
            margin_w = int(cell_w * 0.1)
            cell_trimmed = cell[margin_h:cell_h - margin_h,
                                margin_w:cell_w - margin_w]

            row_cells.append(cell_trimmed)
        cells.append(row_cells)

    return cells


def preprocess_cell(cell: np.ndarray) -> np.ndarray:
    """
    Bereitet eine einzelne Zelle für die OCR-Erkennung vor:
    - Invertiert das Bild (weiße Schrift auf schwarzem Hintergrund)
    - Fügt einen weißen Rand hinzu (verbessert die Erkennung)
    - Skaliert die Zelle auf eine einheitliche Größe

    Args:
        cell: Binäres Zellen-Bild.

    Returns:
        Vorverarbeitetes Zellen-Bild.
    """
    # Invertieren: Tesseract erwartet schwarze Schrift auf weißem Hintergrund
    cell_inv = cv2.bitwise_not(cell)

    # Weißen Rand hinzufügen (10 Pixel)
    cell_padded = cv2.copyMakeBorder(
        cell_inv, 10, 10, 10, 10,
        cv2.BORDER_CONSTANT, value=255
    )

    # Auf eine einheitliche Größe skalieren (z. B. 64x64)
    cell_resized = cv2.resize(cell_padded, (64, 64), interpolation=cv2.INTER_AREA)

    return cell_resized


def is_cell_empty(cell: np.ndarray, threshold: float = 0.02) -> bool:
    """
    Prüft, ob eine Zelle leer ist, indem der Anteil der Vordergrundpixel
    (weiße Pixel im Binärbild) gemessen wird.

    Args:
        cell: Binäres Zellen-Bild.
        threshold: Schwellwert für den Anteil der Vordergrundpixel.
                   Liegt der Anteil darunter, gilt die Zelle als leer.

    Returns:
        True, wenn die Zelle leer ist, sonst False.
    """
    # Zähle weiße Pixel (Vordergrund)
    white_pixels = np.sum(cell > 0)
    total_pixels = cell.size

    ratio = white_pixels / total_pixels
    return ratio < threshold


def recognize_digit(cell: np.ndarray) -> Optional[int]:
    """
    Erkennt eine Ziffer in einer Zelle mit Tesseract OCR.

    Args:
        cell: Vorverarbeitetes Zellen-Bild.

    Returns:
        Die erkannte Ziffer (1-9) oder None, falls keine Ziffer erkannt wurde.
    """
    # Tesseract-Konfiguration:
    #   --psm 10: Einzelzeichen-Modus
    #   --oem 3: Standard-Engine (LSTM + Legacy)
    #   -c tessedit_char_whitelist=123456789: Nur Ziffern 1-9
    config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=123456789'

    try:
        text = pytesseract.image_to_string(cell, config=config).strip()
    except pytesseract.TesseractNotFoundError:
        raise RuntimeError(
            "Tesseract OCR wurde nicht gefunden! "
            "Stelle sicher, dass Tesseract installiert ist und "
            "der Pfad in der Systemvariable PATH oder in der "
            "pytesseract.pytesseract.tesseract_cmd Variable gesetzt ist."
        )

    if text and text.isdigit():
        return int(text)

    return None


def extract_grid(warped_bin: np.ndarray) -> List[List[int]]:
    """
    Extrahiert das vollständige 9x9-Sudoku-Gitter aus dem transformierten Binärbild.

    Args:
        warped_bin: Binäres, transformiertes Sudoku-Bild.

    Returns:
        Ein 9x9-Array mit den erkannten Ziffern (0 für leere Felder).
    """
    # 1. Zellen extrahieren
    cells = extract_cells(warped_bin)

    # 2. 9x9-Array initialisieren
    grid: List[List[int]] = [[0] * 9 for _ in range(9)]

    for row in range(9):
        for col in range(9):
            cell = cells[row][col]

            # Prüfen, ob die Zelle leer ist
            if is_cell_empty(cell):
                grid[row][col] = 0
                continue

            # Zelle für OCR vorbereiten
            cell_processed = preprocess_cell(cell)

            # Ziffer erkennen
            digit = recognize_digit(cell_processed)

            if digit is not None:
                grid[row][col] = digit
            else:
                grid[row][col] = 0  # Fallback: als leer markieren

    return grid


def print_grid(grid: List[List[int]]) -> None:
    """
    Gibt das Sudoku-Gitter formatiert auf der Konsole aus.

    Args:
        grid: 9x9-Sudoku-Array.
    """
    print("╔═══════╤═══════╤═══════╗")
    for i, row in enumerate(grid):
        line = "║ "
        for j, val in enumerate(row):
            line += f"{val if val != 0 else '.'} "
            if (j + 1) % 3 == 0 and j < 8:
                line += "│ "
        line += "║"
        print(line)
        if (i + 1) % 3 == 0 and i < 8:
            print("╟───────┼───────┼───────╢")
    print("╚═══════╧═══════╧═══════╝")