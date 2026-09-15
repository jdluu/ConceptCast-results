import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Function as input-output mapping ---
        self.camera.background_color = "#181825"

        axes = Axes(
            x_range=(-5, 5, 1),
            y_range=(-3, 5, 1),
            axis_config={"color": "#89b4fa", "stroke_width": 2},
            tips=False,
        )
        axes_labels = VGroup(
            Tex("x", color="#89b4fa").scale(0.7).next_to(axes.x_axis, RIGHT),
            Tex("f(x)", color="#89b4fa").scale(0.7).next_to(axes.y_axis, UP),
        )

        self.play(Create(axes), Write(axes_labels), run_time=1.5)

        curve = axes.plot(lambda x: x**2 / 4, color="#a6e3a1", stroke_width=2)
        self.play(Create(curve), run_time=1.5)

        mapping_arrow = Arrow(
            start=axes.c2p(-2, 0), end=axes.c2p(2, 1), color="#94e2d5", stroke_width=2
        )
        self.play(Create(mapping_arrow), run_time=0.5)

        x_tracker = ValueTracker(-4)
        input_dot = Dot(radius=0.08, color="#fab387")
        output_dot = Dot(radius=0.08, color="#f38ba8")

        input_dot.add_updater(lambda m: m.move_to(axes.c2p(x_tracker.get_value(), 0)))
        output_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(x_tracker.get_value(), x_tracker.get_value() ** 2 / 4)
            )
        )

        self.play(FadeIn(input_dot), FadeIn(output_dot), run_time=0.5)

        self.play(x_tracker.animate.set_value(4), run_time=6)

        self.wait(1.0)
        # --- Scene 2: Secant line and average rate of change ---
        self.camera.background_color = "#181825"

        # Palette
        AXIS_COLOR = "#89b4fa"
        CURVE_COLOR = "#a6e3a1"
        POINT_A_COLOR = "#fab387"
        POINT_B_COLOR = "#f38ba8"
        SECANT_COLOR = "#94e2d5"
        BRACE_COLOR = "#89b4fa"

        # Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 6, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": AXIS_COLOR, "stroke_width": 2},
            tips=False,
        )
        axes.add_coordinates()
        axes.move_to(ORIGIN)

        # Function curve f(x)=0.3 x^2 +0.5 x +1.5
        def f(x):
            return 0.3 * x**2 + 0.5 * x + 1.5

        function_curve = axes.plot(
            f, x_range=[-3.5, 3.5], color=CURVE_COLOR, stroke_width=2
        )

        # Points on curve
        x_a = -2
        x_b = 2
        y_a = f(x_a)
        y_b = f(x_b)

        point_a = Dot(point=axes.c2p(x_a, y_a), radius=0.08, color=POINT_A_COLOR)
        point_b = Dot(point=axes.c2p(x_b, y_b), radius=0.08, color=POINT_B_COLOR)

        label_a = MathTex(r"(x,\;f(x))", font_size=28).next_to(point_a, UP + LEFT)
        label_b = MathTex(r"(x+\Delta x,\;f(x+\Delta x))", font_size=28).next_to(
            point_b, UP + RIGHT
        )

        # Secant line
        secant_line = Line(
            start=axes.c2p(x_a, y_a),
            end=axes.c2p(x_b, y_b),
            color=SECANT_COLOR,
            stroke_width=2.5,
        )

        # Projections to x-axis
        proj_a_x = Dot(point=axes.c2p(x_a, 0), radius=0.03, color=POINT_A_COLOR)
        proj_b_x = Dot(point=axes.c2p(x_b, 0), radius=0.03, color=POINT_B_COLOR)
        vert_a = DashedLine(
            axes.c2p(x_a, y_a), axes.c2p(x_a, 0), color=WHITE, stroke_width=1
        )
        vert_b = DashedLine(
            axes.c2p(x_b, y_b), axes.c2p(x_b, 0), color=WHITE, stroke_width=1
        )

        # Delta x brace
        delta_x_brace = BraceBetweenPoints(
            axes.c2p(x_a, 0), axes.c2p(x_b, 0), direction=DOWN, color=BRACE_COLOR
        )
        delta_x_label = MathTex(r"\Delta x", font_size=32).next_to(delta_x_brace, DOWN)

        # Delta y brace
        left_x = -3.8
        delta_y_brace = BraceBetweenPoints(
            axes.c2p(left_x, y_a),
            axes.c2p(left_x, y_b),
            direction=LEFT,
            color=BRACE_COLOR,
        )
        delta_y_label = MathTex(r"\Delta y", font_size=32).next_to(delta_y_brace, LEFT)

        # Animation timeline = 11.0 s
        self.play(Create(axes), Create(function_curve), run_time=2)
        self.play(
            FadeIn(point_a),
            FadeIn(point_b),
            FadeIn(label_a),
            FadeIn(label_b),
            run_time=1.5,
        )
        self.play(
            Create(secant_line),
            Create(vert_a),
            Create(vert_b),
            Create(proj_a_x),
            Create(proj_b_x),
            run_time=1.5,
        )
        self.play(Create(delta_x_brace), Write(delta_x_label), run_time=1.5)
        self.play(Create(delta_y_brace), Write(delta_y_label), run_time=1.5)
        self.wait(3)
        # --- Scene 3: Limiting process of points approaching ---
        self.camera.background_color = "#181825"

        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": "#89b4fa", "stroke_width": 2},
        )

        def f(x):
            return 0.3 * x**2 + 0.2

        curve = axes.plot(f, color="#a6e3a1")
        curve.set_stroke(width=2)

        point_a_pos = axes.c2p(-1.5, f(-1.5))
        point_a = Dot(point=point_a_pos, color="#fab387", radius=0.08)
        label_a = Text("x", font_size=24).next_to(point_a, UP)

        x_b = ValueTracker(0.5)

        def get_b_point():
            x = x_b.get_value()
            return axes.c2p(x, f(x))

        point_b = always_redraw(
            lambda: Dot(point=get_b_point(), color="#f38ba8", radius=0.08)
        )
        label_b = always_redraw(
            lambda: Text("x+Δx", font_size=24).next_to(point_b.get_center(), UP)
        )

        secant = always_redraw(
            lambda: Line(
                start=point_a.get_center(),
                end=get_b_point(),
                color="#fab387",
                stroke_width=2,
            )
        )

        delta_arrow = Arrow(
            start=RIGHT * 2.5 + DOWN * 2.5,
            end=LEFT * 2.5 + DOWN * 2.5,
            color="#94e2d5",
            stroke_width=2,
        )
        delta_label = MathTex(r"\Delta x 	o 0", color="#94e2d5").next_to(
            delta_arrow, DOWN
        )
        delta_group = VGroup(delta_arrow, delta_label)

        self.play(
            Create(axes),
            Create(curve),
            FadeIn(point_a),
            Write(label_a),
            FadeIn(point_b),
            FadeIn(label_b),
            Create(secant),
            FadeIn(delta_group),
            run_time=2,
            lag_ratio=0.1,
        )

        self.play(x_b.animate.set_value(-1.45), run_time=7, rate_func=linear)

        self.wait(2.5)
        # --- Scene 4: Tangent line as instantaneous direction ---
        # Background
        self.camera.background_color = "#181825"

        # 1. Coordinate axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": "#89b4fa", "stroke_width": 2, "include_tip": False},
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": [-4, -2, 0, 2, 4],
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": [-4, -2, 0, 2, 4],
            },
        )

        # 2. Function curve  y = 0.3 x^2
        curve = ParametricFunction(
            lambda t: np.array([t, 0.3 * t * t, 0]),
            t_range=[-3, 3],
            color="#a6e3a1",
            stroke_width=2,
        )

        # 3. Tangent point
        dot_point = axes.c2p(-1, 0.3)  # near intersection with the tangent line
        tangent_point = Dot(point=dot_point, color="#f38ba8", radius=0.08)
        label_x = Text("x", font_size=36).next_to(tangent_point, UP)
        label_x.set_color("#f38ba8")

        # 4. Tangent line
        tangent_line = Line(
            start=axes.c2p(-3, -1), end=axes.c2p(3, 3), color="#fab387", stroke_width=2
        )

        # 5. Direction arrow indicating instantaneous direction
        direction_arrow = Arrow(
            start=axes.c2p(-1.5, -0.2),
            end=axes.c2p(0.5, 1.0),
            color="#94e2d5",
            stroke_width=2,
            buff=0,
        )

        # Animations – total 11 s
        self.play(Create(axes), run_time=2)
        self.play(Create(curve), run_time=2)
        self.play(FadeIn(tangent_point), Write(label_x), run_time=2)
        self.play(Create(tangent_line), run_time=2)
        self.play(Create(direction_arrow), run_time=2)
        self.wait(1)
        # --- Scene 5: Limit definition of derivative ---
        self.camera.background_color = "#181825"
        self.clear()

        # Axes on the left
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 6, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": "#89b4fa", "stroke_width": 2.0},
        )
        axes.move_to(LEFT * 2.5)

        # Curve f(x)=0.5 x^2
        f = lambda x: 0.5 * x**2
        curve = axes.plot(f, x_range=[-3, 3], color="#fab387", stroke_width=2.0)

        # Points for the difference quotient
        x0 = 1.5
        delta_start = 1.5
        delta_end = 0.05

        pt_a = Dot(radius=0.06, color=WHITE).move_to(axes.c2p(x0, f(x0)))
        pt_b = Dot(radius=0.06, color=WHITE).move_to(
            axes.c2p(x0 + delta_start, f(x0 + delta_start))
        )

        secant = Line(
            start=axes.c2p(x0, f(x0)),
            end=axes.c2p(x0 + delta_start, f(x0 + delta_start)),
            color="#94e2d5",
            stroke_width=2.0,
        )

        # Δx interval arrow on the x-axis
        arrow_start = axes.c2p(x0, 0)
        arrow_end = axes.c2p(x0 + delta_start, 0)
        delta_arrow = DoubleArrow(
            start=arrow_start,
            end=arrow_end,
            color="#f38ba8",
            stroke_width=2.0,
            buff=0,
        )
        delta_label = MathTex(r"\Delta x", color="#f38ba8").next_to(
            delta_arrow, UP, buff=0.1
        )
        collapse_label = Text("→ 0", font_size=36, color="#f38ba8").next_to(
            delta_label, RIGHT, buff=0.1
        )

        # Right side texts
        diff_text = (
            MathTex(
                r"\frac{f(x+\Delta x)-f(x)}{\Delta x}",
                color="#94e2d5",
            )
            .scale(0.9)
            .to_corner(UR)
        )

        formula_text = (
            MathTex(
                r"f'(x)=\lim_{\Delta x	o 0}\frac{f(x+\Delta x)-f(x)}{\Delta x}",
                color="#a6e3a1",
            )
            .scale(0.8)
            .next_to(diff_text, DOWN, aligned_edge=LEFT)
        )

        # Build the scene
        self.play(Create(axes), run_time=2.0)
        self.play(Create(curve), run_time=1.5)
        self.wait(0.5)

        self.play(
            FadeIn(pt_a),
            FadeIn(pt_b),
            Create(secant),
            FadeIn(delta_arrow),
            FadeIn(delta_label),
            run_time=2.0,
        )

        self.play(FadeIn(diff_text), run_time=2.0)
        self.wait(0.5)

        # Collapse Δx → 0
        target_pt_b = axes.c2p(x0 + delta_end, f(x0 + delta_end))
        target_arrow_end = axes.c2p(x0 + delta_end, 0)

        self.play(
            pt_b.animate.move_to(target_pt_b),
            secant.animate.put_start_and_end_on(axes.c2p(x0, f(x0)), target_pt_b),
            delta_arrow.animate.put_start_and_end_on(arrow_start, target_arrow_end),
            delta_label.animate.scale(0.5).next_to(delta_arrow, UP),
            run_time=4.0,
        )

        self.play(FadeIn(collapse_label), run_time=0.5)
        self.play(FadeIn(formula_text), run_time=2.5)

        self.wait(2.5)  # total duration 16.0 s
        # --- Scene 6: Derivative as a slope function ---
        self.camera.background_color = "#181825"

        # Palette from style guidelines
        color_axes_left = "#89b4fa"
        color_curve = "#a6e3a1"
        color_tangent = "#fab387"
        color_axes_right = "#94e2d5"
        color_slope = "#f38ba8"

        # Original axes on left
        ax_left = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.5, 4, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": color_axes_left, "stroke_width": 2.0},
        )
        ax_left.shift(LEFT * 4)
        label_f = Text("f(x)", color=color_axes_left, font_size=36).next_to(ax_left, UP)

        # Function curve f(x) = x^2 / 4  -> f'(x) = x/2
        f = lambda x: x**2 / 4
        graph = ax_left.plot(f, color=color_curve, stroke_width=2.0)

        # Multiple tangent lines
        tangent_lines = VGroup()
        xs = [-2, -1, 0, 1, 2]
        for x0 in xs:
            y0 = f(x0)
            m = x0 / 2
            left_pt = ax_left.c2p(x0 - 1.5, y0 + m * -1.5)
            right_pt = ax_left.c2p(x0 + 1.5, y0 + m * 1.5)
            line = Line(
                start=left_pt, end=right_pt, color=color_tangent, stroke_width=2.0
            )
            tangent_lines.add(line)

        # Slope axes on right
        ax_right = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": color_axes_right, "stroke_width": 2.0},
        )
        ax_right.shift(RIGHT * 4)
        label_fp = Text("f'(x)", color=color_axes_right, font_size=36).next_to(
            ax_right, UP
        )

        # Slope graph f'(x) = x/2
        g = lambda x: x / 2
        slope_graph = ax_right.plot(g, color=color_slope, stroke_width=2.0)

        # Animation sequence – total 11.5s
        self.play(Create(ax_left), Write(label_f), run_time=2)
        self.play(Create(graph), run_time=1.5)
        self.play(
            LaggedStart(
                *[FadeIn(line, shift=UP * 0.1) for line in tangent_lines], lag_ratio=0.4
            ),
            run_time=3,
        )
        self.play(Create(ax_right), Write(label_fp), run_time=2)
        self.play(Create(slope_graph), run_time=2)
        self.wait(1)
        # --- Scene 7: Geometric meaning of sign and zero ---
        self.camera.background_color = "#181825"
        self.clear()

        # Hill profile
        hill_curve = ParametricFunction(
            lambda t: np.array([t, -0.2 * (t - 2) ** 2 + 2, 0]), t_range=[-2, 6]
        )
        hill_curve.set_color("#a6e3a1")
        hill_curve.stroke_width = 2

        # Helpers
        def point_on_curve(t):
            return np.array([t, -0.2 * (t - 2) ** 2 + 2, 0])

        def tangent_vec(t):
            dy = -0.4 * (t - 2)
            vec = np.array([1, dy, 0])
            return vec / np.linalg.norm(vec)

        length = 1.8

        # Positive slope - left side
        t_pos = 0.5
        p_pos = point_on_curve(t_pos)
        v_pos = tangent_vec(t_pos) * length
        positive_tangent = Line(p_pos - v_pos / 2, p_pos + v_pos / 2)
        positive_tangent.set_color("#94e2d5")
        positive_tangent.stroke_width = 2
        positive_label = Text("+ slope", color="#94e2d5", font_size=28)
        positive_label.next_to(positive_tangent, UP)

        # Negative slope - right side
        t_neg = 3.5
        p_neg = point_on_curve(t_neg)
        v_neg = tangent_vec(t_neg) * length
        negative_tangent = Line(p_neg - v_neg / 2, p_neg + v_neg / 2)
        negative_tangent.set_color("#f38ba8")
        negative_tangent.stroke_width = 2
        negative_label = Text("- slope", color="#f38ba8", font_size=28)
        negative_label.next_to(negative_tangent, UP)

        # Zero slope - peak
        t_zero = 2
        p_zero = point_on_curve(t_zero)
        zero_tangent = Line(p_zero + LEFT * 0.9, p_zero + RIGHT * 0.9)
        zero_tangent.set_color("#89b4fa")
        zero_tangent.stroke_width = 2
        zero_label = Text("0 slope", color="#89b4fa", font_size=28)
        zero_label.next_to(zero_tangent, UP)

        # Up / down arrows
        up_start = p_pos + UP * 0.6
        up_end = p_pos + UP * 1.4
        up_arrow = Arrow(up_start, up_end, color="#a6e3a1", stroke_width=2)
        up_label = Text("increasing", color="#a6e3a1", font_size=24)
        up_label.next_to(up_arrow, RIGHT)

        down_start = p_neg + DOWN * 0.6
        down_end = p_neg + DOWN * 1.4
        down_arrow = Arrow(down_start, down_end, color="#f38ba8", stroke_width=2)
        down_label = Text("decreasing", color="#f38ba8", font_size=24)
        down_label.next_to(down_arrow, RIGHT)

        positive_group = VGroup(positive_tangent, positive_label, up_arrow, up_label)
        negative_group = VGroup(
            negative_tangent, negative_label, down_arrow, down_label
        )
        zero_group = VGroup(zero_tangent, zero_label)

        self.play(Create(hill_curve), run_time=1.5)
        self.play(FadeIn(positive_group), run_time=1.5)
        self.play(FadeIn(negative_group), run_time=1.5)
        self.play(FadeIn(zero_group), run_time=1.5)
        self.wait(1.5)
