extends Area3D

# ============================================================
# LABORATORIUM 10 - POCISK 3D
# ============================================================
# Ten skrypt jest przypięty do sceny bullet.tscn.
# Korzeniem sceny pocisku jest Area3D, bo pocisk ma wykrywać
# wejście w obszar celu, ale nie musi fizycznie blokować ruchu.
#
# Najważniejsze elementy:
# - pocisk jest tworzony przez statek jako osobna instancja sceny,
# - porusza się w kierunku, w którym patrzył statek w chwili strzału,
# - po czasie lifetime usuwa się przez queue_free(),
# - po trafieniu celu również zostaje usunięty,
# - należy do grupy "player_bullets", żeby cel mógł łatwo sprawdzić,
#   czy wszedł w niego pocisk gracza.
# ============================================================

signal removed(bullet: Area3D)

# Prędkość pocisku w jednostkach Godot na sekundę.
# @export pozwala zmienić wartość w inspektorze bez edycji kodu.
@export var speed: float = 30.0

# Czas życia pocisku. Po tym czasie pocisk sam znika,
# żeby w drzewie sceny nie zostawały niepotrzebne obiekty.
@export var lifetime: float = 3.0

# Kierunek lotu w przestrzeni globalnej.
# Vector3.FORWARD w Godot oznacza (0, 0, -1).
var direction: Vector3 = Vector3.FORWARD

# Flaga zabezpieczająca przed wielokrotnym queue_free().
# Przy szybkich kolizjach kilka sygnałów może pojawić się prawie naraz.
var _is_destroyed: bool = false


func _ready() -> void:
    # Grupa jest prostym sposobem identyfikacji obiektu.
    # Target sprawdza area.is_in_group("player_bullets").
    add_to_group("player_bullets")

    # Warstwa 3 = bit 3, czyli wartość 4.
    # Maska 2 = pocisk skanuje obiekty na warstwie 2, czyli cele.
    collision_layer = 4
    collision_mask = 2

    monitoring = true
    monitorable = true

    # Możemy też reagować po stronie pocisku.
    # Cel i tak usuwa się sam, ale pocisk po wejściu w target znika od razu.
    area_entered.connect(_on_area_entered)


func setup(start_transform: Transform3D) -> void:
    # Funkcja wywoływana przez statek zaraz po utworzeniu pocisku.
    # Przekazujemy globalny transform wylotu lufy / nosa statku.
    global_transform = start_transform

    # W Godot lokalny kierunek "do przodu" dla obiektów 3D to -Z.
    # global_transform.basis.z wskazuje lokalny +Z,
    # dlatego bierzemy minus tej osi.
    direction = -global_transform.basis.z.normalized()


func _process(delta: float) -> void:
    # Pocisk porusza się w przestrzeni globalnej.
    # To ważne, bo nie jest dzieckiem PathFollow3D.
    # Gdyby był dzieckiem szyny, dziedziczyłby jej ruch i logika strzału
    # byłaby mniej czytelna.
    global_position += direction * speed * delta

    lifetime -= delta
    if lifetime <= 0.0:
        destroy()


func destroy() -> void:
    # Jedno wspólne miejsce niszczenia pocisku.
    # Dzięki temu trafienie i koniec czasu życia robią to samo.
    if _is_destroyed:
        return

    _is_destroyed = true
    removed.emit(self)
    queue_free()


func _on_area_entered(area: Area3D) -> void:
    # Jeżeli pocisk dotknie celu, znika.
    # Sam cel ma własny skrypt target.gd i tam obsługuje punktację.
    if area.is_in_group("targets") or area.get_parent().is_in_group("targets"):
        destroy()
