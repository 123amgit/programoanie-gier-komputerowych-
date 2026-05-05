extends PathFollow3D

# ============================================================
# LABORATORIUM 09 - SKRYPT SZYNY
# ============================================================
# Ten skrypt jest podpięty do węzła PathFollow3D.
# PathFollow3D porusza się po ścieżce Path3D.
# Jeżeli kamera i statek są dziećmi PathFollow3D,
# to automatycznie lecą razem z nim.
#
# Najważniejsza idea:
# - Path3D przechowuje kształt trasy,
# - PathFollow3D ma parametr progress_ratio od 0.0 do 1.0,
# - zwiększanie progress_ratio przesuwa obiekt po trasie.
# ============================================================

# Prędkość szyny jako zmienna eksportowana.
# Dzięki @export wartość można zmieniać w inspektorze Godot,
# bez edytowania kodu.
@export var rail_speed: float = 0.075

# Czy po dojściu do końca trasy obiekt ma wrócić na początek.
# W podstawowym laboratorium można zostawić false,
# ale true jest wygodne do testowania sceny.
@export var loop_track: bool = true

func _ready() -> void:
	# Ustawienie początkowego punktu na szynie.
	# 0.0 oznacza początek ścieżki, 1.0 oznacza koniec.
	progress_ratio = 0.0

	# W Godot PathFollow3D ma własną właściwość loop.
	# Dodatkowo korzystamy ze zmiennej loop_track,
	# żeby dało się łatwo przełączać zachowanie z inspektora.
	loop = loop_track

func _process(delta: float) -> void:
	# delta to czas od poprzedniej klatki.
	# Mnożenie przez delta sprawia, że ruch nie zależy od FPS.
	progress_ratio += rail_speed * delta

	# Jeżeli pętla jest włączona, wracamy na początek trasy.
	# Jeżeli pętla jest wyłączona, zatrzymujemy się na końcu.
	if progress_ratio >= 1.0:
		if loop_track:
			progress_ratio = 0.0
		else:
			progress_ratio = 1.0
