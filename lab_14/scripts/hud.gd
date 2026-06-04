extends CanvasLayer

# ============================================================
# LABORATORIUM 13 - HUD W CANVASLAYER
# ============================================================
# HUD jest niezależny od sceny 3D. Słucha sygnałów GameManagera i aktualizuje
# etykiety oraz pasek HP.
# ============================================================

@onready var score_label: Label = $ScoreLabel
@onready var lives_label: Label = $LivesLabel
@onready var hp_bar: ProgressBar = $HPBar


func _ready() -> void:
	hp_bar.min_value = 0
	hp_bar.max_value = GameManager.player_max_hp

	GameManager.score_changed.connect(_on_score_changed)
	GameManager.lives_changed.connect(_on_lives_changed)
	GameManager.hp_changed.connect(_on_hp_changed)

	_on_score_changed(GameManager.score)
	_on_lives_changed(GameManager.lives)
	_on_hp_changed(GameManager.player_hp)


func _on_score_changed(new_score: int) -> void:
	score_label.text = "Wynik: %d" % new_score


func _on_lives_changed(new_lives: int) -> void:
	lives_label.text = "Życia: %d" % new_lives


func _on_hp_changed(new_hp: int) -> void:
	hp_bar.value = new_hp
