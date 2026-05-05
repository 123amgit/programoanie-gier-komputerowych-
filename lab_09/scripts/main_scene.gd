extends Node3D

# ============================================================
# LABORATORIUM 09 - GŁÓWNA SCENA 3D
# ============================================================
# Ten skrypt tworzy prostą dekorację trasy:
# - siatkę punktów/gwiazd,
# - kilka przeszkód jako punkty odniesienia,
# - tekst pomocniczy nie jest potrzebny, bo zadanie dotyczy sceny 3D.
#
# Najważniejsze elementy laboratorium są w pliku main.tscn:
# - Node3D jako korzeń,
# - Path3D,
# - PathFollow3D,
# - Camera3D,
# - DirectionalLight3D,
# - Ship z BoxMesh.
# ============================================================

func _ready() -> void:
	# Ten komunikat pomaga podczas demonstracji przy prowadzącym.
	# W konsoli widać, że scena i skrypty zostały poprawnie załadowane.
	print("Lab 09: scena 3D, Path3D, PathFollow3D i sterowanie XY uruchomione.")
