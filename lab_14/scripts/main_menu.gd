extends Control

func _ready() -> void:
	$CenterContainer/VBoxContainer/PlayButton.pressed.connect(_on_play_pressed)

func _on_play_pressed() -> void:
	GameManager.reset()
	get_tree().change_scene_to_file("res://main.tscn")
