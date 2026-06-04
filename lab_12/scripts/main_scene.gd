extends Node3D

# ============================================================
# LABORATORIUM 11/12 - GŁÓWNA SCENA
# ============================================================
# Main przechowuje wynik i odbiera sygnał died(points) od wrogów.
# Wrogowie nie znają dokładnej ścieżki do Main. Spawner rejestruje ich
# przez register_enemy(), a Main podłącza sygnał. To jest luźniejsze
# powiązanie niż ręczne get_node() z twardą ścieżką.
# ============================================================

var score: int = 0
var enemies_destroyed: int = 0
var enemies_spawned: int = 0


func _ready() -> void:
	print("Lab 12 uruchomiony: środowisko, kamera z opóźnieniem i barrel roll.")
	print("Sterowanie: strzałki = ruch XY, SPACJA = strzał, Q = barrel roll.")
	print("Wrogowie pojawią się falami przed statkiem.")


func register_enemy(enemy: Node) -> void:
	# Funkcja wywoływana przez WaveSpawner zaraz po utworzeniu wroga.
	enemies_spawned += 1

	if enemy.has_signal("died"):
		enemy.died.connect(_on_enemy_died)

	print("Zarejestrowano wroga: ", enemy.name, " | razem spawn: ", enemies_spawned)


func _on_enemy_died(points: int) -> void:
	score += points
	enemies_destroyed += 1
	print("Wynik: ", score, " | Zniszczeni wrogowie: ", enemies_destroyed, "/", enemies_spawned)


func add_score(points: int) -> void:
	# Dodatkowa metoda pomocnicza, zostawiona na przyszłe laboratoria.
	score += points
	print("Wynik: ", score)
