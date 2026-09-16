from manim import *

class SceneGen(Scene):
    def construct(self):
        # ============================================================
        # SCENE 1: Introduction to Average Rate of Change
        # ============================================================
        title1 = Text("Average Rate of Change", font_size=48).to_edge(UP)
        self.play(Write(title1))

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)

        graph = axes.plot(lambda x: x**2, color=BLUE, x_range=[0, 4])
        graph_label = axes.get_graph_label(graph, label="f(x) = x^2", x_val=3.5, direction=UP)

        self.play(Create(axes), Create(graph), Write(graph_label))

        # Points A and B
        x_a, x_b = 1, 3
        point_a = Dot(axes.c2p(x_a, x_a**2), color=RED)
        point_b = Dot(axes.c2p(x_b, x_b**2), color=RED)
        label_a = MathTex("A", font_size=36).next_to(point_a, DL)
        label_b = MathTex("B", font_size=36).next_to(point_b, UR)

        self.play(FadeIn(point_a, point_b), Write(label_a), Write(label_b))

        # Secant Line
        secant = axes.get_secant_slope_group(
            x_a, graph, dx=x_b - x_a, secant_line_color=YELLOW, secant_line_length=6
        )
        self.play(Create(secant))

        # Formula
        formula_avg = MathTex(
            r"\text{Average Rate} = \frac{f(x_2) - f(x_1)}{x_2 - x_1}", font_size=40
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(formula_avg))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ============================================================
        # SCENE 2: The Difference Quotient
        # ============================================================
        title2 = Text("The Difference Quotient", font_size=48).to_edge(UP)
        self.play(Write(title2))

        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 5, 1],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)

        graph = axes.plot(lambda x: x**2, color=BLUE)
        graph_label = axes.get_graph_label(graph, "f(x) = x^2", x_val=2.5)

        self.play(Create(axes), Create(graph), Write(graph_label))

        # Point P (fixed)
        x_p = 1
        point_p = Dot(axes.c2p(x_p, x_p**2), color=RED)
        label_p = MathTex("P(x, f(x))", font_size=32).next_to(point_p, DOWN + LEFT)
        self.play(FadeIn(point_p), Write(label_p))

        # Variable h
        h_tracker = ValueTracker(1.5)
        get_h = h_tracker.get_value

        # Point Q (movable)
        point_q = always_redraw(lambda: Dot(axes.c2p(x_p + get_h(), (x_p + get_h())**2), color=GREEN))
        label_q = always_redraw(lambda: MathTex("Q(x+h, f(x+h))", font_size=28).next_to(point_q, UP + RIGHT))

        # Secant line dynamic
        secant_line = always_redraw(lambda: axes.get_secant_slope_group(
            x_p, graph, dx=get_h(), secant_line_color=YELLOW, secant_line_length=5
        ))

        self.play(FadeIn(point_q), Write(label_q), Create(secant_line))

        # Difference Quotient Formula
        dq_formula = MathTex(
            r"\frac{f(x+h) - f(x)}{h}", font_size=48
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(dq_formula))

        # Animate h -> 0
        self.play(h_tracker.animate.set_value(0.1), run_time=3, rate_func=smooth)
        self.wait(1)
        self.play(h_tracker.animate.set_value(1.5), run_time=2, rate_func=smooth)
        self.wait(1)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ============================================================
        # SCENE 3: The Limit Definition
        # ============================================================
        title3 = Text("The Limit Definition of Derivative", font_size=44).to_edge(UP)
        self.play(Write(title3))

        limit_def = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}", font_size=60
        ).move_to(ORIGIN)
        self.play(Write(limit_def))
        self.wait(1)

        # Highlight parts
        box1 = SurroundingRectangle(limit_def[0][0:3], color=YELLOW) # f'(x)
        box2 = SurroundingRectangle(limit_def[0][4:], color=BLUE)    # limit expression
        self.play(Create(box1))
        self.play(Transform(box1, box2))
        self.wait(1)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ============================================================
        # SCENE 4: Algebraic Computation Example (f(x) = x^2)
        # ============================================================
        title4 = Text("Computing the Derivative: f(x) = x^2", font_size=44).to_edge(UP)
        self.play(Write(title4))

        steps = VGroup(
            MathTex(r"f'(x) = \lim_{h \to 0} \frac{(x+h)^2 - x^2}{h}", font_size=40),
            MathTex(r"= \lim_{h \to 0} \frac{x^2 + 2xh + h^2 - x^2}{h}", font_size=40),
            MathTex(r"= \lim_{h \to 0} \frac{2xh + h^2}{h}", font_size=40),
            MathTex(r"= \lim_{h \to 0} (2x + h)", font_size=40),
            MathTex(r"= 2x", font_size=40),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        for step in steps:
            self.play(Write(step))
            self.wait(0.5)

        result_box = SurroundingRectangle(steps[-1], color=GREEN)
        self.play(Create(result_box))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ============================================================
        # SCENE 5: Geometric Interpretation - Tangent Line
        # ============================================================
        title5 = Text("Geometric Meaning: The Tangent Line", font_size=44).to_edge(UP)
        self.play(Write(title5))

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 1],
            x_length=8,
            y_length=6,
            axis_config={"include_numbers": True},
        )

        graph = axes.plot(lambda x: x**2, color=BLUE)
        graph_label = axes.get_graph_label(graph, "f(x)=x^2", x_val=2.5)

        self.play(Create(axes), Create(graph), Write(graph_label))

        # Tangent line at x=1 (slope 2)
        tangent = axes.plot(lambda x: 2*(x-1) + 1, x_range=[-1, 3], color=RED)
        tangent_label = MathTex("y = 2x - 1", font_size=32, color=RED).next_to(tangent.get_end(), UP)

        point_tan = Dot(axes.c2p(1, 1), color=RED)
        label_tan = MathTex("(1, 1)", font_size=28).next_to(point_tan, DOWN)

        self.play(FadeIn(point_tan), Write(label_tan))
        self.play(Create(tangent), Write(tangent_label))

        # Show slope triangle
        slope_tri = axes.get_secant_slope_group(1, graph, dx=0.001, secant_line_color=RED, secant_line_length=4)
        self.play(Create(slope_tri))

        deriv_text = MathTex("f'(1) = 2", font_size=40).to_edge(DOWN)
        self.play(Write(deriv_text))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ============================================================
        # SCENE 6: Derivative as a Function
        # ============================================================
        title6 = Text("The Derivative Function", font_size=44).to_edge(UP)
        self.play(Write(title6))

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True},
        )

        f_graph = axes.plot(lambda x: x**2, color=BLUE, x_range=[-3, 3])
        f_label = axes.get_graph_label(f_graph, "f(x)=x^2", x_val=-2.5, direction=UP)

        df_graph = axes.plot(lambda x: 2*x, color=RED, x_range=[-3, 3])
        df_label = axes.get_graph_label(df_graph, "f'(x)=2x", x_val=2.5, direction=DOWN)

        self.play(Create(axes), Create(f_graph), Write(f_label))
        self.wait(1)
        self.play(Create(df_graph), Write(df_label))

        # Moving point showing correspondence
        x_tracker = ValueTracker(-2)
        dot_f = always_redraw(lambda: Dot(axes.c2p(x_tracker.get_value(), x_tracker.get_value()**2), color=BLUE))
        dot_df = always_redraw(lambda: Dot(axes.c2p(x_tracker.get_value(), 2*x_tracker.get_value()), color=RED))
        
        v_line = always_redraw(lambda: DashedLine(
            axes.c2p(x_tracker.get_value(), x_tracker.get_value()**2),
            axes.c2p(x_tracker.get_value(), 2*x_tracker.get_value()),
            color=YELLOW
        ))

        self.play(FadeIn(dot_f), FadeIn(dot_df), Create(v_line))
        self.play(x_tracker.animate.set_value(2), run_time=4, rate_func=linear)
        self.wait(1)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ============================================================
        # SCENE 7: Summary
        # ============================================================
        title7 = Text("Summary: The Derivative", font_size=48).to_edge(UP)
        self.play(Write(title7))

        summary_points = VGroup(
            Text("1. Instantaneous Rate of Change", font_size=36),
            Text("2. Slope of the Tangent Line", font_size=36),
            Text("3. Limit of the Difference Quotient", font_size=36),
            MathTex(r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}", font_size=48),
        ).arrange(DOWN, buff=0.5).move_to(ORIGIN)

        for point in summary_points:
            self.play(FadeIn(point, shift=UP))
            self.wait(0.5)

        self.wait(3)
