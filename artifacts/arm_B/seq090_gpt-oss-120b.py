from manim import *
import numpy as np


class SceneGen(Scene):
    def construct(self):
        # -------------------------------------------------
        # Scene 1 – Stationary source and observer, wavefronts
        # -------------------------------------------------
        source = Dot(LEFT * 3, color=RED)
        observer = Dot(RIGHT * 3, color=BLUE)
        label_source = Text("Source", font_size=24).next_to(source, DOWN)
        label_observer = Text("Observer", font_size=24).next_to(observer, DOWN)

        self.play(FadeIn(source), FadeIn(observer))
        self.play(Write(label_source), Write(label_observer))

        # first wavefront
        wave1 = Circle(radius=0.5, color=YELLOW).move_to(source.get_center())
        self.play(Create(wave1))
        self.play(
            wave1.animate.set_width(6).set_stroke(width=2),
            run_time=2,
        )
        # second wavefront
        wave2 = Circle(radius=0.5, color=YELLOW).move_to(source.get_center())
        self.play(Create(wave2))
        self.play(
            wave2.animate.set_width(6).set_stroke(width=2),
            run_time=2,
        )
        self.wait(1)

        self.clear()

        # -------------------------------------------------
        # Scene 2 – Moving source, stationary observer
        # -------------------------------------------------
        source = Dot(LEFT * 4, color=RED)
        observer = Dot(RIGHT * 3, color=BLUE)
        label_source = Text("Moving Source", font_size=24).next_to(source, DOWN)
        label_observer = Text("Observer", font_size=24).next_to(observer, DOWN)
        source_arrow = Arrow(LEFT, RIGHT, buff=0).next_to(source, RIGHT, buff=0.2)

        self.play(FadeIn(source), FadeIn(observer))
        self.play(Write(label_source), Write(label_observer), FadeIn(source_arrow))

        # emit three wavefronts while source moves right
        for i in range(3):
            wave = Circle(radius=0.5, color=YELLOW).move_to(source.get_center())
            self.play(Create(wave))
            self.play(
                wave.animate.set_width(5 - i).set_stroke(width=2),
                run_time=1.5,
            )
            self.play(source.animate.shift(RIGHT * 2), run_time=1.5)

        self.wait(1)
        self.clear()

        # -------------------------------------------------
        # Scene 3 – Stationary source, moving observer
        # -------------------------------------------------
        source = Dot(LEFT * 3, color=RED)
        observer = Dot(RIGHT * 4, color=BLUE)
        label_source = Text("Source", font_size=24).next_to(source, DOWN)
        label_observer = Text("Moving Observer", font_size=24).next_to(observer, DOWN)
        observer_arrow = Arrow(RIGHT, LEFT, buff=0).next_to(observer, LEFT, buff=0.2)

        self.play(FadeIn(source), FadeIn(observer))
        self.play(Write(label_source), Write(label_observer), FadeIn(observer_arrow))

        # emit three wavefronts while observer moves left
        for i in range(3):
            wave = Circle(radius=0.5, color=YELLOW).move_to(source.get_center())
            self.play(Create(wave))
            self.play(
                wave.animate.set_width(5 - i).set_stroke(width=2),
                run_time=1.5,
            )
            self.play(observer.animate.shift(LEFT * 2), run_time=1.5)

        self.wait(1)
        self.clear()

        # -------------------------------------------------
        # Scene 4 – Both source and observer moving
        # -------------------------------------------------
        source = Dot(LEFT * 4, color=RED)
        observer = Dot(RIGHT * 4, color=BLUE)
        label_source = Text("Source →", font_size=24).next_to(source, DOWN)
        label_observer = Text("Observer ←", font_size=24).next_to(observer, DOWN)
        # Use arrows of non‑zero length to indicate motion direction.
        source_arrow = Arrow(LEFT, RIGHT, buff=0).next_to(source, RIGHT, buff=0.2)
        observer_arrow = Arrow(RIGHT, LEFT, buff=0).next_to(observer, LEFT, buff=0.2)

        self.play(FadeIn(source), FadeIn(observer))
        self.play(Write(label_source), Write(label_observer))
        self.play(FadeIn(source_arrow), FadeIn(observer_arrow))

        # simultaneous motion with wave emission
        for i in range(3):
            wave = Circle(radius=0.5, color=YELLOW).move_to(source.get_center())
            self.play(Create(wave))
            self.play(
                wave.animate.set_width(5 - i).set_stroke(width=2),
                run_time=1.2,
            )
            self.play(
                source.animate.shift(RIGHT * 2),
                observer.animate.shift(LEFT * 2),
                run_time=1.2,
            )

        self.wait(1)
        self.clear()

        # -------------------------------------------------
        # Scene 5 – Frequency change visualised on a graph
        # -------------------------------------------------
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": WHITE},
        )
        axes_labels = axes.get_axis_labels(x_label="t", y_label="Amplitude")
        self.play(Create(axes), Write(axes_labels))

        # stationary source frequency
        f0 = 1
        wave0 = axes.plot(lambda x: np.sin(2 * PI * f0 * x), color=YELLOW)
        self.play(Create(wave0), run_time=2)

        # Doppler shifted frequency (higher)
        f_high = 1.5
        wave_high = axes.plot(lambda x: np.sin(2 * PI * f_high * x), color=RED)
        self.play(Transform(wave0, wave_high), run_time=2)

        # Doppler shifted frequency (lower)
        f_low = 0.6
        wave_low = axes.plot(lambda x: np.sin(2 * PI * f_low * x), color=BLUE)
        self.play(Transform(wave0, wave_low), run_time=2)

        self.wait(1)
        self.clear()

        # -------------------------------------------------
        # Scene 6 – Summary and formula
        # -------------------------------------------------
        title = Text("Doppler Effect", font_size=48).to_edge(UP)
        formula = MathTex(
            r"f' = f\\,\\frac{v \pm v_o}{v \pm v_s}",
            tex_to_color_map={
                "f'": YELLOW,
                "f": YELLOW,
                "v": GREEN,
                "v_o": BLUE,
                "v_s": RED,
            },
        ).scale(1.2)

        bullet_points = VGroup(
            Text("• Source moving → compresses waves ahead", font_size=24),
            Text("• Observer moving → perceives waves faster/slower", font_size=24),
            Text("• Relative motion changes observed frequency", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.8)

        self.play(FadeIn(title))
        self.play(Write(bullet_points[0]))
        self.play(Write(bullet_points[1]))
        self.play(Write(bullet_points[2]))
        self.play(Write(formula))
        self.wait(2)
