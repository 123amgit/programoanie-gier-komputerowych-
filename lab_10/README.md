# Laboratorium 10 - Strzelanie i kolizje 3D

Przedmiot: **Tworzenie Gier Komputerowych**  
Technologia: **Godot Engine 4.x / GDScript**

Projekt jest rozwinięciem `lab_09`. W poprzednim laboratorium powstała scena 3D z ruchem po szynie (`Path3D` + `PathFollow3D`) oraz sterowaniem statkiem w lokalnej płaszczyźnie XY. W tym laboratorium dodano strzelanie, pociski jako osobne sceny, cele, kolizje `Area3D`, warstwy kolizji, cooldown strzału i prosty wynik wypisywany w konsoli.

---

## Co zawiera projekt?

- Scena główna `main.tscn`.
- Szyna lotu `Path3D` oraz `PathFollow3D`.
- Statek gracza jako `Node3D` z modelem zastępczym.
- Sterowanie statkiem w lokalnym XY za pomocą strzałek.
- Ograniczenie ruchu statku przez `clamp()`.
- Scena pocisku `bullet.tscn`.
- Skrypt pocisku `bullet.gd` z prędkością, czasem życia i `queue_free()`.
- Scena celu `target.tscn`.
- Skrypt celu `target.gd` z obsługą sygnału `area_entered`.
- Kilka celów ustawionych przed kamerą.
- Cooldown strzału.
- Limit aktywnych pocisków.
- Wynik wypisywany przez `print()` w konsoli Godot.

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
lab_10/
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
│   └── target.gd
└── scenes/
    ├── bullet.tscn
    └── target.tscn
```

---

## Uruchomienie

1. Otwórz **Godot 4.x**.
2. Kliknij **Import**.
3. Wybierz plik:

```text
lab_10/project.godot
```

4. Otwórz scenę:

```text
main.tscn
```

5. Naciśnij **F5**.

Jeżeli Godot zapyta o scenę startową, wybierz:

```text
res://main.tscn
```

---

## Opis techniczny

### 1. Pocisk jako osobna scena

Pocisk znajduje się w pliku `scenes/bullet.tscn`. Jego korzeniem jest `Area3D`, ponieważ pocisk ma wykrywać wejście w obszar celu, ale nie musi działać jak fizyczna bryła blokująca ruch.

Struktura sceny:

```text
Bullet (Area3D)
├── MeshInstance3D
└── CollisionShape3D
```

Skrypt `bullet.gd` ma eksportowane zmienne:

```gdscript
@export var speed: float = 30.0
@export var lifetime: float = 3.0
```

Pocisk porusza się w przestrzeni globalnej i po upływie czasu życia wywołuje `queue_free()`.

---

### 2. Tworzenie pocisku przez statek

Statek ma w skrypcie `player_ship.gd` eksportowaną scenę pocisku:

```gdscript
@export var bullet_scene: PackedScene = preload("res://scenes/bullet.tscn")
```

Przy strzale wykonywane jest:

```gdscript
var bullet := bullet_scene.instantiate() as Area3D
get_tree().current_scene.add_child(bullet)
bullet.setup(muzzle.global_transform)
```

Pocisk jest dodawany do aktualnej sceny, a nie jako dziecko statku. Dzięki temu po wystrzeleniu porusza się niezależnie w przestrzeni globalnej.

---

### 3. Cel i sygnał `area_entered`

Cel znajduje się w pliku `scenes/target.tscn`.

Struktura sceny:

```text
Target (Node3D)
├── MeshInstance3D
└── Area3D
    └── CollisionShape3D
```

W `target.gd` sygnał jest podłączany w kodzie:

```gdscript
hitbox.area_entered.connect(_on_area_entered)
```

Po trafieniu celu:

- sprawdzane jest, czy w hitbox wszedł pocisk gracza,
- cel emituje sygnał `target_destroyed(points)`,
- pocisk zostaje usunięty,
- cel zmienia kolor na czerwony na 0.1 sekundy,
- cel wywołuje `queue_free()`.

---

### 4. Warstwy kolizji

W projekcie użyto prostego podziału:

| Obiekt | Layer | Mask | Znaczenie |
|---|---:|---:|---|
| Gracz | 1 | 2 | Gracz widzi cele/wrogów |
| Cel | 2 | 3 | Cel widzi pociski gracza |
| Pocisk gracza | 3 | 2 | Pocisk widzi cele |

W Godot wartości są bitowe:

```text
Layer 1 = 1
Layer 2 = 2
Layer 3 = 4
```

Dlatego w kodzie pocisku ustawiono:

```gdscript
collision_layer = 4
collision_mask = 2
```

A w hitboxie celu:

```gdscript
hitbox.collision_layer = 2
hitbox.collision_mask = 4
```

---

## Wymagania z laboratorium

Projekt spełnia wymagania:

- pocisk powstaje po naciśnięciu spacji,
- pocisk jest osobną sceną `bullet.tscn`,
- pocisk znika po czasie życia,
- cel jest osobną sceną `target.tscn`,
- cel ma `Area3D` i `CollisionShape3D`,
- cel znika po trafieniu,
- sygnał `area_entered` jest podłączony w kodzie,
- cooldown strzału działa,
- kilka celów znajduje się w scenie,
- wynik jest wypisywany w konsoli,
- projekt nie wymaga wysyłania folderu `.godot/`.

---

## Co wysłać do GitHub?

Wyślij cały folder:

```text
lab_10/
```

Nie wysyłaj:

```text
.godot/
.import/
*.uid
*.tmp
.idea/
.vscode/
```

---

## Propozycja commita

```bash
git add lab_10
git commit -m "Add lab 10 Godot shooting and 3D collisions"
git push
```
