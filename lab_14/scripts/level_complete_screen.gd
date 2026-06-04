extends Control

func _ready() -> void:
	$CenterContainer/VBoxContainer/ScoreLabel.text = "Wynik: %d" % GameManager.score
	$CenterContainer/VBoxContainer/MenuButton.pressed.connect(_on_menu_pressed)

func _on_menu_pressed() -> void:
	get_tree().change_scene_to_file("res://main_menu.tscn")
