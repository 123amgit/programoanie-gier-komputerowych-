# Library Ghost

## Opis gry

**Library Ghost** to autorska gra 2D wykonana w Pythonie z użyciem biblioteki Raylib.  
Gracz steruje małym duchem poruszającym się po bibliotece. Celem gry jest zbieranie zagubionych stron książek i odnoszenie ich do magicznej półki. Jednocześnie należy unikać strażników oraz światła ich latarek, ponieważ światło osłabia ducha.

Projekt został wykonany jako prosta gra typu stealth/collection. Gra nie jest klonem projektów wykonywanych na laboratoriach.

---

## Technologie

Projekt używa:

- Python 3
- Raylib-Python
- PyCharm jako środowisko pracy

---

## Instrukcja uruchomienia

1. Otwórz katalog `lab_15` w PyCharm.
2. Zainstaluj wymagane zależności:

   ```bash
   pip install -r requirements.txt
   ```

3. Uruchom plik:

   ```bash
   python main.py
   ```

---

## Sterowanie

### Aktualnie dostępne

- `ENTER` - start gry z menu albo restart po wygranej/przegranej
- `WASD` - ruch ducha
- `strzałki` - alternatywny ruch ducha
- `BACKSPACE` - powrót z gry, ekranu wygranej albo ekranu przegranej do menu
- `ESC` - zamknięcie okna gry

### Planowane w ostatnim etapie

- `SPACE` - tryb przezroczystości ducha

---

## Cel gry

Celem gry jest zebranie zagubionych stron książek i odniesienie ich do magicznej półki.

Zasady:

- duch może nieść tylko jedną stronę naraz,
- po zebraniu strony trzeba wrócić do magicznej półki,
- po dostarczeniu wymaganej liczby stron gracz wygrywa,
- należy unikać światła strażników,
- gdy duch zbyt długo pozostaje w świetle latarki, jego energia spada,
- gdy energia spadnie do zera, gra kończy się przegraną.

---

## Aktualny stan projektu

Aktualna wersja zawiera:

- strukturę katalogu `lab_15`,
- plik `README.md`,
- plik `requirements.txt`,
- konfigurację projektu w `config.py`,
- prostą pętlę gry Raylib,
- globalną maszynę stanów:
  - `MENU`,
  - `PLAYING`,
  - `GAME_OVER`,
  - `WIN`,
- ekran menu,
- przejście z menu do ekranu gry,
- ekran wygranej,
- ekran przegranej,
- klasę gracza `Player`,
- ruch ducha za pomocą `WASD` oraz strzałek,
- ograniczenie ruchu ducha do granic ekranu,
- prosty wygląd ducha narysowany z figur 2D,
- tło biblioteki,
- klasę `Obstacle`,
- półki biblioteczne jako prawdziwe obiekty gry,
- kolizje ducha z półkami,
- klasę `Page`,
- zagubione strony rozmieszczone na mapie,
- klasę `Shelf`,
- magiczną półkę do oddawania stron,
- zbieranie jednej strony naraz,
- licznik dostarczonych stron,
- warunek wygranej po dostarczeniu wymaganej liczby stron,
- klasę `Guard`,
- prosty patrol strażników,
- uproszczone światło latarki jako obszar wykrywania,
- spadek energii ducha po wejściu w światło,
- warunek przegranej po spadku energii do zera,
- podstawowy HUD z informacją o energii, stronach i aktualnym celu.

---

## Struktura projektu

```text
lab_15/
├── main.py
├── config.py
├── game_state.py
├── player.py
├── obstacle.py
├── page.py
├── shelf.py
├── guard.py
├── utils.py
├── audio_manager.py
├── particle.py
├── requirements.txt
├── README.md
└── assets/
    ├── README_assets.txt
    └── sounds/
```

---

## Opis najważniejszych plików

### `main.py`

Główny plik gry. Zawiera pętlę programu, przełączanie stanów gry, tworzenie obiektów oraz wywoływanie funkcji aktualizacji i rysowania.

### `config.py`

Plik z ustawieniami projektu, takimi jak rozmiar okna, prędkość gracza, liczba stron potrzebnych do wygranej, parametry strażników i światła.

### `game_state.py`

Plik z globalną maszyną stanów gry. Aktualnie używane stany to:

- `MENU`
- `PLAYING`
- `GAME_OVER`
- `WIN`

### `player.py`

Zawiera klasę gracza, czyli ducha. Odpowiada za ruch, reset pozycji, energię oraz rysowanie postaci.

### `obstacle.py`

Zawiera klasę przeszkód bibliotecznych. Przeszkody są prostokątami, z którymi duch może kolidować.

### `page.py`

Zawiera klasę zagubionej strony książki. Strony można zbierać i dostarczać do magicznej półki.

### `shelf.py`

Zawiera klasę magicznej półki, która służy jako miejsce oddawania zebranych stron.

### `guard.py`

Zawiera klasę strażnika. Strażnicy poruszają się po prostych trasach patrolowych i mają obszar światła latarki, który wykrywa ducha.

### `utils.py`

Zawiera funkcje pomocnicze, między innymi obliczanie odległości oraz kolizję koła z prostokątem.

---

## Własny mechanizm

Planowanym własnym mechanizmem gry jest **tryb przezroczystości ducha**.

W ostatnim etapie projektu duch będzie mógł aktywować przezroczystość za pomocą klawisza `SPACE`. W tym trybie gracz będzie mógł przechodzić przez wybrane przeszkody, ale energia ducha będzie spadać szybciej. Dzięki temu gracz będzie musiał podejmować decyzję, czy lepiej ominąć półki normalnie, czy zużyć energię i skrócić drogę przez przeszkodę.

Mechanika ta będzie pełnić funkcję dodatkowego elementu strategicznego.

---

## Znane ograniczenia

- Światło strażnika jest uproszczone jako okrągły obszar wykrywania.
- Strażnicy mają prosty patrol zamiast zaawansowanej sztucznej inteligencji.
- Tryb przezroczystości jest zaplanowany, ale nie został jeszcze zaimplementowany.
- Dźwięki nie zostały jeszcze dodane.
- Grafika jest prosta i oparta głównie na figurach 2D.
- Gra ma jeden poziom.

---

## Plan na ostatni etap

Przed końcowym oddaniem projektu planowane jest dodanie:

- trybu przezroczystości ducha pod klawiszem `SPACE`,
- szybszego zużycia energii podczas przezroczystości,
- możliwości przechodzenia przez wybrane przeszkody w tym trybie,
- końcowej aktualizacji README,
- ewentualnych prostych efektów dźwiękowych,
- zrzutów ekranu z gry.

---

## Autor

Projekt wykonany jako zaliczeniowa gra 2D w Pythonie z użyciem Raylib.
