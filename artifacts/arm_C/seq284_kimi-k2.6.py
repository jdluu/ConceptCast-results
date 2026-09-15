import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Wave fundamentals: wavelength and frequency ---
        self.camera.background_color = "#181825"

        # 1. Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            x_length=9,
            y_length=3,
            axis_config={"stroke_width": 2, "color": "#89b4fa", "include_tip": False},
        )

        # 2. Value tracker to drive the wave phase
        phase_tracker = ValueTracker(0)

        # 3. Sine wave that scrolls left as phase increases
        #    Period = 5 graph units  =>  two full wavelengths visible across [0, 10]
        sine_wave = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(2 * PI * (x - phase_tracker.get_value()) / 5.0),
                color="#f38ba8",
                stroke_width=3,
                x_range=[0, 10],
            )
        )

        # 4. Observation line (fixed vertical dashed line)
        obs_graph_x = 4.375
        observation_line = DashedLine(
            start=axes.c2p(obs_graph_x, -2),
            end=axes.c2p(obs_graph_x, 2),
            color="#94e2d5",
            dash_length=0.15,
        )

        # 5. Wavelength arrow & label spanning two adjacent crests
        #    Crests for the base wave sit at x = 1.25 and x = 6.25
        crest_arrow = Arrow(
            start=axes.c2p(1.25, 2.8),
            end=axes.c2p(6.25, 2.8),
            color="#a6e3a1",
            stroke_width=2.5,
            buff=0.2,
        )
        wavelength_label = Text("Wavelength", font_size=28, color="#a6e3a1")
        wavelength_label.next_to(crest_arrow, UP, buff=0.15)

        # 6. Frequency counter that increments as crests cross the observation line
        #    Crests cross x = 4.375 when phase ≈ 3.125 and 8.125
        counter_label = always_redraw(
            lambda: MathTex(
                f"f = {int(phase_tracker.get_value() >= 3.125) + int(phase_tracker.get_value() >= 8.125)}",
                color="#fab387",
            ).move_to(axes.c2p(5, -2.5))
        )

        # --- ANIMATION TIMELINE (Total = 14.0 s) ---

        # t = 0.0 → 2.0  |  Introduce axes and the scrolling wave
        self.play(
            FadeIn(axes),
            Create(sine_wave),
            run_time=2.0,
        )

        # t = 2.0 → 3.5  |  Reveal wavelength arrow
        self.play(
            FadeIn(crest_arrow),
            FadeIn(wavelength_label),
            run_time=1.5,
        )

        # t = 3.5 → 5.0  |  Reveal observation station and frequency counter
        self.play(
            FadeIn(observation_line),
            FadeIn(counter_label),
            run_time=1.5,
        )

        # t = 5.0 → 14.0 |  Undulate wave for 9 seconds while counter ticks up
        self.play(
            phase_tracker.animate.set_value(10),
            run_time=9.0,
            rate_func=linear,
        )
        # --- Scene 2: Stationary source and observer ---
        self.clear()
        # --- Scene 2: Stationary source and observer ---
        # Configuration
        self.camera.background_color = "#181825"

        # Colors from palette
        SOURCE_COLOR = "#89b4fa"
        OBSERVER_COLOR = "#f38ba8"
        RIPPLE1_COLOR = "#a6e3a1"
        RIPPLE2_COLOR = "#94e2d5"
        RIPPLE3_COLOR = "#fab387"
        TICK_COLOR = "#89b4fa"

        # --- Source and Observer ---
        source = Dot(point=LEFT * 2, radius=0.18, color=SOURCE_COLOR)
        source_label = Text("Source", font_size=24, color=SOURCE_COLOR).next_to(
            source, DOWN, buff=0.3
        )

        observer = Dot(point=RIGHT * 3, radius=0.18, color=OBSERVER_COLOR)
        observer_label = Text("Observer", font_size=24, color=OBSERVER_COLOR).next_to(
            observer, DOWN, buff=0.3
        )

        # --- NumberLine for counting crest arrivals ---
        arrival_line = NumberLine(
            x_range=[0, 6, 1],
            length=3,
            include_numbers=True,
            color=TICK_COLOR,
        ).shift(DOWN * 2.5)

        arrival_title = Text("Crests detected", font_size=20, color=TICK_COLOR).next_to(
            arrival_line, UP, buff=0.4
        )

        # --- Static Ripples (pre-existing waves to show the field) ---
        ripple1 = Circle(radius=1.2, color=RIPPLE1_COLOR, stroke_width=2).move_to(
            source.get_center()
        )
        ripple2 = Circle(radius=2.6, color=RIPPLE2_COLOR, stroke_width=2).move_to(
            source.get_center()
        )
        ripple3 = Circle(radius=4.2, color=RIPPLE3_COLOR, stroke_width=2).move_to(
            source.get_center()
        )

        # --- Intro: Draw source, observer, and existing ripples ---
        self.play(
            FadeIn(source, scale=0.5),
            FadeIn(observer, scale=0.5),
            Write(source_label),
            Write(observer_label),
            run_time=0.8,
        )

        self.play(Create(ripple1), Create(ripple2), Create(ripple3), run_time=1.2)

        # Show NumberLine
        self.play(Create(arrival_line), Write(arrival_title), run_time=0.8)

        # --- Continuous pulsing wave animation ---
        num_waves = 4
        travel_time = 2.5  # time for wave to expand across scene
        wave_interval = 1.5  # time between wave starts

        arrival_markers = VGroup()

        for i in range(num_waves):
            wave = Circle(radius=0.05, color=RIPPLE1_COLOR, stroke_width=2.5)
            wave.move_to(source.get_center())

            # Arrival tick on NumberLine
            tick_point = arrival_line.n2p(i + 1)
            tick_marker = Dot(point=tick_point, radius=0.12, color=OBSERVER_COLOR)
            tick_label = MathTex(
                str(i + 1), font_size=24, color=OBSERVER_COLOR
            ).next_to(tick_marker, UP, buff=0.15)
            tick_group = VGroup(tick_marker, tick_label)

            # Wave appears
            self.play(FadeIn(wave, scale=0.1), run_time=0.1)

            # Expand and fade the wave
            self.play(
                wave.animate.scale(90).set_opacity(0),
                run_time=travel_time,
                rate_func=linear,
            )

            # Flash at observer and mark arrival
            observer_flash = Dot(
                point=observer.get_center(), radius=0.3, color=OBSERVER_COLOR
            )
            self.play(FadeIn(observer_flash, scale=2), run_time=0.2)

            self.play(
                FadeOut(observer_flash),
                FadeIn(tick_marker),
                Write(tick_label),
                run_time=0.3,
            )

            arrival_markers.add(tick_group)
            self.remove(wave)  # Clean up fully faded wave

            if i < num_waves - 1:
                wait_time = wave_interval - travel_time
                if wait_time > 0:
                    self.wait(wait_time)

        # --- Final emphasis: frequency equality formula ---
        formula_box = SurroundingRectangle(
            VGroup(arrival_line, arrival_title), color=TICK_COLOR, buff=0.3
        )

        self.play(Create(formula_box), run_time=0.5)
        self.wait(0.3)

        formula = MathTex(
            r"f_{	ext{observed}} = f_{	ext{emitted}}", font_size=40, color=WHITE
        )
        formula.shift(UP * 2.2)

        self.play(Write(formula), run_time=0.8)

        # Highlight equality with gentle pulse
        self.play(
            formula.animate.scale(1.15).set_color("#a6e3a1"),
            run_time=0.4,
            rate_func=there_and_back,
        )

        self.wait(1.5)

        # Fade everything out
        all_mobjects = VGroup(
            source,
            source_label,
            observer,
            observer_label,
            ripple1,
            ripple2,
            ripple3,
            arrival_line,
            arrival_title,
            formula_box,
            formula,
            arrival_markers,
        )
        self.play(FadeOut(all_mobjects), run_time=0.8)
        self.wait(0.3)
        # --- Scene 3: Moving source: waves bunch and stretch ---
        self.camera.background_color = "#181825"

        # 1. Static Elements
        source = Dot(point=LEFT * 3, color="#f38ba8", radius=0.22)

        arrow = Arrow(
            start=np.array([-3.0, 0.6, 0]),
            end=np.array([1.5, 0.6, 0]),
            color="#fab387",
            buff=0.2,
            stroke_width=2.5,
        )
        v_label = MathTex(r"v_s", color="#fab387", font_size=40).next_to(
            arrow, UP * 1.5
        )

        # 2. Wave Parameters
        num_waves = 8
        wave_interval = 0.9
        source_speed = 2.0
        shift_per_wave = source_speed * wave_interval

        wavefronts = VGroup()

        # 3. Intro
        self.play(FadeIn(source), run_time=0.5)
        self.play(FadeIn(arrow), Write(v_label), run_time=0.5)

        # 4. Main Animation Loop
        for i in range(num_waves):
            new_wave = Circle(
                radius=0.01,
                color="#a6e3a1",
                stroke_width=2,
            ).move_to(source.get_center())

            target_radius = 4.0 + i * 0.5

            self.play(
                source.animate.shift(RIGHT * shift_per_wave),
                new_wave.animate.scale(target_radius / 0.01),
                run_time=wave_interval,
                rate_func=linear,
            )
            wavefronts.add(new_wave)

        # 5. Pinned Annotations
        lambda_right = MathTex(
            r"\lambda_{	ext{right}} < \lambda_0",
            color="#f38ba8",
            font_size=36,
        ).next_to(source, RIGHT * 1.5)

        lambda_left = (
            MathTex(
                r"\lambda_{	ext{left}} > \lambda_0",
                color="#89b4fa",
                font_size=36,
            )
            .to_edge(LEFT)
            .shift(UP * 1.5)
        )

        self.play(
            FadeIn(lambda_right),
            FadeIn(lambda_left),
            run_time=0.5,
        )

        # 6. Final hold to reach exactly 15 s
        total_play_time = 0.5 + 0.5 + (num_waves * wave_interval) + 0.5
        self.wait(max(0.1, 15.0 - total_play_time))
        # --- Scene 4: Moving source toward observer: higher pitch ---
        self.clear()
        # --- Scene 4: Moving source toward observer: higher pitch ---
        self.camera.background_color = "#181825"

        # --- 1. Source and Observer ---
        approach_source = Dot(point=LEFT * 1, color="#f38ba8", radius=0.22)
        observer_right = Dot(point=RIGHT * 4.5, color="#89b4fa", radius=0.2)

        observer_label = Text("Observer", font_size=28, color="#89b4fa")
        observer_label.next_to(observer_right, UP)

        # --- 2. Compressed Ripples on the Right Side ---
        # Concentric arcs centered at the source to simulate wavefronts
        ripples = VGroup()
        source_center = LEFT * 1
        num_ripples = 5
        for i in range(num_ripples):
            radius = 2.0 + i * 0.45  # short spacing = compressed on right
            arc = Arc(
                radius=radius,
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                color="#ECEFF4",
                stroke_width=2,
            )
            arc.shift(source_center - arc.get_arc_center())
            ripples.add(arc)

        # --- 3. Brace showing shorter wavelength ---
        lambda_line = Line(
            start=[0.5, 0, 0], end=[2.2, 0, 0], color="#ECEFF4", stroke_width=2
        )
        compressed_brace = Brace(lambda_line, DOWN, color="#a6e3a1", buff=0.1)

        # FIX: Use Text instead of get_text() to avoid unicode/LaTeX issues with λ
        brace_label = Text("Shorter λ", font_size=28, color="#a6e3a1")
        brace_label.next_to(compressed_brace, DOWN, buff=0.15)

        # --- 4. Frequency counter ---
        freq_counter_high = MathTex(r"f_{obs} > f_{emitted}", color="#fab387")
        freq_counter_high.move_to(DOWN * 2)

        # ======= Animations (Total duration = 15.0 seconds) =======

        # 0.0–1.5s: Fade in source and observer
        self.play(
            FadeIn(approach_source),
            FadeIn(observer_right),
            Write(observer_label),
            run_time=1.5,
        )
        # self.wait(0.5)  # 1.5–2.0

        # 2.0–5.0s: Create compressed ripples with a staggered wave effect
        self.play(
            LaggedStart(*[Create(r) for r in ripples], lag_ratio=0.15), run_time=3.0
        )
        # self.wait(1.0)  # 5.0–6.0

        # 6.0–8.0s: Show brace and label for shorter wavelength
        self.play(
            Create(lambda_line),
            GrowFromCenter(compressed_brace),
            Write(brace_label),
            run_time=2.0,
        )
        # self.wait(1.0)  # 8.0–9.0

        # 9.0–10.5s: Show higher observed frequency
        self.play(Write(freq_counter_high), run_time=1.5)
        # self.wait(1.0)  # 10.5–11.5

        # 11.5–12.5s: Emphasize observer receiving more crests
        self.play(
            Indicate(observer_right, scale_factor=1.5, color="#f38ba8"), run_time=1.0
        )
        # self.wait(0.5)  # 12.5–13.0

        # 13.0–15.0s: Highlight frequency formula with a surrounding rectangle
        freq_box = SurroundingRectangle(freq_counter_high, color="#fab387", buff=0.2)
        self.play(Create(freq_box), run_time=1.0)
        # self.wait(1.0)  # 14.0–15.0
        # --- Scene 5: Moving source away: lower pitch ---
        self.camera.background_color = "#181825"

        # --- 1. Static Objects ---
        # Receding source (right side, pink)
        recede_source = Dot(RIGHT * 1, radius=0.22, color="#f38ba8")

        # Stationary observer (left side, blue)
        observer_left = Dot(LEFT * 4.5, radius=0.2, color="#89b4fa")
        observer_label = Text("Observer", font_size=36)
        observer_label.next_to(observer_left, DOWN)

        # Stretched concentric wave circles (asymmetric - trailing behind source to the right, expanded to the left)
        wave_circles = VGroup()
        num_waves = 6
        for i in range(num_waves):
            # Each successive wavefront is emitted from a position slightly to the right
            # of the previous one, creating the stretched appearance
            offset = i * 0.8  # How far right the emission point moves per wave
            radius = 1.0 + offset * 1.3  # Increasing radius for older waves
            center = RIGHT * 1 + RIGHT * offset * 0.6  # Shift emission points rightward

            c = Circle(radius=radius, color="#ECEFF4", stroke_width=1.5, fill_opacity=0)
            c.move_to(center)
            wave_circles.add(c)

        # Brace showing longer wavelength on the left side
        lambda_line = Line(
            start=LEFT * 2.5, end=LEFT * 0.5, color="#ECEFF4", stroke_width=2
        )
        stretched_brace = Brace(lambda_line, DOWN, color="#94e2d5")
        brace_label = MathTex(r"	ext{Longer } \lambda", color="#94e2d5")
        brace_label.next_to(stretched_brace, DOWN)

        # Frequency counter showing lower observed frequency
        freq_counter = MathTex(r"f_{obs} < f_{emitted}", color="#fab387")
        freq_counter.move_to(DOWN * 2.5)

        # --- 2. Animation Sequence ---
        # Entrance of source and observer (1s)
        self.play(
            FadeIn(recede_source),
            FadeIn(observer_left),
            FadeIn(observer_label),
            run_time=1,
        )

        # Create wavefronts progressively (3s) - showing them spread out
        self.play(Create(wave_circles), run_time=3)

        # Show wavelength measurement line (1s)
        self.play(FadeIn(lambda_line), run_time=1)

        # Show brace and label for longer wavelength (1.5s)
        self.play(FadeIn(stretched_brace), FadeIn(brace_label), run_time=1.5)

        # Brief pause (1s)
        self.wait(1)

        # Show frequency inequality (1.5s)
        self.play(FadeIn(freq_counter), run_time=1.5)

        # Hold final view (5s)
        self.wait(5)

        # Total: 1 + 3 + 1 + 1.5 + 1 + 1.5 + 5 = 14.0 seconds
        # --- Scene 6: Moving observer: cutting across wavefronts ---
        self.camera.background_color = "#181825"

        # ---- OBJECTS ----
        source = Dot(point=LEFT * 4, radius=0.2, color="#89b4fa")
        source_label = Text("Source", font_size=24, color="#89b4fa").next_to(
            source, DOWN, buff=0.25
        )

        moving_observer = Dot(
            point=RIGHT * 3 + DOWN * 1.5, radius=0.22, color="#f38ba8"
        )
        moving_label = Text("Moving observer", font_size=24, color="#f38ba8").next_to(
            moving_observer, DOWN, buff=0.25
        )

        still_observer = Dot(point=RIGHT * 3 + UP * 1.5, radius=0.2, color="#a6e3a1")
        still_label = Text("Still observer", font_size=24, color="#a6e3a1").next_to(
            still_observer, UP, buff=0.25
        )

        wave1 = Circle(radius=1.5, color="#94e2d5", stroke_width=2).move_to(LEFT * 4)
        wave2 = Circle(radius=3.2, color="#94e2d5", stroke_width=2).move_to(LEFT * 4)
        wave3 = Circle(radius=5.0, color="#94e2d5", stroke_width=2).move_to(LEFT * 4)

        v_arrow = Arrow(
            start=RIGHT * 3 + DOWN * 2.2,
            end=ORIGIN + DOWN * 2.2,
            color="#fab387",
            stroke_width=2.5,
            buff=0.2,
        )
        v_label = Text("v_observer", font_size=22, color="#fab387").next_to(
            v_arrow, DOWN, buff=0.15
        )

        title_moving = Text("Moving", font_size=20, color="#f38ba8").move_to(
            RIGHT * 5.5 + UP * 1.0
        )
        title_still = Text("Stationary", font_size=20, color="#a6e3a1").move_to(
            RIGHT * 5.5 + DOWN * 1.0
        )

        freq_moving = Text("Count: 0", font_size=22, color="#f38ba8").move_to(
            RIGHT * 5.5 + UP * 0.3
        )
        freq_still = Text("Count: 0", font_size=22, color="#a6e3a1").move_to(
            RIGHT * 5.5 + DOWN * 1.7
        )

        sep = DashedLine(
            start=UP * 3.5 + RIGHT * 4.5,
            end=DOWN * 3.5 + RIGHT * 4.5,
            color="#6c7086",
            dash_length=0.15,
        )

        # ---- INTRO: 0-4 sec ----
        self.play(
            FadeIn(source),
            FadeIn(still_observer),
            FadeIn(moving_observer),
            run_time=0.5,
        )
        self.play(
            Write(source_label), Write(still_label), Write(moving_label), run_time=0.5
        )
        self.play(
            LaggedStart(FadeIn(wave1), FadeIn(wave2), FadeIn(wave3), lag_ratio=0.3),
            run_time=1.0,
        )
        self.play(GrowFromCenter(v_arrow), Write(v_label), run_time=0.5)
        self.play(
            FadeIn(title_moving),
            FadeIn(title_still),
            FadeIn(freq_moving),
            FadeIn(freq_still),
            FadeIn(sep),
            run_time=0.5,
        )

        freq_mv3 = Text("Count: 3", font_size=22, color="#f38ba8").move_to(
            RIGHT * 5.5 + UP * 0.3
        )
        freq_st3 = Text("Count: 3", font_size=22, color="#a6e3a1").move_to(
            RIGHT * 5.5 + DOWN * 1.7
        )
        self.play(
            ReplacementTransform(freq_moving, freq_mv3),
            ReplacementTransform(freq_still, freq_st3),
            run_time=0.4,
        )
        self.wait(0.6)

        # ---- WAVE EXPANSION + OBSERVER MOVE: 4-16 sec (12 sec block) ----
        wave4 = (
            Circle(radius=0.2, color="#94e2d5", stroke_width=2)
            .move_to(LEFT * 4)
            .set_stroke(opacity=0)
        )
        wave5 = (
            Circle(radius=0.2, color="#94e2d5", stroke_width=2)
            .move_to(LEFT * 4)
            .set_stroke(opacity=0)
        )
        wave6 = (
            Circle(radius=0.2, color="#94e2d5", stroke_width=2)
            .move_to(LEFT * 4)
            .set_stroke(opacity=0)
        )
        wave7 = (
            Circle(radius=0.2, color="#94e2d5", stroke_width=2)
            .move_to(LEFT * 4)
            .set_stroke(opacity=0)
        )

        freq_mv4 = Text("Count: 4", font_size=22, color="#f38ba8").move_to(
            RIGHT * 5.5 + UP * 0.3
        )
        freq_mv5 = Text("Count: 5", font_size=22, color="#f38ba8").move_to(
            RIGHT * 5.5 + UP * 0.3
        )
        freq_mv6 = Text("Count: 6", font_size=22, color="#f38ba8").move_to(
            RIGHT * 5.5 + UP * 0.3
        )
        freq_mv7 = Text("Count: 7", font_size=22, color="#f38ba8").move_to(
            RIGHT * 5.5 + UP * 0.3
        )
        freq_mv8 = Text("Count: 8", font_size=22, color="#f38ba8").move_to(
            RIGHT * 5.5 + UP * 0.3
        )
        freq_st4 = Text("Count: 4", font_size=22, color="#a6e3a1").move_to(
            RIGHT * 5.5 + DOWN * 1.7
        )
        freq_st5 = Text("Count: 5", font_size=22, color="#a6e3a1").move_to(
            RIGHT * 5.5 + DOWN * 1.7
        )
        freq_st6 = Text("Count: 6", font_size=22, color="#a6e3a1").move_to(
            RIGHT * 5.5 + DOWN * 1.7
        )

        self.play(
            moving_observer.animate.shift(LEFT * 0.7),
            wave4.animate.set_stroke(opacity=1).scale(15).set_stroke(opacity=0.2),
            ReplacementTransform(freq_mv3, freq_mv4),
            ReplacementTransform(freq_st3, freq_st4),
            run_time=2.5,
            rate_func=linear,
        )

        self.play(
            moving_observer.animate.shift(LEFT * 0.7),
            wave5.animate.set_stroke(opacity=1).scale(15).set_stroke(opacity=0.2),
            ReplacementTransform(freq_mv4, freq_mv5),
            ReplacementTransform(freq_st4, freq_st5),
            run_time=2.5,
            rate_func=linear,
        )

        self.play(
            moving_observer.animate.shift(LEFT * 0.7),
            wave6.animate.set_stroke(opacity=1).scale(15).set_stroke(opacity=0.2),
            ReplacementTransform(freq_mv5, freq_mv6),
            ReplacementTransform(freq_st5, freq_st6),
            run_time=2.5,
            rate_func=linear,
        )

        self.play(
            moving_observer.animate.shift(LEFT * 0.6),
            wave7.animate.set_stroke(opacity=1).scale(15).set_stroke(opacity=0.2),
            ReplacementTransform(freq_mv6, freq_mv7),
            run_time=2.0,
            rate_func=linear,
        )

        self.play(
            moving_observer.animate.shift(LEFT * 0.4),
            ReplacementTransform(freq_mv7, freq_mv8),
            run_time=1.5,
            rate_func=linear,
        )

        self.play(Indicate(freq_mv8, color="#f38ba8", scale_factor=1.3), run_time=1.0)
        # --- Scene 7: Combined motion: relative velocity matters ---
        self.clear()
        self.camera.background_color = "#181825"

        # ------------------------------------------------------------------
        # 1. Mobjects
        # ------------------------------------------------------------------
        # --- Source & Observer Dots -----------------------------------------
        source_comb = Dot(point=LEFT * 2.5, radius=0.22, color="#f38ba8")
        observer_comb = Dot(point=RIGHT * 2.5, radius=0.22, color="#89b4fa")

        # --- Labels ----------------------------------------------------------
        source_label = Text("Source", font_size=28, color="#f38ba8").next_to(
            source_comb, DOWN, buff=0.3
        )
        observer_label = Text("Observer", font_size=28, color="#89b4fa").next_to(
            observer_comb, DOWN, buff=0.3
        )

        # --- Velocity Arrows -------------------------------------------------
        source_arrow = Arrow(
            start=[-2.5, 0.7, 0],
            end=[-0.5, 0.7, 0],
            buff=0.2,
            color="#fab387",
            stroke_width=2.5,
            tip_length=0.25,
        )
        source_v_label = MathTex(r"v_s", color="#fab387").next_to(
            source_arrow, UP, buff=0.15
        )

        observer_arrow = Arrow(
            start=[2.5, 0.7, 0],
            end=[0.5, 0.7, 0],
            buff=0.2,
            color="#a6e3a1",
            stroke_width=2.5,
            tip_length=0.25,
        )
        observer_v_label = MathTex(r"v_o", color="#a6e3a1").next_to(
            observer_arrow, UP, buff=0.15
        )

        # --- Relative separation arrow ---------------------------------------
        relative_arrow = DoubleArrow(
            start=[-2.5, -1.2, 0],
            end=[2.5, -1.2, 0],
            buff=0.2,
            color="#94e2d5",
            stroke_width=2.5,
            tip_length=0.25,
        )
        relative_label = Text(
            "Changing separation", font_size=24, color="#94e2d5"
        ).next_to(relative_arrow, DOWN, buff=0.2)

        # --- Lopsided ripple field (compressed in front of source) ----------
        # Instead of full circles, draw arcs on the RIGHT side of the source
        # to visually imply compressed wavefronts.
        cr1 = Arc(
            radius=0.9,
            start_angle=-PI / 3,
            angle=2 * PI / 3,
            arc_center=LEFT * 2.5,
            color="#a6e3a1",
            stroke_width=2,
        )
        cr2 = Arc(
            radius=2.0,
            start_angle=-PI / 3,
            angle=2 * PI / 3,
            arc_center=LEFT * 2.5,
            color="#94e2d5",
            stroke_width=2,
        )
        cr3 = Arc(
            radius=3.3,
            start_angle=-PI / 3,
            angle=2 * PI / 3,
            arc_center=LEFT * 2.5,
            color="#89b4fa",
            stroke_width=2,
        )
        comb_rings = VGroup(cr1, cr2, cr3)

        # --- Formula hint (top-center) -----------------------------------------
        formula_hint = MathTex(
            r"f_{obs} = f_{src} \frac{v + v_o}{v - v_s}",
            color="#C0CAF5",
            font_size=36,
        ).to_edge(UP, buff=0.6)

        # ------------------------------------------------------------------
        # 2. Animations  (total duration: 16 s)
        # ------------------------------------------------------------------
        # Phase A – Fade in stationary scene  (4 s)
        self.play(
            FadeIn(source_comb),
            FadeIn(observer_comb),
            FadeIn(source_label),
            FadeIn(observer_label),
            FadeIn(source_arrow),
            FadeIn(source_v_label),
            FadeIn(observer_arrow),
            FadeIn(observer_v_label),
            FadeIn(relative_arrow),
            FadeIn(relative_label),
            FadeIn(comb_rings),
            FadeIn(formula_hint),
            run_time=2,
        )
        self.wait(2)

        # Phase B – Move source right & observer left  (8 s)
        self.play(
            source_comb.animate.shift(RIGHT * 1.2),
            observer_comb.animate.shift(LEFT * 1.2),
            relative_arrow.animate.put_start_and_end_on(
                [-2.5 + 1.2, -1.2, 0], [2.5 - 1.2, -1.2, 0]
            ),
            source_arrow.animate.shift(RIGHT * 1.2),
            source_v_label.animate.shift(RIGHT * 1.2),
            observer_arrow.animate.shift(LEFT * 1.2),
            observer_v_label.animate.shift(LEFT * 1.2),
            comb_rings.animate.shift(RIGHT * 1.2),
            run_time=4,
            rate_func=smooth,
        )
        self.wait(2)

        self.play(
            source_comb.animate.shift(RIGHT * 0.3),
            observer_comb.animate.shift(LEFT * 0.3),
            relative_arrow.animate.put_start_and_end_on(
                [-2.5 + 1.5, -1.2, 0], [2.5 - 1.5, -1.2, 0]
            ),
            source_arrow.animate.shift(RIGHT * 0.3),
            source_v_label.animate.shift(RIGHT * 0.3),
            observer_arrow.animate.shift(LEFT * 0.3),
            observer_v_label.animate.shift(LEFT * 0.3),
            comb_rings.animate.shift(RIGHT * 0.3),
            run_time=2,
            rate_func=smooth,
        )
        self.wait(2)

        # Phase C – Emphasize changing separation  (4 s)
        self.play(
            Indicate(relative_arrow, color="#F7768E", scale_factor=1.1),
            Indicate(relative_label, color="#F7768E", scale_factor=1.05),
            run_time=1.5,
        )
        self.play(
            Circumscribe(formula_hint, shape=Rectangle, color="#E0AF68"),
            run_time=1.5,
        )
        self.wait(1)
        # --- Scene 8: General Doppler equation and direction sign convention ---
        self.camera.background_color = "#181825"
        self.clear()

        # 1. Central Doppler Formula Bar with color-coded terms
        formula = MathTex(
            r"f_{obs} = f_{emitted} \frac{v \pm v_o}{v \mp v_s}",
            font_size=48,
            color="#ECEFF4",
            substrings_to_isolate=[r"v_o", r"v_s", r"v"],
        )
        formula.move_to(UP * 1.2)
        formula.set_color_by_tex(r"v_o", "#94e2d5")
        formula.set_color_by_tex(r"v_s", "#f38ba8")
        formula.set_color_by_tex(r"v", "#fab387")

        # 2. NumberLine showing positive direction (source toward observer)
        direction_line = NumberLine(
            x_range=[-1, 1, 1], length=6, include_tip=True, color="#89b4fa"
        )
        direction_line.move_to(DOWN * 0.5)
        direction_line.add_numbers()

        # Positive arrow sits on the number line pointing right
        pos_arrow = Arrow(
            start=ORIGIN, end=RIGHT * 2.5, color="#a6e3a1", stroke_width=2.5, buff=0.2
        )
        pos_arrow.move_to(DOWN * 0.5)

        pos_label = Text("Source toward Observer", font_size=24, color="#a6e3a1")
        pos_label.next_to(direction_line, UP, buff=0.4)

        # 3. Legend boxes clarifying sign conventions
        box_vo = Rectangle(height=0.6, width=2.2, color="#94e2d5", stroke_width=2)
        label_vo = Text("v_o observer", font_size=22, color="#94e2d5")
        legend_vo = VGroup(box_vo, label_vo)
        legend_vo.move_to(LEFT * 3 + DOWN * 1.8)

        box_vs = Rectangle(height=0.6, width=2.2, color="#f38ba8", stroke_width=2)
        label_vs = Text("v_s source", font_size=22, color="#f38ba8")
        legend_vs = VGroup(box_vs, label_vs)
        legend_vs.move_to(DOWN * 1.8)

        box_v = Rectangle(height=0.6, width=2.2, color="#fab387", stroke_width=2)
        label_v = Text("v wave speed", font_size=22, color="#fab387")
        legend_v = VGroup(box_v, label_v)
        legend_v.move_to(RIGHT * 3 + DOWN * 1.8)

        # 4. Sign convention annotations
        approach_text = MathTex(
            r"	ext{Approach: } +v_o, -v_s", font_size=28, color="#a6e3a1"
        )
        approach_text.next_to(formula, UP, buff=0.6)

        recede_text = MathTex(
            r"	ext{Recede: } -v_o, +v_s", font_size=28, color="#f38ba8"
        )
        recede_text.next_to(formula, DOWN, buff=0.6)

        # --- ANIMATIONS (Total must equal 15.0s) ---
        # Phase 1: Write formula (2.0s)
        self.play(Write(formula), run_time=2.0)

        # Phase 2: Draw direction line + arrow + label (1.5s)
        self.play(
            Create(direction_line), FadeIn(pos_arrow), FadeIn(pos_label), run_time=1.5
        )

        # Phase 3: Show sign convention text (1.5s)
        self.play(
            FadeIn(approach_text, shift=UP * 0.2),
            FadeIn(recede_text, shift=DOWN * 0.2),
            run_time=1.5,
        )

        # Phase 4: Legend boxes stagger in (2.0s)
        self.play(
            LaggedStart(
                FadeIn(legend_vo, shift=UP * 0.2),
                FadeIn(legend_vs, shift=UP * 0.2),
                FadeIn(legend_v, shift=UP * 0.2),
                lag_ratio=0.3,
            ),
            run_time=2.0,
        )

        # Phase 5: Hold for reading and comprehension (8.0s)
        self.wait(8.0)

        # Total: 2.0 + 1.5 + 1.5 + 2.0 + 8.0 = 15.0 seconds
        # --- Scene 9: Everyday examples: siren and radar ---
        self.camera.background_color = "#181825"
        self.clear()

        # === 1. ROAD PLANE ===
        road_plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-4, 4, 1],
            x_length=14,
            y_length=7,
            background_line_style={
                "stroke_opacity": 0.2,
                "stroke_width": 1,
            },
            faded_line_ratio=2,
        )
        road_plane.set_color("#89b4fa")

        # === 2. OBSERVER ===
        observer = Dot(point=RIGHT * 4, radius=0.2, color="#94e2d5")
        observer_label = Text("Observer", font_size=24, color="#94e2d5").next_to(
            observer, DOWN, buff=0.2
        )

        # === 3. AMBULANCE ===
        ambulance_body = Rectangle(
            height=0.6,
            width=1.2,
            stroke_width=2,
            fill_opacity=0.6,
            color="#313244",
            fill_color="#313244",
        )
        ambulance_body.set_stroke("#f38ba8")
        ambulance_body.move_to(LEFT * 4)

        ambulance_light = Dot(point=LEFT * 4 + UP * 0.4, radius=0.12, color="#fab387")

        # === 4. RADAR INSET ===
        inset_frame = Rectangle(
            height=2.4, width=3.5, stroke_width=2, color="#89b4fa"
        ).move_to(RIGHT * 3.5 + UP * 3.2)

        radar_gun = Polygon(
            [4.0, 3.6, 0],
            [4.8, 3.6, 0],
            [4.8, 3.2, 0],
            [4.4, 3.0, 0],
            color="#fab387",
            stroke_width=2,
            fill_opacity=0.6,
            fill_color="#fab387",
        )

        radar_target = Dot(point=RIGHT * 5 + UP * 3.2, radius=0.15, color="#f38ba8")
        radar_target_label = Text("Car", font_size=20, color="#f38ba8").next_to(
            radar_target, RIGHT, buff=0.15
        )

        # Pulse arrows (initially hidden)
        radar_pulse_out = Arrow(
            start=[4.5, 3.2, 0],
            end=[6, 3.2, 0],
            buff=0.1,
            color="#a6e3a1",
            stroke_width=2,
        )
        radar_pulse_out.set_opacity(0)

        radar_pulse_back = Arrow(
            start=[6, 3.2, 0],
            end=[4.5, 3.2, 0],
            buff=0.1,
            color="#f38ba8",
            stroke_width=2,
        )
        radar_pulse_back.set_opacity(0)

        # Doppler labels
        compressed_label = Text("Compressed", font_size=18, color="#a6e3a1").move_to(
            RIGHT * 2 + UP * 2.8
        )
        stretched_label = Text("Stretched", font_size=18, color="#94e2d5").move_to(
            LEFT * 3 + UP * 2.8
        )

        # === PHASE 1: Setup (2s) ===
        self.play(
            FadeIn(road_plane),
            FadeIn(observer),
            FadeIn(observer_label),
            FadeIn(inset_frame),
            FadeIn(radar_gun),
            FadeIn(radar_target),
            FadeIn(radar_target_label),
            run_time=2,
        )

        # === PHASE 2: Ambulance + labels appear (1.5s) ===
        self.play(
            FadeIn(ambulance_body),
            FadeIn(ambulance_light),
            FadeIn(compressed_label),
            FadeIn(stretched_label),
            run_time=1.5,
        )

        # === PHASE 3: Ambulance movement + wave emission (10s) ===
        positions = [LEFT * 4, LEFT * 2, ORIGIN, RIGHT * 2, RIGHT * 4, RIGHT * 6]
        segment_time = 2.0

        for i in range(len(positions) - 1):
            start_pos = positions[i]
            end_pos = positions[i + 1]
            delta = end_pos - start_pos

            # Create a new wave ring at the ambulance's current position
            new_ring = Circle(radius=0.3, color="#a6e3a1", stroke_width=2).move_to(
                start_pos
            )
            self.add(new_ring)

            # Animate: move ambulance + expand ring
            self.play(
                ambulance_body.animate.shift(delta),
                ambulance_light.animate.shift(delta),
                new_ring.animate.scale(4).set_stroke(opacity=0.2),
                run_time=segment_time,
                rate_func=linear,
            )

        # === PHASE 4: Radar pulse animation (2s) ===
        self.play(
            radar_pulse_out.animate.set_opacity(1),
            run_time=0.4,
        )
        self.play(
            radar_pulse_out.animate.shift(RIGHT * 0.2),
            run_time=0.4,
        )
        self.play(
            radar_pulse_out.animate.set_opacity(0),
            radar_pulse_back.animate.set_opacity(1),
            run_time=0.4,
        )
        self.play(
            radar_pulse_back.animate.shift(LEFT * 0.2),
            run_time=0.4,
        )
        self.play(
            radar_pulse_back.animate.set_opacity(0),
            run_time=0.4,
        )

        self.remove(radar_pulse_out, radar_pulse_back)

        # === PHASE 5: Wait (2.5s) ===
        self.wait(2.5)
        # --- Scene 10: Universal principle: applies to all waves ---
        self.clear()
        self.camera.background_color = "#181825"

        # 1. Space axes (vast field)
        space_axes = Axes(
            x_range=[-10, 10],
            y_range=[-6, 6],
            x_length=16,
            y_length=9,
            axis_config={
                "stroke_opacity": 0.15,
                "stroke_width": 1,
                "color": "#89b4fa",
            },
        )

        # 2. Stars with subtle glow rings
        star_approach = Dot(point=LEFT * 5 + UP * 3, radius=0.22, color="#89b4fa")
        star_recede = Dot(point=RIGHT * 5 + UP * 3, radius=0.22, color="#f38ba8")

        glow_approach = Circle(radius=0.45, color="#89b4fa", stroke_width=1)
        glow_approach.set_stroke(opacity=0.3)
        glow_approach.move_to(star_approach.get_center())

        glow_recede = Circle(radius=0.45, color="#f38ba8", stroke_width=1)
        glow_recede.set_stroke(opacity=0.3)
        glow_recede.move_to(star_recede.get_center())

        approach_label = Text("Star", font_size=24, color="WHITE").next_to(
            star_approach, UP, buff=0.2
        )
        recede_label = Text("Star", font_size=24, color="WHITE").next_to(
            star_recede, UP, buff=0.2
        )

        # 3. Earth observer
        earth_dot = Dot(point=DOWN * 3, radius=0.22, color="#a6e3a1")
        earth_label = Text("Earth", font_size=24, color="WHITE").next_to(
            earth_dot, DOWN, buff=0.2
        )

        # 4. Wave rings
        # Blue-shifted (compressed) from left star
        br1 = Circle(radius=1.2, color="#89b4fa", stroke_width=2)
        br1.move_to(star_approach.get_center())
        br2 = Circle(radius=2.6, color="#89b4fa", stroke_width=2)
        br2.move_to(star_approach.get_center())

        # Red-shifted (stretched) from right star
        rr1 = Circle(radius=1.5, color="#f38ba8", stroke_width=2)
        rr1.move_to(star_recede.get_center())
        rr2 = Circle(radius=3.5, color="#f38ba8", stroke_width=2)
        rr2.move_to(star_recede.get_center())

        blue_rings = VGroup(br1, br2)
        red_rings = VGroup(rr1, rr2)

        # 5. Shift labels
        blue_shift_label = Text("Blue-shift", font_size=30, color="#89b4fa")
        blue_shift_label.move_to(LEFT * 2.5 + UP * 2.2)

        red_shift_label = Text("Red-shift", font_size=30, color="#f38ba8")
        red_shift_label.move_to(RIGHT * 2.5 + UP * 2.2)

        # 6. Faint light-path arrows
        blue_arrow = Arrow(
            start=star_approach.get_center(),
            end=earth_dot.get_center(),
            color="#89b4fa",
            stroke_width=2,
            buff=0.3,
        )
        blue_arrow.set_stroke(opacity=0.4)

        red_arrow = Arrow(
            start=star_recede.get_center(),
            end=earth_dot.get_center(),
            color="#f38ba8",
            stroke_width=2,
            buff=0.3,
        )
        red_arrow.set_stroke(opacity=0.4)

        # === ANIMATION SEQUENCE (total 20 s) ===

        # Phase 1: Draw axes + fade in stars + Earth labels  [0 – 4 s]
        self.play(Create(space_axes), run_time=2)
        self.play(
            AnimationGroup(
                FadeIn(star_approach, scale=1.5),
                FadeIn(glow_approach),
                FadeIn(star_recede, scale=1.5),
                FadeIn(glow_recede),
            ),
            run_time=1.5,
        )
        self.play(
            FadeIn(earth_dot, scale=1.5),
            FadeIn(earth_label),
            FadeIn(approach_label),
            FadeIn(recede_label),
            run_time=1.0,
        )
        self.wait(0.5)

        # Phase 2: Stars emit expanding rings  [4 – 10 s]
        self.play(
            AnimationGroup(
                Succession(
                    GrowFromCenter(br1, run_time=1.5),
                    GrowFromCenter(br2, run_time=1.5),
                ),
                Succession(
                    GrowFromCenter(rr1, run_time=2.0),
                    GrowFromCenter(rr2, run_time=2.0),
                ),
                lag_ratio=0.2,
            ),
            run_time=4,
        )
        self.wait(1.0)

        # Phase 3: Light-path arrows appear  [10 – 12 s]
        self.play(FadeIn(blue_arrow), FadeIn(red_arrow), run_time=1.5)
        self.wait(0.5)

        # Phase 4: Color-coded labels appear  [12 – 16 s]
        self.play(
            FadeIn(blue_shift_label, shift=UP * 0.3),
            FadeIn(red_shift_label, shift=UP * 0.3),
            run_time=2.0,
        )
        self.wait(1.0)

        # Phase 5: Crests pulse near Earth  [16 – 18 s]
        self.play(
            AnimationGroup(
                Indicate(br2, color="#89b4fa", scale_factor=1.05),
                Indicate(rr2, color="#f38ba8", scale_factor=1.05),
                Indicate(earth_dot, color="#a6e3a1", scale_factor=1.2),
            ),
            run_time=1.5,
        )
        self.wait(0.5)

        # Phase 6: Labels flash, hold  [18 – 20 s]
        self.play(
            AnimationGroup(
                Indicate(blue_shift_label, color="WHITE", scale_factor=1.1),
                Indicate(red_shift_label, color="WHITE", scale_factor=1.1),
            ),
            run_time=1.5,
        )
        self.wait(1.5)
