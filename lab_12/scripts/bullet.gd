extends Area3D

# ============================================================
# LABORATORIUM 11 - POCISK UNIWERSALNY 3D
# ============================================================
# W Lab 10 pocisk był pociskiem gracza lecącym głównie do przodu.
# W Lab 11 ten sam skrypt obsługuje dwa rodzaje pocisków:
# - pocisk gracza, który trafia wrogów,
# - pocisk wroga, który trafia gracza.
#
# To spełnia wymaganie "pocisk uniwersalny": nie tworzymy dwóch różnych
# skryptów dla pocisku gracza i przeciwnika. Różnica wynika z pola bullet_kind
# oraz z ustawionych warstw kolizji.
# ============================================================

signal removed(bullet: Area3D)

@export var speed: float = 30.0
@export var lifetime: float = 3.0

# Kierunek lotu w przestrzeni globalnej. Musi być znormalizowany.
# Dla gracza zwykle będzie to Vector3.FORWARD, czyli (0, 0, -1).
# Dla wroga jest to wektor od wroga do gracza.
@export var direction: Vector3 = Vector3.FORWARD

# "player" = pocisk gracza, layer 3, mask 2.
# "enemy"  = pocisk wroga, layer 4, mask 1.
@export var bullet_kind: String = "player"

var _is_destroyed: bool = false


func _ready() -> void:
	_apply_kind_settings()
	area_entered.connect(_on_area_entered)


func setup(start_position: Vector3, bullet_direction: Vector3, kind: String = "player") -> void:
	# Funkcja wywoływana tuż po instantiate().
	# Ustawia pozycję startową, kierunek oraz typ pocisku.
	global_position = start_position
	bullet_kind = kind

	if bullet_direction.length() > 0.001:
		direction = bullet_direction.normalized()
	else:
		direction = Vector3.FORWARD

	_apply_kind_settings()


func _apply_kind_settings() -> void:
	# Wartości bitowe warstw Godot:
	# Layer 1 = 1, Layer 2 = 2, Layer 3 = 4, Layer 4 = 8.
	# Laboratorium opisuje numery warstw, a Godot zapisuje je jako bity.
	if bullet_kind == "enemy":
		add_to_group("enemy_bullets")
		remove_from_group("player_bullets")
		collision_layer = 8      # warstwa 4
		collision_mask = 1       # widzi gracza na warstwie 1
	else:
		add_to_group("player_bullets")
		remove_from_group("enemy_bullets")
		collision_layer = 4      # warstwa 3
		collision_mask = 2       # widzi wrogów na warstwie 2

	monitoring = true
	monitorable = true


func _process(delta: float) -> void:
	global_position += direction * speed * delta

	lifetime -= delta
	if lifetime <= 0.0:
		destroy()


func destroy() -> void:
	if _is_destroyed:
		return

	_is_destroyed = true
	removed.emit(self)
	queue_free()


func _on_area_entered(area: Area3D) -> void:
	# Pocisk gracza znika po dotknięciu hitboxa wroga.
	if bullet_kind == "player" and area.is_in_group("enemy_hitboxes"):
		destroy()
		return

	# Pocisk wroga znika po dotknięciu hitboxa gracza.
	if bullet_kind == "enemy" and area.is_in_group("player_hitboxes"):
		destroy()
		return
