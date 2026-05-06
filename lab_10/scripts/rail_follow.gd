extends PathFollow3D

# ============================================================
# LAB 09/10 - RUCH PO SZYNIE, WERSJA ODPORNA NA BŁĘDY
# ============================================================
# Ten skrypt jest przypięty do RailFollow.
# Jeżeli RailPath nie ma poprawnej krzywej, skrypt tworzy ją sam.
# Dzięki temu PathFollow3D ma po czym jechać.
# ============================================================

@export var rail_speed: float = 8.0
@export var loop_rail: bool = true
@export var debug_print: bool = true

var _print_timer: float = 0.0


func _ready() -> void:
	var path_node := get_parent() as Path3D

	if path_node == null:
		push_error("BŁĄD: RailFollow musi być dzieckiem Path3D.")
		return

	# Jeżeli Path3D nie ma krzywej albo krzywa ma długość 0,
	# tworzymy prostą trasę automatycznie.
	if path_node.curve == null or path_node.curve.get_baked_length() <= 0.01:
		print("RailPath miał pustą krzywą. Tworzę prostą ścieżkę automatycznie.")

		var new_curve := Curve3D.new()
		new_curve.add_point(Vector3(0, 0, 0))
		new_curve.add_point(Vector3(0, 0, -20))
		new_curve.add_point(Vector3(4, 0, -40))
		new_curve.add_point(Vector3(-4, 1, -60))
		new_curve.add_point(Vector3(0, 0, -80))

		path_node.curve = new_curve

	progress = 0.0

	print("Długość ścieżki Path3D = ", path_node.curve.get_baked_length())
	print("Rail speed = ", rail_speed)


func _process(delta: float) -> void:
	# Jeżeli w Inspectorze przypadkiem zostało 0,
	# wymuszamy bezpieczną prędkość testową.
	if rail_speed <= 0.0:
		rail_speed = 8.0

	progress += rail_speed * delta

	var path_node := get_parent() as Path3D

	if loop_rail and path_node != null and path_node.curve != null:
		var path_length := path_node.curve.get_baked_length()

		if path_length > 0.01 and progress >= path_length:
			progress = 0.0

	if debug_print:
		_print_timer += delta
		if _print_timer >= 1.0:
			_print_timer = 0.0
			print("RailFollow progress = ", progress)
