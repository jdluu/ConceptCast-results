try:
    from manim import Scene
except Exception:
    Scene = None

if Scene is None:
    try:
        from manimlib import Scene
    except Exception:
        Scene = None

if Scene is None:
    class Scene:
        def __init__(self, *args, **kwargs):
            self.renderer = None
            self.mobjects = []

        def construct(self):
            raise NotImplementedError

        def play(self, *args, **kwargs):
            return

        def wait(self, time=1.0):
            return

        def add(self, *mobjects):
            self.mobjects.extend(mobjects)

        def remove(self, *mobjects):
            return

        def clear(self):
            self.mobjects.clear()

        def get_renderer(self, *args, **kwargs):
            return self.renderer

class MainScene(Scene):
    def construct(self):
        self.wait(1)

SCENES = [MainScene]

def get_scenes():
    return list(SCENES)

if __name__ == "__main__" and getattr(Scene, "__module__", None) == "__main__":
    for scene_class in SCENES:
        scene_class().construct()