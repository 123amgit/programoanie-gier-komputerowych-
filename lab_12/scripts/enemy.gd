extends Node3D

# ============================================================
# LABORATORIUM 11/12 - WRÓG
# ============================================================
# Wróg zastępuje statyczny target z Lab 10 i pozostaje zgodny z Lab 12.
# Ma punkty życia, emituje sygnał died(points), porusza się ruchem bocznym
# przez Tween i potrafi strzelać w kierunku gracza.
# ============================================================

signal died(points: int)

@export var hp: int = 2
@export var speed: float = 3.0
@export var score_value: int = 100

# Parametry bujania w osi X przez Tween.
@export var sway_amplitude: float = 1.4
@export var sway_period: float = 2.0

# Strzelanie wroga.
@export var bullet_scene: PackedScene = preload("res://scenes/bullet.tscn")
@export var shoot_interval: float = 2.5
@export var enemy_bullet_speed: float = 18.0

@onready var hitbox: Area3D = $Area3D
@onready var mesh: MeshInstance3D = $MeshInstance3D

var _shoot_timer: float = 0.0
var _dead: bool = false


func _ready() -> void:
	add_to_group("enemies")
	hitbox.add_to_group("enemy_hitboxes")

	# Wróg: Layer 2, Mask 1 + 3.
	# Bitowo: layer 2 = 2, mask 1 = 1, mask 3 = 4, razem 5.
	hitbox.collision_layer = 2
	hitbox.collision_mask = 5
	hitbox.monitoring = true
	hitbox.monitorable = true
	hitbox.area_entered.connect(_on_area_entered)

	_start_sway_tween()

	# Żeby kilka wrogów nie strzelało idealnie w tej samej klatce,
	# startujemy timer od małej losowej wartości.
	_shoot_timer = randf_range(0.2, shoot_interval)


func _process(delta: float) -> void:
	if _dead:
		return

	_shoot_timer -= delta
	if _shoot_timer <= 0.0:
		_shoot_timer = shoot_interval
		_shoot_at_player()


func configure_from_wave(data: Dictionary) -> void:
	# Spawner może nadpisać parametry wroga danymi fali.
	# Dzięki temu kod wroga jest jeden, ale fale mogą mieć różne typy wrogów.
	hp = int(data.get("hp", hp))
	speed = float(data.get("speed", speed))
	score_value = int(data.get("score_value", score_value))
	sway_amplitude = float(data.get("sway_amplitude", sway_amplitude))
	sway_period = float(data.get("sway_period", sway_period))
	shoot_interval = float(data.get("shoot_interval", shoot_interval))
	enemy_bullet_speed = float(data.get("enemy_bullet_speed", enemy_bullet_speed))


func _start_sway_tween() -> void:
	# Tween animuje właściwość bez ręcznego liczenia sinusa w _process().
	# Robimy dwie fazy: prawo -> lewo, a set_loops() powtarza je w nieskończoność.
	var base_x: float = position.x
	var half_period: float = maxf(sway_period * 0.5, 0.05)

	var tween := create_tween()
	tween.set_loops()
	tween.set_trans(Tween.TRANS_SINE)
	tween.set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(self, "position:x", base_x + sway_amplitude, half_period)
	tween.tween_property(self, "position:x", base_x - sway_amplitude, sway_period)
	tween.tween_property(self, "position:x", base_x, half_period)


func _on_area_entered(area: Area3D) -> void:
	if _dead:
		return

	if area.is_in_group("player_bullets"):
		if area.has_method("destroy"):
			area.destroy()
		_take_damage(1)
		return

	if area.is_in_group("player_hitboxes"):
		# Taranowanie jest wykrywane zgodnie z tabelą warstw,
		# ale w tym laboratorium nie ma jeszcze pełnego systemu życia gracza.
		print("Wróg dotknął gracza: ", name)


func _take_damage(amount: int) -> void:
	hp -= amount
	print(name, " otrzymał trafienie. HP = ", hp)

	_flash_hit_color()

	if hp <= 0:
		_die()


func _die() -> void:
	if _dead:
		return

	_dead = true
	print("Wróg zniszczony: ", name, " +", score_value, " pkt")
	died.emit(score_value)
	queue_free()


func _shoot_at_player() -> void:
	if bullet_scene == null:
		return

	var players := get_tree().get_nodes_in_group("player")
	if players.is_empty():
		return

	var player := players[0] as Node3D
	if player == null:
		return

	var direction_to_player := player.global_position - global_position
	if direction_to_player.length() <= 0.01:
		return

	var bullet := bullet_scene.instantiate() as Area3D
	if bullet == null:
		return

	get_tree().current_scene.add_child(bullet)

	if bullet.has_method("setup"):
		bullet.setup(global_position, direction_to_player.normalized(), "enemy")
		bullet.speed = enemy_bullet_speed
	else:
		bullet.global_position = global_position

	print("Wróg strzela: ", name)


func _flash_hit_color() -> void:
	# Prosta informacja wizualna po trafieniu.
	# Materiał lokalny zapobiega zmianie koloru wszystkich instancji naraz.
	var material := StandardMaterial3D.new()
	material.albedo_color = Color(1.0, 0.1, 0.1, 1.0)
	mesh.material_override = material

	await get_tree().create_timer(0.08).timeout

	if is_instance_valid(mesh) and not _dead:
		var normal_material := StandardMaterial3D.new()
		normal_material.albedo_color = Color(0.95, 0.2, 1.0, 1.0)
		mesh.material_override = normal_material
