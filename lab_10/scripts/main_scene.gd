extends Node3D

# ============================================================
# LABORATORIUM 10 - GŁÓWNA SCENA
# ============================================================
# Główna scena przechowuje wynik i podłącza sygnały celów.
# Pełny HUD pojawi się w późniejszym laboratorium, dlatego tutaj
# wynik jest wypisywany w konsoli za pomocą print().
# ============================================================

var score: int = 0
var targets_left: int = 0


func _ready() -> void:
    _connect_targets()
    print("Lab 10 uruchomiony. Sterowanie: strzałki = ruch, SPACJA = strzał.")
    print("Cele w scenie: ", targets_left)


func _connect_targets() -> void:
    var targets := get_tree().get_nodes_in_group("targets")
    targets_left = targets.size()

    for target in targets:
        if target.has_signal("target_destroyed"):
            # CONNECT_ONE_SHOT nie jest użyte, bo target i tak znika po trafieniu.
            target.target_destroyed.connect(_on_target_destroyed)


func _on_target_destroyed(points: int) -> void:
    score += points
    targets_left = max(targets_left - 1, 0)

    print("Wynik: ", score, " | Pozostałe cele: ", targets_left)

    if targets_left == 0:
        print("Wszystkie cele zestrzelone. Koniec zadania Lab 10.")
