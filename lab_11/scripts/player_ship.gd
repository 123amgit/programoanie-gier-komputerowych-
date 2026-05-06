extends Node3D

# ============================================================
# LABORATORIUM 11 - STATEK GRACZA
# ============================================================
# Statek nadal jest dzieckiem PathFollow3D, więc automatycznie leci po szynie.
# Ten skrypt odpowiada za lokalny ruch XY, strzelanie oraz reakcję hitboxa.
#
# Zmiany względem Lab 10:
# - statek trafia do grupy "player", żeby wrogowie mogli znaleźć go bez
#   twardej ścieżki typu get_node("/root/Main/...").
# - hitbox gracza ma maskę 2 + 4, czyli reaguje na wrogów i pociski wroga.
# - pocisk gracza używa uniwersalnego bullet.gd z kierunkiem Vector3.FORWARD.
# ============================================================

@export var bullet_scene: PackedScene = preload("res://scenes/bullet.tscn")
@export var move_speed: float = 8.0
@export var limit_x: float = 5.0
@export var limit_y: float = 3.0
@export var shoot_cooldown_time: float = 0.30
@export var max_active_bullets: int = 5

@onready var muzzle: Node3D = $Nose
@onready var player_hitbox: Area3D = $PlayerHitbox

var _shoot_cooldown: float = 0.0
var _active_bullets: Array[Area3D] = []


func _ready() -> void:
	add_to_group("player")
	player_hitbox.add_to_group("player_hitboxes")

	# Gracz: Layer 1, Mask 2 + 4.
	# Bitowo: layer 1 = 1, mask 2 = 2, mask 4 = 8, razem 10.
	player_hitbox.collision_layer = 1
	player_hitbox.collision_mask = 10
	player_hitbox.monitoring = true
	player_hitbox.monitorable = true
	player_hitbox.area_entered.connect(_on_player_area_entered)


func _process(delta: float) -> void:
	_handle_movement(delta)
	_handle_shooting(delta)
	_clean_bullet_list()


func _handle_movement(delta: float) -> void:
	var input_x := Input.get_axis("ui_left", "ui_right")
	var input_y := Input.get_axis("ui_down", "ui_up")

	position.x += input_x * move_speed * delta
	position.y += input_y * move_speed * delta

	position.x = clamp(position.x, -limit_x, limit_x)
	position.y = clamp(position.y, -limit_y, limit_y)


func _handle_shooting(delta: float) -> void:
	if _shoot_cooldown > 0.0:
		_shoot_cooldown -= delta

	if Input.is_action_pressed("ui_accept") and _shoot_cooldown <= 0.0:
		_shoot()


func _shoot() -> void:
	if bullet_scene == null:
		push_warning("Brak sceny bullet_scene w PlayerShip.")
		return

	if _active_bullets.size() >= max_active_bullets:
		return

	var bullet := bullet_scene.instantiate() as Area3D
	if bullet == null:
		push_warning("bullet_scene nie jest Area3D.")
		return

	# Pocisk dodajemy do głównej sceny, nie jako dziecko statku.
	# Dzięki temu po wystrzeleniu nie dziedziczy ruchu PathFollow3D.
	get_tree().current_scene.add_child(bullet)

	# Kierunek strzału gracza. Przy tej scenie kamera i statek patrzą w -Z,
	# więc Vector3.FORWARD jest wystarczające i czytelne.
	if bullet.has_method("setup"):
		bullet.setup(muzzle.global_position, Vector3.FORWARD, "player")
	else:
		bullet.global_position = muzzle.global_position

	if bullet.has_signal("removed"):
		bullet.removed.connect(_on_bullet_removed)

	_active_bullets.append(bullet)
	_shoot_cooldown = shoot_cooldown_time


func _on_bullet_removed(bullet: Area3D) -> void:
	_active_bullets.erase(bullet)


func _clean_bullet_list() -> void:
	var cleaned: Array[Area3D] = []
	for bullet in _active_bullets:
		if is_instance_valid(bullet):
			cleaned.append(bullet)
	_active_bullets = cleaned


func _on_player_area_entered(area: Area3D) -> void:
	# Lab 11 nie wymaga jeszcze pełnego systemu życia gracza,
	# więc tylko wypisujemy informację diagnostyczną.
	if area.is_in_group("enemy_bullets"):
		print("Gracz trafiony pociskiem wroga.")
		if area.has_method("destroy"):
			area.destroy()
		return

	if area.is_in_group("enemy_hitboxes"):
		print("Gracz staranował wroga / wróg dotknął gracza.")
