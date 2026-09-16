from manim import *


class SceneGen(Scene):
    """The single scene the renderer expects, named exactly 'SceneGen'.

    The previous script contained no scene classes (only an empty SCENES
    list), so no scenes were dropped. This adds the exactly-one Scene
    subclass named SceneGen that validation requires.
    """

    def construct(self):
        title = Text("SceneGen")
        title.scale(1.2)
        self.play(Write(title))
        self.wait(1)
