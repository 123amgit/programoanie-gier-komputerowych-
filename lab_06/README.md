# Lab 06 - Asteroids / Świat Toroidalny

Projekt wykonany w Pythonie z użyciem biblioteki **pyray / raylib**.

## Opis
Program rozszerza projekt z Lab 05 do klasycznej mechaniki gry typu **Asteroids**.

Zaimplementowano świat toroidalny (bez ścian), w którym:
- prawa krawędź łączy się z lewą,
- górna krawędź łączy się z dolną.

Obiekty nie znikają przy przejściu przez krawędź — są jednocześnie widoczne po obu stronach (ghost rendering).

Na scenie znajdują się:
- sterowany statek,
- losowo generowane asteroidy o nieregularnych kształtach.

## Główne funkcjonalności
- świat toroidalny (wrap przez modulo)
- ghost rendering (wielokrotne rysowanie przy krawędziach)
- statek z fizyką:
  - rotacja
  - thrust
  - bezwładność
  - tarcie
  - limit prędkości
- proceduralne asteroidy:
  - losowy kształt wielokąta
  - losowa prędkość i rotacja
- wspólna logika w `utils.py`
- konfiguracja w `config.py`

## Struktura projektu
