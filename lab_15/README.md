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

Uruchom plik:

python main.py
Sterowanie
Aktualnie dostępne
ENTER - start gry z menu
WASD - ruch ducha
strzałki - alternatywny ruch ducha
BACKSPACE - powrót z ekranu gry do menu
ESC - zamknięcie okna gry
Planowane w kolejnych etapach
SPACE - tryb przezroczystości ducha
możliwe dodatkowe klawisze do restartu po przegranej lub wygranej
Aktualny stan projektu

Aktualna wersja zawiera:

strukturę katalogu lab_15,
plik README.md,
plik requirements.txt,
konfigurację projektu w config.py,
prostą pętlę gry Raylib,
globalną maszynę stanów:
MENU,
PLAYING,
GAME_OVER,
WIN,
ekran menu,
przejście z menu do ekranu gry,
klasę gracza Player,
ruch ducha za pomocą WASD oraz strzałek,
ograniczenie ruchu ducha do granic ekranu,
prosty wygląd ducha narysowany z figur 2D,
prosty zarys biblioteki jako tło,
podstawowy HUD z informacją o energii i sterowaniu.
Planowane mechaniki

W kolejnych commitach zostaną dodane:

realne przeszkody biblioteczne,
kolizje z półkami i ścianami,
zbieranie zagubionych stron,
odnoszenie stron do magicznej półki,
strażnicy poruszający się po bibliotece,
wykrywanie ducha przez światło latarki,
utrata energii po wejściu w światło,
ekran wygranej i przegranej,
efekty dźwiękowe.
Własny mechanizm

Planowanym własnym mechanizmem jest tryb przezroczystości ducha.
Duch będzie mógł na krótko przechodzić przez wybrane przeszkody, ale zużyje wtedy
więcej energii. Gracz będzie musiał zdecydować, kiedy opłaca się skrócić drogę,
a kiedy lepiej zachować energię.

Czy projekt jest klonem?

Nie. Projekt nie jest klonem gry z zajęć. Nie jest to Space Invaders,
Asteroids ani on-rails shooter. Jest to autorska gra 2D typu stealth/collection.

Znane ograniczenia
Półki biblioteczne są obecnie tylko elementami tła.
Nie dodano jeszcze realnych kolizji z przeszkodami.
Nie dodano jeszcze stron do zbierania.
Nie dodano jeszcze strażników, latarek ani dźwięków.
Tryb przezroczystości jest zaplanowany, ale nie został jeszcze zaimplementowany.
