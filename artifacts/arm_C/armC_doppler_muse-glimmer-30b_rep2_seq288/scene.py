from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Wave trains have wavelength and frequency ---
        self.camera.background_color = "#181825"

        title_1 = Text(
            "Wave trains have wavelength and frequency",
            font="Sans",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        main_1 = Text(
            "Waves repeat in space and time.",
            font="Sans",
            font_size=48,
            color="#89b4fa",
        ).move_to(ORIGIN)

        wavelength_label = Text(
            "Wavelength = distance between peaks",
            font="Sans",
            font_size=28,
            color="#fab387",
        ).next_to(main_1, DOWN, buff=0.8)

        frequency_label = Text(
            "Frequency = repetitions per second",
            font="Sans",
            font_size=28,
            color="#f38ba8",
        ).next_to(wavelength_label, DOWN, buff=0.5)

        self.play(Write(title_1), run_time=2)
        self.wait(0.5)
        self.play(GrowFromCenter(main_1), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(wavelength_label), run_time=1)
        self.play(FadeIn(frequency_label), run_time=1)
        self.wait(1.5)
        # --- Scene 2: Step 2: Source emits periodic wavefronts ---
        self.camera.background_color = "#181825"

        # Title
        title = Text("Source emits periodic wavefronts", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Axes
        axes = Axes(x_range=[-3, 3], y_range=[-2, 2], x_length=6, y_length=4)
        axes.set_color("#fab387")
        axes.stroke_width = 2
        axes.move_to(ORIGIN)

        # Source
        source = Dot(point=ORIGIN, radius=0.08, color="#a6e3a1")
        source_label = Text("Source", font_size=24, color=WHITE)
        source_label.next_to(source, DOWN)

        # Wavefronts
        colors = ["#89b4fa", "#f38ba8", "#94e2d5"]
        circles = VGroup()
        for col in colors:
            c = Circle(radius=0.1, color=col, stroke_width=2)
            c.set_fill(col, opacity=0.15)
            circles.add(c)

        self.play(FadeIn(title), run_time=0.8)
        self.play(Create(axes), run_time=1.2)
        self.play(FadeIn(source), run_time=0.5)
        self.play(Write(source_label), run_time=0.5)
        self.play(GrowFromCenter(circles[0]), run_time=1.0)
        self.play(GrowFromCenter(circles[1]), run_time=1.0)
        self.play(GrowFromCenter(circles[2]), run_time=1.0)
        self.wait(1.0)
        # --- Scene 3: Step 3: Motion toward observer compresses wavelength ahead ---
        self.camera.background_color = "#181825"

        # Title
        title = Text(
            "Motion toward observer compresses wavelength ahead",
            font_size=36,
            color=WHITE,
        )
        title.move_to(UP * 3)
        self.play(Write(title), run_time=1.0)

        # Number line
        number_line = NumberLine(x_range=[-5, 5], length=10, color="#f38ba8")
        number_line.stroke_width = 2.0
        number_line.move_to(DOWN * 2)
        number_line.add_numbers()
        self.play(Create(number_line), run_time=1.5)

        # Observer and source
        observer_dot = Dot(point=number_line.n2p(4), radius=0.12, color="#a6e3a1")
        observer_label = Text("Observer", font_size=24, color=WHITE).next_to(
            observer_dot, UP
        )
        source_dot = Dot(point=number_line.n2p(0), radius=0.12, color="#fab387")
        source_label = Text("Source", font_size=24, color=WHITE).next_to(source_dot, UP)

        self.play(FadeIn(VGroup(observer_dot, observer_label)), run_time=0.8)
        self.play(FadeIn(VGroup(source_dot, source_label)), run_time=0.8)

        # Wavefronts behind (stretched)
        behind_positions = [-3, -2, -1]
        behind_dots = VGroup(
            *[
                Dot(point=number_line.n2p(x), radius=0.06, color="#94e2d5")
                for x in behind_positions
            ]
        )
        # Wavefronts ahead (compressed)
        ahead_positions = [0.7, 1.3, 1.8, 2.2]
        ahead_dots = VGroup(
            *[
                Dot(point=number_line.n2p(x), radius=0.06, color="#89b4fa")
                for x in ahead_positions
            ]
        )

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in behind_dots], lag_ratio=0.15),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in ahead_dots], lag_ratio=0.15),
            run_time=1.0,
        )

        # Indicate compression ahead
        brace = BraceBetweenPoints(
            number_line.n2p(0.7), number_line.n2p(2.2), direction=UP, color=WHITE
        )
        brace_label = Text("compressed λ", font_size=20, color=WHITE).next_to(brace, UP)
        self.play(GrowFromCenter(brace), run_time=0.7)
        self.play(Write(brace_label), run_time=0.5)

        self.wait(0.7)
        # --- Scene 4: Step 4: Motion away from observer stretches wavelength behind ---
        # Background
        self.camera.background_color = "#181825"

        # Title
        title_4 = Text(
            "Motion away from observer stretches wavelength behind",
            font_size=36,
            color=WHITE,
            font="Sans",
        )
        title_4.move_to(UP * 3)

        # Main visual group
        source = Dot(radius=0.12, color="#a6e3a1")
        source.move_to(ORIGIN)

        # Motion arrow to the right
        motion_arrow = Arrow(
            start=LEFT * 2, end=RIGHT * 2, color=WHITE, buff=0, stroke_width=2
        )

        # Observer on the left
        observer = Dot(radius=0.10, color="#fab387")
        observer.move_to(LEFT * 3.5)

        # Wavefronts behind source with increasing spacing (stretched wavelength)
        wave_positions = [-0.8, -2.0, -3.6]
        wave_lines = VGroup()
        for x in wave_positions:
            line = DashedLine(
                start=LEFT * x + UP * 0.8,
                end=LEFT * x + DOWN * 0.8,
                color="#89b4fa",
                dash_length=0.08,
                stroke_width=2,
            )
            wave_lines.add(line)

        # Labels
        source_label = Text("Source", font_size=24, color="#a6e3a1", font="Sans")
        source_label.next_to(source, DOWN, buff=0.3)

        stretch_label = Text(
            "λ increases behind", font_size=24, color="#f38ba8", font="Sans"
        )
        stretch_label.next_to(wave_lines, DOWN, buff=0.5)

        # Group main elements
        main_4 = VGroup(
            source, motion_arrow, observer, wave_lines, source_label, stretch_label
        )
        main_4.move_to(ORIGIN)
        main_4.set_color("#a6e3a1")

        # Animations with total duration 8.0s
        self.play(FadeIn(title_4, shift=UP), run_time=1.0)
        self.wait(0.5)

        self.play(
            FadeIn(observer, scale=0.5),
            FadeIn(source, scale=0.5),
            FadeIn(motion_arrow),
            run_time=1.0,
        )

        wave_anims = [GrowFromCenter(w) for w in wave_lines]
        self.play(LaggedStart(*wave_anims, lag_ratio=0.3), run_time=2.0)

        self.play(Write(source_label), Write(stretch_label), run_time=1.5)

        self.wait(2.0)
        # --- Scene 5: Step 5: Observer measures frequency from crest arrival rate ---
        self.camera.background_color = "#181825"
        self.clear()

        # Title
        title = Text(
            "Observer measures frequency from crest arrival rate",
            font_size=36,
            color=WHITE,
            font="Sans",
        )
        title.move_to(UP * 3)

        # Table data
        data = [
            ["Wavelength λ", "Crest spacing", "Crests / sec (f)"],
            ["Long λ", "Wide", "Low f"],
            ["Short λ", "Narrow", "High f"],
        ]
        table = Table(data)
        table.scale(0.9)
        table.set_stroke(color="#94e2d5", width=2)
        table.set_fill(opacity=0)
        table.move_to(ORIGIN)

        # Supporting labels
        label1 = Text(
            "Observer counts crests per second",
            font_size=28,
            color="#89b4fa",
            font="Sans",
        )
        label2 = Text(
            "Shorter wavelength → more crests pass",
            font_size=28,
            color="#fab387",
            font="Sans",
        )
        label3 = MathTex("f \\propto \\frac{1}{\\lambda}")
        label3.set_color("#f38ba8")
        labels = VGroup(label1, label2, label3).arrange(
            DOWN, buff=0.4, aligned_edge=LEFT
        )
        labels.next_to(table, DOWN, buff=1.0)

        # Animations
        self.play(Write(title), run_time=1.0)
        self.play(GrowFromCenter(table), run_time=2.0)
        self.play(FadeIn(labels, shift=UP * 0.2), run_time=1.5)
        self.wait(2.5)
        # --- Scene 6: Step 6: Approaching causes blueshift and higher pitch ---
        self.camera.background_color = "#181825"
        self.clear()

        # Title
        title_6 = Text(
            "Approaching causes blueshift and higher pitch",
            font_size=36,
            color=WHITE,
            font="Sans",
        )
        title_6.move_to(UP * 3)

        # Main approaching arrow
        main_6 = Arrow(start=LEFT * 3, end=RIGHT * 3, color="#cdd6f4", stroke_width=2.0)

        # Source / Observer
        source_dot = Dot(radius=0.12, color="#fab387")
        source_dot.move_to(LEFT * 3.2)
        observer_dot = Dot(radius=0.12, color="#94e2d5")
        observer_dot.move_to(RIGHT * 3.2)

        source_label = Text("Source", font_size=24, color="#fab387", font="Sans")
        source_label.next_to(source_dot, DOWN)
        observer_label = Text("Observer", font_size=24, color="#94e2d5", font="Sans")
        observer_label.next_to(observer_dot, DOWN)

        # Supporting labels
        sound_label = Text(
            "Sound → higher pitch", font_size=28, color="#a6e3a1", font="Sans"
        )
        sound_label.move_to(DOWN * 1.5 + LEFT * 1.5)

        light_label = Text("Light → bluer", font_size=28, color="#89b4fa", font="Sans")
        light_label.move_to(DOWN * 1.5 + RIGHT * 1.5)

        # Compressed wavefronts visual metaphor
        wave_group = VGroup(
            Line(LEFT * 2.5, LEFT * 1.5, color="#a6e3a1", stroke_width=2),
            Line(LEFT * 1.8, LEFT * 0.8, color="#a6e3a1", stroke_width=2),
            Line(LEFT * 1.0, RIGHT * 0.5, color="#89b4fa", stroke_width=2),
            Line(RIGHT * 0.3, RIGHT * 1.2, color="#89b4fa", stroke_width=2),
        )

        self.play(Write(title_6), run_time=1.2)
        self.play(GrowFromCenter(main_6), run_time=1.0)
        self.play(FadeIn(source_dot), run_time=0.5)
        self.play(FadeIn(observer_dot), run_time=0.5)
        self.play(FadeIn(source_label), run_time=0.5)
        self.play(FadeIn(observer_label), run_time=0.5)
        self.play(FadeIn(wave_group), run_time=0.8)
        self.play(FadeIn(sound_label), run_time=0.8)
        self.play(FadeIn(light_label), run_time=0.7)

        self.wait(7.0 - (1.2 + 1.0 + 0.5 + 0.5 + 0.5 + 0.5 + 0.8 + 0.8 + 0.7))
        # --- Scene 7: Step 7: Receding causes redshift and lower pitch with relativistic limit ---
        self.camera.background_color = "#181825"

        # Title
        title_7 = Text(
            "Receding causes redshift and lower pitch with relativistic limit",
            font_size=36,
        )
        title_7.set_color(WHITE)
        title_7.move_to(UP * 3)

        # Main concept text
        main_7 = Text(
            "Receding → Lower Frequency\nSound ↓ pitch, Light → Redshift", font_size=48
        )
        main_7.set_color("#89b4fa")
        main_7.move_to(ORIGIN)

        self.play(GrowFromCenter(title_7), run_time=1.2)
        self.wait(0.3)
        self.play(Write(main_7), run_time=2.0)

        # Supporting labels from narration
        label1 = Text("Receding sources lower frequency", font_size=28)
        label1.set_color("#fab387")
        label1.move_to(DOWN * 1.5)

        label2 = Text("Sound sounds deeper, light shifts red", font_size=28)
        label2.set_color("#f38ba8")
        label2.move_to(DOWN * 2.2)

        label3 = Text(
            "At high speeds, relativistic effects modify the shift", font_size=28
        )
        label3.set_color("#a6e3a1")
        label3.move_to(DOWN * 2.9)

        self.play(FadeIn(label1, shift=UP * 0.2), run_time=0.8)
        self.wait(0.2)
        self.play(FadeIn(label2, shift=UP * 0.2), run_time=0.8)
        self.wait(0.2)
        self.play(FadeIn(label3, shift=UP * 0.2), run_time=0.8)
        self.wait(2.7)
