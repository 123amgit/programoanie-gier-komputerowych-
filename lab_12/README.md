# Laboratorium 12 - Środowisko, Barrel Roll i Kamera

Przedmiot: **Tworzenie Gier Komputerowych**  
Technologia: **Godot Engine 4.x / GDScript**

Projekt jest rozwinięciem `lab_11`. W poprzednim laboratorium działały fale wrogów, wrogowie z HP, ruch przez `Tween`, uniwersalne pociski oraz strzelanie wrogów w kierunku gracza. W tym laboratorium dodano elementy poprawiające **game feel** i czytelność sceny: tło świata, korytarz ze ścianami, kamerę z opóźnieniem oraz barrel roll z chwilową nieśmiertelnością.

---

## Najważniejsze funkcje

- Zachowany ruch po szynie `Path3D` + `PathFollow3D`.
- Zachowany spawner fal z Lab 11.
- Wrogowie dalej pojawiają się falami, mają HP, strzelają i dają punkty.
- `WorldEnvironment` używa `Sky` z `ProceduralSkyMaterial`.
- Scena ma korytarz z czterema ścianami `StaticBody3D`.
- Statek wykrywa uderzenie w ścianę przez `Area3D.body_entered`.
- Statek ma lokalne `hp` wypisywane w konsoli.
- Kamera została przeniesiona poza `RailFollow`.
- `CameraTarget` jest dzieckiem `RailFollow`, a `Camera3D` śledzi go z opóźnieniem przez `lerp()`.
- Barrel roll działa na klawiszu `Q`.
- Barrel roll używa `AnimationPlayer`.
- Podczas barrel roll flaga `_is_invincible` blokuje obrażenia.
- Brak potrzeby wysyłania folderu `.godot/` do GitHub.

---

## Sterowanie

| Klawisz | Działanie |
|---|---|
| Strzałka w lewo | Ruch statku w lewo |
| Strzałka w prawo | Ruch statku w prawo |
| Strzałka w górę | Ruch statku w górę |
| Strzałka w dół | Ruch statku w dół |
| Spacja | Strzał |
| Q | Barrel roll / unik |

---

## Struktura projektu

```text
lab_12/
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
│   ├── wave_spawner.gd
│   └── camera_follow.gd
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
lab_12/project.godot
```

4. Otwórz scenę:

```text
main.tscn
```

5. Uruchom przez **F5**.

Jeśli Godot zapyta o scenę startową, wybierz:

```text
res://main.tscn
```

---

## Opis techniczny

### 1. WorldEnvironment i niebo

W scenie `main.tscn` znajduje się węzeł:

```text
WorldEnvironment
```

Ma on zasób `Environment`, którego tłem jest `Sky` z materiałem `ProceduralSkyMaterial`. Kolory są ciemne, żeby pasowały do kosmicznego korytarza i żeby pociski oraz wrogowie były dobrze widoczne.

To spełnia wymaganie:

```text
WorldEnvironment + Sky jako tło sceny 3D
```

---

### 2. Korytarz ze ścianami

W scenie jest węzeł:

```text
Corridor
├── LeftWall
├── RightWall
├── TopWall
└── BottomWall
```

Każda ściana jest typu `StaticBody3D` i ma:

```text
MeshInstance3D
CollisionShape3D
```

Ściany są na warstwie kolizji 5, czyli bitowo:

```gdscript
collision_layer = 16
```

Hitbox gracza ma maskę:

```gdscript
collision_mask = 26
```

czyli reaguje na:

| Obiekt | Numer warstwy | Wartość bitowa |
|---|---:|---:|
| Wrogowie | 2 | 2 |
| Pociski wroga | 4 | 8 |
| Ściany | 5 | 16 |

Razem:

```text
2 + 8 + 16 = 26
```

---

### 3. Dlaczego `body_entered`, a nie `area_entered`?

Statek ma hitbox typu `Area3D`, ale ściana jest typu `StaticBody3D`. Dla kontaktu:

```text
Area3D -> Area3D
```

używa się:

```gdscript
area_entered
```

Dla kontaktu:

```text
Area3D -> StaticBody3D / PhysicsBody3D
```

używa się:

```gdscript
body_entered
```

Dlatego w `player_ship.gd` są podłączone oba sygnały:

```gdscript
player_hitbox.area_entered.connect(_on_player_area_entered)
player_hitbox.body_entered.connect(_on_player_body_entered)
```

---

### 4. Lokalny system HP

W `player_ship.gd` dodano:

```gdscript
@export var max_hp: int = 5
var hp: int = 5
```

Metoda:

```gdscript
func _take_damage(amount: int) -> void:
```

zmniejsza HP i wypisuje wynik w konsoli:

```text
Statek otrzymał obrażenia: -1 | HP = 4/5
```

To jest lokalna wersja systemu życia. Pełny `GameManager` ma pojawić się w późniejszym laboratorium.

---

### 5. Kamera z opóźnieniem

W Lab 11 kamera była dzieckiem `RailFollow`, czyli była sztywno przyklejona do ruchu szyny. W Lab 12 hierarchia została zmieniona:

```text
Main
├── RailPath
│   └── RailFollow
│       ├── Ship
│       └── CameraTarget
└── Camera3D
```

`CameraTarget` dalej jedzie po szynie, ale kamera jest poza `RailFollow` i ma skrypt:

```text
scripts/camera_follow.gd
```

W skrypcie kamera wykonuje:

```gdscript
global_position = global_position.lerp(_camera_target.global_position, follow_weight)
```

Dzięki temu kamera nie jest absolutnie sztywna. Przy gwałtownym ruchu statku widać lekkie opóźnienie, które poprawia odczucie sterowania.

---

### 6. Barrel Roll

Węzeł `Ship` ma dziecko:

```text
AnimationPlayer
```

Skrypt `player_ship.gd` tworzy animację `barrel_roll`, jeśli nie została przygotowana ręcznie w edytorze. Animacja obraca `ShipMesh.rotation.z` od `0` do `TAU` w czasie około `0.6 s`.

Uruchomienie:

```gdscript
animation_player.play("barrel_roll")
```

Podczas animacji:

```gdscript
_is_invincible = true
```

Po zakończeniu animacji:

```gdscript
_is_invincible = false
```

W `_take_damage()` jest zabezpieczenie:

```gdscript
if _is_invincible:
    return
```

Dzięki temu pocisk wroga albo ściana nie odbiera HP podczas barrel roll.

---

## Jak sprawdzić laboratorium?

Po uruchomieniu przez **F5** sprawdź:

1. W tle widać ciemne niebo / środowisko.
2. W scenie widać korytarz ze ścianami.
3. Statek i gra dalej lecą po szynie.
4. Wrogowie dalej spawnują się falami.
5. Kamera ma lekkie opóźnienie względem `CameraTarget`.
6. Gdy dotkniesz ściany albo pocisku wroga, konsola pokazuje spadek HP.
7. Gdy wciśniesz `Q`, statek wykonuje barrel roll.
8. Podczas barrel roll uderzenie nie zmniejsza HP.
9. W konsoli nie ma czerwonych błędów.

---

## Co wysłać na GitHub?

Wyślij cały folder:

```text
lab_12/
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
git add lab_12
git commit -m "Add lab 12 environment camera lag and barrel roll"
git push
```
