# Laboratorium 11 - Wrogowie i fale

Przedmiot: **Tworzenie Gier Komputerowych**  
Technologia: **Godot Engine 4.x / GDScript**

Projekt jest rozwinięciem `lab_10`. W poprzednim laboratorium działał lot po szynie, sterowanie statkiem w XY, strzelanie gracza i trafianie statycznych celów. W tym laboratorium cele zostały zastąpione przez **wrogów**, którzy mają punkty życia, poruszają się przez `Tween`, pojawiają się falami i strzelają w stronę gracza.

---

## Najważniejsze funkcje

- Scena główna `main.tscn` z ruchem po szynie `Path3D` + `PathFollow3D`.
- Statek gracza jako dziecko `RailFollow`, więc leci automatycznie razem z kamerą.
- Sterowanie statkiem w lokalnej płaszczyźnie XY za pomocą strzałek.
- Ograniczenie ruchu statku funkcją `clamp()`.
- Pocisk uniwersalny `bullet.tscn`, używany przez gracza i wrogów.
- Wrogowie jako osobna scena `enemy.tscn`.
- Wrogowie mają `hp`, `score_value`, `shoot_interval`, `sway_amplitude`, `sway_period`.
- Wróg emituje sygnał `died(points)` po zniszczeniu.
- Ruch boczny wroga jest wykonany przez `Tween`, a nie ręczne liczenie w każdej klatce.
- `WaveSpawner` tworzy fale na podstawie tablicy słowników, bez `if/elif` dla numerów fal.
- Wróg znajduje gracza przez grupę `player`, nie przez twardą ścieżkę węzłów.
- Pocisk wroga leci w kierunku gracza.
- Wynik jest wypisywany w konsoli Godot.

---

## Sterowanie

| Klawisz | Działanie |
|---|---|
| Strzałka w lewo | Ruch statku w lewo |
| Strzałka w prawo | Ruch statku w prawo |
| Strzałka w górę | Ruch statku w górę |
| Strzałka w dół | Ruch statku w dół |
| Spacja | Strzał |

---

## Struktura projektu

```text
lab_11/
├── project.godot
├── main.tscn
├── icon.svg
├── README.md
├── .gitignore
├── scripts/
│   ├── main_scene.gd
│   ├── rail_follow.gd
│   ├── player_ship.gd
│   ├── bullet.gd
│   ├── enemy.gd
│   └── wave_spawner.gd
└── scenes/
    ├── bullet.tscn
    └── enemy.tscn
```

---

## Uruchomienie

1. Otwórz **Godot 4.x**.
2. Kliknij **Import**.
3. Wybierz plik:

```text
lab_11/project.godot
```

4. Otwórz scenę:

```text
main.tscn
```

5. Uruchom przez **F5**.

Jeżeli Godot zapyta o scenę startową, wybierz:

```text
res://main.tscn
```

---

## Opis techniczny

### 1. Wrogowie zamiast statycznych celów

W Lab 10 cel był prostym obiektem do zestrzelenia. W Lab 11 cel został zastąpiony przez wroga. Wróg ma własną scenę:

```text
Enemy (Node3D)
├── MeshInstance3D
├── Core
└── Area3D
    └── CollisionShape3D
```

Korzeniem jest `Node3D`, ponieważ wróg jest pełnym obiektem logicznym. `Area3D` jest tylko hitboxem, który wykrywa wejście pocisku gracza.

---

### 2. Parametry wroga

W `enemy.gd` znajdują się eksportowane parametry:

```gdscript
@export var hp: int = 2
@export var speed: float = 3.0
@export var score_value: int = 100
@export var sway_amplitude: float = 1.4
@export var sway_period: float = 2.0
@export var shoot_interval: float = 2.5
```

Dzięki `@export` można zmieniać wartości z poziomu Inspektora albo przez spawner fali.

---

### 3. Sygnał `died(points)`

Wróg emituje sygnał:

```gdscript
signal died(points: int)
```

Po zniszczeniu wroga wywoływane jest:

```gdscript
died.emit(score_value)
queue_free()
```

Główna scena rejestruje wroga przez `register_enemy(enemy)` i podłącza ten sygnał do `_on_enemy_died(points)`. Dzięki temu wróg nie musi znać dokładnej ścieżki do sceny głównej.

