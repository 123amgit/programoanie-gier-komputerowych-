# Library Ghost

## Opis gry

**Library Ghost** to autorska gra 2D wykonana w Pythonie z użyciem Raylib.
Gracz steruje małym duchem w bibliotece, zbiera zagubione strony książek
i odnosi je do magicznej półki. Należy unikać strażników oraz światła ich latarek,
ponieważ światło osłabia ducha.

## Wybrany silnik

Projekt używa:

- Python 3
- Raylib-Python

## Instrukcja uruchomienia

1. Otwórz katalog `lab_15` w PyCharm.
2. Zainstaluj zależności:

   ```bash
   pip install -r requirements.txt
   ```

3. Uruchom plik:

   ```bash
   python main.py
   ```

## Sterowanie

- `ENTER` - start gry z menu
- `ESC` - wyjście z gry

W kolejnych etapach zostanie dodane:
- ruch ducha,
- kolizje z przeszkodami,
- zbieranie stron,
- strażnicy,
- tryb przezroczystości.

## Własny mechanizm

Planowanym własnym mechanizmem jest **tryb przezroczystości ducha**.
Duch będzie mógł na krótko przechodzić przez wybrane przeszkody, ale zużyje wtedy
więcej energii. Gracz będzie musiał zdecydować, kiedy opłaca się skrócić drogę,
a kiedy lepiej zachować energię.

## Czy projekt jest klonem?

Nie. Projekt nie jest klonem gry z zajęć. Nie jest to Space Invaders,
Asteroids ani on-rails shooter. Jest to autorska gra 2D typu stealth/collection.

## Aktualny stan projektu

Wersja początkowa zawiera:
- strukturę katalogu `lab_15`,
- podstawowy plik `README.md`,
- konfigurację projektu,
- prostą pętlę Raylib,
- maszynę stanów `MENU`, `PLAYING`, `GAME_OVER`, `WIN`,
- ekran menu jako pierwszy działający fragment projektu.

## Znane ograniczenia

- Na tym etapie gra ma tylko ekran menu.
- Mechanika gracza, kolizje, przeciwnicy i dźwięki zostaną dodane w kolejnych commitach.
