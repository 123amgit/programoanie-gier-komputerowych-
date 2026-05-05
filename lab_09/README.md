# Laboratorium 09 - Scena 3D i szyna

Przedmiot: **Tworzenie Gier Komputerowych**  
Technologia: **Godot Engine 4.x / GDScript**

Projekt jest pierwszym laboratorium z bloku 3D. Celem jest przygotowanie prostej sceny typu **on-rails**, czyli takiej, w której kamera i statek automatycznie przesuwają się po trasie, a gracz steruje tylko odchyleniem statku w płaszczyźnie XY.

## Co zostało zrobione

- Utworzono projekt Godot 4.x.
- Dodano scenę `main.tscn` z korzeniem `Node3D`.
- Dodano `Path3D` jako szynę lotu.
- Dodano `PathFollow3D`, który przesuwa się po ścieżce.
- Kamera i statek są dziećmi `PathFollow3D`, więc lecą razem z szyną.
- Statek jest tymczasowym modelem z `BoxMesh`.
- Dodano `Camera3D` ustawioną za statkiem.
- Dodano `DirectionalLight3D` oświetlający scenę.
- Dodano sterowanie statkiem w osi X/Y.
- Dodano ograniczenie obszaru ruchu przez `clamp()`.
- Prędkość szyny jest zmienną eksportowaną `@export var rail_speed`.

## Sterowanie

| Klawisz | Działanie |
|---|---|
| Strzałka lewo | Ruch statku w lewo |
| Strzałka prawo | Ruch statku w prawo |
| Strzałka góra | Ruch statku w górę |
| Strzałka dół | Ruch statku w dół |
| F5 | Uruchomienie sceny w Godot |

## Struktura projektu

```text
lab_09/
├── project.godot
├── main.tscn
├── icon.svg
├── README.md
├── .gitignore
└── scripts/
    ├── main_scene.gd
    ├── rail_follow.gd
    └── player_ship.gd
```

## Opis techniczny

### Path3D

`Path3D` przechowuje trasę lotu. W projekcie jest to krzywa z kilkoma punktami kontrolnymi. To ona pełni funkcję szyny.

### PathFollow3D

`PathFollow3D` jest dzieckiem `Path3D`. Ma właściwość `progress_ratio`, która określa pozycję na trasie od `0.0` do `1.0`.

W skrypcie `rail_follow.gd` zwiększamy `progress_ratio` w każdej klatce:

```gdscript
progress_ratio += rail_speed * delta
```

Dzięki temu kamera i statek poruszają się automatycznie po szynie.

### Statek

Statek jest dzieckiem `PathFollow3D`, dlatego jego pozycja jest lokalna względem punktu na szynie. Zmiana `position.x` i `position.y` przesuwa statek przed kamerą, ale nie odłącza go od automatycznego ruchu do przodu.

### clamp()

W skrypcie `player_ship.gd` użyto:

```gdscript
position.x = clamp(position.x, -limit_x, limit_x)
position.y = clamp(position.y, -limit_y, limit_y)
```

To ogranicza obszar manewrowania i spełnia wymaganie laboratorium.

## Uruchomienie

1. Otwórz Godot 4.x.
2. Wybierz **Import**.
3. Wskaż plik `project.godot` z folderu `lab_09`.
4. Otwórz projekt.
5. Uruchom scenę klawiszem `F5`.

## Co pokazać prowadzącemu

- Scena uruchamia się bez błędów.
- W drzewie sceny widać `Path3D` i `PathFollow3D`.
- Kamera i statek poruszają się po trasie.
- Strzałki przesuwają statek lokalnie w osi X/Y.
- Statek nie wylatuje poza obszar dzięki `clamp()`.
- `rail_speed` można zmieniać w inspektorze.
