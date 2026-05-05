# Laboratorium 07 - Pociski, zasoby i kolizje

Przedmiot: **Tworzenie Gier Komputerowych**  
Technologia: **Raylib-Python / pyray**

Projekt jest rozwinięciem poprzedniego laboratorium z asteroidami. Dodano strzelanie, dynamiczną listę pocisków, dźwięki, teksturę tła, kolizje kołowe oraz animację eksplozji.

## Funkcje

- Sterowanie statkiem za pomocą strzałek.
- Strzelanie klawiszem `SPACE`.
- Pociski mają czas życia `TTL` i po nim znikają.
- Limit pocisków na ekranie: 5.
- Dźwięk strzału `shoot.wav`.
- Dźwięk eksplozji `explode.wav`.
- Tło gwiazd jako tekstura `stars.png`.
- Kolizja pocisk-asteroida przez odległość między środkami okręgów.
- Animacja eksplozji po trafieniu asteroidy.
- Zadanie dodatkowe: kolizja statek-asteroida resetuje statek na środek planszy.
- Zasoby są zwalniane po zamknięciu programu.

## Sterowanie

| Klawisz | Działanie |
|---|---|
| Strzałka lewo | Obrót statku w lewo |
| Strzałka prawo | Obrót statku w prawo |
| Strzałka góra | Przyspieszenie statku |
| Spacja | Strzał |

## Struktura projektu

```text
lab07/
├── main.py
├── ship.py
├── asteroid.py
├── bullet.py
├── explosion.py
├── utils.py
├── config.py
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
pip install raylib
```

Jeżeli ta wersja nie działa w danym środowisku, można spróbować:

```bash
pip install raylib-python-cffi
```

Uruchomienie:

```bash
python main.py
```

## Opis techniczny

### Pociski

Klasa `Bullet` znajduje się w pliku `bullet.py`. Pocisk ma pozycję, prędkość, promień kolizyjny, czas życia `ttl` oraz flagę `alive`. W każdej klatce pocisk zmienia pozycję, zawija się na krawędziach ekranu i zmniejsza swój czas życia.

### Dynamiczne listy obiektów

Pociski, asteroidy i eksplozje są czyszczone przez list comprehension, np.:

```python
bullets = [b for b in bullets if b.alive]
```

Dzięki temu nie usuwamy elementów z listy bezpośrednio podczas iteracji.

### Kolizje

W pliku `utils.py` znajduje się funkcja `circle_collision`, która korzysta z `math.hypot`. Kolizja zachodzi, gdy odległość między środkami dwóch okręgów jest mniejsza lub równa sumie ich promieni.

### Zasoby

Program ładuje dźwięki i teksturę przed pętlą gry, a po zakończeniu zwalnia je funkcjami `unload_sound`, `unload_texture` oraz zamyka urządzenie audio przez `close_audio_device`.
