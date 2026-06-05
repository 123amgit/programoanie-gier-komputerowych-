# audio_manager.py
# Prosty manager dźwięków. Działa nawet wtedy, gdy pliki dźwiękowe nie istnieją.

from pathlib import Path
import pyray as pr


class AudioManager:
    def __init__(self) -> None:
        self.sounds = {}
        self.enabled = False

    def load(self) -> None:
        """
        Ładuje dźwięki z katalogu assets/sounds.
        Jeśli pliki nie istnieją, gra działa dalej bez dźwięków.
        """
        try:
            pr.init_audio_device()
            self.enabled = True
        except Exception:
            self.enabled = False
            return

        sound_paths = {
            "pickup": "assets/sounds/pickup.wav",
            "deliver": "assets/sounds/deliver.wav",
            "hit": "assets/sounds/hit.wav",
            "win": "assets/sounds/win.wav",
        }

        for name, path in sound_paths.items():
            file_path = Path(path)

            if file_path.exists():
                try:
                    self.sounds[name] = pr.load_sound(str(file_path))
                except Exception:
                    pass

    def play(self, name: str) -> None:
        if not self.enabled:
            return

        sound = self.sounds.get(name)

        if sound is not None:
            try:
                pr.play_sound(sound)
            except Exception:
                pass

    def unload(self) -> None:
        if not self.enabled:
            return

        for sound in self.sounds.values():
            try:
                pr.unload_sound(sound)
            except Exception:
                pass

        try:
            pr.close_audio_device()
        except Exception:
            pass
