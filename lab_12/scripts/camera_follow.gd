extends Camera3D

# ============================================================
# LABORATORIUM 12 - KAMERA Z OPÓŹNIENIEM
# ============================================================
# W Lab 09/10/11 kamera była dzieckiem RailFollow, więc była przyklejona
# do szyny. W Lab 12 kamera zostaje przeniesiona poza RailFollow.
#
# CameraTarget nadal jest dzieckiem RailFollow i wskazuje idealne miejsce kamery.
# Kamera śledzi CameraTarget z opóźnieniem przez lerp(). Dzięki temu ruch statku
# ma lepsze odczucie ciężaru i bezwładności.
# ============================================================

@export var camera_target_path: NodePath
@export var look_at_target_path: NodePath
@export var lag_speed: float = 7.0
@export var look_lag_speed: float = 12.0

var _camera_target: Node3D
var _look_at_target: Node3D


func _ready() -> void:
	_camera_target = get_node_or_null(camera_target_path) as Node3D
	_look_at_target = get_node_or_null(look_at_target_path) as Node3D

	if _camera_target == null:
		push_warning("CameraFollow: nie ustawiono CameraTarget.")
	else:
		# Startujemy od pozycji celu, żeby kamera nie przeskakiwała z daleka.
		global_position = _camera_target.global_position

	current = true
	print("CameraFollow gotowy. lag_speed = ", lag_speed)


func _process(delta: float) -> void:
	if _camera_target == null:
		return

	# Zabezpieczenie przed zbyt dużą wartością czynnika lerp.
	var follow_weight: float = clampf(lag_speed * delta, 0.0, 1.0)
	global_position = global_position.lerp(_camera_target.global_position, follow_weight)

	# Kamera patrzy na statek / punkt przed statkiem. To utrzymuje czytelny kadr.
	if _look_at_target != null:
		look_at(_look_at_target.global_position, Vector3.UP)
