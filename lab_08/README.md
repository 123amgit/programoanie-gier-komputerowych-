# Laboratorium 08 - Architektura, FSM, podział asteroid i koniec gry

Przedmiot: **Programowanie Gier Komputerowych**  
Technologia: **Python + Raylib/Pyray**

Projekt jest kontynuacją `lab_07`. W poprzednim laboratorium dodano pociski, dźwięki, kolizje i eksplozje. W tym laboratorium gra dostała strukturę pełniejszej mini-gry: menu, rozgrywkę, ekran końcowy, punktację, najlepszy wynik oraz trzypoziomowy podział asteroid.

## Najważniejsze funkcje

- Maszyna stanów FSM oparta o `enum.Enum`.
- Stany:
  - `MENU`,
  - `GAME`,
  - `GAME_OVER`.
- Trzy poziomy asteroid:
  - `level 3` - duża asteroida,
  - `level 2` - średnia asteroida,
  - `level 1` - mała asteroida.
- Metoda `split()` w klasie `Asteroid`.
- Podział asteroidy po trafieniu:
  - duża asteroida tworzy dwie średnie,
  - średnia asteroida tworzy dwie małe,
  - mała asteroida znika bez podziału.
- System punktacji:
  - małe asteroidy dają więcej punktów,
  - wynik jest wyświetlany w HUD,
  - najlepszy wynik jest zapisywany do `scores.txt`.
- Warunki końca gry:
  - zwycięstwo po zniszczeniu wszystkich asteroid,
  - porażka po kolizji statku z asteroidą.
- Refaktoryzacja:
  - konfiguracja w `config.py`,
  - funkcje pomocnicze w `utils.py`,
  - osobne pliki dla klas,
  - funkcje `update_*` i `draw_*` dla stanów gry.

## Sterowanie

| Klawisz | Działanie |
|---|---|
| `ENTER` | Start gry / powrót do menu po końcu gry |
| Strzałka lewo | Obrót statku w lewo |
| Strzałka prawo | Obrót statku w prawo |
| Strzałka góra | Przyspieszenie statku |
| `SPACE` | Strzał |

## Struktura projektu

```text
lab_08/
├── main.py
├── ship.py
├── asteroid.py
├── bullet.py
├── explosion.py
├── utils.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
└── assets/
    ├── shoot.wav
    ├── explode.wav
    └── stars.png
```

## Uruchomienie

Najpierw zainstaluj bibliotekę:

```bash
pip install -r requirements.txt
```

albo ręcznie:

```bash
pip install raylib
```

Uruchomienie programu:

```bash
python main.py
```

## Opis architektury

### FSM

Gra ma trzy stany. Dzięki temu kod menu, gry i ekranu końcowego nie miesza się w jednej ogromnej pętli.

W `main.py` znajdują się funkcje:

- `update_menu()`,
- `update_game()`,
- `update_game_over()`,
- `draw_menu()`,
- `draw_game()`,
- `draw_game_over()`.

To poprawia czytelność i pokazuje, że każdy stan ma własną logikę.

### Asteroidy

Klasa `Asteroid` ma parametr `level`. Nie przekazujemy już promienia z zewnątrz. Promień i prędkość wynikają z poziomu asteroidy. To spełnia wymaganie z laboratorium.

Najważniejsza metoda:

```python
split()
```

Zwraca listę nowych asteroid. Dzięki temu `main.py` nie musi samodzielnie decydować, co zrobić z asteroidą po trafieniu.

### Punktacja

Punktacja znajduje się w `config.py`:

```python
SCORE_BY_LEVEL = {
    1: 100,
    2: 50,
    3: 20,
}
```

Mniejsza asteroida jest trudniejsza do trafienia, więc daje więcej punktów.

### Zasoby

Dźwięki i tekstura są ładowane przed pętlą gry i zwalniane po jej zakończeniu. To jest ważne przy Raylib.

### Zapis najlepszego wyniku

Najlepszy wynik jest zapisywany w pliku `scores.txt`. Plik nie musi istnieć przy pierwszym uruchomieniu. Program używa `try/except`, więc tworzy go dopiero przy zapisie.
