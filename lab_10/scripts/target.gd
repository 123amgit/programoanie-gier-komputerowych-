extends Node3D

# ============================================================
# LABORATORIUM 10 - CEL DO ZESTRZELENIA
# ============================================================
# Ten skrypt jest przypięty do sceny target.tscn.
# Target jest zwykłym Node3D z modelem oraz dzieckiem Area3D.
# Area3D pełni funkcję hitboxa, czyli obszaru trafienia.
#
# Sygnał area_entered jest podłączany w kodzie w funkcji _ready(),
# zgodnie z wymaganiami laboratorium. Dzięki temu połączenia sygnałów
# są widoczne w skrypcie, a nie ukryte tylko w edytorze.
# ============================================================

signal target_destroyed(points: int)

# Liczba punktów za zniszczenie tego celu.
# Można ją zmienić w inspektorze dla każdej instancji celu.
@export var points: int = 100

# Czy po trafieniu cel ma przez chwilę zmienić kolor.
# To jest mały efekt dodatkowy, ale bezpieczny i prosty.
@export var flash_on_hit: bool = true

@onready var hitbox: Area3D = $Area3D
@onready var mesh: MeshInstance3D = $MeshInstance3D

var _already_hit: bool = false


func _ready() -> void:
    add_to_group("targets")

    # Dodajemy do grupy również hitbox, bo sygnał area_entered
    # przekazuje Area3D, a nie cały Node3D celu.
    hitbox.add_to_group("targets")

    # Warstwa 2 = wartość 2. To jest warstwa wrogów / celów.
    # Maska 3 = wartość 4. Cel skanuje pociski gracza.
    hitbox.collision_layer = 2
    hitbox.collision_mask = 4
    hitbox.monitoring = true
    hitbox.monitorable = true

    # Połączenie sygnału w kodzie.
    # Gdy jakiekolwiek Area3D wejdzie w hitbox celu,
    # Godot wywoła funkcję _on_area_entered.
    hitbox.area_entered.connect(_on_area_entered)


func _on_area_entered(area: Area3D) -> void:
    if _already_hit:
        return

    if not area.is_in_group("player_bullets"):
        return

    _already_hit = true

    print("Trafiony cel: ", name, "  +", points, " pkt")
    target_destroyed.emit(points)

    # Jeżeli pocisk ma metodę destroy(), prosimy go o usunięcie.
    # Sprawdzenie has_method zabezpiecza przed błędem, gdyby weszło inne Area3D.
    if area.has_method("destroy"):
        area.destroy()

    if flash_on_hit:
        await _flash_red()

    queue_free()


func _flash_red() -> void:
    # Prosty efekt trafienia: cel przez ułamek sekundy robi się czerwony.
    # Materiał tworzymy lokalnie, żeby nie zmienić wszystkich celów naraz.
    var material := StandardMaterial3D.new()
    material.albedo_color = Color.RED
    mesh.material_override = material

    await get_tree().create_timer(0.1).timeout
