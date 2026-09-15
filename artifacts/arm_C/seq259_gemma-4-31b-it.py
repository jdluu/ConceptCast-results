from manim import *


class SceneGen(Scene):
    def construct(self):
        self.clear()
        # STYLE GUIDELINES
        self.camera.background_color = "#181825"
        C_BLUE = "#89b4fa"
        C_ORANGE = "#fab387"
        C_PINK = "#f38ba8"
        C_GREEN = "#a6e3a1"
        C_TEAL = "#94e2d5"

        # -----------------------------------------------------------------
        # SCENE 1: Average Rate of Change (13s)
        # -----------------------------------------------------------------
        axes = Axes(
            x_range=[-1, 3],
            y_range=[-1, 8],
            x_length=6,
            y_length=6,
            axis_config={"color": C_BLUE},
        ).shift(LEFT * 2)

        def f(x):
            return x**3

        curve = axes.plot(f, x_range=[0, 2], color=C_TEAL)

        p_x = 1.0
        q_x = 2.5
        point_p = Dot(axes.c2p(p_x, f(p_x)), color=C_ORANGE)
        point_q = Dot(axes.c2p(q_x, f(q_x)), color=C_ORANGE)

        secant_line = Line(point_p.get_center(), point_q.get_center(), color=C_PINK)

        self.play(Create(axes), Create(curve), run_time=2)
        self.play(FadeIn(point_p), FadeIn(point_q), run_time=2)
        self.play(Create(secant_line), run_time=3)
        self.wait(6)  # Total: 13s

        # -----------------------------------------------------------------
        # SCENE 2: Interval Width (12s)
        # -----------------------------------------------------------------
        x_p = axes.c2p(p_x, 0)
        x_q = axes.c2p(q_x, 0)
        proj_p = DashedLine(point_p.get_center(), x_p, color=C_BLUE)
        proj_q = DashedLine(point_q.get_center(), x_q, color=C_BLUE)

        h_brace = Brace(Line(x_p, x_q), DOWN, color=C_GREEN)
        h_label = MathTex("h", color=C_GREEN).next_to(h_brace, DOWN)

        self.play(Create(proj_p), Create(proj_q), run_time=3)
        self.play(Create(h_brace), Write(h_label), run_time=3)
        self.play(Indicate(h_brace), run_time=2)
        self.wait(4)  # Total: 12s

        # -----------------------------------------------------------------
        # SCENE 3: Slope Formula (13s)
        # -----------------------------------------------------------------
        # Vertical rise: from P's height to Q's height at Q's x-position
        rise_start = axes.c2p(q_x, f(p_x))
        rise_end = point_q.get_center()
        vertical_rise = DashedLine(rise_start, rise_end, color=C_PINK)

        formula = MathTex(
            r"	ext{Slope} = \frac{f(x+h) - f(x)}{h}", color=C_ORANGE
        ).shift(RIGHT * 4 + UP * 1)
        # Highlight numerator: f(x+h) - f(x)
        num_box = SurroundingRectangle(formula[0][4:12], color=C_PINK)

        self.play(Create(vertical_rise), run_time=3)
        self.play(Write(formula), run_time=3)
        self.play(Create(num_box), run_time=3)
        self.wait(4)  # Total: 13s

        # -----------------------------------------------------------------
        # SCENE 4: The Limit Process (13s) - OPTIMIZED
        # -----------------------------------------------------------------
        # We use a ValueTracker for h
        h_tracker = ValueTracker(q_x - p_x)

        # Redrawables
        point_q_dyn = always_redraw(
            lambda: Dot(
                axes.c2p(p_x + h_tracker.get_value(), f(p_x + h_tracker.get_value())),
                color=C_ORANGE,
            )
        )
        secant_dyn = always_redraw(
            lambda: Line(point_p.get_center(), point_q_dyn.get_center(), color=C_PINK)
        )
        proj_q_dyn = always_redraw(
            lambda: DashedLine(
                point_q_dyn.get_center(),
                axes.c2p(p_x + h_tracker.get_value(), 0),
                color=C_BLUE,
            )
        )
        brace_dyn = always_redraw(
            lambda: Brace(
                Line(x_p, axes.c2p(p_x + h_tracker.get_value(), 0)), DOWN, color=C_GREEN
            )
        )

        limit_text = MathTex(r"h 	o 0", color=C_BLUE).next_to(formula, DOWN)

        # Swap static for dynamic
        self.remove(point_q, secant_line, proj_q, h_brace)
        self.add(point_q_dyn, secant_dyn, proj_q_dyn, brace_dyn)

        self.play(Write(limit_text), run_time=3)
        self.play(h_tracker.animate.set_value(0.01), run_time=7, rate_func=linear)
        self.wait(3)  # Total: 13s

        # -----------------------------------------------------------------
        # SCENE 5: The Tangent Line (14s)
        # -----------------------------------------------------------------
        # Final tangent line calculation
        slope_at_p = 3 * (p_x**2)
        tangent_line = Line(
            axes.c2p(p_x - 0.5, f(p_x) - 0.5 * slope_at_p),
            axes.c2p(p_x + 0.5, f(p_x) + 0.5 * slope_at_p),
            color=C_PINK,
        )

        derivative_notation = MathTex(
            r"f'(x) = \lim_{h 	o 0} \frac{f(x+h) - f(x)}{h}", color=C_ORANGE
        ).move_to(formula)

        self.play(
            ReplacementTransform(secant_dyn, tangent_line),
            ReplacementTransform(formula, derivative_notation),
            FadeOut(num_box),
            FadeOut(limit_text),
            run_time=4,
        )
        self.play(Indicate(point_p, color=C_ORANGE, scale_factor=2), run_time=2)
        self.wait(8)  # Total: 14s

        # -----------------------------------------------------------------
        # SCENE 6: The Derivative Function (12s)
        # -----------------------------------------------------------------
        # Cleanup for split screen
        self.play(
            axes.animate.scale(0.7).to_edge(UP),
            curve.animate.scale(0.7).to_edge(UP),
            tangent_line.animate.scale(0.7).to_edge(UP),
            point_p.animate.scale(0.7).to_edge(UP),
            FadeOut(derivative_notation),
            run_time=3,
        )

        lower_axes = Axes(
            x_range=[0, 2],
            y_range=[0, 12],
            x_length=6,
            y_length=4,
            axis_config={"color": C_BLUE},
        ).shift(DOWN * 2)

        # Derivative of x^3 is 3x^2
        def df(x):
            return 3 * (x**2)

        der_curve = lower_axes.plot(df, x_range=[0, 2], color=C_GREEN)

        slope_tracker = Dot(lower_axes.c2p(0, 0), color=C_ORANGE)
        moving_p = Dot(axes.c2p(0, f(0)), color=C_ORANGE)

        connector = always_redraw(
            lambda: DashedLine(
                moving_p.get_center(), slope_tracker.get_center(), color=C_TEAL
            )
        )

        # ValueTracker for the motion
        x_val = ValueTracker(0)
        moving_p.add_updater(
            lambda m: m.move_to(axes.c2p(x_val.get_value(), f(x_val.get_value())))
        )
        slope_tracker.add_updater(
            lambda m: m.move_to(
                lower_axes.c2p(x_val.get_value(), df(x_val.get_value()))
            )
        )

        self.add(lower_axes, der_curve, slope_tracker, moving_p, connector)
        self.play(x_val.animate.set_value(2), run_time=6)
        self.wait(3)  # Total: 12s (approx, scaled for rendering stability)

        # -----------------------------------------------------------------
        # SCENE 7: Physical Interpretation (13s)
        # -----------------------------------------------------------------
        self.clear()
        pos_axes = Axes(
            x_range=[0, 5],
            y_range=[0, 10],
            x_length=6,
            y_length=6,
            axis_config={"color": C_BLUE},
        )
        pos_label = Text("Position", font_size=24, color=C_BLUE).next_to(
            pos_axes.y_axis, LEFT
        )

        # Simple curve for position
        pos_curve = pos_axes.plot(lambda x: 0.5 * x**2, x_range=[0, 4], color=C_TEAL)
        car = Dot(pos_axes.c2p(0, 0), color=C_ORANGE).scale(2)

        self.play(Create(pos_axes), Create(pos_label), Create(pos_curve), run_time=3)
        self.play(MoveAlongPath(car, pos_curve), run_time=4)

        # Transition to Velocity
        vel_axes = Axes(
            x_range=[0, 5],
            y_range=[0, 10],
            x_length=6,
            y_length=6,
            axis_config={"color": C_BLUE},
        )
        vel_label = Text("Velocity", font_size=24, color=C_GREEN).next_to(
            vel_axes.y_axis, LEFT
        )
        vel_curve = vel_axes.plot(lambda x: x, x_range=[0, 4], color=C_GREEN)

        self.play(
            ReplacementTransform(pos_axes, vel_axes),
            ReplacementTransform(pos_label, vel_label),
            ReplacementTransform(pos_curve, vel_curve),
            car.animate.move_to(vel_axes.c2p(0, 0)),
            run_time=3,
        )
        self.play(MoveAlongPath(car, vel_curve), run_time=3)
        # The total duration for this scene is already 13s based on previous animations
