import numpy as np
from manim import *

class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: The Concept of Rate of Change (Average vs Instantaneous) ---
        plane1 = NumberPlane(
            x_range=[-1, 4, 1],
            y_range=[-1, 8, 1],
            x_length=6,
            y_length=5,
        ).shift(RIGHT * 0.5)
        
        def func(x):
            return 0.5 * x**2 - 0.2 * x + 1

        curve1 = plane1.plot(func, x_range=[-0.5, 3.5], color=BLUE)
        curve_label = MathTex("y = f(x)", color=BLUE).next_to(curve1, UP, buff=0.5)
        
        dot_a = Dot(plane1.c2p(1, func(1)), color=YELLOW)
        dot_b = Dot(plane1.c2p(3, func(3)), color=YELLOW)
        labels = VGroup(
            MathTex("A").next_to(dot_a, DOWN+LEFT, buff=0.1),
            MathTex("B").next_to(dot_b, DOWN+RIGHT, buff=0.1)
        )

        secant_line = Line(
            plane1.c2p(1, func(1)), 
            plane1.c2p(3, func(3)), 
            color=GREEN
        )

        rise = DashedLine(
            plane1.c2p(3, func(1)), 
            plane1.c2p(3, func(3)), 
            color=YELLOW_B
        )
        run = DashedLine(
            plane1.c2p(1, func(1)), 
            plane1.c2p(3, func(1)), 
            color=YELLOW_B
        )
        rise_label = MathTex(r"\Delta y").next_to(rise, RIGHT, buff=0.1).set_color(YELLOW_B)
        run_label = MathTex(r"\Delta x").next_to(run, DOWN, buff=0.1).set_color(YELLOW_B)

        avg_rate = MathTex(
            r"\text{Average Rate} = \frac{\Delta y}{\Delta x} = \frac{f(b) - f(a)}{b - a}"
        ).to_edge(DOWN).set_color(GREEN)

        self.play(Write(plane1), Create(curve1), Write(curve_label))
        self.play(FadeIn(dot_a), FadeIn(dot_b), Write(labels))
        self.play(Create(secant_line))
        self.play(Create(rise), Create(run), Write(rise_label), Write(run_label))
        self.play(Write(avg_rate))
        self.wait(2)
        
        # Clear for next scene
        self.play(
            FadeOut(plane1), FadeOut(curve1), FadeOut(curve_label),
            FadeOut(dot_a), FadeOut(dot_b), FadeOut(labels),
            FadeOut(secant_line), FadeOut(rise), FadeOut(run),
            FadeOut(rise_label), FadeOut(run_label), FadeOut(avg_rate)
        )
        self.clear()

        # --- Scene 2: Zooming In - The Limit Process ---
        plane2 = NumberPlane(
            x_range=[0.5, 1.5, 0.1],
            y_range=[0.8, 1.8, 0.1],
            x_length=6,
            y_length=5,
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1, "stroke_opacity": 0.5}
        ).shift(RIGHT * 0.5)
        curve2 = plane2.plot(func, x_range=[0.5, 1.5], color=BLUE)
        
        x0 = 1.0
        y0 = func(x0)
        p_dot = Dot(plane2.c2p(x0, y0), color=YELLOW)
        p_label = MathTex("P").next_to(p_dot, UP, buff=0.1)

        title = Text("Approaching the Instantaneous Rate").to_edge(UP)

        self.play(Write(plane2), Create(curve2), FadeIn(p_dot), Write(p_label), Write(title))
        
        # Animate the second point Q getting closer to P
        q_tracker = ValueTracker(2.0)
        
        q_dot = always_redraw(
            lambda: Dot(plane2.c2p(q_tracker.get_value(), func(q_tracker.get_value())), color=GREEN)
        )
        secant2 = always_redraw(
            lambda: Line(
                plane2.c2p(x0, y0),
                plane2.c2p(q_tracker.get_value(), func(q_tracker.get_value())),
                color=GREEN
            )
        )
        slope_text = always_redraw(
            lambda: MathTex(
                f"\\text{{Slope}} \\approx { (func(q_tracker.get_value()) - y0) / (q_tracker.get_value() - x0):.2f}"
            ).set_color(GREEN).to_edge(DOWN)
        )

        self.play(FadeIn(q_dot), Create(secant2), Write(slope_text))
        self.play(q_tracker.animate.set_value(1.1), run_time=3, rate_func=linear)
        self.play(q_tracker.animate.set_value(1.01), run_time=3, rate_func=linear)
        
        tangent_line = plane2.get_secant_slope_group(
            x=1.0,
            graph=curve2,
            dx=0.00001, # Very small dx to approximate tangent
            secant_line_color=RED,
            secant_line_length=4
        )

        limit_text = MathTex(
            r"\lim_{x \to a} \frac{f(x) - f(a)}{x - a} = f'(a)"
        ).set_color(RED).to_edge(DOWN)

        self.play(FadeOut(secant2), FadeOut(q_dot), FadeOut(slope_text))
        self.play(Create(tangent_line), Write(limit_text))
        self.wait(2)

        self.play(
            FadeOut(plane2), FadeOut(curve2), FadeOut(p_dot), FadeOut(p_label),
            FadeOut(title), FadeOut(tangent_line), FadeOut(limit_text)
        )
        self.clear()

        # --- Scene 3: The Formal Definition ---
        definition = MathTex(
            r"f'(x) &= \lim_{\Delta x \to 0} \frac{f(x + \Delta x) - f(x)}{\Delta x}",
            font_size=48
        ).to_edge(UP)

        step1 = MathTex(
            r"\text{Let } \Delta x = h", 
            font_size=36
        ).next_to(definition, DOWN, buff=0.5)

        step2 = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            font_size=48
        ).next_to(step1, DOWN, buff=0.5)

        note = Text(
            "This is the 'Difference Quotient' approaching a limit.",
            font_size=24,
            color=YELLOW
        ).next_to(step2, DOWN, buff=0.5)

        self.play(Write(definition))
        self.wait(1)
        self.play(Write(step1))
        self.wait(1)
        self.play(Write(step2))
        self.play(FadeIn(note))
        self.wait(2)

        self.play(FadeOut(definition), FadeOut(step1), FadeOut(step2), FadeOut(note))
        self.clear()

        # --- Scene 4: Example 1 - Calculating f(x) = x^2 ---
        title_ex = Text("Example: Find the derivative of f(x) = x²").to_edge(UP)
        
        calc1 = MathTex(r"f(x) = x^2").next_to(title_ex, DOWN, buff=0.5)
        calc2 = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{(x+h)^2 - x^2}{h}"
        ).next_to(calc1, DOWN, buff=0.4)
        calc3 = MathTex(
            r"= \lim_{h \to 0} \frac{x^2 + 2xh + h^2 - x^2}{h}"
        ).next_to(calc2, DOWN, buff=0.4)
        calc4 = MathTex(
            r"= \lim_{h \to 0} \frac{2xh + h^2}{h}"
        ).next_to(calc3, DOWN, buff=0.4)
        calc5 = MathTex(
            r"= \lim_{h \to 0} (2x + h)"
        ).next_to(calc4, DOWN, buff=0.4)
        final_res = MathTex(r"= 2x").next_to(calc5, DOWN, buff=0.4).set_color(GREEN)

        box = SurroundingRectangle(final_res, color=YELLOW, buff=0.2)

        self.play(Write(title_ex))
        self.play(Write(calc1))
        self.wait(0.5)
        self.play(Write(calc2))
        self.wait(1)
        self.play(Write(calc3))
        self.wait(1)
        self.play(Write(calc4))
        self.wait(1)
        self.play(Write(calc5))
        self.wait(1)
        self.play(Write(final_res))
        self.play(Create(box))
        self.wait(2)

        self.play(
            FadeOut(title_ex), FadeOut(calc1), FadeOut(calc2), FadeOut(calc3),
            FadeOut(calc4), FadeOut(calc5), FadeOut(final_res), FadeOut(box)
        )
        self.clear()

        # --- Scene 5: Geometric Interpretation of the Result ---
        plane3 = NumberPlane(
            x_range=[-3, 4, 1],
            y_range=[-1, 10, 1],
            x_length=6,
            y_length=5,
        ).shift(LEFT * 2)
        
        func_sq = lambda x: x**2
        deriv_sq = lambda x: 2*x

        curve_sq = plane3.plot(func_sq, x_range=[-2.5, 3], color=BLUE)
        curve_label_sq = MathTex("x^2", color=BLUE).move_to(plane3.c2p(-2, 5))
        
        deriv_graph = plane3.plot(deriv_sq, x_range=[-2.5, 3], color=RED)
        deriv_label = MathTex("2x", color=RED).move_to(plane3.c2p(1.5, 4))

        explanation = VGroup(
            Text("The derivative", font_size=24),
            MathTex("f'(x) = 2x", font_size=36, color=RED),
            Text("gives the slope of the tangent", font_size=24),
            Text("at any point x on the curve.", font_size=24)
        ).arrange(DOWN, center=False, aligned_edge=LEFT).to_edge(RIGHT)

        self.play(Create(plane3), Write(curve_sq), Write(curve_label_sq))
        self.play(Write(explanation))
        self.wait(1)
        self.play(Create(deriv_graph), Write(deriv_label))

        # Animated tangent at x=2
        x_val = ValueTracker(-2)
        tangent_line_anim = always_redraw(
            lambda: plane3.get_secant_slope_group(
                x=x_val.get_value(),
                graph=curve_sq,
                dx=0.001,
                secant_line_color=YELLOW,
                secant_line_length=5
            )
        )
        
        slope_display = always_redraw(
            lambda: MathTex(
                f"slope = {2*x_val.get_value():.1f}", 
                font_size=36
            ).next_to(explanation, DOWN, buff=0.5).set_color(YELLOW)
        )

        self.play(Create(tangent_line_anim), Write(slope_display))
        self.play(x_val.animate.set_value(3), run_time=5, rate_func=smooth)
        self.wait(2)

        self.play(
            FadeOut(plane3), FadeOut(curve_sq), FadeOut(curve_label_sq),
            FadeOut(deriv_graph), FadeOut(deriv_label), FadeOut(explanation),
            FadeOut(tangent_line_anim), FadeOut(slope_display)
        )
        self.clear()

        # --- Scene 6: Physical Meaning - Velocity ---
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 25, 5],
            x_length=6,
            y_length=5,
            axis_config={"include_numbers": True}
        ).shift(LEFT * 2)
        
        t_label = axes.get_x_axis_label("t (s)")
        s_label = axes.get_y_axis_label("s (m)")

        def pos_func(t):
            return 2 * t**2

        pos_graph = axes.plot(pos_func, x_range=[0, 5], color=BLUE)
        pos_label = MathTex("s(t) = 2t^2").next_to(pos_graph, UR, buff=0.1)

        vel_text = VGroup(
            MathTex(r"v(t) = \frac{ds}{dt} = 4t", font_size=48, color=GREEN),
            MathTex(r"\text{Velocity is the derivative of position}", font_size=28)
        ).arrange(DOWN, buff=0.3).to_edge(RIGHT)

        self.play(Write(axes), Write(t_label), Write(s_label))
        self.play(Create(pos_graph), Write(pos_label))
        self.play(Write(vel_text))
        self.wait(1)

        # Show tangent slope at t=2
        t_val = 2.0
        slope_grp = axes.get_secant_slope_group(
            x=t_val, graph=pos_graph, dx=0.001,
            secant_line_color=YELLOW, secant_line_length=4
        )
        dot_v = Dot(axes.c2p(t_val, pos_func(t_val)), color=YELLOW)
        speed_val = MathTex(f"v(2) = 8 m/s", color=YELLOW).next_to(dot_v, RIGHT, buff=0.2)
        
        self.play(Create(slope_grp), FadeIn(dot_v), Write(speed_val))
        self.wait(2)

        self.play(
            FadeOut(axes), FadeOut(t_label), FadeOut(s_label), FadeOut(pos_graph),
            FadeOut(pos_label), FadeOut(vel_text), FadeOut(slope_grp),
            FadeOut(dot_v), FadeOut(speed_val)
        )
        self.clear()

        # --- Scene 7: Derivative Notation ---
        notations = VGroup(
            MathTex(r"\text{Leibniz: } \frac{dy}{dx} \text{ or } \frac{df}{dx}", font_size=40),
            MathTex(r"\text{Lagrange: } f'(x)", font_size=40),
            MathTex(r"\text{Newton: } \dot{y}", font_size=40),
            MathTex(r"\text{Evaluation: } f'(a) = \left. \frac{df}{dx} \right|_{x=a}", font_size=40),
        ).arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to(ORIGIN)

        self.play(Write(notations[0]))
        self.wait(1)
        self.play(Write(notations[1]))
        self.wait(1)
        self.play(Write(notations[2]))
        self.wait(1)
        self.play(Write(notations[3]))
        self.wait(2)

        self.play(FadeOut(notations))
        self.clear()

        # --- Scene 8: Summary and Conclusion ---
        summary_title = Text("Summary: The Derivative", font_size=48, color=YELLOW).to_edge(UP)
        
        points = VGroup(
            MathTex(r"1. \text{ Measures instantaneous rate of change}", font_size=32),
            MathTex(r"2. \text{ Slope of the tangent line}", font_size=32),
            MathTex(r"3. \text{ Defined by the limit of the difference quotient:}", font_size=32),
            MathTex(r"   f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}", font_size=36, color=GREEN),
            MathTex(r"4. \text{ Foundation of Differential Calculus}", font_size=32),
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).next_to(summary_title, DOWN, buff=0.8)

        final_curve = Axes(
            x_range=[-2, 4], y_range=[-1, 5],
            x_length=4, y_length=3
        ).to_edge(DOWN+RIGHT)
        f_graph = final_curve.plot(lambda x: 0.5*x**2, x_range=[-2, 3], color=BLUE)
        tan_final = final_curve.get_secant_slope_group(
            x=1.5, graph=f_graph, dx=0.001,
            secant_line_color=RED, secant_line_length=3
        )

        self.play(Write(summary_title))
        for p in points:
            self.play(Write(p), run_time=1.5)
            self.wait(0.5)
        
        self.play(Create(final_curve), Create(f_graph), Create(tan_final))
        self.wait(3)

        self.play(
            *[FadeOut(m) for m in self.mobjects]
        )
