from manim import *
import numpy as np

class SineWaveScene(Scene):
    def construct(self):
        # Title
        title = Text("Sine Wave Animation", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Axes
        axes = Axes(
            x_range=[-4 * np.pi, 4 * np.pi, np.pi],
            y_range=[-2, 2, 1],
            x_length=12,
            y_length=5,
            axis_config={"include_numbers": False, "include_tip": False},
        ).shift(DOWN * 0.3)
        self.play(Create(axes))

        # Sine curve
        sine_curve = axes.plot(lambda x: np.sin(x), color=YELLOW)
        self.play(Create(sine_curve), run_time=3)

        # Moving dot
        dot = Dot(color=RED).move_to(axes.c2p(-4 * np.pi, np.sin(-4 * np.pi)))
        self.play(FadeIn(dot))

        # Tracing the curve with the dot
        self.play(MoveAlongPath(dot, sine_curve), run_time=5, rate_func=linear)

        # Closing
        self.wait(1)
        self.play(FadeOut(dot), FadeOut(sine_curve), FadeOut(axes), FadeOut(title))
        self.wait()
