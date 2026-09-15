import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Wavefronts propagate at constant speed ---
        self.camera.background_color = "#181825"

        # Title
        title_1 = Text(
            "Wavefronts propagate at constant speed", font_size=36, color=WHITE
        )
        title_1.move_to(UP * 3)

        # Main concept text
        main_1 = Text("c = constant", font_size=48, color="#89b4fa")
        main_1.move_to(ORIGIN)

        # Supporting wavefront visualization
        center_dot = Dot(radius=0.06, color="#fab387")
        wave_colors = ["#a6e3a1", "#94e2d5", "#f38ba8"]
        circles = VGroup(
            *[
                Circle(radius=0.8 + i * 0.6, color=wave_colors[i], stroke_width=2)
                for i in range(3)
            ]
        )
        circles.move_to(ORIGIN)

        # Build scene with creative animations
        self.play(Write(title_1), run_time=2.0)
        self.play(GrowFromCenter(center_dot), run_time=0.8)
        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in circles], lag_ratio=0.3),
            run_time=2.0,
        )
        self.play(GrowFromCenter(main_1), run_time=1.2)
        self.wait(2.5)  # 2.0 + 0.8 + 2.0 + 1.2 + 2.5 = 8.5
        # --- Scene 2: Step 2: Source motion changes wave spacing ---
        self.camera.background_color = "#181825"
        self.clear()

        # Title
        title = Text(
            "Source motion changes wave spacing", font_size=36, color=WHITE, font="Sans"
        )
        title.move_to(UP * 3)

        # Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=4,
            axis_config={"color": "#fab387", "stroke_width": 2, "include_tip": False},
            x_axis_config={"color": "#fab387", "stroke_width": 2},
            y_axis_config={"color": "#fab387", "stroke_width": 2},
        )
        axes.move_to(ORIGIN)

        # Source
        source = Dot(radius=0.08, color="#f38ba8")
        source.move_to(axes.c2p(0, 0))

        # Wavefronts with changing spacing
        wave_left = axes.plot(
            lambda x: np.sin(2 * np.pi * x / 1.2),
            x_range=[-2.5, 0],
            color="#89b4fa",
            stroke_width=2,
        )
        wave_right = axes.plot(
            lambda x: np.sin(2 * np.pi * x / 0.6),
            x_range=[0, 2.5],
            color="#89b4fa",
            stroke_width=2,
        )

        # Supporting labels
        rear_label = Text(
            "Rear (stretched)", font_size=24, color="#a6e3a1", font="Sans"
        )
        rear_label.move_to(axes.c2p(-1.8, 1.4))
        forward_label = Text(
            "Forward (compressed)", font_size=24, color="#f38ba8", font="Sans"
        )
        forward_label.move_to(axes.c2p(1.8, 1.4))

        # Motion indication
        arrow = Arrow(
            start=axes.c2p(-1, 0), end=axes.c2p(1, 0), color="#f38ba8", stroke_width=2
        )
        arrow.shift(UP * 0.3)

        self.play(Write(title), run_time=1.0)
        self.play(Create(axes), run_time=1.5)
        self.play(GrowFromCenter(source), run_time=0.5)
        self.play(Create(wave_left), run_time=1.0)
        self.play(Create(wave_right), run_time=1.0)
        self.play(FadeIn(rear_label), FadeIn(forward_label), run_time=0.8)
        self.play(Create(arrow), run_time=0.7)
        self.wait(2.0)
        # --- Scene 3: Step 3: Observer measures arrival rate ---
        self.camera.background_color = "#181825"

        # Title
        title = Text("Observer measures arrival rate", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Number line as time axis
        number_line = NumberLine(x_range=[-5, 5], length=10, include_numbers=False)
        number_line.set_color("#f38ba8")
        number_line.stroke_width = 2.0
        number_line.shift(DOWN * 2)
        number_line.add_numbers()

        # Observer at origin
        observer = Dot(radius=0.12, color="#89b4fa")
        observer.move_to(number_line.n2p(0))
        observer_label = Text("Observer", font_size=24, color=WHITE)
        observer_label.next_to(observer, UP)

        # Wavefronts: farther = sparse, closer = dense
        far_dots = VGroup(
            *[
                Dot(radius=0.08, color="#fab387").move_to(number_line.n2p(x))
                for x in [-4, -2]
            ]
        )
        near_dots = VGroup(
            *[
                Dot(radius=0.08, color="#a6e3a1").move_to(number_line.n2p(x))
                for x in [1, 2, 3, 4]
            ]
        )

        low_label = Text("low frequency", font_size=24, color="#a6e3a1")
        low_label.next_to(number_line.n2p(-3), DOWN)
        high_label = Text("high frequency", font_size=24, color="#94e2d5")
        high_label.next_to(number_line.n2p(2.5), DOWN)

        time_label = Text("time", font_size=24, color=WHITE)
        time_label.next_to(number_line, DOWN)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=1.0)
        self.play(Create(number_line), run_time=1.5)
        self.play(GrowFromCenter(observer), run_time=0.8)
        self.play(FadeIn(observer_label), run_time=0.7)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in far_dots], lag_ratio=0.2),
            run_time=1.5,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in near_dots], lag_ratio=0.2),
            run_time=1.5,
        )
        self.play(
            FadeIn(low_label), FadeIn(high_label), FadeIn(time_label), run_time=0.5
        )
        self.wait(1.0)
        # --- Scene 4: Step 4: Acoustic Doppler shift ---
        self.camera.background_color = "#181825"

        palette = ["#89b4fa", "#fab387", "#f38ba8", "#a6e3a1", "#94e2d5"]

        title = Text("Acoustic Doppler shift", font_size=36, color=WHITE, font="Sans")
        title.move_to(UP * 3)

        source = Dot(radius=0.12, color=palette[1])
        source.move_to(LEFT * 2.5)

        observer = Dot(radius=0.12, color=palette[4])
        observer.move_to(RIGHT * 2.5)

        source_label = Text("Source", font_size=24, color=WHITE, font="Sans")
        source_label.next_to(source, DOWN)

        observer_label = Text("Observer", font_size=24, color=WHITE, font="Sans")
        observer_label.next_to(observer, DOWN)

        wave1 = Circle(radius=0.3, color=palette[3], stroke_width=2.0)
        wave2 = Circle(radius=0.6, color=palette[3], stroke_width=2.0)
        wave3 = Circle(radius=0.9, color=palette[3], stroke_width=2.0)

        waves = VGroup(wave1, wave2, wave3)
        waves.move_to(source.get_center())

        main_4 = VGroup(source, observer, source_label, observer_label, waves)
        main_4.set_color(palette[3])
        main_4.move_to(ORIGIN)

        freq_up = Text(
            "Higher frequency → approaching",
            font_size=24,
            color=palette[0],
            font="Sans",
        )
        freq_up.next_to(observer, UP)

        freq_down = Text(
            "Lower frequency ← receding", font_size=24, color=palette[2], font="Sans"
        )
        freq_down.next_to(source, UP)

        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(main_4, scale=0.8), run_time=1.5)
        self.wait(0.5)
        self.play(GrowFromCenter(waves), run_time=1.0)
        self.play(source.animate.shift(RIGHT * 1.0), run_time=2.0)
        self.wait(1.0)
        self.play(FadeIn(freq_up), run_time=1.0)
        self.play(FadeIn(freq_down), run_time=1.0)
        # --- Scene 5: Step 5: Doppler frequency formula ---
        # background
        self.camera.background_color = "#181825"

        # title
        title_5 = Text("Doppler frequency formula", font_size=36, color=WHITE)
        title_5.move_to(UP * 3)

        # table data with supporting labels
        data = [
            ["Term", "Meaning"],
            ["f'", "Observed frequency"],
            ["f", "Source frequency"],
            ["v_o", "Observer speed toward source"],
            ["v_s", "Source speed toward observer"],
            ["c", "Wave speed"],
        ]
        main_5 = Table(data)
        main_5.set_stroke(color="#94e2d5", width=2)
        main_5.scale(0.9)
        main_5.move_to(ORIGIN)

        # creative build
        self.play(Write(title_5), run_time=1.0)
        self.play(GrowFromCenter(main_5), run_time=2.0)
        self.wait(6.5)
        # --- Scene 6: Step 6: Relativistic Doppler for light ---
        self.camera.background_color = "#181825"

        # Title
        title = Text("Relativistic Doppler for light", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Main light propagation arrow
        main_arrow = Arrow(
            start=LEFT * 3, end=RIGHT * 3, color="#cdd6f4", stroke_width=2.0
        )

        # Receding → Redshift
        red_arrow = Arrow(
            start=LEFT * 2, end=RIGHT * 2, color="#f38ba8", stroke_width=2.0
        )
        red_label = Text("Receding → Redshift", font_size=24, color="#f38ba8")
        red_group = VGroup(red_arrow, red_label).arrange(DOWN, aligned_edge=LEFT)
        red_group.next_to(main_arrow, DOWN, buff=0.8)
        red_group.shift(LEFT * 1.5)

        # Approaching → Blueshift
        blue_arrow = Arrow(
            start=RIGHT * 2, end=LEFT * 2, color="#89b4fa", stroke_width=2.0
        )
        blue_label = Text("Approaching → Blueshift", font_size=24, color="#89b4fa")
        blue_group = VGroup(blue_arrow, blue_label).arrange(DOWN, aligned_edge=LEFT)
        blue_group.next_to(main_arrow, DOWN, buff=0.8)
        blue_group.shift(RIGHT * 1.5)

        # Animations - total 8.0 s
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(GrowFromCenter(main_arrow), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(red_group), run_time=1.0)
        self.wait(0.3)
        self.play(FadeIn(blue_group), run_time=1.2)
        self.wait(2.0)
        # --- Scene 7: Step 7: Practical applications of Doppler shift ---
        self.clear()
        self.camera.background_color = "#181825"

        title_7 = Text(
            "Practical applications of Doppler shift",
            font="Sans",
            font_size=36,
            color=WHITE,
        )
        title_7.move_to(UP * 3)

        main_7 = Text(
            "Measure speed & cosmic expansion",
            font="Sans",
            font_size=48,
            color="#89b4fa",
        )
        main_7.move_to(ORIGIN)

        radar = Text("Radar guns", font="Sans", font_size=32, color="#fab387")
        ultrasound = Text(
            "Medical ultrasound", font="Sans", font_size=32, color="#f38ba8"
        )
        astronomy = Text("Astronomy", font="Sans", font_size=32, color="#a6e3a1")

        radar.next_to(main_7, DOWN, buff=0.8)
        ultrasound.next_to(radar, DOWN, buff=0.6)
        astronomy.next_to(ultrasound, DOWN, buff=0.6)

        self.play(Write(title_7), run_time=1.5)
        self.play(GrowFromCenter(main_7), run_time=2.0)
        self.play(FadeIn(radar), run_time=1.0)
        self.play(FadeIn(ultrasound), run_time=1.0)
        self.play(FadeIn(astronomy), run_time=1.0)
        self.wait(1.0)
