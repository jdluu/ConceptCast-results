import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: The Static Emitter ---
        # Use the background color from the style guidelines
        self.camera.background_color = "#181825"

        # --- Source (Glowing Pulsating Dot) ---
        source = Dot(point=ORIGIN, radius=0.15, color="#88C0D0")

        # --- Wavefronts (Concentric Expanding Rings) ---
        # Create multiple rings for the "emanating" effect
        wavefronts = VGroup(
            *[
                Circle(radius=r, color="#81A1C1", stroke_opacity=0.6, stroke_width=2)
                for r in np.arange(0.5, 3.0, 0.5)
            ]
        )

        # --- Timeline (Bottom Axis) ---
        timeline = NumberLine(x_range=[-5, 5, 1], length=10, color="#D8DEE9").shift(
            DOWN * 3
        )

        # Add "Time" label to the timeline
        time_label = Text("Time", font_size=24, color="#D8DEE9").next_to(
            timeline, DOWN, buff=0.2
        )

        # --- Animations ---

        # 1. Fade in source and timeline
        self.play(FadeIn(source), FadeIn(timeline), FadeIn(time_label))

        # 2. Pulse the source and create the wavefronts
        self.play(GrowFromCenter(source), run_time=0.5)

        # 3. Create wavefronts sequentially (ripple effect)
        self.play(
            LaggedStart(
                *[Create(wave) for wave in wavefronts], lag_ratio=0.5, run_time=2.0
            )
        )

        # 4. Animate the wavefronts expanding outward over the duration
        self.play(
            *[wave.animate.scale(2) for wave in wavefronts],
            run_time=3.0,
            rate_func=linear,
        )

        # Hold the final frame
        self.wait(1)
        # --- Scene 2: The Static Observer ---
        self.clear()
        self.camera.background_color = "#181825"

        # === OBJECTS ===

        # Source at origin
        source_dot = Dot(point=ORIGIN, radius=0.1, color="#81A1C1")
        source_label = Text("Source", font_size=20, color="#81A1C1").next_to(
            source_dot, DOWN, buff=0.25
        )

        # Observer at RIGHT * 4
        observer_pos = RIGHT * 4
        observer_dot = Dot(point=observer_pos, radius=0.15, color="#EBCB8B")
        observer_label = Text("Observer", font_size=20, color="#EBCB8B").next_to(
            observer_dot, DOWN, buff=0.25
        )

        # Ear icon (concentric arcs suggesting an ear)
        ear_inner = Arc(
            radius=0.2,
            start_angle=-PI / 3,
            angle=2 * PI / 3,
            color="#EBCB8B",
            stroke_width=3,
        ).move_arc_center_to(observer_dot.get_center() + UP * 0.35)
        ear_outer = Arc(
            radius=0.32,
            start_angle=-PI / 2.5,
            angle=2 * PI / 2.5,
            color="#EBCB8B",
            stroke_width=2.5,
        ).move_arc_center_to(observer_dot.get_center() + UP * 0.3)
        ear_group = VGroup(ear_outer, ear_inner)

        # Oscilloscope Axes - constant sine wave display
        axes = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-1, 1, 0.5],
            x_length=2.0,
            y_length=1.2,
            axis_config={
                "color": "#A3BE8C",
                "stroke_width": 1.0,
                "include_numbers": False,
            },
            tips=False,
        )
        axes.move_to(RIGHT * 4 + UP * 2.0)

        sine_wave = axes.plot(
            lambda x: 0.7 * np.sin(2 * PI * x),
            x_range=[0, 2],
            color="#A3BE8C",
            stroke_width=2.5,
        )

        freq_label = Text("Steady Pitch", font_size=16, color="#A3BE8C").next_to(
            axes, UP, buff=0.1
        )

        scope_bg = SurroundingRectangle(
            VGroup(axes, freq_label),
            color="#A3BE8C",
            buff=0.12,
            corner_radius=0.1,
            stroke_width=1.5,
            stroke_opacity=0.5,
        )

        # Dashed line from source to observer showing the path
        path_line = DashedLine(
            ORIGIN, observer_pos, color="#4C566A", stroke_width=1, dash_length=0.15
        )

        # === ANIMATIONS ===
        # Total duration: 7.5s

        # Phase 1: Setup source and observer (0s - 2.0s)
        self.play(
            Create(path_line),
            FadeIn(source_dot, scale=0.5),
            Write(source_label),
            run_time=1.0,
        )
        self.play(
            FadeIn(observer_dot, scale=0.5),
            FadeIn(ear_group),
            Write(observer_label),
            run_time=1.0,
        )

        # Phase 2: Show oscilloscope (2.0s - 3.5s)
        self.play(Create(scope_bg), Create(axes), run_time=0.8)
        self.play(Create(sine_wave), Write(freq_label), run_time=0.7)

        # Phase 3: Expanding wavefronts pass through observer (3.5s - 7.5s = 4.0s)
        wave_color = "#81A1C1"
        num_waves = 5

        wave_anims = []
        for i in range(num_waves):
            w = Circle(
                radius=0.08, color=wave_color, stroke_width=2.5, stroke_opacity=0.85
            ).move_to(ORIGIN)
            # Scale from radius 0.08 to ~4.5 => scale factor ~56
            wave_anims.append(w.animate.scale(56).set_opacity(0))

        # LaggedStart: waves expand from source at regular intervals
        # lag_ratio=0.45 with 5 waves gives ~1s spacing between wave starts
        self.play(
            LaggedStart(*wave_anims, lag_ratio=0.45, rate_func=linear), run_time=4.0
        )

        # Timing verification: 1.0 + 1.0 + 0.8 + 0.7 + 4.0 = 7.5s ✓
        # --- Scene 3: Source Approaching ---
        # Background
        self.camera.background_color = "#181825"

        # ─── 1. Observer (stationary on right) ───
        observer = Dot(point=RIGHT * 4, radius=0.12, color="#a6e3a1")
        observer_label = Text("Observer", font_size=24, color="#a6e3a1").next_to(
            observer, DOWN, buff=0.25
        )

        # ─── 2. Moving source ───
        source = Dot(point=LEFT * 3, radius=0.15, color="#88C0D0")
        source_label = Text("Source", font_size=24, color="#88C0D0").next_to(
            source, DOWN, buff=0.25
        )
        source_label.add_updater(lambda m: m.next_to(source, DOWN, buff=0.25))

        # ─── 3. Trail positions for wave emission ───
        trail_positions = [LEFT * 3, LEFT * 2.2, LEFT * 1.4, LEFT * 0.6]

        # ─── 4. Wavefront data: center, radius, opacity ───
        wavefront_data = [
            {"center": LEFT * 3, "radius": 2.8, "opacity": 0.25},
            {"center": LEFT * 2.2, "radius": 2.1, "opacity": 0.35},
            {"center": LEFT * 1.4, "radius": 1.4, "opacity": 0.5},
            {"center": LEFT * 0.6, "radius": 0.7, "opacity": 0.7},
        ]

        # ─── 5. Brace showing compression on the right side ───
        compression_brace = BraceBetweenPoints(
            LEFT * 0.15, RIGHT * 0.85, direction=DOWN, color="#BF616A"
        )
        compression_label = Text("Compression", font_size=20, color="#BF616A").next_to(
            compression_brace, DOWN, buff=0.15
        )

        # ─── 6. Brace showing spread on the left side ───
        spread_brace = BraceBetweenPoints(
            LEFT * 2.5, LEFT * 0.9, direction=UP, color="#a6e3a1"
        )
        spread_label = Text("Spread out", font_size=20, color="#a6e3a1").next_to(
            spread_brace, UP, buff=0.15
        )

        # ─── 7. Title ───
        title = Text(
            "Source Approaching Observer", font_size=30, color="#ECEFF4"
        ).to_edge(UP, buff=0.3)

        # ═══════════════════════════════════════════════
        # ANIMATION SEQUENCE  (total = 8.5 s)
        # ═══════════════════════════════════════════════

        # 0) Title & static elements  (0.8 + 0.7 = 1.5 s)
        self.play(Write(title), run_time=0.8)
        self.play(
            FadeIn(observer, shift=UP * 0.2), FadeIn(observer_label), run_time=0.7
        )

        # 1) Source appears and first wavefront  (0.4 + 0.6 = 1.0 s)
        self.play(FadeIn(source, shift=RIGHT * 0.2), FadeIn(source_label), run_time=0.4)
        first_wf = (
            Circle(radius=0.4, color="#81A1C1", stroke_width=2.0)
            .move_to(LEFT * 3)
            .set_opacity(0.8)
        )
        self.play(Create(first_wf), run_time=0.6)

        # 2) Source moves right, emits wavefronts along the way  (0.7 + 0.7 + 0.7 = 2.1 s)
        wavefront_circles = VGroup(first_wf)

        for i in range(1, len(trail_positions)):
            pos = trail_positions[i]
            wf = wavefront_data[i]

            trail_dot = Dot(
                point=trail_positions[i - 1], radius=0.06, color="#88C0D0"
            ).set_opacity(0.3 + 0.15 * (i - 1))
            wf_circle = (
                Circle(
                    radius=wf["radius"],
                    color="#81A1C1",
                    stroke_width=2.0,
                )
                .move_to(wf["center"])
                .set_opacity(wf["opacity"])
            )

            self.play(
                source.animate.move_to(pos),
                FadeIn(trail_dot),
                FadeIn(wf_circle),
                run_time=0.7,
            )
            wavefront_circles.add(wf_circle)

        # Brief pause  (0.5 s)
        self.wait(0.5)

        # 3) Show compression brace on the right  (1.0 s)
        self.play(
            GrowFromCenter(compression_brace),
            FadeIn(compression_label, shift=DOWN * 0.15),
            run_time=1.0,
        )

        # 4) Show spread brace on the left  (1.0 s)
        self.play(
            GrowFromCenter(spread_brace),
            FadeIn(spread_label, shift=UP * 0.15),
            run_time=1.0,
        )

        # 5) Final hold  (1.4 s)
        self.wait(1.4)
        # --- Scene 4: The Blue Shift (Higher Pitch) ---
        # Configuration
        bg_color = "#181825"
        self.camera.background_color = bg_color
        observer_color = "#EBCB8B"
        wave_color = "#81A1C1"
        scope_color = "#BF616A"
        text_color = "#ECEFF4"

        # 1. Observer (Zoom Target)
        observer = Dot(RIGHT * 4, radius=0.2, color=observer_color, z_index=10)
        observer_label = Text("Observer", font_size=24, color=observer_color).next_to(
            observer, DOWN
        )

        # 2. High Frequency Waves (Compressed Wavefronts)
        wave_group = VGroup()
        for i in range(12):
            x_pos = -6 + i * 0.7  # Tighter spacing for high freq appearance
            dash = DashedLine(
                start=[x_pos, -3, 0],
                end=[x_pos, 3, 0],
                color=wave_color,
                stroke_width=2.0,
            )
            wave_group.add(dash)

        # 3. Oscilloscope (High Frequency Sine Wave)
        scope_axes = Axes(
            x_range=[0, 4 * PI, PI / 2],
            y_range=[-1, 1, 0.5],
            x_length=2.5,
            y_length=1.0,
            axis_config={"color": scope_color, "stroke_width": 1.5},
            tips=False,
        )

        high_freq_graph = scope_axes.plot(
            lambda x: np.sin(5 * x),  # Higher frequency for visual impact
            color=scope_color,
            stroke_width=2.5,
        )

        scope_box = SurroundingRectangle(
            scope_axes, color=scope_color, buff=0.15, stroke_width=1.5
        )
        scope_label = Text("Oscilloscope", font_size=18, color=scope_color).next_to(
            scope_box, UP, buff=0.1
        )
        scope_group = VGroup(scope_axes, high_freq_graph, scope_box, scope_label)

        # 4. Text Label
        label = Text("Higher f", font_size=42, color=text_color, weight=BOLD)

        # --- Animations ---
        # Timeline: 7.5 seconds total

        # 1. Initial setup: Show observer and waves (1.0s)
        self.play(FadeIn(observer), FadeIn(observer_label), run_time=0.5)
        self.play(FadeIn(wave_group), run_time=0.5)

        # 2. Zoom In Effect (1.5s)
        # Scale everything up, centering on observer
        all_elements = VGroup(wave_group, observer, observer_label)
        self.play(
            all_elements.animate.scale(2.0, about_point=observer.get_center()).shift(
                LEFT * 2
            ),
            run_time=1.5,
            rate_func=smooth,
        )

        # 3. Animate waves passing through rapidly (1.5s total)
        # Multiple quick passes to show high frequency
        for _ in range(5):
            self.play(
                wave_group.animate.shift(RIGHT * 0.7), run_time=0.3, rate_func=linear
            )

        # 4. Show oscilloscope and label (1.5s)
        scope_group.move_to(UP * 2.5 + LEFT * 1)
        label.next_to(scope_group, DOWN, buff=0.3)

        self.play(FadeIn(scope_group, shift=UP * 0.3), run_time=0.75)
        self.play(
            Write(label),
            Indicate(label, color=scope_color, scale_factor=1.1),
            run_time=0.75,
        )

        # 5. Pulse the graph to emphasize high frequency (1.0s)
        self.play(
            Circumscribe(
                high_freq_graph, color=scope_color, time_width=1.5, stroke_width=3
            ),
            run_time=1.0,
        )

        # 6. Final wait (1.0s)
        self.wait(1.0)
        # --- Scene 5: Source Receding ---
        # --- Background ---
        self.camera.background_color = "#181825"

        # --- Title ---
        title = Text("Source Receding from Observer", font_size=36, color="#CDD6F4")
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)

        # --- Fixed Observer ---
        observer = Dot(LEFT * 4.5, radius=0.15, color="#fab387")
        obs_label = Text("Observer", font_size=22, color="#fab387").next_to(
            observer, DOWN, buff=0.25
        )
        self.play(FadeIn(observer), FadeIn(obs_label), run_time=0.4)

        # --- Moving Source (starts near origin, moves right) ---
        source = Dot(LEFT * 1, radius=0.15, color="#88C0D0")
        src_label = Text("Source", font_size=22, color="#88C0D0").next_to(
            source, UP, buff=0.25
        )
        self.play(FadeIn(source), FadeIn(src_label), run_time=0.4)

        # Emission points with increasing spacing to show redshift effect
        emission_points = [
            LEFT * 1,  # 0
            LEFT * 0.2,  # 0.8 gap
            RIGHT * 0.8,  # 1.0 gap
            RIGHT * 2.0,  # 1.2 gap
            RIGHT * 3.5,  # 1.5 gap
            RIGHT * 5.0,  # 1.5 gap
        ]

        wave_colors = ["#81A1C1", "#88C0D0", "#89B4FA", "#74C7EC", "#8AADF4"]

        # --- Phase 1: Emit wave0 at start position ---
        wave0 = Circle(
            radius=0.01, color=wave_colors[0], stroke_width=2, stroke_opacity=0.8
        ).move_to(emission_points[0])
        self.add(wave0)

        self.play(
            source.animate.move_to(emission_points[1]),
            src_label.animate.next_to(emission_points[1], UP, buff=0.25),
            wave0.animate.scale(60).set_stroke(opacity=0.3),
            run_time=0.8,
            rate_func=smooth,
        )

        # --- Phase 2: Emit wave1, expand previous ---
        wave1 = Circle(
            radius=0.01, color=wave_colors[1], stroke_width=2, stroke_opacity=0.8
        ).move_to(emission_points[1])
        self.add(wave1)

        self.play(
            source.animate.move_to(emission_points[2]),
            src_label.animate.next_to(emission_points[2], UP, buff=0.25),
            wave1.animate.scale(50).set_stroke(opacity=0.35),
            wave0.animate.set_stroke(opacity=0.15),
            run_time=0.9,
            rate_func=smooth,
        )

        # --- Phase 3: Emit wave2, expand previous ---
        wave2 = Circle(
            radius=0.01, color=wave_colors[2], stroke_width=2, stroke_opacity=0.8
        ).move_to(emission_points[2])
        self.add(wave2)

        self.play(
            source.animate.move_to(emission_points[3]),
            src_label.animate.next_to(emission_points[3], UP, buff=0.25),
            wave2.animate.scale(40).set_stroke(opacity=0.35),
            wave0.animate.set_stroke(opacity=0.08),
            wave1.animate.set_stroke(opacity=0.18),
            run_time=1.0,
            rate_func=smooth,
        )

        # --- Phase 4: Emit wave3, expand ---
        wave3 = Circle(
            radius=0.01, color=wave_colors[3], stroke_width=2, stroke_opacity=0.8
        ).move_to(emission_points[3])
        self.add(wave3)

        self.play(
            source.animate.move_to(emission_points[4]),
            src_label.animate.next_to(emission_points[4], UP, buff=0.25),
            wave3.animate.scale(30).set_stroke(opacity=0.4),
            wave1.animate.set_stroke(opacity=0.08),
            wave2.animate.set_stroke(opacity=0.2),
            run_time=1.0,
            rate_func=smooth,
        )

        # --- Phase 5: Emit wave4, final move ---
        wave4 = Circle(
            radius=0.01, color=wave_colors[4], stroke_width=2, stroke_opacity=0.8
        ).move_to(emission_points[4])
        self.add(wave4)

        self.play(
            source.animate.move_to(emission_points[5]),
            src_label.animate.next_to(emission_points[5], UP, buff=0.25),
            wave4.animate.scale(25).set_stroke(opacity=0.45),
            wave2.animate.set_stroke(opacity=0.1),
            wave3.animate.set_stroke(opacity=0.25),
            run_time=1.0,
            rate_func=smooth,
        )

        # --- Phase 6: Show expansion brace on observer side ---
        brace_left = observer.get_center() + UP * 1.8 + RIGHT * 0.3
        brace_right_pt = observer.get_center() + UP * 1.8 + RIGHT * 2.5

        brace = BraceBetweenPoints(
            brace_left, brace_right_pt, direction=UP, color="#A3BE8C"
        )
        brace_label = brace.get_text("Stretched\nWavelength")

        self.play(FadeIn(brace), Write(brace_label), run_time=0.9)
        # --- Scene 6: The Red Shift (Lower Pitch) ---
        self.clear()
        # Palette & Theme
        self.camera.background_color = "#181825"
        COL_OBS = "#EBCB8B"  # Observer Yellow
        COL_WAVE = "#B48EAD"  # Wavefront Mauve
        COL_SIGNAL = "#89b4fa"  # Signal Blue
        COL_AXIS = "#6272A4"

        # --- 1. Objects ---

        # Observer (focused on left)
        observer = Dot(LEFT * 3, radius=0.2, color=COL_OBS)
        observer_label = Text("Observer", font_size=20, color=COL_OBS).next_to(
            observer, DOWN, buff=0.2
        )

        # Zoom Focus Ring (visual cue for "ZoomIn effect focuses on Observer")
        focus_ring = Circle(radius=0.4, color=WHITE, stroke_opacity=0.6).move_to(
            observer.get_center()
        )

        # Oscilloscope (above observer)
        oscilloscope = Axes(
            x_range=[0, 2, 1],
            y_range=[-1, 1, 1],
            x_length=3.5,
            y_length=1.5,
            tips=False,
            axis_config={"color": COL_AXIS},
        ).move_to(LEFT * 3 + UP * 2.5)

        osc_box = SurroundingRectangle(oscilloscope, color=COL_AXIS, buff=0.1)
        osc_title = Text(
            "Low Frequency Waveform", font_size=16, color=COL_AXIS
        ).next_to(osc_box, UP, buff=0.1)

        # Low Frequency Wave (visually stretched — long wavelength)
        # sin(PI * x) has period = 2, showing a clearly stretched low-frequency wave
        low_freq_wave = oscilloscope.plot(
            lambda x: 0.8 * np.sin(PI * x),
            x_range=[0, 2],
            color=COL_SIGNAL,
            stroke_width=3,
        )

        # Stretched Wavefronts (Dashed Lines with wide spacing)
        wavefronts = VGroup()
        for i in range(4):
            w = DashedLine(
                start=RIGHT * (3 + i * 2.0) + UP * 3,
                end=RIGHT * (3 + i * 2.0) + DOWN * 3,
                color=COL_WAVE,
                dash_length=0.3,
                stroke_width=2,
            )
            wavefronts.add(w)

        # "Lower f" label
        lower_f_label = Text("Lower f", font_size=36, color=COL_SIGNAL).to_edge(RIGHT)

        # --- 2. Animations (total: 6.0s) ---

        # A. ZoomIn / Focus on Observer (0.0s - 1.0s)
        self.play(FadeIn(observer, scale=2), Write(observer_label), run_time=0.7)
        self.play(
            FadeIn(oscilloscope), FadeIn(osc_box), FadeIn(osc_title), run_time=0.3
        )

        # B. Expanding pulse ring effect (1.0s - 1.5s)
        self.play(focus_ring.animate.scale(2).set_opacity(0), run_time=0.5)

        # C. Stretched wavefronts pass slowly through observer (1.5s - 4.5s)
        # Slow movement = low frequency / red-shift visual metaphor
        self.play(wavefronts.animate.shift(LEFT * 12), run_time=3.0, rate_func=linear)

        # D. Oscilloscope updates with low-frequency trace + "Lower f" label (4.5s - 5.5s)
        self.play(Create(low_freq_wave), FadeIn(lower_f_label), run_time=1.0)

        # E. Final hold (5.5s - 6.0s)
        self.wait(0.5)
        # --- Scene 7: Observer Approaching Source ---
        self.camera.background_color = "#2E3440"

        # Colors from Nord palette
        C_CYAN = "#88C0D0"
        C_BLUE = "#81A1C1"
        C_GREEN = "#A3BE8C"
        C_YELLOW = "#EBCB8B"
        C_RED = "#BF616A"
        C_WHITE = "#ECEFF4"
        C_GREY = "#D8DEE9"

        # --- 1. Title ---
        title = Text("Observer Approaching Source", font_size=48, color=C_WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.5)
        self.wait(0.3)

        # --- 2. Source at Origin ---
        source = Dot(ORIGIN, radius=0.15, color=C_CYAN)
        source_label = Text("Static Source", font_size=28, color=C_CYAN)
        source_label.next_to(source, DOWN, buff=0.4)
        self.play(FadeIn(source), FadeIn(source_label), run_time=0.4)

        # --- 3. Stationary Wavefronts ---
        wavefronts = VGroup()
        for i in range(4):
            radius = 1.0 + i * 0.8
            wave = Circle(
                radius=radius, color=C_BLUE, stroke_width=1.5, stroke_opacity=0.6
            )
            wave.move_to(ORIGIN)
            wavefronts.add(wave)

        self.play(
            LaggedStart(*[Create(w) for w in wavefronts], lag_ratio=0.15, run_time=1.5)
        )

        # --- 4. Moving Observer ---
        observer_start = RIGHT * 4
        observer = Dot(observer_start, radius=0.15, color=C_YELLOW)
        observer_label = Text("Moving Observer", font_size=28, color=C_YELLOW)
        observer_label.next_to(observer, UP, buff=0.4)

        vel_arrow = Arrow(
            observer.get_center() + RIGHT * 0.8,
            observer.get_center(),
            buff=0,
            color=C_YELLOW,
            stroke_width=4,
            tip_length=0.2,
        )
        vel_label = Text("v_obs", font_size=24, color=C_YELLOW)
        vel_label.next_to(vel_arrow, UP, buff=0.2)

        self.play(
            FadeIn(observer),
            FadeIn(vel_arrow),
            FadeIn(observer_label),
            FadeIn(vel_label),
            run_time=0.4,
        )

        # --- 5. Move Observer Toward Source ---
        target_point = RIGHT * 1.5

        vel_arrow.add_updater(
            lambda m: m.become(
                Arrow(
                    observer.get_center() + RIGHT * 0.8,
                    observer.get_center(),
                    buff=0,
                    color=C_YELLOW,
                    stroke_width=4,
                    tip_length=0.2,
                )
            )
        )
        observer_label.add_updater(lambda m: m.next_to(observer, UP, buff=0.4))

        self.play(
            observer.animate.move_to(target_point), run_time=2.0, rate_func=linear
        )

        vel_arrow.clear_updaters()
        observer_label.clear_updaters()
        self.play(FadeOut(vel_arrow), FadeOut(vel_label), run_time=0.3)

        # --- 6. Relative Velocity Decomposition ---
        base_point = observer.get_center() + UP * 1.5

        c_arrow = Arrow(
            base_point + RIGHT * 1.5,
            base_point + RIGHT * 0.2,
            buff=0,
            color=C_CYAN,
            stroke_width=5,
            tip_length=0.25,
        )
        c_label = MathTex("c", font_size=36, color=C_CYAN)
        c_label.next_to(c_arrow, UP, buff=0.2)
        self.play(GrowArrow(c_arrow), FadeIn(c_label), run_time=0.5)

        v_arrow = Arrow(
            base_point + RIGHT * 0.2,
            base_point + LEFT * 0.8,
            buff=0,
            color=C_YELLOW,
            stroke_width=5,
            tip_length=0.25,
        )
        v_label = MathTex("v_{obs}", font_size=36, color=C_YELLOW)
        v_label.next_to(v_arrow, UP, buff=0.2)

        plus_sign = MathTex("+", font_size=40, color=C_WHITE)
        plus_sign.move_to(base_point + RIGHT * 1.8)
        self.play(GrowArrow(v_arrow), FadeIn(v_label), FadeIn(plus_sign), run_time=0.5)

        total_arrow = Arrow(
            base_point + RIGHT * 1.5,
            base_point + LEFT * 0.8,
            buff=0,
            color=C_RED,
            stroke_width=6,
            tip_length=0.3,
        )
        total_label = MathTex("c + v_{obs}", font_size=36, color=C_RED)
        total_label.next_to(total_arrow, DOWN, buff=0.3)
        self.play(GrowArrow(total_arrow), FadeIn(total_label), run_time=0.4)

        # --- 7. Result ---
        result = Text("Higher Perceived Frequency!", font_size=38, color=C_GREEN)
        result_box = SurroundingRectangle(
            result, color=C_GREEN, buff=0.2, corner_radius=0.1
        )
        result_group = VGroup(result, result_box)
        result_group.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(result_group, scale=0.9), run_time=0.5)

        # --- 8. Narration ---
        narration = Text(
            "The observer meets waves more frequently, higher pitch",
            font_size=26,
            color=C_GREY,
        )
        narration.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(narration, shift=UP * 0.2), run_time=0.5)

        # --- 9. Hold and Fade ---
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)
        # --- Scene 8: The Doppler Formula ---
        # Background
        self.camera.background_color = "#181825"

        # Title
        title = Text("The Doppler Formula", font_size=48, color="#88C0D0")
        title.to_edge(UP, buff=0.5)

        # Central Doppler Formula
        doppler_eq = MathTex(
            r"f' = f \left( \frac{v \pm v_o}{v \mp v_s} \right)",
            font_size=64,
            color="#ECEFF4",
        )
        doppler_eq.move_to(UP * 0.5)

        # Table setup (Manual VGroup for reliable layout)
        h1 = Text("Motion", font_size=24, color="#EBCB8B")
        h2 = Text("Observer (v_o)", font_size=24, color="#88C0D0")
        h3 = Text("Source (v_s)", font_size=24, color="#81A1C1")

        r1_label = Text("Approaching", font_size=22, color="#A3BE8C")
        r1_obs = MathTex(r"+", color="#A3BE8C", font_size=36)
        r1_src = MathTex(r"-", color="#A3BE8C", font_size=36)

        r2_label = Text("Receding", font_size=22, color="#BF616A")
        r2_obs = MathTex(r"-", color="#BF616A", font_size=36)
        r2_src = MathTex(r"+", color="#BF616A", font_size=36)

        header = VGroup(h1, h2, h3).arrange(RIGHT, buff=1.0)
        row1 = VGroup(r1_label, r1_obs, r1_src).arrange(RIGHT, buff=1.6)
        row2 = VGroup(r2_label, r2_obs, r2_src).arrange(RIGHT, buff=1.6)

        row1[1].align_to(header[1], LEFT)
        row1[2].align_to(header[2], LEFT)
        row2[1].align_to(header[1], LEFT)
        row2[2].align_to(header[2], LEFT)

        table_content = VGroup(header, row1, row2).arrange(DOWN, buff=0.5)
        table_content.move_to(DOWN * 1.8)

        table_bg = BackgroundRectangle(
            table_content,
            color="#2E3440",
            fill_opacity=0.9,
            buff=0.4,
            corner_radius=0.15,
        )
        table_frame = SurroundingRectangle(
            table_content, color="#4C566A", buff=0.4, corner_radius=0.15
        )

        table_label = Text("Sign Convention", font_size=20, color="#D8DEE9")
        table_label.next_to(table_frame, UP, buff=0.15)

        approach_arrow = Arrow(
            start=LEFT * 0.6,
            end=RIGHT * 0.6,
            color="#A3BE8C",
            stroke_width=3,
            buff=0,
            tip_length=0.15,
        ).next_to(r1_label, LEFT, buff=0.3)

        recede_arrow = Arrow(
            start=RIGHT * 0.6,
            end=LEFT * 0.6,
            color="#BF616A",
            stroke_width=3,
            buff=0,
            tip_length=0.15,
        ).next_to(r2_label, LEFT, buff=0.3)

        # ---- ANIMATIONS ----
        self.play(Write(title), run_time=1.0)
        self.play(GrowFromCenter(doppler_eq), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(table_bg), Create(table_frame), run_time=0.5)
        self.play(Write(table_label), run_time=0.5)
        self.play(
            LaggedStart(
                FadeIn(header, shift=DOWN * 0.2),
                FadeIn(r1_label),
                FadeIn(approach_arrow),
                FadeIn(r1_obs),
                FadeIn(r1_src),
                lag_ratio=0.2,
            ),
            run_time=1.5,
        )
        self.play(
            LaggedStart(
                FadeIn(r2_label),
                FadeIn(recede_arrow),
                FadeIn(r2_obs),
                FadeIn(r2_src),
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )
        self.play(
            Circumscribe(doppler_eq, color="#EBCB8B", time_width=1.5), run_time=1.0
        )
        self.wait(1.0)
        # --- Scene 9: Real World: The Ambulance ---
        self.clear()
        # --- Color Palette (Nord) ---
        bg_color = "#181825"
        ambulance_color = "#BF616A"
        listener_color = "#EBCB8B"
        high_pitch_color = "#81A1C1"
        low_pitch_color = "#B48EAD"
        text_color = "#ECEFF4"
        secondary_text = "#D8DEE9"
        wheel_color = "#4C566A"
        transition_color = "#D08770"

        self.camera.background_color = bg_color

        # --- Title ---
        title = Text(
            "The Doppler Effect: Ambulance Siren", font_size=32, color=text_color
        ).to_edge(UP, buff=0.4)

        # --- Ambulance ---
        body = RoundedRectangle(
            corner_radius=0.1,
            width=2.5,
            height=1,
            color=ambulance_color,
            fill_opacity=0.9,
        )
        cabin = Polygon(
            [1.25, 0.5, 0],
            [1.25, -0.1, 0],
            [1.7, -0.4, 0],
            [1.7, 0.5, 0],
            color=ambulance_color,
            fill_opacity=0.9,
        )
        h_bar = Rectangle(width=0.6, height=0.15, color=WHITE, fill_opacity=1)
        v_bar = Rectangle(width=0.15, height=0.6, color=WHITE, fill_opacity=1)
        cross = VGroup(h_bar, v_bar).move_to(body.get_center())
        wheel1 = Circle(radius=0.18, color=wheel_color, fill_opacity=1).move_to(
            body.get_bottom() + UP * 0.18 + LEFT * 0.6
        )
        wheel2 = Circle(radius=0.18, color=wheel_color, fill_opacity=1).move_to(
            body.get_bottom() + UP * 0.18 + RIGHT * 0.6
        )
        ambulance = VGroup(body, cabin, cross, wheel1, wheel2).move_to(
            LEFT * 7 + DOWN * 0.2
        )

        # --- Listener ---
        listener_head = Circle(
            radius=0.12, color=listener_color, fill_opacity=1
        ).move_to(ORIGIN + UP * 0.15)
        listener_body = Line(
            ORIGIN + UP * 0.03,
            ORIGIN + DOWN * 0.35,
            color=listener_color,
            stroke_width=3,
        )
        listener = VGroup(listener_head, listener_body).move_to(ORIGIN + DOWN * 0.3)
        listener_label = Text("Listener", font_size=22, color=listener_color).next_to(
            listener, DOWN, buff=0.15
        )

        # --- Ground ---
        ground = Line(
            LEFT * 7.5, RIGHT * 7.5, color=secondary_text, stroke_width=1
        ).move_to(DOWN * 0.75)

        # --- Frequency Graphs ---
        # High Pitch (Approaching)
        axes_high = Axes(
            x_range=[0, 4, 1],
            y_range=[-1, 1, 1],
            x_length=3.5,
            y_length=1.0,
            tips=False,
            axis_config={"color": secondary_text, "stroke_width": 1},
        ).move_to(LEFT * 3.2 + DOWN * 2.8)
        high_label = Text(
            "High Pitch (Approaching)", font_size=18, color=high_pitch_color
        ).next_to(axes_high, UP, buff=0.1)
        high_graph = axes_high.plot(
            lambda x: 0.7 * np.sin(14 * x), color=high_pitch_color, stroke_width=3
        )
        high_group = VGroup(axes_high, high_label, high_graph)

        # Low Pitch (Receding)
        axes_low = Axes(
            x_range=[0, 4, 1],
            y_range=[-1, 1, 1],
            x_length=3.5,
            y_length=1.0,
            tips=False,
            axis_config={"color": secondary_text, "stroke_width": 1},
        ).move_to(RIGHT * 3.2 + DOWN * 2.8)
        low_label = Text(
            "Low Pitch (Receding)", font_size=18, color=low_pitch_color
        ).next_to(axes_low, UP, buff=0.1)
        low_graph = axes_low.plot(
            lambda x: 0.7 * np.sin(5 * x), color=low_pitch_color, stroke_width=3
        )
        low_group = VGroup(axes_low, low_label, low_graph)

        # --- Wavefronts ---
        waves = VGroup()

        # ================================================================
        # TIMELINE (Total = 8.5s)
        # play: 0.5+0.5+0.4+(0.45×4)+0.8+0.5+(0.4×2)+(0.4×3)+0.7+0.5+0.5 = 8.2
        # wait: 0.3
        # Total: 8.5 ✓
        # ================================================================

        # Phase 1: Intro [0.0 – 1.0]
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.5)
        self.play(
            FadeIn(ground), FadeIn(listener), FadeIn(listener_label), run_time=0.5
        )

        # Phase 2: Ambulance Approaches [1.0 – 4.0]
        self.play(FadeIn(ambulance, shift=RIGHT * 0.5), run_time=0.4)

        # Emit compressed wavefronts (short wavelength = high pitch)
        for i in range(4):
            wave = Arc(
                radius=0.4 + i * 0.35,
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                color=high_pitch_color,
                stroke_width=2.5,
            ).set_opacity(max(0.3, 0.9 - i * 0.15))
            wave.move_to(ambulance.get_center())
            self.play(
                ambulance.animate.shift(RIGHT * 1.4),
                FadeIn(wave, scale=0.8),
                run_time=0.45,
            )
            waves.add(wave)

        # Show high-frequency graph
        self.play(FadeIn(high_group, shift=UP * 0.3), Create(high_graph), run_time=0.8)

        # Phase 3: Ambulance passes listener [4.0 – 5.3]
        self.play(
            Indicate(listener, color=listener_color, scale_factor=1.3), run_time=0.5
        )

        # Transition waves (orange)
        for i in range(2):
            wave = Arc(
                radius=0.8 + i * 0.5,
                start_angle=-PI / 4,
                angle=PI / 2,
                color=transition_color,
                stroke_width=2,
            ).set_opacity(0.7 - i * 0.1)
            wave.move_to(ambulance.get_center())
            self.play(
                ambulance.animate.shift(RIGHT * 1.5),
                FadeIn(wave, scale=0.8),
                run_time=0.4,
            )
            waves.add(wave)

        # Phase 4: Ambulance recedes [5.3 – 7.2]
        # Stretched wavefronts (long wavelength = low pitch)
        for i in range(3):
            wave = Arc(
                radius=1.0 + i * 0.6,
                start_angle=PI / 3,
                angle=2 * PI / 3,
                color=low_pitch_color,
                stroke_width=2.5,
            ).set_opacity(max(0.25, 0.8 - i * 0.15))
            wave.move_to(ambulance.get_center())
            self.play(
                ambulance.animate.shift(RIGHT * 1.2),
                FadeIn(wave, scale=0.8),
                run_time=0.4,
            )
            waves.add(wave)

        # Show low-frequency graph
        self.play(FadeIn(low_group, shift=UP * 0.3), Create(low_graph), run_time=0.7)

        # Phase 5: Ambulance exits [7.2 – 7.7]
        self.play(ambulance.animate.move_to(RIGHT * 8), run_time=0.5, rate_func=linear)

        # Phase 6: Final emphasis [7.7 – 8.2]
        self.play(
            Circumscribe(high_graph, color=high_pitch_color, buff=0.1),
            Circumscribe(low_graph, color=low_pitch_color, buff=0.1),
            run_time=0.5,
        )

        # Hold final frame
        self.wait(0.3)
