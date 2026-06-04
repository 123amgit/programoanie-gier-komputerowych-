# Laboratorium 13 - HUD, Stany Gry i Audio

Projekt jest zrobiony bez zaczynania od zera: to kontynuacja przesłanego `lab_12_complete.zip`.
Zachowane są elementy z poprzednich laboratoriów:

- `Path3D` + `PathFollow3D` z Lab 09,
- pociski i kolizje z Lab 10,
- wrogowie, fale i sygnał `died(points)` z Lab 11,
- `WorldEnvironment`, korytarz, kamera z opóźnieniem i barrel roll z Lab 12.

Lab 13 dodaje na to warstwę systemową: `GameManager`, HUD, menu, koniec gry, ukończenie poziomu i dźwięki.

---

## Najważniejsze pliki dodane w Lab 13

```text
scripts/game_manager.gd          # Autoload / singleton stanu gry
scripts/hud.gd                   # HUD w CanvasLayer
scripts/main_menu.gd             # menu startowe
scripts/game_over_screen.gd      # ekran końca gry
scripts/level_complete_screen.gd # ekran ukończenia poziomu
main_menu.tscn
game_over.tscn
level_complete.tscn
assets/audio/score.wav
assets/audio/hit.wav
assets/audio/game_over.wav
```

---

## GameManager

`GameManager` jest zarejestrowany w `project.godot` jako Autoload:

```ini
[autoload]
GameManager="*res://scripts/game_manager.gd"
```

Przechowuje:

```gdscript
var score: int = 0
var lives: int = 3
var player_max_hp: int = 5
var player_hp: int = 5
var best_score: int = 0
```

Emituje sygnały stanu do HUD:

```gdscript
score_changed(new_score)
lives_changed(new_lives)
hp_changed(new_hp)
game_over
level_complete
```

Emituje sygnały zdarzeń do dźwięków:

```gdscript
enemy_killed
player_damaged
```

Dzięki temu dźwięk zabicia wroga nie jest podpięty do `score_changed`, bo wynik może kiedyś wzrosnąć także za bonus czasu albo monetę.

---

## HUD

HUD jest w `main.tscn` jako:

```text
HUD (CanvasLayer)
├── ScoreLabel
├── LivesLabel
└── HPBar
```

Skrypt `scripts/hud.gd` podłącza się do sygnałów `GameManager` i aktualizuje:

- wynik,
- życia,
- pasek HP.

---

## Integracja z wrogami

Spawner nadal tworzy wrogów z danych fal. Po utworzeniu wroga wywołuje:

```gdscript
main_node.register_enemy(enemy)
```

A `main_scene.gd` podłącza sygnał:

```gdscript
enemy.died.connect(_on_enemy_died)
```

Po śmierci wroga:

```gdscript
GameManager.add_score(points)
```

To spełnia wymaganie Lab 13: `died(points)` z Lab 11 trafia do `GameManager.add_score(points)`.

---

## Integracja z graczem

W Lab 12 gracz miał lokalne HP. W Lab 13 metoda `_take_damage()` została zmieniona:

```gdscript
func _take_damage(amount: int) -> void:
    if _is_invincible:
        print("Obrażenia zablokowane przez barrel roll.")
        return

    GameManager.player_hit(amount)
```

Barrel roll dalej blokuje obrażenia, ale samo HP jest już w `GameManager`.

---

## Pętla scen

Startowa scena projektu to:

```text
main_menu.tscn
```

Pętla gry:

```text
main_menu.tscn -> main.tscn -> game_over.tscn -> main_menu.tscn
```

albo:

```text
main_menu.tscn -> main.tscn -> level_complete.tscn -> main_menu.tscn
```

Przycisk `Graj` wywołuje:

```gdscript
GameManager.reset()
get_tree().change_scene_to_file("res://main.tscn")
```

---

## Kiedy jest koniec gry?

Gracz traci HP po:

- trafieniu pociskiem wroga,
- kontakcie z wrogiem,
- uderzeniu w ścianę.

Gdy HP spadnie do 0, gracz traci życie. Gdy życia spadną do 0, `GameManager` emituje:

```gdscript
game_over
```

`main_scene.gd` przełącza wtedy scenę na:

```text
game_over.tscn
```

---

## Kiedy poziom jest ukończony?

`WaveSpawner` emituje `all_waves_spawned`, kiedy wypuści wszystkie fale. `Main` sprawdza wtedy, czy wszyscy zarejestrowani wrogowie zostali zniszczeni.

Warunek:

```text
wszystkie fale wypuszczone + liczba zniszczonych wrogów >= liczba zespawnowanych wrogów
```

Wtedy `GameManager.finish_level()` emituje:

```gdscript
level_complete
```

---

## Sterowanie

| Klawisz | Działanie |
|---|---|
| Strzałki | ruch statku w X/Y |
| Spacja | strzał |
| Q | barrel roll / chwilowa nieśmiertelność |
