extends Node3D

# ============================================================
# LABORATORIUM 14 - EKSPLOZJA CZĄSTECZKOWA
# ============================================================
# Krótka scena efektu. Boss instancjonuje ją w swojej globalnej pozycji.
# Po zakończeniu emisji scena sama się usuwa, więc nie zostają śmieci w drzewie.
# ============================================================

@export var cleanup_time: float = 0.8

@onready var particles: GPUParticles3D = $GPUParticles3D


func _ready() -> void:
	if particles != null:
		particles.emitting = true

	await get_tree().create_timer(cleanup_time).timeout
	queue_free()
