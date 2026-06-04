extends Node3D

# ============================================================
# LABORATORIUM 12 - STATEK GRACZA
# ============================================================
# Ten skrypt kontynuuje pracę z Lab 11:
# - statek nadal jest dzieckiem RailFollow, więc automatycznie leci po szynie,
# - gracz porusza się lokalnie w osi X/Y,
# - gracz strzela uniwersalnym pociskiem bullet.tscn,
# - wrogowie mogą znaleźć statek przez grupę "player".
#
# Nowości z Lab 12:
# - HP statku przeniesione do GameManagera w Lab 13,
# - wykrywanie kolizji ze ścianą StaticBody3D przez sygnał body_entered,
# - wykrywanie trafienia pociskiem wroga przez area_entered,
# - barrel roll uruchamiany klawiszem Q,
# - flaga _is_invincible blokująca obrażenia podczas barrel roll,
# - AnimationPlayer generuje/odtwarza animację obrotu modelu.
# ============================================================

@export var bullet_scene: PackedScene = preload("res://scenes/bullet.tscn")
@export var move_speed: float = 8.0
@export var limit_x: float = 5.6
@export var limit_y: float = 3.8
@export var shoot_cooldown_time: float = 0.30
@export var max_active_bullets: int = 5

# Czas animacji barrel roll. Wymaganie laboratorium: około 0.6 s.
@export var barrel_roll_duration: float = 0.6

@onready var muzzle: Node3D = $Nose
@onready var player_hitbox: Area3D = $PlayerHitbox
@onready var ship_mesh: MeshInstance3D = $ShipMesh
@onready var animation_player: AnimationPlayer = $AnimationPlayer

var _shoot_cooldown: float = 0.0
var _active_bullets: Array[Area3D] = []
var _is_invincible: bool = false
var _barrel_roll_running: bool = false


func _ready() -> void:
	add_to_group("player")
	player_hitbox.add_to_group("player_hitboxes")

	# Gracz: Layer 1.
	# Mask: 2 + 4 + 5, czyli:
	# - Layer 2 = wrogowie,
	# - Layer 4 = pociski wrogów,
	# - Layer 5 = ściany StaticBody3D.
	# Godot zapisuje to bitowo: 2 + 8 + 16 = 26.
	player_hitbox.collision_layer = 1
	player_hitbox.collision_mask = 26
	player_hitbox.monitoring = true
	player_hitbox.monitorable = true

	# Area3D -> Area3D: pociski wroga i hitboxy wrogów.
	player_hitbox.area_entered.connect(_on_player_area_entered)

	# Area3D -> PhysicsBody3D: ściany StaticBody3D.
	# To jest odpowiedź na pytanie z instrukcji: dla ściany używamy body_entered,
	# bo ściana nie jest Area3D, tylko StaticBody3D.
	player_hitbox.body_entered.connect(_on_player_body_entered)

	_ensure_barrel_roll_animation()

	print("PlayerShip gotowy. HP z GameManager = ", GameManager.player_hp, ". Q = barrel roll.")


func _process(delta: float) -> void:
	_handle_movement(delta)
	_handle_shooting(delta)
	_handle_barrel_roll_input()
	_clean_bullet_list()


func _handle_movement(delta: float) -> void:
	# Ruch jest lokalny względem RailFollow. Dzięki temu statek porusza się
	# w oknie przed kamerą, a jednocześnie cały zestaw leci po szynie.
	var input_x := Input.get_axis("ui_left", "ui_right")
	var input_y := Input.get_axis("ui_down", "ui_up")

	position.x += input_x * move_speed * delta
	position.y += input_y * move_speed * delta

	# clamp() ogranicza strefę manewru. Ściany stoją tuż za tym zakresem,
	# więc przy mocnym wychyleniu można wywołać kolizję ze ścianą.
	position.x = clampf(position.x, -limit_x, limit_x)
	position.y = clampf(position.y, -limit_y, limit_y)


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

	# Pocisk dodajemy do Main, nie do Ship ani RailFollow.
	# Wtedy po wystrzeleniu leci niezależnie w globalnej przestrzeni.
	get_tree().current_scene.add_child(bullet)

	if bullet.has_method("setup"):
		bullet.setup(muzzle.global_position, Vector3.FORWARD, "player")
	else:
		bullet.global_position = muzzle.global_position

	if bullet.has_signal("removed"):
		bullet.removed.connect(_on_bullet_removed)

	_active_bullets.append(bullet)
	_shoot_cooldown = shoot_cooldown_time


