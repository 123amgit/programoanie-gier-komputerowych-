extends Control

func _ready() -> void:
	$CenterContainer/VBoxContainer/ScoreLabel.text = "Wynik końcowy: %d" % GameManager.score
	$CenterContainer/VBoxContainer/BestLabel.text = "Najlepszy wynik sesji: %d" % GameManager.best_score
	$CenterContainer/VBoxContainer/MenuButton.pressed.connect(_on_menu_pressed)

func _on_menu_pressed() -> void:
	get_tree().change_scene_to_file("res://main_menu.tscn")
