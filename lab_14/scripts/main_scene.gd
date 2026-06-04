extends Node3D

# ============================================================
# LABORATORIUM 14 - GŁÓWNA SCENA GRY
# ============================================================
# Lab 14 domyka projekt: po falach pojawia się boss z FSM.
# Main nie steruje szczegółami bossa. Tylko podpina jego signal died
# do zakończenia poziomu w GameManagerze.
# ============================================================

@export var boss_path: NodePath = ^"Boss"
@export var boss_intro_delay: float = 0.7

var enemies_destroyed: int = 0
var enemies_spawned: int = 0
var all_waves_spawned: bool = false
var _boss_defeated: bool = false
var _boss_intro_done: bool = false


func _ready() -> void:
	print("Lab 14 uruchomiony na bazie Lab 13.")
	print("Sterowanie: strzałki = ruch XY, SPACJA = strzał, Q = barrel roll.")
	print("Cel: przejdź fale, pokonaj bossa FSM i zobacz ekran ukończenia.")

	GameManager.game_over.connect(_on_game_over)
	GameManager.level_complete.connect(_on_level_complete)

	_connect_spawner_signals()
	_connect_boss_signals()
	_sync_hud_state()


func register_enemy(enemy: Node) -> void:
	enemies_spawned += 1

	if enemy.has_signal("died"):
		enemy.died.connect(_on_enemy_died)

	print("Zarejestrowano wroga: ", enemy.name, " | razem spawn: ", enemies_spawned)


func _connect_spawner_signals() -> void:
	var spawner := get_node_or_null("WaveSpawner")
	if spawner != null and spawner.has_signal("all_waves_spawned"):
		spawner.all_waves_spawned.connect(_on_all_waves_spawned)


func _connect_boss_signals() -> void:
	var boss := get_node_or_null(boss_path)
	if boss == null:
		push_warning("Nie znaleziono bossa pod ścieżką: " + str(boss_path))
		return

	if boss.has_signal("died"):
		boss.died.connect(_on_boss_died)
		print("Boss podłączony do Main przez signal died.")


func _sync_hud_state() -> void:
	# Menu wywołuje reset(), ale synchronizacja tutaj pomaga przy starcie main.tscn bezpośrednio.
	GameManager.score_changed.emit(GameManager.score)
	GameManager.lives_changed.emit(GameManager.lives)
	GameManager.hp_changed.emit(GameManager.player_hp)


func _on_enemy_died(points: int) -> void:
	enemies_destroyed += 1
	GameManager.add_score(points)
	print("Zniszczeni wrogowie: ", enemies_destroyed, "/", enemies_spawned)
	_check_boss_intro()


func _on_all_waves_spawned() -> void:
	all_waves_spawned = true
	print("Wszystkie fale zostały wypuszczone. Boss czeka na końcu korytarza.")
	_check_boss_intro()


func _check_boss_intro() -> void:
	if _boss_intro_done:
		return

	if all_waves_spawned and enemies_spawned > 0 and enemies_destroyed >= enemies_spawned:
		_boss_intro_done = true
		await get_tree().create_timer(boss_intro_delay).timeout
		print("Fale wyczyszczone. Teraz walka z bossem.")


func _on_boss_died() -> void:
	if _boss_defeated:
		return

	_boss_defeated = true
	print("Boss pokonany. Main wywołuje GameManager.finish_level().")
	GameManager.finish_level()


func _on_game_over() -> void:
	await get_tree().create_timer(0.8).timeout
	get_tree().change_scene_to_file("res://game_over.tscn")


func _on_level_complete() -> void:
	await get_tree().create_timer(0.8).timeout
	get_tree().change_scene_to_file("res://level_complete.tscn")
