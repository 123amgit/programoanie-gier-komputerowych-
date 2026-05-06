extends Node3D

# ============================================================
# LABORATORIUM 10 - STATEK GRACZA
# ============================================================
# Statek jest dzieckiem PathFollow3D, więc automatycznie porusza się
# po szynie razem z kamerą. Ten skrypt odpowiada tylko za:
# - lokalne sterowanie w płaszczyźnie X/Y,
# - ograniczenie ruchu funkcją clamp(),
# - strzelanie pociskami przez instantiate(),
# - cooldown strzału.
# ============================================================

# Scena pocisku. W inspektorze można przeciągnąć bullet.tscn,
# ale daję też domyślny preload, żeby projekt działał od razu.
@export var bullet_scene: PackedScene = preload("res://scenes/bullet.tscn")

# Prędkość ruchu statku w lokalnej płaszczyźnie XY.
@export var move_speed: float = 8.0

# Granice manewrowania. Statek nie powinien wypadać z kadru.
@export var limit_x: float = 5.0
@export var limit_y: float = 3.0

# Minimalny odstęp między strzałami.
# Dzięki temu przy trzymaniu spacji nie tworzymy setek pocisków na sekundę.
@export var shoot_cooldown_time: float = 0.30

# Opcjonalny limit aktywnych pocisków. Jest to zadanie dodatkowe,
# ale przydaje się też do porządku w scenie.
@export var max_active_bullets: int = 5

@onready var muzzle: Node3D = $Nose
@onready var player_hitbox: Area3D = $PlayerHitbox

var _shoot_cooldown: float = 0.0
var _active_bullets: Array[Area3D] = []


func _ready() -> void:
    # Gracz ma warstwę 1 i maskę 2 zgodnie z tabelą z laboratorium.
    # W tym laboratorium pocisk gracza nie powinien zderzać się ze statkiem.
    player_hitbox.collision_layer = 1
    player_hitbox.collision_mask = 2
    player_hitbox.monitoring = true
    player_hitbox.monitorable = true


func _process(delta: float) -> void:
    _handle_movement(delta)
    _handle_shooting(delta)
    _clean_bullet_list()


func _handle_movement(delta: float) -> void:
    # Input.get_axis zwraca:
    # -1, gdy naciskamy pierwszy kierunek,
    #  1, gdy naciskamy drugi kierunek,
    #  0, gdy nie ma ruchu albo kierunki się znoszą.
    var input_x := Input.get_axis("ui_left", "ui_right")
    var input_y := Input.get_axis("ui_down", "ui_up")

    position.x += input_x * move_speed * delta
    position.y += input_y * move_speed * delta

    # clamp() ogranicza statek do prostokątnej strefy manewru.
    # To jest jeden z głównych wymogów Lab 09/10.
    position.x = clamp(position.x, -limit_x, limit_x)
    position.y = clamp(position.y, -limit_y, limit_y)


func _handle_shooting(delta: float) -> void:
    if _shoot_cooldown > 0.0:
        _shoot_cooldown -= delta

    # Używam is_action_pressed zamiast is_action_just_pressed,
    # ponieważ wtedy cooldown naprawdę kontroluje tempo serii strzałów.
    # Jeżeli prowadzący woli jeden strzał na klik, można zmienić na:
    # Input.is_action_just_pressed("ui_accept")
    if Input.is_action_pressed("ui_accept") and _shoot_cooldown <= 0.0:
        _shoot()


func _shoot() -> void:
    if bullet_scene == null:
        push_warning("Brak przypisanej sceny bullet_scene w PlayerShip.")
        return

    if _active_bullets.size() >= max_active_bullets:
        # Limit aktywnych pocisków jest zadaniem dodatkowym.
        # Nie jest błędem, tylko celowym ograniczeniem.
        return

    var bullet := bullet_scene.instantiate() as Area3D

    # Pocisk dodajemy do aktualnej sceny, a nie jako dziecko statku.
    # Wtedy po wystrzeleniu żyje własnym ruchem w przestrzeni globalnej.
    get_tree().current_scene.add_child(bullet)

    if bullet.has_method("setup"):
        bullet.setup(muzzle.global_transform)
    else:
        bullet.global_transform = muzzle.global_transform

    if bullet.has_signal("removed"):
        bullet.removed.connect(_on_bullet_removed)

    _active_bullets.append(bullet)
    _shoot_cooldown = shoot_cooldown_time

    print("Strzał. Aktywne pociski: ", _active_bullets.size())


func _on_bullet_removed(bullet: Area3D) -> void:
    _active_bullets.erase(bullet)


func _clean_bullet_list() -> void:
    # Zabezpieczenie: gdyby pocisk został usunięty bez sygnału,
    # lista i tak zostanie posprzątana.
    _active_bullets = _active_bullets.filter(func(bullet): return is_instance_valid(bullet))
