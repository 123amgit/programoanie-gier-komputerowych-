# Lab 05 - Statek: geometria, ruch i fizyka

Projekt wykonany w Pythonie z użyciem biblioteki **pyray / raylib**.

## Opis
Program przedstawia statek kosmiczny poruszający się w oknie 800x600.  
Statek:
- obraca się w lewo i w prawo,
- przyspiesza w kierunku nosa,
- zachowuje bezwładność po puszczeniu klawisza,
- zwalnia przez tarcie,
- ma ograniczenie maksymalnej prędkości,
- odbija się od krawędzi ekranu,
- pokazuje płomień silnika podczas thrustu,
- posiada tryb debug wyświetlający wektor prędkości i parametry ruchu.

## Struktura projektu
- `main.py` - pętla gry, okno, HUD, obsługa uruchomienia
- `ship.py` - klasa `Ship`, fizyka, sterowanie, rysowanie statku

## Wymagania
Python 3.x

Biblioteka:
```bash
pip install raylib