func _handle_barrel_roll_input() -> void:
	# Akcja barrel_roll jest dodana w project.godot i przypisana do klawisza Q.
	if Input.is_action_just_pressed("barrel_roll"):
		_start_barrel_roll()


func _start_barrel_roll() -> void:
	if _barrel_roll_running:
		return

	if animation_player == null:
		push_warning("Brak AnimationPlayer w statku.")
		return

	_barrel_roll_running = true
	_is_invincible = true

	print("Barrel roll start: statek chwilowo nieśmiertelny.")
	animation_player.play("barrel_roll")

	# Czekamy na koniec animacji. W tym czasie _take_damage() ignoruje obrażenia.
	await animation_player.animation_finished

	# Po animacji zdejmujemy nieśmiertelność i resetujemy obrót wizualnego modelu.
	_is_invincible = false
	_barrel_roll_running = false
	ship_mesh.rotation.z = 0.0
	print("Barrel roll koniec: statek znowu może otrzymywać obrażenia.")


func _ensure_barrel_roll_animation() -> void:
	# Żeby projekt był odporny na brak ręcznie utworzonej animacji w edytorze,
	# tworzymy animację przez kod, jeśli AnimationPlayer jej nie ma.
	# Nadal używamy AnimationPlayer, zgodnie z wymaganiem laboratorium.
	if animation_player == null:
		return

	if animation_player.has_animation("barrel_roll"):
		return

	var animation := Animation.new()
	animation.resource_name = "barrel_roll"
	animation.length = barrel_roll_duration

	var track_index := animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(track_index, NodePath("ShipMesh:rotation:z"))
	animation.track_insert_key(track_index, 0.0, 0.0)
	animation.track_insert_key(track_index, barrel_roll_duration, TAU)

	var library := AnimationLibrary.new()
	library.add_animation("barrel_roll", animation)
	animation_player.add_animation_library("", library)


func _take_damage(amount: int) -> void:
	# Najważniejszy warunek Lab 12 zostaje zachowany: podczas barrel roll
	# statek nie traci HP. Różnica w Lab 13: HP nie jest już lokalne,
	# tylko obsługiwane centralnie przez GameManager.
	if _is_invincible:
		print("Obrażenia zablokowane przez barrel roll.")
		return

	GameManager.player_hit(amount)


func _on_bullet_removed(bullet: Area3D) -> void:
	_active_bullets.erase(bullet)


func _clean_bullet_list() -> void:
	var cleaned: Array[Area3D] = []
	for bullet in _active_bullets:
		if is_instance_valid(bullet):
			cleaned.append(bullet)
	_active_bullets = cleaned


func _on_player_area_entered(area: Area3D) -> void:
	# Trafienie pociskiem wroga.
	if area.is_in_group("enemy_bullets"):
		print("Gracz trafiony pociskiem wroga.")
		if area.has_method("destroy"):
			area.destroy()
		_take_damage(1)
		return

	# Kontakt z wrogiem. To nadal Area3D -> Area3D.
	if area.is_in_group("enemy_hitboxes"):
		print("Gracz dotknął wroga.")
		_take_damage(1)


func _on_player_body_entered(body: Node3D) -> void:
	# Kontakt ze ścianą. Ściana jest StaticBody3D, więc przychodzi tutaj.
	if body.is_in_group("walls"):
		print("Gracz uderzył w ścianę: ", body.name)
		_take_damage(1)
