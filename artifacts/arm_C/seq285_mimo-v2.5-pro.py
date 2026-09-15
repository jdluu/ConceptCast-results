import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Wave Fundamentals ---
        self.clear()

        # ── Palette ────────────────────────────────────────────────
        BG = "#181825"
        SOURCE_CLR = "#CBA6F7"
        WAVE_CLR = "#89B4FA"
        TEXT_CLR = "#CDD6F4"
        SUB_CLR = "#A6ADC8"

        self.camera.background_color = BG

        # ── Source dot with layered glow ────────────────────────────
        glow_outer = Circle(
            radius=0.55,
            stroke_width=0,
            fill_color=SOURCE_CLR,
            fill_opacity=0.08,
        )
        glow_mid = Circle(
            radius=0.38,
            stroke_width=0,
            fill_color=SOURCE_CLR,
            fill_opacity=0.15,
        )
        glow_inner = Circle(
            radius=0.25,
            stroke_width=0,
            fill_color=SOURCE_CLR,
            fill_opacity=0.30,
        )
        source_dot = Dot(
            point=ORIGIN,
            radius=0.15,
            color=SOURCE_CLR,
        )
        source_highlight = Dot(
            point=ORIGIN + 0.04 * UP + 0.04 * LEFT,
            radius=0.05,
            color=WHITE,
            fill_opacity=0.6,
        )
        source_group = VGroup(
            glow_outer,
            glow_mid,
            glow_inner,
            source_dot,
            source_highlight,
        )

        # ── Wavefront circles ──────────────────────────────────────
        num_rings = 7
        max_radius = 5.5
        wavefronts = VGroup()
        for i in range(num_rings):
            ring = Circle(
                radius=0.01,
                stroke_color=WAVE_CLR,
                stroke_width=2.5,
                stroke_opacity=0.0,
            )
            wavefronts.add(ring)

        # ── Labels ──────────────────────────────────────────────────
        source_label = Text("Source", font_size=28, color=TEXT_CLR)
        source_label.next_to(source_dot, DOWN, buff=0.45)

        title = Text("Wave Fundamentals", font_size=40, color=TEXT_CLR, weight=BOLD)
        title.to_edge(UP, buff=0.5)

        subtitle = Text(
            "Energy spreads outward in concentric wavefronts",
            font_size=24,
            color=SUB_CLR,
        )
        subtitle.next_to(title, DOWN, buff=0.25)

        # ═══════════════════════════════════════════════════════════
        #  ANIMATION SEQUENCE   total = 5.5 s
        # ═══════════════════════════════════════════════════════════

        # 1  Title + subtitle  ─ 0.6 s
        self.play(
            FadeIn(title, shift=DOWN * 0.3),
            FadeIn(subtitle, shift=DOWN * 0.2),
            run_time=0.6,
        )

        # 2  Source appears  ─ 0.6 s
        self.play(
            GrowFromCenter(glow_outer),
            GrowFromCenter(glow_mid),
            GrowFromCenter(glow_inner),
            GrowFromCenter(source_dot),
            FadeIn(source_highlight, scale=0.5),
            run_time=0.6,
        )

        # 2b  Source label  ─ 0.3 s
        self.play(
            FadeIn(source_label, shift=UP * 0.2),
            run_time=0.3,
        )

        # 3  Pulse the source glow  ─ 0.5 s
        self.play(
            glow_outer.animate.scale(1.3).set_opacity(0.12),
            glow_mid.animate.scale(1.2).set_opacity(0.20),
            run_time=0.25,
        )
        self.play(
            glow_outer.animate.scale(1 / 1.3).set_opacity(0.08),
            glow_mid.animate.scale(1 / 1.2).set_opacity(0.15),
            run_time=0.25,
        )

        # 4  Expanding wavefronts  ─ 3.0 s  (≈0.429 s × 7)
        ring_dur = 3.0 / num_rings
        for i, ring in enumerate(wavefronts):
            target_r = max_radius * (i + 1) / num_rings
            scale_fac = target_r / 0.01
            target_opa = max(0.15, 0.85 - 0.10 * i)
            self.play(
                ring.animate.scale(scale_fac).set_stroke(opacity=target_opa),
                rate_func=linear,
                run_time=ring_dur,
            )

        # 5  Indicate source  ─ 0.35 s
        self.play(
            Indicate(source_dot, color=SOURCE_CLR, scale_factor=1.4),
            run_time=0.35,
        )

        # 6  Hold  ─ 0.15 s  (makes total = 5.5 s)
        self.wait(0.15)
        # --- Scene 2: Source Motion Introduction ---
        # Scene 2: Source Motion Introduction
        self.camera.background_color = "#181825"

        # Create moving source with glow
        moving_source = Dot(point=LEFT * 3, radius=0.15, color="#CBA6F7")

        source_glow = Dot(point=LEFT * 3, radius=0.3, color="#CBA6F7", fill_opacity=0.3)

        # Create trail waves at different positions
        trail_wave_1 = Circle(radius=0.5, stroke_width=2.0, color="#89B4FA").move_to(
            LEFT * 3
        )

        trail_wave_2 = Circle(radius=1.2, stroke_width=2.0, color="#89B4FA").move_to(
            LEFT * 2
        )

        trail_wave_3 = Circle(radius=2.0, stroke_width=2.0, color="#89B4FA").move_to(
            LEFT * 1
        )

        trail_wave_4 = Circle(radius=2.8, stroke_width=2.0, color="#89B4FA").move_to(
            ORIGIN
        )

        # Initial appearance
        self.play(FadeIn(moving_source), FadeIn(source_glow), run_time=0.5)

        # Move source and show trail waves simultaneously
        self.play(
            moving_source.animate.move_to(RIGHT * 3),
            source_glow.animate.move_to(RIGHT * 3),
            FadeIn(trail_wave_1),
            run_time=1.0,
        )

        self.play(FadeIn(trail_wave_2), run_time=1.0)
        self.play(FadeIn(trail_wave_3), run_time=1.0)
        self.play(FadeIn(trail_wave_4), run_time=1.0)

        # Pulse effect on source
        self.play(
            ScaleInPlace(source_glow, 1.3), run_time=0.5, rate_func=there_and_back
        )

        self.wait(0.5)
        # --- Scene 3: Wavefront Compression ---
        # Background color
        self.camera.background_color = "#181825"

        # --- 1. Objects ---

        # Central moving source
        moving_source = Dot(ORIGIN, radius=0.15, color="#CBA6F7")
        source_label = (
            MathTex("v_{source}", color="#CBA6F7")
            .scale(0.6)
            .next_to(moving_source, UP, buff=0.2)
        )
        arrow_motion = Arrow(
            LEFT * 0.5, RIGHT * 0.5, buff=0, color="#CBA6F7", stroke_width=3
        )

        # Compressed wavefronts (right side - direction of motion, tight spacing)
        c1 = Circle(radius=0.5, color="#89B4FA", stroke_width=2.0).move_to(RIGHT * 1.5)
        c2 = Circle(radius=0.5, color="#89B4FA", stroke_width=2.0).move_to(RIGHT * 2.0)
        c3 = Circle(radius=0.5, color="#89B4FA", stroke_width=2.0).move_to(RIGHT * 2.4)
        compressed_group = VGroup(c1, c2, c3)

        # Stretched wavefronts (left side - opposite motion, loose spacing)
        s1 = Circle(radius=0.5, color="#89B4FA", stroke_width=2.0).move_to(LEFT * 2.0)
        s2 = Circle(radius=0.5, color="#89B4FA", stroke_width=2.0).move_to(LEFT * 3.5)
        s3 = Circle(radius=0.5, color="#89B4FA", stroke_width=2.0).move_to(LEFT * 5.5)
        stretched_group = VGroup(s1, s2, s3)

        # Braces and labels
        compression_brace = Brace(compressed_group, DOWN, color="#F38BA8")
        compression_label = (
            compression_brace.get_text("Compression", buff=0.1)
            .set_color("#F38BA8")
            .scale(0.8)
        )
        expansion_brace = Brace(stretched_group, DOWN, color="#A6E3A1")
        expansion_label = (
            expansion_brace.get_text("Expansion", buff=0.1)
            .set_color("#A6E3A1")
            .scale(0.8)
        )

        # --- 2. Animations (Total: 5.25s) ---

        # Show source and direction arrow (0.8s)
        self.play(
            FadeIn(moving_source, scale=1.5),
            Write(source_label),
            GrowArrow(arrow_motion),
            run_time=0.8,
        )

        # Show wavefronts with staggered animation (1.8s)
        self.play(
            LaggedStart(
                Create(c1),
                Create(c2),
                Create(c3),
                Create(s1),
                Create(s2),
                Create(s3),
                lag_ratio=0.3,
            ),
            run_time=1.8,
        )

        # Highlight with braces (1.0s)
        self.play(
            GrowFromCenter(compression_brace),
            FadeIn(compression_label, shift=UP * 0.15),
            GrowFromCenter(expansion_brace),
            FadeIn(expansion_label, shift=UP * 0.15),
            run_time=1.0,
        )

        # Final hold (1.65s)
        self.wait(1.65)
        # --- Scene 4: Frequency and Wavelength Relationship ---
        self.clear()
        self.camera.background_color = "#181825"

        # === LEFT SIDE: High Frequency ===
        axes_high = Axes(
            x_range=[0, 6, 1],
            y_range=[-1, 1, 1],
            x_length=5,
            y_length=2,
            axis_config={"color": "#CDD6F4", "stroke_width": 2.0},
        ).shift(LEFT * 3.5)

        graph_high = axes_high.plot(
            lambda x: np.sin(3 * x), x_range=[0, 6], color="#F38BA8", stroke_width=3.0
        )

        label_high = Text("High Frequency", font_size=24, color="#F38BA8").next_to(
            axes_high, UP, buff=0.3
        )

        # === RIGHT SIDE: Low Frequency ===
        axes_low = Axes(
            x_range=[0, 6, 1],
            y_range=[-1, 1, 1],
            x_length=5,
            y_length=2,
            axis_config={"color": "#CDD6F4", "stroke_width": 2.0},
        ).shift(RIGHT * 3.5)

        graph_low = axes_low.plot(
            lambda x: np.sin(1 * x), x_range=[0, 6], color="#A6E3A1", stroke_width=3.0
        )

        label_low = Text("Low Frequency", font_size=24, color="#A6E3A1").next_to(
            axes_low, UP, buff=0.3
        )

        # === ANIMATIONS ===

        # 0.0s – 1.5s: Show high-frequency side
        self.play(FadeIn(axes_high), run_time=0.5)
        self.play(Create(graph_high), FadeIn(label_high), run_time=1.0)

        # 1.5s – 3.0s: Show low-frequency side
        self.play(FadeIn(axes_low), run_time=0.5)
        self.play(Create(graph_low), FadeIn(label_low), run_time=1.0)

        # 3.0s – 4.5s: Brace annotations to highlight wavelength contrast
        brace_high = BraceBetweenPoints(
            axes_high.c2p(1, 0), axes_high.c2p(3, 0), direction=DOWN
        )
        brace_high_text = (
            brace_high.get_tex("\	ext{Short }\\lambda")
            .scale(0.8)
            .set_color("#F38BA8")
        )

        brace_low = BraceBetweenPoints(
            axes_low.c2p(0, 0), axes_low.c2p(2 * np.pi, 0), direction=DOWN
        )
        brace_low_text = (
            brace_low.get_tex("\	ext{Long }\\lambda").scale(0.8).set_color("#A6E3A1")
        )

        self.play(
            GrowFromCenter(brace_high),
            FadeIn(brace_high_text),
            GrowFromCenter(brace_low),
            FadeIn(brace_low_text),
            run_time=1.5,
        )

        # 4.5s – 6.0s: Closing narration text
        final_text = Text(
            "Frequency shift = Doppler Effect", font_size=28, color="#CDD6F4"
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(final_text), run_time=1.0)
        self.wait(0.5)
        # --- Scene 5: Observer Perspective - Approaching ---
        self.clear()

        # === COLOR PALETTE (Catppuccin Mocha) ===
        BG = "#1E1E2E"
        SOURCE_COLOR = "#CBA6F7"
        OBSERVER_COLOR = "#FAB387"
        WAVE_COLOR = "#89B4FA"
        TEXT_COLOR = "#CDD6F4"
        ACCENT_COLOR = "#A6E3A1"

        # === BACKGROUND ===
        self.camera.background_color = BG

        # === TITLE ===
        title = Text(
            "Observer Perspective — Approaching Source",
            font_size=32,
            color=TEXT_COLOR,
            weight=BOLD,
        ).to_edge(UP, buff=0.35)

        # === GROUND LINE ===
        ground = Line(
            LEFT * 6 + DOWN * 0.5,
            RIGHT * 6 + DOWN * 0.5,
            color=TEXT_COLOR,
            stroke_width=1,
            stroke_opacity=0.3,
        )

        # === SOURCE ===
        source = Dot(LEFT * 5 + DOWN * 0.5, radius=0.16, color=SOURCE_COLOR)
        source_label = Text("Source", font_size=22, color=SOURCE_COLOR)
        source_label.add_updater(lambda m: m.next_to(source, DOWN, buff=0.2))

        # Direction arrow
        dir_arrow = Arrow(
            LEFT * 5.6 + DOWN * 0.5,
            LEFT * 4.4 + DOWN * 0.5,
            color=SOURCE_COLOR,
            buff=0,
            stroke_width=3,
        )

        # === OBSERVER ===
        observer = Dot(RIGHT * 3.0, radius=0.16, color=OBSERVER_COLOR)
        observer_label = Text("Observer", font_size=22, color=OBSERVER_COLOR)
        observer_label.next_to(observer, DOWN, buff=0.2)

        # Ear shape (small arc next to observer)
        ear_arc = Arc(
            radius=0.3,
            start_angle=-PI / 3,
            angle=2 * PI / 3,
            color=OBSERVER_COLOR,
            stroke_width=2.5,
        )
        ear_arc.next_to(observer, RIGHT, buff=0.05)

        # === WAVEFRONT CIRCLES (expanding rings from source) ===
        source_x_tracker = ValueTracker(-5.0)
        source.add_updater(
            lambda m: m.move_to(RIGHT * source_x_tracker.get_value() + DOWN * 0.5)
        )
        dir_arrow.add_updater(
            lambda m: m.put_start_and_end_on(
                RIGHT * (source_x_tracker.get_value() - 0.6) + DOWN * 0.5,
                RIGHT * (source_x_tracker.get_value() + 0.2) + DOWN * 0.5,
            )
        )

        # Store wavefront birth positions and create expanding circles
        wavefront_circles = VGroup()

        # === PHASE 1: SETUP (0.0 - 1.2s) ===
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.4)
        self.play(
            FadeIn(ground),
            FadeIn(source, scale=0.5),
            FadeIn(source_label),
            FadeIn(dir_arrow),
            run_time=0.4,
        )
        self.play(
            FadeIn(observer, scale=0.5),
            FadeIn(observer_label),
            FadeIn(ear_arc),
            run_time=0.4,
        )

        # === PHASE 2: SOURCE MOVES, EMITTING WAVEFRONTS (1.2 - 3.8s) ===
        move_duration = 2.6
        num_wavefronts = 8
        emit_interval = move_duration / num_wavefronts

        emission_times = [i * emit_interval for i in range(num_wavefronts)]
        emission_positions = [
            -5.0 + i * (4.5 / num_wavefronts) for i in range(num_wavefronts)
        ]

        for i in range(num_wavefronts):
            emit_x = emission_positions[i]
            circle = Circle(
                radius=0.01, color=WAVE_COLOR, stroke_width=2, stroke_opacity=0.6
            ).move_to(RIGHT * emit_x + DOWN * 0.5)
            wavefront_circles.add(circle)

        for i, circle in enumerate(wavefront_circles):
            age_at_end = move_duration - emission_times[i]
            target_radius = age_at_end * 1.5
            circle.target_radius = target_radius

        self.add(wavefront_circles)

        self.play(
            source_x_tracker.animate.set_value(-0.5),
            *[c.animate.scale(c.target_radius / 0.01) for c in wavefront_circles],
            run_time=move_duration,
            rate_func=linear,
        )

        # === PHASE 3: SHOW WAVEFRONT LINES APPROACHING (3.8 - 4.6s) ===
        wf_positions = [1.4, 1.7, 1.9, 2.05, 2.15, 2.25, 2.32, 2.38]
        wf_lines = VGroup()
        for pos in wf_positions:
            line = Line(
                UP * 1.5 + RIGHT * pos,
                DOWN * 1.5 + RIGHT * pos,
                color=WAVE_COLOR,
                stroke_width=2,
                stroke_opacity=0.7,
            )
            wf_lines.add(line)

        self.play(
            LaggedStart(*[Create(line) for line in wf_lines], lag_ratio=0.1),
            run_time=0.8,
        )

        # === PHASE 4: FREQUENCY INDICATOR (4.6 - 5.0s) ===
        freq_label = Text(
            "f ↑  perceived frequency increases",
            font_size=26,
            color=ACCENT_COLOR,
            weight=BOLD,
        )
        freq_label.to_edge(DOWN, buff=0.5)

        incoming = VGroup(
            *[
                Arrow(
                    RIGHT * 2.2 + UP * (0.6 - i * 0.3),
                    RIGHT * 2.9 + UP * (0.6 - i * 0.3),
                    color=WAVE_COLOR,
                    buff=0,
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.35,
                )
                for i in range(3)
            ]
        )

        self.play(
            FadeIn(freq_label, shift=UP * 0.2),
            LaggedStart(*[GrowFromCenter(a) for a in incoming], lag_ratio=0.15),
            run_time=0.4,
        )

        # === PHASE 5: EMPHASIS (5.0 - 5.25s) ===
        self.play(
            Indicate(freq_label, color=ACCENT_COLOR, scale_factor=1.1), run_time=0.25
        )
        # --- Scene 6: Observer Perspective - Receding ---
        self.camera.background_color = "#181825"

        # --- 1. Setup Objects ---
        # Observer (Left)
        observer = Dot(LEFT * 2, radius=0.15, color="#FAB387")
        observer_label = Text("Observer", font_size=24, color="#FAB387").next_to(
            observer, DOWN
        )

        # Source (Right, moving away)
        source = Dot(RIGHT * 4, radius=0.15, color="#CBA6F7")
        source_label = Text("Source", font_size=24, color="#CBA6F7").next_to(source, UP)

        # Direction Arrow (Receding/Moving Right)
        direction_arrow = Arrow(
            start=RIGHT * 3.5, end=RIGHT * 4.5, color="#CBA6F7", buff=0
        )

        # --- 2. Wavefronts (Stretched spacing) ---
        # Lines closer together near source, farther apart near observer
        wavefronts = VGroup(
            Line(
                UP * 2 + RIGHT * 4,
                DOWN * 2 + RIGHT * 4,
                color="#89B4FA",
                stroke_width=1,
            ),
            Line(UP * 2 + RIGHT * 2, DOWN * 2 + RIGHT * 2, color="#89B4FA"),
            Line(UP * 2 + RIGHT * 0.5, DOWN * 2 + RIGHT * 0.5, color="#89B4FA"),
            Line(UP * 2 + LEFT * 1.2, DOWN * 2 + LEFT * 1.2, color="#89B4FA"),
            Line(UP * 2 + LEFT * 3.0, DOWN * 2 + LEFT * 3.0, color="#89B4FA"),
        )
        wavefronts[3].set_opacity(0.7)
        wavefronts[4].set_opacity(0.5)

        # --- 3. Incoming Arrows (Frequency Indicator) ---
        incoming_arrows = VGroup(
            Arrow(LEFT * 0 + UP * 1, LEFT * 1.5 + UP * 1, color="#FAB387", buff=0.1),
            Arrow(
                LEFT * 0.5 + DOWN * 1, LEFT * 1.5 + DOWN * 1, color="#FAB387", buff=0.1
            ),
        )
        incoming_label = Text("f ↓", font_size=30, color="#FAB387").next_to(
            incoming_arrows, RIGHT
        )

        # --- 4. Title ---
        title = Text(
            "Observer Perspective: Receding Source", font_size=36, color="#CDD6F4"
        ).to_edge(UP)

        # --- 5. Animations (Total: 5.5s) ---

        # 0.5s
        self.play(Write(title), run_time=0.5)

        # 1.0s
        self.play(
            FadeIn(source),
            FadeIn(source_label),
            GrowFromCenter(direction_arrow),
            FadeIn(observer),
            FadeIn(observer_label),
            run_time=1.0,
        )

        # 1.5s
        self.play(
            LaggedStart(
                *[FadeIn(wf, shift=RIGHT * 0.2) for wf in wavefronts],
                lag_ratio=0.3,
            ),
            run_time=1.5,
        )

        # 1.0s
        self.play(
            GrowFromCenter(incoming_arrows),
            FadeIn(incoming_label, shift=LEFT),
            run_time=1.0,
        )

        # 1.0s
        self.play(Circumscribe(observer, color="#FAB387"), run_time=1.0)

        # 0.5s wait
        self.wait(0.5)
        # --- Scene 7: The Doppler Formula ---
        self.clear()

        # --- Background rectangle for the equation ---
        equation_bg = Rectangle(
            width=8,
            height=3,
            color="#313244",
            fill_color="#313244",
            fill_opacity=0.5,
            stroke_width=2,
        ).move_to(ORIGIN)

        # --- Main Doppler equation ---
        doppler_eq = MathTex(
            r"f' = f \left( \frac{v \pm v_o}{v \mp v_s} \right)",
            font_size=48,
            color="#CDD6F4",
        ).move_to(ORIGIN)

        # --- Labels with arrows (f' observed frequency) ---
        label_f_prime = Text(
            "f' (Observed Freq)", font_size=20, color="#F38BA8"
        ).move_to(UP * 2.5 + LEFT * 2)

        arrow_f_prime = Arrow(
            start=UP * 2.2 + LEFT * 2,
            end=UP * 1.5 + LEFT * 2,
            color="#F38BA8",
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
        )

        # --- Labels with arrows (f source frequency) ---
        label_f_source = Text("f (Source Freq)", font_size=20, color="#89B4FA").move_to(
            UP * 2.5 + RIGHT * 2
        )

        arrow_f_source = Arrow(
            start=UP * 2.2 + RIGHT * 2,
            end=UP * 1.5 + RIGHT * 1,
            color="#89B4FA",
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
        )

        # --- Labels with arrows (v_s source velocity) ---
        label_v_source = Text(
            "v_s (Source Vel)", font_size=20, color="#CBA6F7"
        ).move_to(DOWN * 2.5 + RIGHT * 2)

        arrow_v_source = Arrow(
            start=DOWN * 2.2 + RIGHT * 2,
            end=DOWN * 1.5 + RIGHT * 0.5,
            color="#CBA6F7",
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
        )

        # --- Additional label: wave speed v ---
        label_v_wave = Text("v (Wave Speed)", font_size=20, color="#A6E3A1").move_to(
            DOWN * 2.5 + LEFT * 2
        )

        arrow_v_wave = Arrow(
            start=DOWN * 2.2 + LEFT * 2,
            end=DOWN * 1.5 + LEFT * 0.3,
            color="#A6E3A1",
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
        )

        # --- Plus/minus note at bottom ---
        pm_note = Text(
            "± and ∓ signs flip based on direction of motion",
            font_size=18,
            color="#A6ADC8",
        ).move_to(DOWN * 3.3)

        # =============================================
        # ANIMATION SEQUENCE (6.75s total)
        # =============================================

        # 1. Fade in background (0.6s)
        self.play(FadeIn(equation_bg, scale=0.95), run_time=0.6)

        # 2. Write the main equation (1.5s)
        self.play(Write(doppler_eq), run_time=1.5)

        # 3. Brief pause to let equation settle (0.4s)
        self.wait(0.4)

        # 4. Animate f' label and arrow (0.8s)
        self.play(
            FadeIn(label_f_prime, shift=DOWN * 0.3),
            GrowFromCenter(arrow_f_prime),
            run_time=0.8,
        )

        # 5. Animate f source label and arrow (0.8s)
        self.play(
            FadeIn(label_f_source, shift=DOWN * 0.3),
            GrowFromCenter(arrow_f_source),
            run_time=0.8,
        )

        # 6. Animate v_s label and arrow (0.7s)
        self.play(
            FadeIn(label_v_source, shift=UP * 0.3),
            GrowFromCenter(arrow_v_source),
            run_time=0.7,
        )

        # 7. Animate v wave speed label and arrow (0.6s)
        self.play(
            FadeIn(label_v_wave, shift=UP * 0.3),
            GrowFromCenter(arrow_v_wave),
            run_time=0.6,
        )

        # 8. Fade in the plus/minus note (0.45s)
        self.play(FadeIn(pm_note, shift=UP * 0.2), run_time=0.45)

        # 9. Final hold (0.9s)
        self.wait(0.9)
        # --- Scene 8: Everyday Applications ---
        # === Color Palette (Catppuccin Mocha) ===
        BG_COLOR = "#181825"
        SURFACE = "#313244"
        RED = "#F38BA8"
        BLUE = "#89B4FA"
        GREEN = "#A6E3A1"
        TEAL = "#94E2D5"
        PEACH = "#FAB387"
        TEXT_COLOR = "#CDD6F4"

        self.camera.background_color = BG_COLOR

        # ==============================
        # PANEL 1: POLICE RADAR
        # ==============================
        panel1_title = Text("Police Radar", font_size=28, color=TEXT_COLOR).to_edge(
            UP, buff=0.5
        )

        # Radar gun
        radar_body = Rectangle(
            width=1.5, height=0.8, color=RED, fill_opacity=0.6, stroke_width=2
        )
        radar_barrel = Rectangle(
            width=0.8, height=0.3, color=RED, fill_opacity=0.8, stroke_width=2
        )
        radar_barrel.next_to(radar_body, RIGHT, buff=0)
        radar_gun = VGroup(radar_body, radar_barrel).move_to(LEFT * 4)

        # Car silhouette
        car_body = (
            Polygon(
                [-1.5, -0.5, 0],
                [-0.5, -0.5, 0],
                [0, 0, 0],
                [0.5, -0.5, 0],
                [1.5, -0.5, 0],
                [1.5, 0.5, 0],
                [-1.5, 0.5, 0],
                color=BLUE,
                fill_opacity=0.6,
                stroke_width=2,
            )
            .scale(0.5)
            .move_to(RIGHT * 3)
        )

        # Radar waves
        wave1 = Arc(
            radius=0.5, start_angle=-PI / 4, angle=PI / 2, color=RED, stroke_width=2
        ).move_to(LEFT * 2.5)
        wave2 = Arc(
            radius=1.0, start_angle=-PI / 4, angle=PI / 2, color=RED, stroke_width=2
        ).move_to(LEFT * 2.5)
        wave3 = Arc(
            radius=1.5, start_angle=-PI / 4, angle=PI / 2, color=RED, stroke_width=2
        ).move_to(LEFT * 2.5)
        waves = VGroup(wave1, wave2, wave3)

        # Speed readout
        speed_text = Text("120 km/h", font_size=24, color=GREEN).next_to(
            car_body, UP, buff=0.5
        )
        speed_box = SurroundingRectangle(speed_text, color=GREEN, buff=0.1)

        # Animate Panel 1
        self.play(FadeIn(panel1_title), run_time=0.5)
        self.play(FadeIn(radar_gun), run_time=0.4)
        self.play(FadeIn(car_body), run_time=0.4)
        self.play(Create(waves), run_time=0.6)
        self.play(FadeIn(speed_text), FadeIn(speed_box), run_time=0.4)

        # ==============================
        # TRANSITION 1 -> PANEL 2
        # ==============================
        panel1_group = VGroup(
            panel1_title, radar_gun, car_body, waves, speed_text, speed_box
        )
        self.play(FadeOut(panel1_group, shift=LEFT * 2), run_time=0.3)

        # ==============================
        # PANEL 2: WEATHER RADAR
        # ==============================
        panel2_title = Text("Weather Radar", font_size=28, color=TEXT_COLOR).to_edge(
            UP, buff=0.5
        )

        # Radar station
        radar_base = Rectangle(
            width=1.0, height=0.6, color=TEAL, fill_opacity=0.6, stroke_width=2
        )
        radar_dish = Arc(
            radius=0.6,
            start_angle=-PI / 3,
            angle=2 * PI / 3,
            color=TEAL,
            stroke_width=3,
        )
        radar_dish.next_to(radar_base, UP, buff=0)
        radar_station = VGroup(radar_base, radar_dish).move_to(LEFT * 4)

        # Storm cloud (overlapping circles)
        cloud1 = Circle(radius=0.6, color=GREEN, fill_opacity=0.4, stroke_width=2)
        cloud2 = Circle(
            radius=0.5, color=GREEN, fill_opacity=0.4, stroke_width=2
        ).shift(RIGHT * 0.5 + UP * 0.2)
        cloud3 = Circle(
            radius=0.55, color=GREEN, fill_opacity=0.4, stroke_width=2
        ).shift(LEFT * 0.4 + UP * 0.15)
        cloud = VGroup(cloud1, cloud2, cloud3).move_to(RIGHT * 3)

        # Weather waves
        w_wave1 = Arc(
            radius=0.5, start_angle=-PI / 4, angle=PI / 2, color=GREEN, stroke_width=2
        ).move_to(LEFT * 2.5)
        w_wave2 = Arc(
            radius=1.0, start_angle=-PI / 4, angle=PI / 2, color=GREEN, stroke_width=2
        ).move_to(LEFT * 2.5)
        w_wave3 = Arc(
            radius=1.5, start_angle=-PI / 4, angle=PI / 2, color=GREEN, stroke_width=2
        ).move_to(LEFT * 2.5)
        weather_waves = VGroup(w_wave1, w_wave2, w_wave3)

        # Movement arrow
        move_arrow = Arrow(
            start=cloud.get_center(),
            end=cloud.get_center() + RIGHT * 1.5,
            color=TEAL,
            stroke_width=3,
            buff=0.1,
        )
        move_label = Text("Moving →", font_size=20, color=TEAL).next_to(
            move_arrow, DOWN, buff=0.2
        )

        # Animate Panel 2
        self.play(FadeIn(panel2_title), run_time=0.5)
        self.play(FadeIn(radar_station), run_time=0.4)
        self.play(FadeIn(cloud), run_time=0.4)
        self.play(Create(weather_waves), run_time=0.5)
        self.play(FadeIn(move_arrow), FadeIn(move_label), run_time=0.4)

        # ==============================
        # TRANSITION 2 -> PANEL 3
        # ==============================
        panel2_group = VGroup(
            panel2_title, radar_station, cloud, weather_waves, move_arrow, move_label
        )
        self.play(FadeOut(panel2_group, shift=LEFT * 2), run_time=0.3)

        # ==============================
        # PANEL 3: ASTRONOMICAL REDSHIFT
        # ==============================
        panel3_title = Text(
            "Astronomical Redshift", font_size=28, color=TEXT_COLOR
        ).to_edge(UP, buff=0.5)

        # Star
        star = Star(
            n=5,
            outer_radius=0.8,
            inner_radius=0.35,
            color=PEACH,
            fill_opacity=0.8,
            stroke_width=2,
        ).move_to(LEFT * 3)

        # Star waves
        s_wave1 = Arc(
            radius=0.4, start_angle=-PI / 4, angle=PI / 2, color=PEACH, stroke_width=2
        ).move_to(LEFT * 1.8)
        s_wave2 = Arc(
            radius=0.8, start_angle=-PI / 4, angle=PI / 2, color=PEACH, stroke_width=2
        ).move_to(LEFT * 1.8)
        star_waves = VGroup(s_wave1, s_wave2)

        # Earth
        earth = Circle(
            radius=0.5, color=BLUE, fill_opacity=0.6, stroke_width=2
        ).move_to(RIGHT * 2)

        # Receding arrow
        recede_arrow = Arrow(
            start=star.get_center() + UP * 1.2,
            end=star.get_center() + UP * 1.2 + LEFT * 2,
            color=RED,
            stroke_width=3,
            buff=0.1,
        )
        recede_label = Text("Receding", font_size=20, color=RED).next_to(
            recede_arrow, UP, buff=0.1
        )

        # Spectrum comparison
        emit_bar = Line(LEFT * 1.5, RIGHT * 1.5, color=PEACH, stroke_width=6)
        receive_bar = Line(LEFT * 1.8, RIGHT * 1.2, color=RED, stroke_width=6)
        emit_label = Text("Emitted", font_size=16, color=PEACH)
        receive_label = Text("Received", font_size=16, color=RED)
        redshift_label = Text("Red-shifted", font_size=18, color=RED)

        spectrum_group = (
            VGroup(
                VGroup(emit_bar, emit_label).arrange(DOWN, buff=0.1),
                VGroup(receive_bar, receive_label).arrange(DOWN, buff=0.1),
                redshift_label,
            )
            .arrange(RIGHT, buff=0.5)
            .move_to(DOWN * 2)
        )

        # Animate Panel 3
        self.play(FadeIn(panel3_title), run_time=0.35)
        self.play(FadeIn(star), run_time=0.25)
        self.play(Create(star_waves), run_time=0.25)
        self.play(FadeIn(earth), run_time=0.35)
        self.play(FadeIn(recede_arrow), FadeIn(recede_label), run_time=0.25)
        self.play(FadeIn(spectrum_group), run_time=0.45)

        # Final hold
        self.wait(0.1)
        # --- Scene 9: Summary and Key Takeaway ---
        # 1. Set Background and Colors
        BG_COLOR = "#181825"
        BLUE_ACCENT = "#89b4fa"
        RED_ACCENT = "#f38ba8"
        TEXT_COLOR = "#cdd6f4"

        self.camera.background_color = BG_COLOR

        # 2. Define Objects

        # Central Source
        source = Dot(radius=0.2, color=WHITE).set_z_index(10)
        source_label = Text("Source", font_size=24, color=WHITE).next_to(
            source, UP, buff=0.3
        )

        # Background Zones (Rectangles)
        # Left: Approaching
        zone_approach = Rectangle(
            width=4.5,
            height=5.5,
            color=BLUE_ACCENT,
            fill_opacity=0.15,
            stroke_width=1.5,
        ).move_to(LEFT * 3.25)

        # Right: Receding
        zone_recede = Rectangle(
            width=4.5, height=5.5, color=RED_ACCENT, fill_opacity=0.15, stroke_width=1.5
        ).move_to(RIGHT * 3.25)

        # Zone Labels
        label_approach = Text("Approaching", font_size=28, color=BLUE_ACCENT).move_to(
            zone_approach.get_top() + DOWN * 0.6
        )
        label_recede = Text("Receding", font_size=28, color=RED_ACCENT).move_to(
            zone_recede.get_top() + DOWN * 0.6
        )

        # Frequency Symbols (Math)
        math_high = MathTex(r"f \uparrow", font_size=48, color=BLUE_ACCENT).move_to(
            zone_approach.get_center()
        )
        math_low = MathTex(r"f \downarrow", font_size=48, color=RED_ACCENT).move_to(
            zone_recede.get_center()
        )

        # Descriptive Subtext
        desc_high = Text("Higher Frequency", font_size=20, color=BLUE_ACCENT).next_to(
            math_high, DOWN, buff=0.5
        )
        desc_low = Text("Lower Frequency", font_size=20, color=RED_ACCENT).next_to(
            math_low, DOWN, buff=0.5
        )

        # Motion Indicators (Arrows)
        arrow_approach = Arrow(
            start=LEFT * 1.5,
            end=LEFT * 0.5,
            color=BLUE_ACCENT,
            buff=0.1,
            stroke_width=4,
        )
        arrow_recede = Arrow(
            start=RIGHT * 0.5,
            end=RIGHT * 1.5,
            color=RED_ACCENT,
            buff=0.1,
            stroke_width=4,
        )

        # Bottom Summary Text
        summary_text = Text(
            "Relative motion changes perceived frequency.",
            font_size=24,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.6)

        # 3. Animations

        # Phase 1: Intro (0.0 - 1.5s)
        self.play(FadeIn(source, scale=0.5))
        self.play(Write(source_label))
        self.wait(0.5)

        # Phase 2: Show Zones (1.5 - 2.5s)
        self.play(FadeIn(zone_approach), FadeIn(zone_recede), run_time=1.0)

        # Phase 3: Add Zone Details (2.5 - 4.0s)
        self.play(
            Write(label_approach),
            Write(label_recede),
            Write(math_high),
            Write(math_low),
            run_time=1.5,
        )

        # Phase 4: Add Motion & Subtext (4.0 - 5.0s)
        self.play(
            FadeIn(desc_high),
            FadeIn(desc_low),
            GrowArrow(arrow_approach),
            GrowArrow(arrow_recede),
            run_time=1.0,
        )

        # Phase 5: Summary (5.0 - 6.5s)
        self.play(Write(summary_text), run_time=1.5)

        # Phase 6: Hold (6.5 - 7.0s)
        self.wait(0.5)
