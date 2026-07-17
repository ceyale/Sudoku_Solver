"""
Modul 4: Pipeline & Main-Skript
================================
Verbinder alle Module und führt die vollständige Pipeline aus:
Bild laden → Sudoku erkennen → Lösen → Ergebnis anzeigen.

Bonus: Die gelösten Zahlen werden visuell in das transformierte
Sudoku-Bild zurückgezeichnet.
"""

import cv2
import numpy as np
from typing import List, Tuple
import sys
import os

# Eigene Module importieren
from image_processing import process_image
from grid_extraction import extract_grid, print_grid
from sudoku_solver import solve_sudoku


def draw_solution(warped: np.ndarray, original_grid: List[List[int]],
                  solved_grid: List[List[int]]) -> np.ndarray:
    """
    Zeichnet die gelösten Zahlen in die leeren Felder des transformierten
    Sudoku-Bildes (BGR) ein.

    Args:
        warped: Das transformierte Sudoku-Bild (BGR, 450x450).
        original_grid: Das ursprünglich erkannte 9x9-Gitter (0 = leer).
        solved_grid: Das gelöste 9x9-Gitter.

    Returns:
        Das Bild mit eingetragenen Lösungszahlen.
    """
    # Arbeitskopie erstellen (BGR)
    result = warped.copy()
    height, width = result.shape[:2]
    cell_h = height // 9
    cell_w = width // 9

    # Schriftart-Einstellungen
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2
    font_thickness = 2
    font_color = (0, 0, 255)  # Rot in BGR

    for row in range(9):
        for col in range(9):
            # Nur leere Felder beschriften
            if original_grid[row][col] == 0:
                digit = str(solved_grid[row][col])

                # Zellenmittelpunkt berechnen
                x_center = col * cell_w + cell_w // 2
                y_center = row * cell_h + cell_h // 2

                # Textgröße für Zentrierung ermitteln
                (text_w, text_h), baseline = cv2.getTextSize(
                    digit, font, font_scale, font_thickness
                )

                # Text zentriert positionieren
                x = x_center - text_w // 2
                y = y_center + text_h // 2

                cv2.putText(result, digit, (x, y), font, font_scale,
                            font_color, font_thickness, cv2.LINE_AA)

    return result


def run_pipeline(image_path: str, show_steps: bool = True) -> None:
    """
    Führt die vollständige Sudoku-Löser-Pipeline aus.

    Args:
        image_path: Pfad zum Eingabebild.
        show_steps: Wenn True, werden Zwischenschritte angezeigt.
    """
    print("=" * 50)
    print("  SUDOKU-LÖSER MIT KAMERA")
    print("=" * 50)

    # ----------------------------------------------------------------
    # Schritt 1: Bild laden und Sudoku-Quadrat finden
    # ----------------------------------------------------------------
    print("\n[1/4] Bild wird geladen und Sudoku-Quadrat wird gesucht...")
    try:
        original, warped, warped_bin = process_image(image_path)
        print("      ✓ Sudoku-Quadrat gefunden und transformiert!")
    except (FileNotFoundError, ValueError) as e:
        print(f"      ✗ Fehler: {e}")
        return

    if show_steps:
        cv2.imshow("Original", original)
        cv2.imshow("Transformiert (BGR)", warped)
        cv2.imshow("Transformiert (Binär)", warped_bin)
        cv2.waitKey(0)

    # ----------------------------------------------------------------
    # Schritt 2: Gitter extrahieren und Zellen erkennen (OCR)
    # ----------------------------------------------------------------
    print("\n[2/4] Gitter wird extrahiert und Ziffern werden erkannt (OCR)...")
    try:
        grid = extract_grid(warped_bin)
        print("      ✓ Erkennung abgeschlossen!")
    except RuntimeError as e:
        print(f"      ✗ Fehler: {e}")
        return

    print("\n   Erkanntes Sudoku:")
    print_grid(grid)

    # ----------------------------------------------------------------
    # Schritt 3: Sudoku lösen
    # ----------------------------------------------------------------
    print("\n[3/4] Sudoku wird gelöst...")
    success, solved = solve_sudoku(grid)

    if not success:
        print("      ✗ Das Sudoku konnte nicht gelöst werden!")
        print("        Mögliche Ursachen:")
        print("        - Die OCR-Erkennung war fehlerhaft")
        print("        - Das Sudoku ist ungültig (mehrere Fehler)")
        print("        - Das Sudoku hat keine Lösung")
        return

    print("      ✓ Sudoku erfolgreich gelöst!")
    print("\n   Gelöstes Sudoku:")
    print_grid(solved)  # type: ignore

    # ----------------------------------------------------------------
    # Schritt 4: Ergebnis visualisieren
    # ----------------------------------------------------------------
    print("\n[4/4] Ergebnis wird visualisiert...")

    # Textausgabe
    print("\n   ┌─────────────────────────────────────────────────┐")
    print("   │                 E R G E B N I S                  │")
    print("   ├─────────────────────────────────────────────────┤")
    print("   │  Das Sudoku wurde erfolgreich gelöst!           │")
    print("   │  Die roten Zahlen im Bild zeigen die Lösung.    │")
    print("   └─────────────────────────────────────────────────┘")

    # Visuelle Darstellung (Bonus)
    result_img = draw_solution(warped, grid, solved)  # type: ignore
    cv2.imshow("Gelöstes Sudoku (rot = Lösung)", result_img)
    print("\n   Drücke eine beliebige Taste, um alle Fenster zu schließen...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("\n✓ Pipeline erfolgreich abgeschlossen!")


def main() -> None:
    """
    Hauptfunktion: Parst Kommandozeilenargumente und startet die Pipeline.
    """
    if len(sys.argv) < 2:
        print("Verwendung: python main.py <bilddatei>")
        print("Beispiel:  python main.py test_sudoku.jpg")
        print("\nOder lege ein Testbild im Projektordner ab und führe aus:")
        print("  python main.py mein_sudoku.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"Fehler: Datei '{image_path}' nicht gefunden!")
        sys.exit(1)

    run_pipeline(image_path)


if __name__ == "__main__":
    main()