---

### 4. Ruch przez Tween

Wróg porusza się bocznie przez `Tween`:

```gdscript
var tween := create_tween()
tween.set_loops()
tween.set_trans(Tween.TRANS_SINE)
tween.set_ease(Tween.EASE_IN_OUT)
tween.tween_property(self, "position:x", base_x + sway_amplitude, half_period)
```

To spełnia wymaganie laboratorium: ruch wroga nie jest liczony ręcznie przez `position.x += ...` w `_process()`, tylko jest animowany przez system `Tween`.

---

### 5. Spawner fal jako dane

`WaveSpawner` używa tablicy słowników:

```gdscript
var waves: Array[Dictionary] = [
    {
        "name": "Fala 1",
        "delay": 1.0,
        "x_positions": [-3.0, 0.0, 3.0],
        "z_offset": -28.0,
        "hp": 2,
        "score_value": 100
    }
]
```

Kod spawnera nie ma osobnych instrukcji `if wave == 1`, `elif wave == 2`. Każda fala jest tylko kolejnym wpisem w tablicy. To jest prosty wariant podejścia **data-driven**.

---

### 6. Dlaczego wrogowie nie są dziećmi `RailFollow`?

Statek i kamera są dziećmi `RailFollow`, bo mają automatycznie lecieć po szynie. Wrogowie są dodawani do głównej sceny `Main`, a nie do `RailFollow`.

Gdyby wróg był dzieckiem `RailFollow`, poruszałby się razem z kamerą i statkiem. Wtedy wyglądałoby, jakby gracz nigdy się do niego nie zbliżał. Dlatego spawner ustawia pozycję globalną:

```gdscript
rail_follow.global_position + Vector3(x, y, z_offset)
```

---

### 7. Pocisk uniwersalny

`bullet.gd` obsługuje pociski gracza i wroga. O rodzaju decyduje zmienna:

```gdscript
@export var bullet_kind: String = "player"
```

Dla pocisku gracza:

```gdscript
collision_layer = 4   # layer 3
collision_mask = 2    # widzi wrogów
```

Dla pocisku wroga:

```gdscript
collision_layer = 8   # layer 4
collision_mask = 1    # widzi gracza
```

W Godot warstwy są bitami:

| Numer warstwy | Wartość bitowa |
|---:|---:|
| 1 | 1 |
| 2 | 2 |
| 3 | 4 |
| 4 | 8 |

---

### 8. Wróg strzela do gracza przez grupę

Statek dodaje się do grupy:

```gdscript
add_to_group("player")
```

Wróg znajduje gracza tak:

```gdscript
var players := get_tree().get_nodes_in_group("player")
```

To jest luźniejsze powiązanie niż ścieżka typu:

```gdscript
get_node("/root/Main/RailPath/RailFollow/Ship")
```

Jeżeli zmieni się hierarchia sceny, grupy dalej działają.

---

## Warstwy kolizji

| Obiekt | Layer | Mask |
|---|---:|---:|
| Gracz | 1 | 2, 4 |
| Wróg | 2 | 1, 3 |
| Pocisk gracza | 3 | 2 |
| Pocisk wroga | 4 | 1 |

W kodzie odpowiada to wartościom bitowym:

```gdscript
player_hitbox.collision_layer = 1
player_hitbox.collision_mask = 10 # 2 + 8

hitbox.collision_layer = 2
hitbox.collision_mask = 5 # 1 + 4

player_bullet.collision_layer = 4
player_bullet.collision_mask = 2

enemy_bullet.collision_layer = 8
enemy_bullet.collision_mask = 1
```

---

## Wymagania z laboratorium

Projekt spełnia główne wymagania:

- wrogowie spawnują się falami,
- fale są zapisane jako tablica słowników,
- wrogowie mają punkty życia,
- wrogowie giną po trafieniach,
- wróg emituje `died(points)`,
- wynik jest aktualizowany przez sygnał,
- ruch wroga jest wykonany przez `Tween`,
- wróg strzela w kierunku gracza,
- pocisk jest uniwersalny dla gracza i wroga,
- gracz jest znajdowany przez grupę `player`,
- projekt nie wymaga wysyłania folderu `.godot/`.
