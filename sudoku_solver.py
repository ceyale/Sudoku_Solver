"""
Modul 3: Sudoku-Löser (Backtracking-Algorithmus)
=================================================
Implementiert einen hocheffizienten Backtracking-Algorithmus,
der ein 9x9-Sudoku in Millisekunden löst.
"""

from typing import List, Tuple, Optional
import copy


def is_valid(grid: List[List[int]], row: int, col: int, num: int) -> bool:
    """
    Prüft, ob eine Zahl an einer bestimmten Position platziert werden kann,
    ohne die Sudoku-Regeln zu verletzen.

    Args:
        grid: 9x9-Sudoku-Array.
        row: Zeilenindex (0-8).
        col: Spaltenindex (0-8).
        num: Die zu prüfende Zahl (1-9).

    Returns:
        True, wenn die Platzierung gültig ist, sonst False.
    """
    # 1. Prüfe die Zeile
    for c in range(9):
        if grid[row][c] == num:
            return False

    # 2. Prüfe die Spalte
    for r in range(9):
        if grid[r][col] == num:
            return False

    # 3. Prüfe den 3x3-Block
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == num:
                return False

    return True


def find_empty(grid: List[List[int]]) -> Optional[Tuple[int, int]]:
    """
    Findet die nächste leere Zelle (Wert = 0) im Gitter.

    Args:
        grid: 9x9-Sudoku-Array.

    Returns:
        Tuple (row, col) der leeren Zelle oder None, wenn keine leer ist.
    """
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return None


def solve(grid: List[List[int]]) -> bool:
    """
    Löst das Sudoku mit Backtracking (in-place).

    Der Algorithmus:
    1. Finde eine leere Zelle.
    2. Versuche nacheinander die Zahlen 1-9.
    3. Wenn eine Zahl gültig ist, setze sie und rufe rekursiv solve() auf.
    4. Wenn die Rekursion erfolgreich ist, ist das Sudoku gelöst.
    5. Wenn nicht, setze die Zelle zurück (Backtrack) und versuche die nächste Zahl.

    Args:
        grid: 9x9-Sudoku-Array (wird direkt modifiziert).

    Returns:
        True, wenn das Sudoku gelöst wurde, sonst False.
    """
    # Leere Zelle finden
    empty = find_empty(grid)
    if empty is None:
        return True  # Keine leeren Zellen → gelöst!

    row, col = empty

    # Zahlen 1-9 durchprobieren
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num

            if solve(grid):
                return True

            # Backtrack: Zelle zurücksetzen
            grid[row][col] = 0

    return False  # Keine Zahl passt → Sackgasse


def validate_initial(grid: List[List[int]]) -> bool:
    """
    Validiert die Ausgangskonfiguration des Sudokus.
    Prüft, ob die gegebenen Zahlen legal sind (keine Regelverstöße).

    Args:
        grid: 9x9-Sudoku-Array mit 0 für leere Felder.

    Returns:
        True, wenn die Konfiguration legal ist, sonst False.
    """
    # Prüfe jede Zelle mit einer Zahl
    for row in range(9):
        for col in range(9):
            num = grid[row][col]
            if num != 0:
                # Temporär die Zelle auf 0 setzen und dann prüfen
                grid[row][col] = 0
                valid = is_valid(grid, row, col, num)
                grid[row][col] = num

                if not valid:
                    return False

    return True


def solve_sudoku(grid: List[List[int]]) -> Tuple[bool, Optional[List[List[int]]]]:
    """
    Löst ein Sudoku und gibt das Ergebnis zurück.

    Führt eine vollständige Validierung durch, bevor der
    Backtracking-Algorithmus gestartet wird.

    Args:
        grid: 9x9-Sudoku-Array mit 0 für leere Felder.

    Returns:
        Tuple aus (erfolgreich_gelöst, gelöstes_Gitter_oder_None).
    """
    # 1. Ausgangskonfiguration validieren
    if not validate_initial(grid):
        return False, None

    # 2. Tiefe Kopie erstellen (Original bleibt erhalten)
    grid_copy = copy.deepcopy(grid)

    # 3. Lösen
    solved = solve(grid_copy)

    if solved:
        return True, grid_copy
    else:
        return False, None


def count_solutions(grid: List[List[int]]) -> int:
    """
    Zählt die Anzahl der Lösungen für ein Sudoku (maximal 2).
    Nützlich, um zu prüfen, ob ein Sudoku eindeutig lösbar ist.

    Args:
        grid: 9x9-Sudoku-Array.

    Returns:
        Anzahl der Lösungen (abgeschnitten bei 2).
    """
    empty = find_empty(grid)
    if empty is None:
        return 1  # Eine Lösung gefunden

    row, col = empty
    count = 0

    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            count += count_solutions(grid)
            grid[row][col] = 0

            if count > 1:
                return count  # Frühzeitiger Abbruch bei Mehrdeutigkeit

    return count


def is_uniquely_solvable(grid: List[List[int]]) -> bool:
    """
    Prüft, ob ein Sudoku eindeutig lösbar ist (genau eine Lösung hat).

    Args:
        grid: 9x9-Sudoku-Array.

    Returns:
        True, wenn das Sudoku genau eine Lösung hat.
    """
    grid_copy = copy.deepcopy(grid)
    return count_solutions(grid_copy) == 1