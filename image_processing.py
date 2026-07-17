"""
Modul 1: Bildverarbeitung (OpenCV)
====================================
Liest ein Testbild ein, führt Preprocessing durch,
findet das Sudoku-Quadrat und wendet eine Perspektiventransformation an.
"""

import cv2
import numpy as np
from typing import Tuple, Optional


def load_image(path: str) -> np.ndarray:
    """
    Lädt ein Bild von der angegebenen Datei.

    Args:
        path: Dateipfad zum Bild.

    Returns:
        Das geladene Bild als numpy-Array (BGR-Format).

    Raises:
        FileNotFoundError: Wenn die Datei nicht existiert oder nicht geladen werden kann.
    """
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Bild konnte nicht geladen werden: {path}")
    return img


def preprocess_image(img: np.ndarray) -> np.ndarray:
    """
    Wendet Preprocessing auf das Bild an:
    1. Graustufen-Konvertierung
    2. Gaußscher Weichzeichner (Rauschreduzierung)
    3. Adaptive Schwellenwertbildung (binäres Bild)

    Args:
        img: Eingabebild (BGR).

    Returns:
        Vorverarbeitetes Binärbild.
    """
    # 1. Graustufen
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Gaußscher Weichzeichner (5x5 Kernel)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Adaptive Schwellenwertbildung
    #    Blockgröße 11, C = 2 (Subtraktionskonstante)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    return thresh


def find_sudoku_contour(thresh: np.ndarray) -> Optional[np.ndarray]:
    """
    Findet die größte viereckige Kontur im Bild (das Sudoku-Quadrat).

    Args:
        thresh: Binäres Bild.

    Returns:
        Die 4 Eckpunkte des Sudoku-Quadrats (als numpy-Array),
        oder None, falls keine geeignete Kontur gefunden wurde.
    """
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    # Sortiere Konturen absteigend nach Fläche
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        # Annäherung der Kontur an ein Polygon
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # Wir suchen ein Viereck (4 Eckpunkte)
        if len(approx) == 4:
            return approx.reshape(4, 2).astype(np.float32)

    return None


def order_points(pts: np.ndarray) -> np.ndarray:
    """
    Ordnet 4 Punkte in der Reihenfolge:
    [oben-links, oben-rechts, unten-rechts, unten-links].

    Args:
        pts: 4x2-Array mit (x, y)-Koordinaten.

    Returns:
        Geordnetes 4x2-Array.
    """
    rect = np.zeros((4, 2), dtype=np.float32)

    # Summe der Koordinaten: kleinste Summe = oben-links, größte Summe = unten-rechts
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # oben-links
    rect[2] = pts[np.argmax(s)]  # unten-rechts

    # Differenz der Koordinaten: kleinste Differenz = oben-rechts, größte = unten-links
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # oben-rechts
    rect[3] = pts[np.argmax(diff)]  # unten-links

    return rect


def warp_perspective(img: np.ndarray, corners: np.ndarray,
                     size: int = 450) -> np.ndarray:
    """
    Wendet eine Perspektiventransformation an, um das Sudoku-Quadrat
    als quadratisches Bild von oben darzustellen.

    Args:
        img: Originalbild (BGR).
        corners: Die 4 Eckpunkte des Sudoku-Quadrats.
        size: Seitenlänge des Ausgabequadrats (in Pixeln).

    Returns:
        Transformiertes, flaches Sudoku-Bild.
    """
    rect = order_points(corners)

    # Zielpunkte: ein Quadrat der Größe 'size x size'
    dst = np.array([
        [0, 0],
        [size - 1, 0],
        [size - 1, size - 1],
        [0, size - 1]
    ], dtype=np.float32)

    # Berechne die Perspektivtransformations-Matrix
    matrix = cv2.getPerspectiveTransform(rect, dst)

    # Wende die Transformation an
    warped = cv2.warpPerspective(img, matrix, (size, size))

    return warped


def process_image(path: str, output_size: int = 450) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Führt die gesamte Bildverarbeitungs-Pipeline aus:
    Lädt das Bild, findet das Sudoku und transformiert es.

    Args:
        path: Dateipfad zum Bild.
        output_size: Seitenlänge des transformierten Sudoku-Bilds.

    Returns:
        Tuple aus (Originalbild, transformiertes Sudoku-Bild, Binärbild des Sudokus).
    """
    # 1. Bild laden
    original = load_image(path)

    # 2. Preprocessing
    thresh = preprocess_image(original)

    # 3. Sudoku-Kontur finden
    corners = find_sudoku_contour(thresh)
    if corners is None:
        raise ValueError("Kein Sudoku-Quadrat im Bild gefunden!")

    # 4. Perspektiventransformation
    warped = warp_perspective(original, corners, output_size)

    # 5. Auch das Binärbild transformieren (für OCR)
    warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    _, warped_bin = cv2.threshold(warped_gray, 128, 255, cv2.THRESH_BINARY_INV)

    return original, warped, warped_bin