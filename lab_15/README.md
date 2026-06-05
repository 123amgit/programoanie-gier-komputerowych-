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

- `ENTER` - start gry z menu albo restart po wygranej/przegranej
- `WASD` - ruch ducha
- `strzałki` - alternatywny ruch ducha
- `SPACE` - tryb przezroczystości ducha
- `BACKSPACE` - powrót z gry, ekranu wygranej albo ekranu przegranej do menu
- `ESC` - zamknięcie okna gry

---

## Cel gry

Celem gry jest zebranie zagubionych stron książek i odniesienie ich do magicznej półki.

Zasady:

- duch może nieść tylko jedną stronę naraz,
- po zebraniu strony trzeba wrócić do magicznej półki,
- po dostarczeniu wymaganej liczby stron gracz wygrywa,
- należy unikać światła strażników,
- gdy duch zbyt długo pozostaje w świetle latarki, jego energia spada,
- gdy energia spadnie do zera, gra kończy się przegraną,
- tryb przezroczystości pozwala przechodzić przez półki, ale zużywa energię.

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
- tryb przezroczystości ducha pod klawiszem `SPACE`,
- możliwość przechodzenia przez półki podczas przezroczystości,
- dodatkowe zużycie energii podczas przezroczystości,
- klasę `Particle`,
- proste efekty cząsteczkowe przy zbieraniu i oddawaniu stron,
- klasę `AudioManager`,
- obsługę opcjonalnych efektów dźwiękowych,
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

Plik z ustawieniami projektu, takimi jak rozmiar okna, prędkość gracza, liczba stron potrzebnych do wygranej, parametry strażników, światła oraz trybu przezroczystości.

### `game_state.py`

Plik z globalną maszyną stanów gry. Używane stany to:

- `MENU`
- `PLAYING`
- `GAME_OVER`
- `WIN`

### `player.py`

Zawiera klasę gracza, czyli ducha. Odpowiada za ruch, reset pozycji, energię, tryb przezroczystości oraz rysowanie postaci.

### `obstacle.py`

Zawiera klasę przeszkód bibliotecznych. Przeszkody są prostokątami, z którymi duch może kolidować. W trybie przezroczystości duch może przez nie przechodzić.

### `page.py`

Zawiera klasę zagubionej strony książki. Strony można zbierać i dostarczać do magicznej półki.

### `shelf.py`

Zawiera klasę magicznej półki, która służy jako miejsce oddawania zebranych stron.

### `guard.py`

Zawiera klasę strażnika. Strażnicy poruszają się po prostych trasach patrolowych i mają obszar światła latarki, który wykrywa ducha.

### `particle.py`

Zawiera klasę prostych cząsteczek wizualnych. Cząsteczki pojawiają się przy zbieraniu i oddawaniu stron, dzięki czemu gracz otrzymuje czytelniejszą informację zwrotną.

### `audio_manager.py`

Zawiera prosty manager dźwięków. Klasa `AudioManager` próbuje załadować pliki `.wav` z katalogu `assets/sounds`, ale gra działa również wtedy, gdy pliki dźwiękowe nie zostały dodane.

### `utils.py`

Zawiera funkcje pomocnicze, między innymi obliczanie odległości, ograniczanie wartości oraz kolizję koła z prostokątem.

---

## Własny mechanizm

Własnym mechanizmem gry jest **tryb przezroczystości ducha**.

Gracz może aktywować przezroczystość za pomocą klawisza `SPACE`. W tym trybie duch może przechodzić przez półki biblioteczne, co pozwala skrócić drogę do strony albo magicznej półki. Mechanika nie jest jednak darmowa, ponieważ podczas przezroczystości energia ducha spada.

Dodatkowo przezroczysty duch otrzymuje trochę mniejsze obrażenia od światła strażników, ale nadal traci energię. Gracz musi więc decydować, czy warto użyć przezroczystości, czy lepiej ominąć przeszkody normalną drogą.

Mechanika ta dodaje element planowania trasy i zarządzania energią.

---

## Efekty wizualne i dźwiękowe

Projekt zawiera proste efekty cząsteczkowe przy zbieraniu oraz oddawaniu stron. Dzięki temu akcje gracza są bardziej widoczne.

Projekt posiada także klasę `AudioManager`, która obsługuje opcjonalne efekty dźwiękowe. Jeżeli w katalogu `assets/sounds` znajdują się pliki:

```text
pickup.wav
deliver.wav
hit.wav
win.wav
```

to gra może je odtworzyć w odpowiednich momentach. Jeżeli plików nie ma, gra nadal uruchamia się normalnie i działa bez dźwięków.

---

## Czy projekt jest klonem?

Nie. Projekt nie jest klonem gry wykonywanej na zajęciach.

Projekt nie jest:

- Space Invaders
- Asteroids
- on-rails shooterem

Jest to autorska gra 2D typu stealth/collection, w której głównym celem jest zbieranie stron, odnoszenie ich do półki, unikanie światła strażników i używanie trybu przezroczystości.

---

## Znane ograniczenia

- Światło strażnika jest uproszczone jako okrągły obszar wykrywania.
- Strażnicy mają prosty patrol zamiast zaawansowanej sztucznej inteligencji.
- Dźwięki są obsługiwane przez `AudioManager`, ale projekt działa również bez zewnętrznych plików `.wav`.
- Grafika jest prosta i oparta głównie na figurach 2D.
- Gra ma jeden poziom.

---

## Autor

Projekt wykonany jako zaliczeniowa gra 2D w Pythonie z użyciem Raylib.
