# Laboratorium 14: Boss, FSM i Domknięcie Projektu

Projekt `lab14` powstał jako kontynuacja `lab13`. Zostawiono działające elementy z poprzednich laboratoriów: szynę lotu, statek gracza, strzelanie, fale przeciwników, HUD, `GameManager` jako Autoload, menu, ekran końca gry i ekran ukończenia poziomu.

## Co zostało dodane w Lab 14

### 1. Boss z dwoma hitboxami

Dodano scenę:

```text
scenes/boss.tscn
scripts/boss.gd
```

Boss ma dwa niezależne `Area3D`:

- `HitboxPhase1` - większy hitbox aktywny na początku walki,
- `HitboxPhase2` - mniejszy hitbox aktywny po spadku HP poniżej połowy.

Oba hitboxy są ustawione jak hitbox przeciwnika: warstwa kolizji 2 i maska widząca pociski gracza.

### 2. Maszyna stanów FSM

W `scripts/boss.gd` użyto:

```gdscript
enum State { IDLE, ATTACK, RETREAT, DEATH }
```

Zmiana stanu odbywa się przez metodę `_enter_state(new_state)`, a inicjalizacja stanów jest rozdzielona na:

- `_start_idle()`
- `_start_attack()`
- `_start_retreat()`
- `_start_death()`

Zachowanie:

- `IDLE` - boss czeka około 2 sekundy,
- `ATTACK` - boss strzela do gracza i porusza się przez `Tween`,
- `RETREAT` - boss cofa się w osi Z przez `Tween`,
- `DEATH` - boss emituje `died`, dodaje punkty, tworzy eksplozję i usuwa się ze sceny.

### 3. Eksplozja cząsteczkowa

Dodano scenę:

```text
scenes/explosion.tscn
scripts/explosion.gd
```

Efekt używa `GPUParticles3D` z ustawieniami:

- `amount = 48`,
- `lifetime = 0.6`,
- `one_shot = true`,
- `explosiveness = 1.0`,
- `ParticleProcessMaterial` ze sferycznym rozrzutem.

Po około 0.8 sekundy scena eksplozji sama wykonuje `queue_free()`.

### 4. Integracja bossa z grą

Boss został dodany do `main.tscn` jako instancja:

```text
Boss -> scenes/boss.tscn
```

W `scripts/main_scene.gd` podłączono sygnał:

```gdscript
boss.died.connect(_on_boss_died)
```

Dzięki temu boss nie wywołuje samodzielnie `GameManager.finish_level()`. Boss tylko informuje, że umarł, a główna scena decyduje, że oznacza to ukończenie poziomu.

Pełna pętla:

```text
menu -> gra -> fale przeciwników -> boss -> level_complete
```

### 5. Refaktoryzacja

Wprowadzono poprawki zgodne z wymaganiami laboratorium:

1. **Magiczne liczby**  
   W `boss.gd` użyto `const` i `@export`, np. `PHASE_TWO_RATIO`, `SCORE_FOR_BOSS`, `attack_duration`, `shoot_interval`, `retreat_distance`.

2. **Długie metody**  
   Logika bossa jest podzielona na osobne metody `_start_*`, `_process_*`, `_shoot_at_player()`, `_spawn_explosion()`, `_set_phase_two_enabled()`.

3. **Sygnały zamiast bezpośrednich wywołań**  
   Boss emituje `died`, a `Main` obsługuje zakończenie poziomu przez `GameManager.finish_level()`.

## Uruchomienie

1. Otwórz folder `lab14` w Godot Engine 4.x.
2. Uruchom projekt.
3. Sceną startową jest `main_menu.tscn`.
4. Kliknij `Graj`.
5. Sterowanie:
   - strzałki - ruch statku,
   - spacja - strzał,
   - Q - barrel roll.
