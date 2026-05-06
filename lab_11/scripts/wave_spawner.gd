extends Node

# ============================================================
# LABORATORIUM 11 - SPAWNER FAL
# ============================================================
# Najważniejszy cel tego pliku: dane fal są oddzielone od logiki.
# Zamiast pisać:
#   if wave == 1: ... elif wave == 2: ...
# trzymamy fale w tablicy słowników.
#
# Kod spawnera czyta dane i tworzy wrogów. Dodanie nowej fali wymaga dopisania
# nowego słownika, nie nowej gałęzi if/elif. To jest prosty wzorzec data-driven.
# ============================================================

@export var enemy_scene: PackedScene = preload("res://scenes/enemy.tscn")
@export var rail_follow_path: NodePath = ^"../RailPath/RailFollow"

var _elapsed_time: float = 0.0
var _spawned: Array[bool] = []

# Co najmniej trzy fale, różne układy, opóźnienia i parametry.
# x_positions określa rozstaw wrogów względem pozycji RailFollow.
# z_offset jest ujemny, bo gracz leci w stronę -Z.
var waves: Array[Dictionary] = [
	{
		"name": "Fala 1 - trójka prosta",
		"delay": 1.0,
		"x_positions": [-3.0, 0.0, 3.0],
		"y": 0.0,
		"z_offset": -28.0,
		"hp": 2,
		"score_value": 100,
		"sway_amplitude": 1.1,
		"sway_period": 2.2,
		"shoot_interval": 2.7
	},
	{
		"name": "Fala 2 - góra i dół",
		"delay": 5.0,
		"x_positions": [-4.0, -1.5, 1.5, 4.0],
		"y_positions": [1.5, -1.0, -1.0, 1.5],
		"z_offset": -34.0,
		"hp": 2,
		"score_value": 125,
		"sway_amplitude": 1.6,
		"sway_period": 1.8,
		"shoot_interval": 2.3
	},
	{
		"name": "Fala 3 - mocniejsi wrogowie",
		"delay": 9.5,
		"x_positions": [-2.5, 0.0, 2.5],
		"y": 1.1,
		"z_offset": -38.0,
		"hp": 3,
		"score_value": 180,
		"sway_amplitude": 2.0,
		"sway_period": 2.6,
		"shoot_interval": 1.9,
		"enemy_bullet_speed": 20.0
	}
]


func _ready() -> void:
	_spawned.resize(waves.size())
	for i in range(_spawned.size()):
		_spawned[i] = false

	print("WaveSpawner gotowy. Liczba fal: ", waves.size())


func _process(delta: float) -> void:
	_elapsed_time += delta

	for wave_index in range(waves.size()):
		if _spawned[wave_index]:
			continue

		var wave := waves[wave_index]
		var delay := float(wave.get("delay", 0.0))

		if _elapsed_time >= delay:
			_spawn_wave(wave_index, wave)
			_spawned[wave_index] = true


func _spawn_wave(wave_index: int, wave: Dictionary) -> void:
	if enemy_scene == null:
		push_warning("Brak enemy_scene w WaveSpawner.")
		return

	var rail_follow := get_node_or_null(rail_follow_path) as PathFollow3D
	if rail_follow == null:
		push_warning("Nie znaleziono RailFollow pod ścieżką: " + str(rail_follow_path))
		return

	print("Spawn fali ", wave_index + 1, ": ", wave.get("name", "bez nazwy"))

	var x_positions: Array = wave.get("x_positions", [0.0])
	var y_positions: Array = wave.get("y_positions", [])
	var default_y := float(wave.get("y", 0.0))
	var z_offset := float(wave.get("z_offset", -30.0))

	for enemy_index in range(x_positions.size()):
		var x := float(x_positions[enemy_index])
		var y := default_y

		if enemy_index < y_positions.size():
			y = float(y_positions[enemy_index])

		_spawn_enemy(wave, rail_follow.global_position + Vector3(x, y, z_offset), wave_index, enemy_index)


func _spawn_enemy(wave: Dictionary, spawn_position: Vector3, wave_index: int, enemy_index: int) -> void:
	var enemy := enemy_scene.instantiate() as Node3D
	if enemy == null:
		push_warning("enemy_scene nie jest Node3D.")
		return

	get_tree().current_scene.add_child(enemy)
	enemy.global_position = spawn_position
	enemy.name = "Enemy_W%d_%d" % [wave_index + 1, enemy_index + 1]

	if enemy.has_method("configure_from_wave"):
		enemy.configure_from_wave(wave)

	var main_node := get_tree().current_scene
	if main_node != null and main_node.has_method("register_enemy"):
		main_node.register_enemy(enemy)

	# Wrogów dodajemy do Main, a nie do RailFollow.
	# Gdyby byli dziećmi RailFollow, lecieliby razem z kamerą i statkiem,
	# więc gracz nigdy naprawdę by się do nich nie zbliżał.
	print("  Utworzono ", enemy.name, " w pozycji ", enemy.global_position)
