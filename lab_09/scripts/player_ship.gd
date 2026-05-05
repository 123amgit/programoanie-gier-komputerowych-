extends Node3D

# ============================================================
# LABORATORIUM 09 - STEROWANIE STATKIEM W PŁASZCZYŹNIE XY
# ============================================================
# Ten skrypt jest podpięty do węzła Ship.
# Ship jest dzieckiem PathFollow3D.
#
# To oznacza, że statek ma dwa rodzaje ruchu:
# 1. Automatyczny lot do przodu razem z PathFollow3D.
# 2. Ręczne odchylenie w lewo/prawo/góra/dół przez zmianę
#    lokalnej pozycji position.x oraz position.y.
#
# Bardzo ważne:
# position jest pozycją lokalną względem rodzica.
# Rodzicem statku jest PathFollow3D, więc sterowanie XY działa
# jak przesuwanie statku przed kamerą, a nie jak ruch po świecie.
# ============================================================

# Prędkość ruchu bocznego statku.
@export var move_speed: float = 8.0

# Granice obszaru, w którym statek może się poruszać.
# clamp() nie pozwala mu wylecieć poza ekran/kadr kamery.
@export var limit_x: float = 4.0
@export var limit_y: float = 2.4

# Delikatne pochylenie wizualne statku przy ruchu na boki.
# Nie jest konieczne do zaliczenia, ale pokazuje, że input może
# wpływać nie tylko na pozycję, lecz także na wygląd obiektu.
@export var tilt_strength: float = 0.35

func _process(delta: float) -> void:
	var input_vector := Vector2.ZERO

	# Domyślne akcje ui_left/ui_right/ui_up/ui_down istnieją w Godot.
	# Dlatego nie trzeba ręcznie tworzyć Input Map dla podstawowego sterowania.
	if Input.is_action_pressed("ui_left"):
		input_vector.x -= 1.0
	if Input.is_action_pressed("ui_right"):
		input_vector.x += 1.0
	if Input.is_action_pressed("ui_up"):
		input_vector.y += 1.0
	if Input.is_action_pressed("ui_down"):
		input_vector.y -= 1.0

	# Normalizacja zapobiega szybszemu ruchowi po przekątnej.
	if input_vector.length() > 1.0:
		input_vector = input_vector.normalized()

	# Zmieniamy lokalną pozycję statku.
	position.x += input_vector.x * move_speed * delta
	position.y += input_vector.y * move_speed * delta

	# Ograniczamy strefę manewrowania.
	# To jest wymagany element laboratorium: clamp().
	position.x = clamp(position.x, -limit_x, limit_x)
	position.y = clamp(position.y, -limit_y, limit_y)

	# Prosta animacja pochylenia statku.
	# rotation.z odpowiada za przechył wokół osi Z.
	rotation.z = lerp(rotation.z, -input_vector.x * tilt_strength, 8.0 * delta)
