# Lab 06 - Asteroids / Świat Toroidalny

Projekt wykonany w Pythonie z użyciem biblioteki **pyray / raylib**.

## Opis
Program rozszerza projekt z Lab 05 do klasycznej mechaniki gry typu **Asteroids**.

Zaimplementowano świat toroidalny, w którym:
- prawa krawędź łączy się z lewą,
- górna krawędź łączy się z dolną.

Obiekty nie znikają nagle po przejściu przez krawędź ekranu. Dzięki ghost rendering są widoczne jednocześnie po obu stronach, co daje płynne przejście.

Na scenie znajdują się:
- sterowany statek,
- losowo generowane asteroidy o nieregularnych kształtach.

## Główne funkcjonalności
- świat toroidalny z zawijaniem pozycji przez modulo,
- ghost rendering przy krawędziach ekranu,
- statek z fizyką ruchu:
  - obrót,
  - thrust,
  - bezwładność,
  - tarcie,
  - ograniczenie maksymalnej prędkości,
- proceduralnie generowane asteroidy,
- losowy ruch i rotacja asteroid,
- wspólna logika pomocnicza w `utils.py`,
- konfiguracja parametrów w `config.py`.

## Struktura projektu
```text
lab06/
├── main.py
├── ship.py
├── asteroid.py
├── utils.py
└── config.py
