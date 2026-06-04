extends Node3D

# ============================================================
# LABORATORIUM 14 - BOSS, FSM I DWIE FAZY
# ============================================================
# Boss używa maszyny stanów enum + match. Ma dwa hitboxy:
# - faza 1: większy hitbox, trafienie zadaje 1 obrażenie,
# - faza 2: mniejszy hitbox, trafienie zadaje 2 obrażenia.
# Śmierć emituje signal died. Main decyduje, że to kończy poziom.
# ============================================================

signal died

enum State { IDLE, ATTACK, RETREAT, DEATH }

const PHASE_TWO_RATIO: float = 0.5
const MIN_SHOOT_VECTOR_LENGTH: float = 0.01
const SCORE_FOR_BOSS: int = 1000

@export var max_hp: int = 20
@export var idle_duration: float = 2.0
@export var attack_duration: float = 4.0
@export var retreat_duration: float = 1.5
@export var shoot_interval: float = 0.75
@export var enemy_bullet_speed: float = 22.0
@export var retreat_distance: float = 4.0
@export var attack_sway_distance: float = 2.5
@export var bullet_scene: PackedScene = preload("res://scenes/bullet.tscn")
@export var explosion_scene: PackedScene = preload("res://scenes/explosion.tscn")

@onready var body_mesh: MeshInstance3D = $Body
@onready var core_mesh: MeshInstance3D = $Core
@onready var muzzle: Node3D = $Muzzle
@onready var hitbox_phase_1: Area3D = $HitboxPhase1
@onready var hitbox_phase_2: Area3D = $HitboxPhase2
@onready var shape_phase_1: CollisionShape3D = $HitboxPhase1/CollisionShape3D
@onready var shape_phase_2: CollisionShape3D = $HitboxPhase2/CollisionShape3D

var current_state: State = State.IDLE
var hp: int = 20
var _phase_two_enabled: bool = false
var _state_timer: float = 0.0
var _shoot_timer: float = 0.0
var _active_tween: Tween
var _death_started: bool = false


func _ready() -> void:
	add_to_group("boss")
	hp = max_hp
	_prepare_hitbox(hitbox_phase_1)
	_prepare_hitbox(hitbox_phase_2)
	_set_phase_two_enabled(false)
	_enter_state(State.IDLE)
	print("Boss gotowy. HP = ", hp, "/", max_hp)


func _process(delta: float) -> void:
	match current_state:
		State.IDLE:
			_process_idle(delta)
		State.ATTACK:
			_process_attack(delta)
		State.RETREAT:
			_process_retreat(delta)
		State.DEATH:
			pass


func take_hit(damage: int) -> void:
	if current_state == State.DEATH or _death_started:
		return

	hp -= damage
	hp = maxi(hp, 0)
	print("Boss trafiony za ", damage, ". HP = ", hp, "/", max_hp)
	_flash_hit_color()

	if hp <= 0:
		_enter_state(State.DEATH)
		return

	if not _phase_two_enabled and hp <= int(max_hp * PHASE_TWO_RATIO):
		_set_phase_two_enabled(true)
		print("Boss przechodzi do fazy 2: mniejszy hitbox, większe obrażenia per trafienie.")


func _enter_state(new_state: State) -> void:
	if current_state == State.DEATH and new_state != State.DEATH:
		return

	current_state = new_state
	_state_timer = 0.0

	if _active_tween != null and _active_tween.is_valid():
		_active_tween.kill()

	match current_state:
		State.IDLE:
			_start_idle()
		State.ATTACK:
			_start_attack()
		State.RETREAT:
			_start_retreat()
		State.DEATH:
			_start_death()


func _start_idle() -> void:
	_shoot_timer = shoot_interval
	print("Boss FSM: IDLE")


func _start_attack() -> void:
	_shoot_timer = 0.15
	print("Boss FSM: ATTACK")
	_active_tween = create_tween()
	_active_tween.set_trans(Tween.TRANS_SINE)
	_active_tween.set_ease(Tween.EASE_IN_OUT)
	_active_tween.tween_property(self, "position:x", position.x + attack_sway_distance, attack_duration * 0.5)
	_active_tween.tween_property(self, "position:x", position.x - attack_sway_distance, attack_duration * 0.5)


