from manim import *

class SceneGen(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # SCENE 1: The Concept of Slope (Rise over Run)
        # ---------------------------------------------------------
        self.next_section("The Concept of Slope")

        title_slope = Text("1. Understanding Slope").to_edge(UP)
        self.play(Write(title_slope))

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_numbers": True},
        ).scale(0.7).shift(LEFT * 2)
        
        # Draw a simple linear function
        graph_lin = axes.plot(lambda x: 0.5 * x + 1, x_range=[0, 5], color=BLUE)
        label_lin = MathTex("f(x)").next_to(graph_lin, UR, buff=0.1)

        self.play(Create(axes), run_time=1.5)
        self.play(Create(graph_lin), Write(label_lin), run_time=1.5)
        self.wait(1)

        # Pick two points on the line
        p1 = axes.c2p(1, 1.5)
        p2 = axes.c2p(4, 3)
        
        dot_p1 = Dot(p1, color=YELLOW)
        dot_p2 = Dot(p2, color=YELLOW)
        
        # Vertical line (Rise)
        v_line = Line(
            axes.c2p(4, 1.5), axes.c2p(4, 3), color=RED
        )
        v_label = MathTex(r"\Delta y", color=RED).next_to(v_line, RIGHT)
        
        # Horizontal line (Run)
        h_line = Line(
            axes.c2p(1, 1.5), axes.c2p(4, 1.5), color=GREEN
        )
        h_label = MathTex(r"\Delta x", color=GREEN).next_to(h_line, DOWN)

        self.play(FadeIn(dot_p1), FadeIn(dot_p2))
        self.play(Create(h_line), Write(h_label))
        self.play(Create(v_line), Write(v_label))
        self.wait(1)

        slope_val = MathTex(
            r"\text{Slope } m = \frac{\text{Rise}}{\text{Run}} = \frac{\Delta y}{\Delta x} = \frac{2}{3}"
        ).to_edge(DOWN)
        
        self.play(Write(slope_val))
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title_slope), FadeOut(axes), FadeOut(graph_lin), FadeOut(label_lin),
            FadeOut(dot_p1), FadeOut(dot_p2), FadeOut(v_line), FadeOut(h_line),
            FadeOut(v_label), FadeOut(h_label), FadeOut(slope_val)
        )
        self.clear()
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 2: Average Rate of Change (Secant Line)
        # ---------------------------------------------------------
        self.next_section("Average Rate of Change")

        title_avg = Text("2. Average Rate of Change").to_edge(UP)
        self.play(Write(title_avg))

        # Re-use axes setup
        axes = Axes(x_range=[-1, 5, 1], y_range=[-1, 5, 1], x_length=6, y_length=6).scale(0.7).shift(LEFT*2)
        graph_sq = axes.plot(lambda x: 0.5 * x**2, x_range=[-1, 3.5], color=BLUE)
        
        self.play(Create(axes), Create(graph_sq), run_time=1.5)

        # Define a secant line crossing two points
        x1_val, x2_val = 1.0, 3.0
        y1_val = 0.5 * x1_val**2
        y2_val = 0.5 * x2_val**2

        secant = axes.get_secant_slope_group(
            x=x1_val,
            graph=graph_sq,
            dx=x2_val - x1_val,
            dx_label=Tex(r"$\Delta x$"),
            dy_label=Tex(r"$\Delta y$"),
            dx_line_color=YELLOW,
            dy_line_color=YELLOW,
            secant_line_color=GREEN,
        )
        
        slope_eq = MathTex(
            r"\text{Average Slope} = \frac{f(x_2) - f(x_1)}{x_2 - x_1}"
        ).to_edge(DOWN)

        self.play(Create(secant))
        self.play(Write(slope_eq))
        self.wait(2)
        
        # Concept: The line connects two points and measures the overall behavior.
        concept_text = Text("This measures change over a finite interval.", font_size=24).next_to(slope_eq, UP)
        self.play(FadeIn(concept_text))
        self.wait(2)

        self.play(FadeOut(title_avg), FadeOut(axes), FadeOut(graph_sq), FadeOut(secant), FadeOut(slope_eq), FadeOut(concept_text))
        self.clear()
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 3: Shrinking the Interval ($\Delta x \to 0$)
        # ---------------------------------------------------------
        self.next_section("Shrinking Interval")

        title_limit = Text("3. Shrinking the Interval").to_edge(UP)
        self.play(Write(title_limit))

        axes = Axes(x_range=[-1, 5, 1], y_range=[-1, 5, 1], x_length=6, y_length=6).scale(0.7).shift(LEFT*2)
        graph_sq = axes.plot(lambda x: 0.5 * x**2, x_range=[-1, 3.5], color=BLUE)
        self.play(Create(axes), Create(graph_sq), run_time=1)

        x1_val = 1.0
        x2_val = 3.0
        y1_val = 0.5 * x1_val**2

        dot_fix = Dot(axes.c2p(x1_val, y1_val), color=YELLOW)
        dot_move = Dot(axes.c2p(x2_val, 0.5*x2_val**2), color=YELLOW)
        secant_line = axes.get_secant_slope_group(
            x=x1_val, graph=graph_sq, dx=x2_val - x1_val,
            secant_line_color=GREEN, dx_line_color=YELLOW, dy_line_color=YELLOW
        )
        
        self.play(FadeIn(dot_fix), FadeIn(dot_move), Create(secant_line))
        self.wait(1)

        # Explanation text
        explanation = Text("As we move the second point closer...", font_size=24).to_edge(DOWN)
        self.play(Write(explanation))

        # Animate shrinking dx
        # We update the moving dot and the secant line group
        # Note: Manim's secant group update is tricky, we can recreate or use ValueTracker.
        # For simplicity in this script, we'll use ValueTracker.

        # Remove static objects to prepare for dynamic ones
        self.play(FadeOut(dot_fix), FadeOut(dot_move), FadeOut(secant_line))

        x_tracker = ValueTracker(3.0)
        
        # Dynamic moving dot
        moving_dot = always_redraw(
            lambda: Dot(
                axes.c2p(x_tracker.get_value(), 0.5 * x_tracker.get_value()**2),
                color=YELLOW
            )
        )
        
        # Dynamic secant line
        dynamic_secant = always_redraw(
            lambda: axes.get_secant_slope_group(
                x=x1_val,
                graph=graph_sq,
                dx=x_tracker.get_value() - x1_val,
                secant_line_color=GREEN,
                dx_line_color=YELLOW_A,
                dy_line_color=YELLOW_A,
                dx_label=None, # Hide labels for cleanliness during animation
                dy_label=None
            )
        )

        self.play(FadeIn(dot_fix), FadeIn(moving_dot), Create(dynamic_secant))

        # Animate the change
        self.play(x_tracker.animate.set_value(1.5), run_time=3)
        self.wait(0.5)
        self.play(x_tracker.animate.set_value(1.1), run_time=3)
        self.wait(0.5)
        self.play(x_tracker.animate.set_value(1.01), run_time=3)
        self.wait(2)

        limit_text = Text("It approaches the tangent line!", font_size=24).next_to(explanation, UP)
        self.play(Write(limit_text))
        self.wait(2)

        self.play(FadeOut(title_limit), FadeOut(axes), FadeOut(graph_sq), FadeOut(dot_fix), FadeOut(moving_dot), FadeOut(dynamic_secant), FadeOut(explanation), FadeOut(limit_text))
        self.clear()
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 4: The Difference Quotient
        # ---------------------------------------------------------
        self.next_section("Difference Quotient")

        title_dq = Text("4. The Difference Quotient").to_edge(UP)
        self.play(Write(title_dq))

        # Show the formula for the derivative
        dq = MathTex(
            r"\text{Slope} = \frac{f(x + h) - f(x)}{h}"
        )
        self.play(Write(dq))
        self.wait(1)

        # Explain terms
        explain_x = MathTex(r"x", color=YELLOW).next_to(dq, DOWN, buff=0.5)
        explain_h = MathTex(r"h \text{ (the small step)}", color=GREEN).next_to(explain_x, DOWN)
        explain_fx = MathTex(r"f(x) \text{ and } f(x+h)", color=BLUE).next_to(explain_h, DOWN)

        self.play(Write(explain_x))
        self.play(Write(explain_h))
        self.play(Write(explain_fx))
        self.wait(2)

        # Transition to the limit definition
        limit_def = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}"
        ).scale(1.2)
        
        self.play(
            FadeOut(explain_x), FadeOut(explain_h), FadeOut(explain_fx),
            TransformMatchingTex(dq, limit_def)
        )
        self.wait(2)

        # Highlight that we are taking the limit as h approaches zero
        box = SurroundingRectangle(limit_def, color=YELLOW)
        self.play(Create(box))
        self.wait(2)

        self.play(FadeOut(title_dq), FadeOut(limit_def), FadeOut(box))
        self.clear()
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 5: Visualizing the Derivative (Tangent Line)
        # ---------------------------------------------------------
        self.next_section("Visualizing Derivative")

        title_tan = Text("5. The Tangent Line").to_edge(UP)
        self.play(Write(title_tan))

        axes = Axes(x_range=[-1, 5, 1], y_range=[-1, 5, 1], x_length=6, y_length=6).scale(0.7).shift(LEFT*2)
        graph = axes.plot(lambda x: 0.5 * x**2, x_range=[-1, 3.5], color=BLUE)
        self.play(Create(axes), Create(graph), run_time=1)

        # Dynamic tangent line at a specific point x
        x_val = 1.5
        y_val = 0.5 * x_val**2
        slope_val = x_val # derivative of 0.5x^2 is x

        tangent_line = axes.plot(
            lambda x: slope_val * (x - x_val) + y_val,
            x_range=[-1, 5],
            color=YELLOW
        )
        
        dot = Dot(axes.c2p(x_val, y_val), color=YELLOW)
        
        # Labels
        label_x = MathTex("x_0").next_to(axes.c2p(x_val, 0), DOWN)
        label_fx = MathTex("f(x_0)").next_to(axes.c2p(0, y_val), LEFT)
        
        self.play(FadeIn(dot))
        self.play(Create(tangent_line), run_time=2)
        self.play(Write(label_x), Write(label_fx))
        self.wait(1)

        # Explain that the slope of THIS line is the derivative
        slope_label = MathTex(
            r"\text{Slope} = f'(x_0)"
        ).to_edge(DOWN)
        self.play(Write(slope_label))
        self.wait(2)

        # Show the derivative function graph
        deriv_graph = axes.plot(lambda x: x, x_range=[-1, 3.5], color=GREEN)
        label_deriv = MathTex("f'(x) = x", color=GREEN).next_to(deriv_graph, UP, buff=0.2)

        self.play(Create(deriv_graph), Write(label_deriv))
        self.wait(2)

        self.play(FadeOut(title_tan), FadeOut(axes), FadeOut(graph), FadeOut(dot), FadeOut(tangent_line), FadeOut(label_x), FadeOut(label_fx), FadeOut(slope_label), FadeOut(deriv_graph), FadeOut(label_deriv))
        self.clear()
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 6: Geometric Interpretation
        # ---------------------------------------------------------
        self.next_section("Geometric Interpretation")

        title_geo = Text("6. Geometric Interpretation").to_edge(UP)
        self.play(Write(title_geo))

        axes = Axes(x_range=[-1, 5, 1], y_range=[-1, 5, 1], x_length=6, y_length=6).scale(0.7).shift(LEFT*2)
        graph = axes.plot(lambda x: 0.5 * x**2, x_range=[-1, 3.5], color=BLUE)
        self.play(Create(axes), Create(graph), run_time=1)

        # Interactive point moving along the curve
        x_val_tracker = ValueTracker(0.5)

        dot = always_redraw(
            lambda: Dot(
                axes.c2p(x_val_tracker.get_value(), 0.5 * x_val_tracker.get_value()**2),
                color=YELLOW
            )
        )
        
        tangent = always_redraw(
            lambda: axes.plot(
                lambda x: x_val_tracker.get_value() * (x - x_val_tracker.get_value()) + 0.5 * x_val_tracker.get_value()**2,
                x_range=[-1, 5],
                color=YELLOW
            )
        )

        # The derivative value
        deriv_val_text = always_redraw(
            lambda: MathTex(
                f"f'({x_val_tracker.get_value():.2f}) = {x_val_tracker.get_value():.2f}",
                color=GREEN
            ).to_edge(DOWN)
        )

        self.play(FadeIn(dot), Create(tangent), Write(deriv_val_text))
        self.wait(1)

        # Move the point
        self.play(x_val_tracker.animate.set_value(3.0), run_time=4)
        self.wait(0.5)
        self.play(x_val_tracker.animate.set_value(1.0), run_time=4)
        self.wait(0.5)
        self.play(x_val_tracker.animate.set_value(2.5), run_time=3)
        self.wait(2)

        # Interpretation text
        interp = Text("The derivative is the slope of the tangent at any point.", font_size=24).next_to(deriv_val_text, UP)
        self.play(FadeIn(interp))
        self.wait(2)

        self.play(FadeOut(title_geo), FadeOut(axes), FadeOut(graph), FadeOut(dot), FadeOut(tangent), FadeOut(deriv_val_text), FadeOut(interp))
        self.clear()
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 7: The Power Rule (A Basic Derivative Rule)
        # ---------------------------------------------------------
        self.next_section("Power Rule")

        title_power = Text("7. The Power Rule").to_edge(UP)
        self.play(Write(title_power))

        # Show a common rule
        rule_text = MathTex(r"\text{If } f(x) = x^n, \text{ then } f'(x) = n x^{n-1}").scale(1.2)
        self.play(Write(rule_text))
        self.wait(2)

        # Example 1: f(x) = x^2
        ex1_title = Text("Example: f(x) = x²").to_edge(LEFT).shift(UP*2)
        ex1_math = MathTex(r"f'(x) = 2x^{2-1} = 2x").next_to(ex1_title, RIGHT)
        self.play(Write(ex1_title), Write(ex1_math))
        self.wait(1)

        # Example 2: f(x) = x^3
        ex2_title = Text("Example: f(x) = x³").to_edge(LEFT).shift(UP*1)
        ex2_math = MathTex(r"f'(x) = 3x^{3-1} = 3x^2").next_to(ex2_title, RIGHT)
        self.play(Write(ex2_title), Write(ex2_math))
        self.wait(1)

        # Example 3: f(x) = x^-1
        ex3_title = Text("Example: f(x) = 1/x").to_edge(LEFT)
        ex3_math = MathTex(r"f'(x) = -1x^{-2} = -\frac{1}{x^2}").next_to(ex3_title, RIGHT)
        self.play(Write(ex3_title), Write(ex3_math))
        self.wait(2)

        self.play(FadeOut(title_power), FadeOut(rule_text), FadeOut(ex1_title), FadeOut(ex1_math), FadeOut(ex2_title), FadeOut(ex2_math), FadeOut(ex3_title), FadeOut(ex3_math))
        self.clear()
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 8: Conclusion
        # ---------------------------------------------------------
        self.next_section("Conclusion")

        # Final summary
        summary_title = Text("Summary: What is a Derivative?").to_edge(UP)
        self.play(Write(summary_title))

        points = VGroup(
            Text("1. It measures the instantaneous rate of change.", font_size=24),
            Text("2. It is the limit of the average slope (secant line).", font_size=24),
            Text("3. Geometrically, it's the slope of the tangent line.", font_size=24),
            Text("4. Formally: f'(x) = lim [f(x+h)-f(x)] / h", font_size=24),
        ).arrange(DOWN, buff=0.5).shift(DOWN*0.5)

        for point in points:
            self.play(Write(point), run_time=1.5)
            self.wait(1)

        # Final equation
        final_eq = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            color=YELLOW
        ).scale(1.2).to_edge(DOWN)
        
        self.play(Write(final_eq))
        self.wait(3)

        self.play(FadeOut(summary_title), FadeOut(points), FadeOut(final_eq))
        self.clear()
        self.wait(1)
