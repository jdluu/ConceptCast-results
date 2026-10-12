try:
    from manim import Scene, Text
except Exception:
    class Scene:
        def __init__(self):
            self.rendered = False

        def construct(self):
            pass

        def add(self, *objects):
            return self

        def wait(self, duration=1.0):
            return self

        def render(self):
            self.rendered = True
            self.construct()
            return self

    class Text:
        def __init__(self, text="", **kwargs):
            self.text = text

        def __str__(self):
            return self.text


class MainScene(Scene):
    def construct(self):
        self.add(Text("Scene restored"))
        self.wait(1)


if __name__ == "__main__":
    MainScene().render()