func _start_retreat() -> void:
	print("Boss FSM: RETREAT")
	_active_tween = create_tween()
	_active_tween.set_trans(Tween.TRANS_SINE)
	_active_tween.set_ease(Tween.EASE_IN_OUT)
	_active_tween.tween_property(self, "position:z", position.z - retreat_distance, retreat_duration * 0.5)
	_active_tween.tween_property(self, "position:z", position.z + retreat_distance, retreat_duration * 0.5)


func _start_death() -> void:
	if _death_started:
		return

	_death_started = true
	print("Boss FSM: DEATH")
	_spawn_explosion()
	GameManager.add_score(SCORE_FOR_BOSS)
	died.emit()
	queue_free()


func _process_idle(delta: float) -> void:
	_state_timer += delta
	if _state_timer >= idle_duration:
		_enter_state(State.ATTACK)


func _process_attack(delta: float) -> void:
	_state_timer += delta
	_shoot_timer -= delta

	if _shoot_timer <= 0.0:
		_shoot_timer = shoot_interval
		_shoot_at_player()

	if _state_timer >= attack_duration:
		_enter_state(State.RETREAT)


func _process_retreat(delta: float) -> void:
	_state_timer += delta
	if _state_timer >= retreat_duration:
		_enter_state(State.ATTACK)


func _prepare_hitbox(hitbox: Area3D) -> void:
	hitbox.add_to_group("enemy_hitboxes")
	hitbox.collision_layer = 2
	hitbox.collision_mask = 5
	hitbox.monitoring = true
	hitbox.monitorable = true
	hitbox.area_entered.connect(_on_hitbox_area_entered)


func _set_phase_two_enabled(enabled: bool) -> void:
	_phase_two_enabled = enabled
	shape_phase_1.disabled = enabled
	shape_phase_2.disabled = not enabled
	hitbox_phase_1.monitoring = not enabled
	hitbox_phase_2.monitoring = enabled

	if enabled:
		_set_boss_color(Color(1.0, 0.25, 0.1, 1.0))
	else:
		_set_boss_color(Color(0.25, 0.85, 1.0, 1.0))


func _on_hitbox_area_entered(area: Area3D) -> void:
	if not area.is_in_group("player_bullets"):
		return

	if area.has_method("destroy"):
		area.destroy()

	if _phase_two_enabled:
		take_hit(2)
	else:
		take_hit(1)


func _shoot_at_player() -> void:
	if bullet_scene == null:
		return

	var player := _get_player_node()
	if player == null:
		return

	var direction_to_player := player.global_position - muzzle.global_position
	if direction_to_player.length() <= MIN_SHOOT_VECTOR_LENGTH:
		return

	var bullet := bullet_scene.instantiate() as Area3D
	if bullet == null:
		return

	get_tree().current_scene.add_child(bullet)

	if bullet.has_method("setup"):
		bullet.setup(muzzle.global_position, direction_to_player.normalized(), "enemy")
		bullet.speed = enemy_bullet_speed
	else:
		bullet.global_position = muzzle.global_position


func _get_player_node() -> Node3D:
	var players := get_tree().get_nodes_in_group("player")
	if players.is_empty():
		return null
	return players[0] as Node3D


func _spawn_explosion() -> void:
	if explosion_scene == null:
		return

	var explosion := explosion_scene.instantiate() as Node3D
	if explosion == null:
		return

	get_tree().current_scene.add_child(explosion)
	explosion.global_position = global_position
	explosion.scale = Vector3(1.8, 1.8, 1.8)


func _flash_hit_color() -> void:
	var hit_material := StandardMaterial3D.new()
	hit_material.albedo_color = Color(1.0, 1.0, 1.0, 1.0)
	hit_material.emission_enabled = true
	hit_material.emission = Color(1.0, 0.8, 0.3, 1.0)
	hit_material.emission_energy_multiplier = 1.0
	body_mesh.material_override = hit_material
	core_mesh.material_override = hit_material

	await get_tree().create_timer(0.06).timeout

	if is_instance_valid(self) and current_state != State.DEATH:
		if _phase_two_enabled:
			_set_boss_color(Color(1.0, 0.25, 0.1, 1.0))
		else:
			_set_boss_color(Color(0.25, 0.85, 1.0, 1.0))


func _set_boss_color(color: Color) -> void:
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.emission_enabled = true
	material.emission = color
	material.emission_energy_multiplier = 0.45
	body_mesh.material_override = material
	core_mesh.material_override = material
