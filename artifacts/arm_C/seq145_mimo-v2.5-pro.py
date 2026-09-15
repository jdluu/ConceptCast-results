import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: The Unchanging Arrow ---
        # ── Colors (Tokyo Night palette) ──
        BG_COLOR = "#1A1B26"
        GRID_COLOR = "#565F89"
        ACCENT_BLUE = "#7AA2F7"
        TEXT_COLOR = "#C0CAF5"

        # Set background
        self.camera.background_color = BG_COLOR

        # ── 1. Objects ──

        # NumberPlane (transformation grid)
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GRID_COLOR,
                "stroke_width": 1.0,
                "stroke_opacity": 0.6,
            },
            axis_config={
                "stroke_color": GRID_COLOR,
                "stroke_width": 1.5,
                "stroke_opacity": 0.8,
            },
            faded_line_ratio=2,
        )

        # Hero vector: a glowing blue arrow from origin outward
        hero_vector = Arrow(
            ORIGIN,
            RIGHT * 3,
            buff=0,
            color=ACCENT_BLUE,
            stroke_width=6,
            tip_length=0.35,
        )
        # Label "v" next to the arrow tip
        v_label = MathTex(r"\vec{v}", font_size=40, color=ACCENT_BLUE)
        v_label.next_to(hero_vector.get_end(), UR, buff=0.15)

        # Glow effect: a larger, semi-transparent copy behind the arrow
        hero_glow = Arrow(
            ORIGIN,
            RIGHT * 3,
            buff=0,
            color=ACCENT_BLUE,
            stroke_width=14,
            tip_length=0.35,
        )
        hero_glow.set_stroke(opacity=0.2)

        # Title text
        title = Text(
            "Eigenvectors",
            font_size=56,
            color=TEXT_COLOR,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.6)

        # Subtitle tagline
        subtitle = Text(
            "The Unchanging Arrow",
            font_size=28,
            color=ACCENT_BLUE,
        )
        subtitle.next_to(title, DOWN, buff=0.25)

        # ── 2. Animations (Total: ~8.0s) ──

        # Phase 1 (0–2s): Grid fades in
        self.play(FadeIn(grid), run_time=2.0)

        # Phase 2 (2–4s): Hero vector + title appear together
        self.play(
            FadeIn(hero_glow, scale=0.8),
            GrowArrow(hero_vector),
            Write(v_label),
            FadeIn(title, shift=DOWN * 0.3),
            run_time=2.0,
        )

        # Phase 3 (4–6.5s): Grid warps via shear; arrow stays fixed, only scales
        grid_target = grid.copy()
        grid_target.apply_matrix([[1.4, 0.6, 0], [0.3, 1.1, 0], [0, 0, 1]])
        self.play(
            Transform(grid, grid_target),
            hero_vector.animate.scale(1.15),
            hero_glow.animate.scale(1.15),
            v_label.animate.shift(RIGHT * 0.35 + UP * 0.1),
            run_time=2.5,
        )

        # Phase 4 (6.5–8s): Subtitle fades in, vector pulses
        self.play(
            FadeIn(subtitle, shift=UP * 0.2),
            Indicate(hero_vector, color=ACCENT_BLUE, scale_factor=1.1),
            run_time=1.5,
        )

        self.wait(0.5)
        # --- Scene 2: The Motivation: Simplifying Complexity ---
        # Palette
        bg_color = "#181825"
        chaos_color = "#BF616A"
        simple_color = "#A3BE8C"
        bridge_color = "#EBCB8B"
        text_color = "#CDD6F4"

        self.camera.background_color = bg_color

        # 1. Left Side: Chaos
        chaos_group = VGroup()
        curves = [
            CurvedArrow([-4, 1, 0], [-1.5, 2, 0], angle=PI / 2, color=chaos_color),
            CurvedArrow([-5, -1, 0], [-2, 0, 0], angle=-PI / 3, color=chaos_color),
            CurvedArrow([-3, -2, 0], [-1, 2, 0], angle=PI / 4, color=chaos_color),
            CurvedArrow([-4.5, 2, 0], [-2, -1, 0], angle=-PI / 2, color=chaos_color),
        ]

        for c in curves:
            c.set_stroke(width=4, opacity=0.8)
            chaos_group.add(c)

        chaos_label = Text("Complex Basis", font_size=24, color=text_color)
        chaos_label.next_to(chaos_group, DOWN, buff=0.5)

        chaos_bg = SurroundingRectangle(
            chaos_group, color=chaos_color, buff=0.5, corner_radius=0.2
        )
        chaos_bg.set_fill(color=chaos_color, opacity=0.1)
        chaos_bg.set_stroke(width=1, opacity=0.5)

        # 2. Right Side: Simplicity
        simple_arrow = Arrow(
            ORIGIN, RIGHT * 2.5, color=simple_color, stroke_width=8, buff=0
        )
        simple_arrow.shift(RIGHT * 3)

        simple_label = Text("Eigen-direction", font_size=24, color=text_color)
        simple_label.next_to(simple_arrow, DOWN, buff=0.5)

        simple_bg = SurroundingRectangle(
            simple_arrow, color=simple_color, buff=0.5, corner_radius=0.2
        )
        simple_bg.set_fill(color=simple_color, opacity=0.1)
        simple_bg.set_stroke(width=1, opacity=0.5)

        # 3. Center: Bridge - FIXED: Use linear interpolation
        bridge_start = np.array([-1, 0, 0])
        bridge_end = np.array([1.5, 0, 0])
        bridge = DashedLine(
            bridge_start, bridge_end, color=bridge_color, stroke_width=3
        )

        blocks = VGroup()
        for p in np.linspace(0.2, 0.8, 5):
            block = Square(side_length=0.3, color=bridge_color)
            block.set_fill(color=bridge_color, opacity=0.5)
            # Fix: interpolate directly between start/end points
            position = bridge_start + p * (bridge_end - bridge_start)
            block.move_to(position)
            blocks.add(block)

        bridge_label = Text("Simplification", font_size=24, color=text_color)
        bridge_label.next_to(bridge, UP, buff=0.5)

        # ---- ANIMATIONS ----
        self.play(
            FadeIn(chaos_bg),
            LaggedStart(*[Create(arrow) for arrow in curves], lag_ratio=0.2),
            run_time=2.0,
        )
        self.play(Write(chaos_label), run_time=0.5)
        self.wait(1.0)

        self.play(FadeIn(simple_bg), GrowArrow(simple_arrow), run_time=1.5)
        self.play(Write(simple_label), run_time=0.5)
        self.wait(1.0)

        self.play(
            Create(bridge),
            LaggedStart(*[GrowFromCenter(b) for b in blocks], lag_ratio=0.2),
            run_time=2.0,
        )
        self.play(Write(bridge_label), run_time=0.5)
        self.wait(1.0)
        # --- Scene 3: The Core Mechanic: Av = λv ---
        self.camera.background_color = "#181825"

        # Grid
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": "#3B4252",
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={"stroke_color": "#4C566A", "stroke_width": 2},
        )

        # Original eigenvector v
        vector_v = Arrow(
            start=ORIGIN,
            end=np.array([2, 1, 0]),
            buff=0,
            color="#88C0D0",
            stroke_width=5,
            tip_length=0.2,
        )
        label_v = MathTex("v", color="#88C0D0").scale(0.8)
        label_v.next_to(vector_v.get_end(), UR, buff=0.15)

        # Core equation
        equation = MathTex(r"A\vec{v} = \lambda \vec{v}", color="#ECEFF4").scale(0.9)
        equation.to_edge(UP, buff=0.6)
        equation_bg = BackgroundRectangle(
            equation, color="#181825", fill_opacity=0.85, buff=0.15
        )

        # Transformed vector Av (same direction, 2x magnitude)
        vector_av = Arrow(
            start=ORIGIN,
            end=np.array([4, 2, 0]),
            buff=0,
            color="#EBCB8B",
            stroke_width=5,
            tip_length=0.2,
        )
        label_av = MathTex(r"A\vec{v}", color="#EBCB8B").scale(0.8)
        label_av.next_to(vector_av.get_end(), UR, buff=0.15)

        # Lambda brace showing scale factor
        brace = BraceBetweenPoints(
            np.array([2, 1, 0]),
            np.array([4, 2, 0]),
            direction=np.array([0, 0, 0]),
            color="#A3BE8C",
        )
        lambda_label = MathTex(r"\lambda = 2", color="#A3BE8C").scale(0.7)
        lambda_label.next_to(brace, RIGHT, buff=0.15)

        vector_v_copy = vector_v.copy()

        # --- Animation Sequence ---
        self.play(FadeIn(plane), run_time=1.5)
        self.play(GrowArrow(vector_v), FadeIn(label_v), run_time=2.0)
        self.play(FadeIn(equation_bg), Write(equation), run_time=1.5)
        self.play(Transform(vector_v_copy, vector_av), FadeOut(label_v), run_time=3.0)
        self.play(
            FadeIn(label_av), GrowFromCenter(brace), FadeIn(lambda_label), run_time=2.0
        )
        self.play(Indicate(equation, color="#EBCB8B", scale_factor=1.15), run_time=1.0)
        self.wait(1.0)
        # --- Scene 4: The Pitfall: Rotation Trap ---
        # --- Color Palette (Nord Theme) ---
        BG_COLOR = "#2E3440"
        TEXT_COLOR = "#ECEFF4"
        SECONDARY_TEXT = "#D8DEE9"
        BLUE = "#88C0D0"
        GREEN = "#A3BE8C"
        YELLOW = "#EBCB8B"
        RED = "#BF616A"

        # --- Setup Background ---
        self.camera.background_color = BG_COLOR

        # --- Title ---
        title = Text(
            "The Pitfall: Rotation Trap", font_size=42, color=TEXT_COLOR, weight=BOLD
        )
        title.to_edge(UP, buff=0.4)

        subtitle = Text("Rotation vs Scaling", font_size=28, color=SECONDARY_TEXT)
        subtitle.next_to(title, DOWN, buff=0.15)

        # --- Divider ---
        divider = DashedLine(
            start=UP * 2.2,
            end=DOWN * 2.5,
            dash_length=0.15,
            color=SECONDARY_TEXT,
            stroke_width=1.5,
        )

        # --- Labels ---
        left_label = Text("✗ Rotation", font_size=28, color=RED, weight=BOLD)
        left_label.move_to(UP * 1.8 + LEFT * 3.5)

        right_label = Text("✓ Scaling", font_size=28, color=GREEN, weight=BOLD)
        right_label.move_to(UP * 1.8 + RIGHT * 3.5)

        # --- Vectors Setup ---
        left_origin = LEFT * 3.5 + DOWN * 0.5
        right_origin = RIGHT * 3.5 + DOWN * 0.5

        left_arrow_orig = Arrow(
            start=left_origin,
            end=left_origin + UP * 1.5 + RIGHT * 1.0,
            buff=0,
            color=BLUE,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.2,
        )

        right_arrow_orig = Arrow(
            start=right_origin,
            end=right_origin + UP * 1.5 + RIGHT * 1.0,
            buff=0,
            color=BLUE,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.2,
        )

        # --- Transformed Vectors ---
        # Left: Rotated (direction changed!)
        left_arrow_transformed = Arrow(
            start=left_origin,
            end=left_origin + UP * 0.5 + RIGHT * 1.8,
            buff=0,
            color=RED,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.2,
        )

        # Right: Scaled 1.5x (same direction!)
        right_arrow_transformed = Arrow(
            start=right_origin,
            end=right_origin + (UP * 1.5 + RIGHT * 1.0) * 1.5,
            buff=0,
            color=GREEN,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.2,
        )

        # --- Rotation Arc ---
        angle_arc = Arc(
            radius=0.6,
            start_angle=left_arrow_orig.get_angle(),
            angle=left_arrow_transformed.get_angle() - left_arrow_orig.get_angle(),
            arc_center=left_origin,
            color=YELLOW,
            stroke_width=2,
        )
        angle_label = MathTex(r"\theta", font_size=32, color=YELLOW)
        angle_label.next_to(angle_arc, UR, buff=0.1)

        # --- Marks ---
        cross_mark = Text("✗", font_size=60, color=RED, weight=BOLD)
        cross_mark.move_to(left_origin + DOWN * 1.8)

        check_mark = Text("✓", font_size=60, color=GREEN, weight=BOLD)
        check_mark.move_to(right_origin + DOWN * 1.8)

        # --- Explanation Text ---
        left_explain = Text(
            "Direction changed!\nNot an Eigenvector", font_size=18, color=RED
        )
        left_explain.move_to(cross_mark.get_center() + DOWN * 0.8)

        right_explain = Text(
            "Direction preserved!\nIs an Eigenvector", font_size=18, color=GREEN
        )
        right_explain.move_to(check_mark.get_center() + DOWN * 0.8)

        # --- Span Line (for right side) ---
        span_line = DashedLine(
            start=right_origin,
            end=right_origin + (UP * 1.5 + RIGHT * 1.0) * 2.2,
            dash_length=0.1,
            color=YELLOW,
            stroke_width=2,
        )

        # --- Key Insight ---
        insight = MathTex(r"A\vec{x} = \lambda\vec{x}", font_size=36, color=TEXT_COLOR)
        insight.to_edge(DOWN, buff=0.5)

        insight_text = Text(
            "Direction must stay on the span", font_size=20, color=YELLOW
        )
        insight_text.next_to(insight, DOWN, buff=0.1)

        # ==================== ANIMATIONS ====================

        # 1. Title + subtitle fade in
        self.play(FadeIn(title), run_time=0.6)
        self.play(FadeIn(subtitle), run_time=0.5)
        self.wait(0.3)

        # 2. Divider + labels appear
        self.play(
            Create(divider), FadeIn(left_label), FadeIn(right_label), run_time=0.8
        )
        self.wait(0.2)

        # 3. Original vectors grow
        self.play(GrowArrow(left_arrow_orig), GrowArrow(right_arrow_orig), run_time=0.8)
        self.wait(0.3)

        # 4. Left: rotation happens
        self.play(
            Transform(left_arrow_orig, left_arrow_transformed),
            Create(angle_arc),
            FadeIn(angle_label),
            run_time=1.0,
        )

        # 5. Right: scaling happens
        self.play(
            Transform(right_arrow_orig, right_arrow_transformed),
            Create(span_line),
            run_time=1.0,
        )
        self.wait(0.2)

        # 6. Marks pop in
        self.play(
            FadeIn(cross_mark, scale=1.5), FadeIn(check_mark, scale=1.5), run_time=0.6
        )

        # 7. Explanatory notes
        self.play(FadeIn(left_explain), FadeIn(right_explain), run_time=0.8)
        self.wait(0.3)

        # 8. Key insight appears
        self.play(Write(insight), run_time=0.8)
        self.play(FadeIn(insight_text), run_time=0.5)
        self.play(Circumscribe(insight, color=YELLOW, buff=0.15), run_time=0.7)

        # Hold final frame
        self.wait(1.5)
        # --- Scene 5: Application: Stability Analysis ---
        self.camera.background_color = "#181825"

        # --- Objects ---

        # 1. Input Matrix (Stable system: A = [[-2, -1], [-1, -2]])
        input_matrix = (
            Matrix(
                [[-2, -1], [-1, -2]],
                bracket_h_buff=0.2,
                bracket_v_buff=0.2,
                element_to_mobject_config={"color": "#ECEFF4"},
            )
            .set_color("#81A1C1")
            .scale(0.8)
        )

        input_text = Text("System Matrix A", font_size=24, color="#D8DEE9").next_to(
            input_matrix, DOWN, buff=0.2
        )
        input_group = VGroup(input_matrix, input_text).move_to(LEFT * 4.5)

        # 2. Computation Block
        calc_rect = RoundedRectangle(
            corner_radius=0.15,
            width=3.0,
            height=2.0,
            fill_color="#5E6580",
            fill_opacity=1,
            stroke_color="#D8DEE9",
            stroke_width=1.5,
        ).move_to(ORIGIN)
        calc_text = Text(
            "Compute\nEigenvalues", font_size=24, color="#ECEFF4", line_spacing=1
        ).move_to(calc_rect)
        calc_group = VGroup(calc_rect, calc_text)

        # 3. Eigenvalue Display
        eigenval_1 = MathTex(r"\lambda_1 = -1", color="#BF616A").scale(0.8)
        eigenval_2 = MathTex(r"\lambda_2 = -3", color="#BF616A").scale(0.8)
        eigenval_text = Text("Negative Real Parts", font_size=20, color="#A3BE8C")
        eigenvals = VGroup(eigenval_1, eigenval_2, eigenval_text).arrange(
            DOWN, buff=0.15
        )

        # 4. Phase Portrait Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
            axis_config={
                "color": "#D8DEE9",
                "stroke_width": 1,
                "include_numbers": False,
            },
        ).move_to(RIGHT * 4.5)

        origin_dot = Dot(axes.c2p(0, 0), color="#EBCB8B", radius=0.1)
        origin_label = Text("Stable Sink", font_size=18, color="#EBCB8B").next_to(
            origin_dot, DOWN, buff=0.2
        )

        # 5. Streamlines pointing inward (sink visualization)
        stream_lines = VGroup()
        n_lines = 12
        radius = 2.8
        for i in range(n_lines):
            angle = i * TAU / n_lines
            start_point = axes.c2p(radius * np.cos(angle), radius * np.sin(angle))
            end_point = axes.c2p(0, 0)
            arrow = Arrow(
                start_point,
                end_point,
                buff=0.4,
                color="#88C0D0",
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
                stroke_opacity=0.6,
            )
            stream_lines.add(arrow)

        # 6. Eigenvector Lines (v1=(1,-1), v2=(1,1))
        v1_start = axes.c2p(-2.5, 2.5)
        v1_end = axes.c2p(2.5, -2.5)
        v2_start = axes.c2p(-2.5, -2.5)
        v2_end = axes.c2p(2.5, 2.5)

        eigen_line_1 = DashedLine(v1_start, v1_end, color="#EBCB8B", stroke_width=4)
        eigen_line_2 = DashedLine(v2_start, v2_end, color="#EBCB8B", stroke_width=4)
        eigen_lines = VGroup(eigen_line_1, eigen_line_2)

        eigen_label = Text("Eigenvectors", font_size=22, color="#EBCB8B").next_to(
            axes, UP, buff=0.3
        )

        # Connecting pipeline arrows
        arrow_1 = Arrow(
            input_group.get_right() + RIGHT * 0.2,
            calc_group.get_left() + LEFT * 0.2,
            buff=0.1,
            color="#D8DEE9",
        )
        arrow_2 = Arrow(
            calc_group.get_right() + RIGHT * 0.2,
            axes.get_left() + LEFT * 0.2,
            buff=0.1,
            color="#D8DEE9",
        )

        # --- Animations (12.0s total) ---

        # Phase 1: Input & Setup (0.0 - 3.0s)
        self.play(FadeIn(input_group, shift=RIGHT * 0.5), run_time=1.0)
        self.wait(0.5)
        self.play(GrowArrow(arrow_1), run_time=0.5)
        self.play(FadeIn(calc_group, scale=0.8), run_time=0.5)
        self.wait(0.5)

        # Phase 2: Calculation (3.0 - 5.5s)
        self.play(Indicate(calc_text, color="#88C0D0"), run_time=1.0)
        self.play(
            calc_text.animate.scale(0.7).next_to(calc_rect, UP, buff=0.1),
            FadeIn(eigenvals, shift=UP * 0.3),
            run_time=1.0,
        )
        self.wait(0.5)

        # Phase 3: Visualization Output (5.5 - 8.0s)
        self.play(GrowArrow(arrow_2), run_time=0.5)
        self.play(Create(axes), FadeIn(origin_dot), run_time=0.8)
        self.play(FadeIn(origin_label), run_time=0.2)
        self.play(
            LaggedStart(*[GrowArrow(line) for line in stream_lines], lag_ratio=0.05),
            run_time=0.5,
        )
        self.wait(0.5)

        # Phase 4: Eigenvectors & Convergence (8.0 - 12.0s)
        self.play(Create(eigen_lines), FadeIn(eigen_label), run_time=1.0)
        self.wait(0.5)

        # Animate particle converging to origin
        particle = Dot(color="#F38BA8", z_index=10).scale(1.2)
        start_pos = stream_lines[9].get_start()
        particle.move_to(start_pos)
        self.play(FadeIn(particle), run_time=0.5)

        self.play(
            particle.animate.move_to(origin_dot),
            run_time=1.0,
            rate_func=rate_functions.ease_in_quad,
        )
        self.play(
            FadeOut(particle, scale=0.5),
            Flash(origin_dot, color="#F38BA8", line_length=0.2),
            run_time=0.5,
        )

        self.wait(0.5)

        # Final fade
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)
