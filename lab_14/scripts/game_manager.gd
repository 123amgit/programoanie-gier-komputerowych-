extends Node

# ============================================================
# LABORATORIUM 13 - GAMEMANAGER / AUTOLOAD
# ============================================================
# Globalny stan gry. Ten plik trzeba zarejestrować jako Autoload
# pod nazwą GameManager. W tym projekcie jest już wpis w project.godot.
#
# GameManager zbiera wynik, życia i HP gracza. HUD tylko słucha sygnałów,
# a gracz/wrogowie nie muszą znać ścieżek do UI.
# ============================================================

signal score_changed(new_score: int)
signal lives_changed(new_lives: int)
signal hp_changed(new_hp: int)
signal game_over
signal level_complete

# Sygnały zdarzeń do SFX. Są osobne od sygnałów stanu.
signal enemy_killed
signal player_damaged

var score: int = 0
var lives: int = 3
var player_max_hp: int = 5
var player_hp: int = 5
var best_score: int = 0

var _game_finished: bool = false

var _sfx_score := AudioStreamPlayer.new()
var _sfx_hit := AudioStreamPlayer.new()
var _sfx_game_over := AudioStreamPlayer.new()


func _ready() -> void:
	add_child(_sfx_score)
	add_child(_sfx_hit)
	add_child(_sfx_game_over)

	# Krótkie placeholdery WAV są w assets/audio.
	_sfx_score.stream = preload("res://assets/audio/score.wav")
	_sfx_hit.stream = preload("res://assets/audio/hit.wav")
	_sfx_game_over.stream = preload("res://assets/audio/game_over.wav")

	enemy_killed.connect(func(): _sfx_score.play())
	player_damaged.connect(func(): _sfx_hit.play())
	game_over.connect(func(): _sfx_game_over.play())

	print("GameManager Autoload gotowy.")


func reset() -> void:
	score = 0
	lives = 3
	player_hp = player_max_hp
	_game_finished = false

	score_changed.emit(score)
	lives_changed.emit(lives)
	hp_changed.emit(player_hp)

	print("GameManager reset: score=0, lives=3, hp=", player_hp)


func add_score(points: int) -> void:
	if _game_finished:
		return

	score += points
	score_changed.emit(score)
	enemy_killed.emit()

	print("GameManager score: ", score)


func player_hit(damage: int = 1) -> void:
	if _game_finished:
		return

	player_hp -= damage
	player_hp = maxi(player_hp, 0)
	hp_changed.emit(player_hp)
	player_damaged.emit()

	print("GameManager damage: HP = ", player_hp, "/", player_max_hp)

	if player_hp <= 0:
		lives -= 1
		lives_changed.emit(lives)

		if lives <= 0:
			_trigger_game_over()
		else:
			player_hp = player_max_hp
			hp_changed.emit(player_hp)
			print("Utrata życia. Pozostało żyć: ", lives)


func finish_level() -> void:
	if _game_finished:
		return

	_game_finished = true
	_update_best_score()
	level_complete.emit()
	print("Poziom ukończony. Wynik = ", score)


func _trigger_game_over() -> void:
	if _game_finished:
		return

	_game_finished = true
	_update_best_score()
	game_over.emit()
	print("Koniec gry. Wynik = ", score)


func _update_best_score() -> void:
	if score > best_score:
		best_score = score
