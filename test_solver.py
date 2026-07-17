"""
Test-Skript für den Sudoku-Löser (Modul 3).
Testet den Backtracking-Algorithmus mit einem bekannten Sudoku.
Kann ohne Kamera/Bild ausgeführt werden.
"""

from sudoku_solver import solve_sudoku, is_uniquely_solvable
from grid_extraction import print_grid


def test_sudoku_solver() -> None:
    """
    Testet den Sudoku-Löser mit einem bekannten Beispiel.
    Verwendet das "weltberühmte" Sudoku aus der Wikipedia.
    """
    # Bekanntes Sudoku (schwierig)
    # Quelle: https://en.wikipedia.org/wiki/Sudoku
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    # Erwartete Lösung
    expected = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    print("=" * 50)
    print("  TEST: SUDOKU-LÖSER")
    print("=" * 50)

    print("\nEingabe-Sudoku:")
    print_grid(grid)

    # Test: Ist es eindeutig lösbar?
    unique = is_uniquely_solvable(grid)
    print(f"\nEindeutig lösbar: {'✓ Ja' if unique else '✗ Nein'}")

    # Test: Lösen
    success, solved = solve_sudoku(grid)

    if success and solved:
        print("\n✓ Sudoku erfolgreich gelöst!")
        print("\nGelöstes Sudoku:")
        print_grid(solved)

        # Mit erwarteter Lösung vergleichen
        if solved == expected:
            print("\n✓ Lösung stimmt mit der Erwartung überein!")
        else:
            print("\n✗ Lösung weicht von der Erwartung ab!")
    else:
        print("\n✗ Sudoku konnte nicht gelöst werden!")
        return

    # Test: Ungültiges Sudoku
    print("\n" + "-" * 50)
    print("Test: Ungültiges Sudoku erkennen...")
    invalid_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 5],  # 5 doppelt in der letzten Zeile
    ]
    success_inv, _ = solve_sudoku(invalid_grid)
    if not success_inv:
        print("✓ Ungültiges Sudoku wurde korrekt erkannt!")
    else:
        print("✗ Ungültiges Sudoku wurde fälschlicherweise als gültig erkannt!")

    print("\n" + "=" * 50)
    print("  TEST ABGESCHLOSSEN")
    print("=" * 50)


if __name__ == "__main__":
    test_sudoku_solver()