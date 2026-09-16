from manim import *

class SceneGen(Scene):
    def construct(self):
        # SCENE 1: Introduction to the Problem - Motion and Average Speed
        title = Text("Understanding Instantaneous Rate of Change", font_size=36)
        title.to_edge(UP)
        
        car = Square(side_length=0.8, color=BLUE, fill_opacity=0.7)
        car.move_to(LEFT * 5 + DOWN * 2)
        
        road = Line(LEFT * 6 + DOWN * 2.4, RIGHT * 6 + DOWN * 2.4, color=GRAY)
        
        self.play(Write(title), run_time=2)
        self.play(Create(road), run_time=1)
        self.play(DrawBorderThenFill(car), run_time=1)
        
        position_label = MathTex("s(t) = t^2", font_size=32)
        position_label.next_to(car, UP, buff=0.5)
        self.play(Write(position_label), run_time=1)
        
        # Animate car moving
        self.play(car.animate.shift(RIGHT * 8), position_label.animate.shift(RIGHT * 8), run_time=3)
        
        question = Text("How fast is the car going at exactly t=2?", font_size=28, color=YELLOW)
        question.next_to(title, DOWN, buff=0.5)
        self.play(Write(question), run_time=2)
        
        self.wait(2)
        self.play(
            FadeOut(title), FadeOut(road), FadeOut(car), 
            FadeOut(position_label), FadeOut(question), run_time=1
        )
        
        
        # SCENE 2: Average Speed Over an Interval - The Difference Quotient
        self.clear()
        
        title2 = Text("Average Speed Over an Interval", font_size=36)
        title2.to_edge(UP)
        self.play(Write(title2), run_time=1.5)
        
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 20, 5],
            axis_config={"include_tip": True},
            x_length=8,
            y_length=5,
        )
        axes.shift(DOWN * 0.5)
        axes_labels = axes.get_axis_labels(x_label="t", y_label="s(t)")
        
        self.play(Create(axes), Write(axes_labels), run_time=2)
        
        graph = axes.plot(lambda x: x**2, x_range=[0, 4.5], color=BLUE)
        self.play(Create(graph), run_time=2)
        
        graph_label = MathTex("s(t) = t^2", font_size=28, color=BLUE)
        graph_label.next_to(axes.c2p(3.5, 12.25), UR, buff=0.1)
        self.play(Write(graph_label), run_time=1)
        
        # Mark two points on curve
        t1 = 2
        t2 = 3
        p1 = axes.c2p(t1, t1**2)
        p2 = axes.c2p(t2, t2**2)
        
        dot1 = Dot(p1, color=RED, radius=0.08)
        dot2 = Dot(p2, color=RED, radius=0.08)
        
        label1 = MathTex(f"a = {t1}", font_size=24, color=RED)
        label1.next_to(dot1, DOWN, buff=0.15)
        label2 = MathTex(f"b = {t2}", font_size=24, color=RED)
        label2.next_to(dot2, DOWN, buff=0.15)
        
        self.play(FadeIn(dot1), FadeIn(dot2), Write(label1), Write(label2), run_time=1.5)
        
        # Draw secant line
        secant = Line(p1, p2, color=GREEN)
        self.play(Create(secant), run_time=1.5)
        
        # Show rise and run
        run_line = DashedLine(p1, axes.c2p(t2, t1**2), color=YELLOW)
        rise_line = DashedLine(axes.c2p(t2, t1**2), p2, color=YELLOW)
        
        run_label = MathTex("\Delta t = b-a", font_size=22, color=YELLOW)
        run_label.next_to(run_line, DOWN, buff=0.1)
        rise_label = MathTex("\Delta s", font_size=22, color=YELLOW)
        rise_label.next_to(rise_line, RIGHT, buff=0.15)
        
        self.play(Create(run_line), Create(rise_line), run_time=1)
        self.play(Write(run_label), Write(rise_label), run_time=1)
        
        formula = MathTex(
            "\\text{Average speed} = \\frac{\\Delta s}{\\Delta t} = \\frac{s(b) - s(a)}{b - a}",
            font_size=30, color=GREEN
        )
        formula.to_edge(DOWN, buff=0.3)
        self.play(Write(formula), run_time=2)
        
        self.wait(2)
        self.play(
            FadeOut(title2), FadeOut(axes), FadeOut(axes_labels),
            FadeOut(graph), FadeOut(graph_label), FadeOut(dot1), FadeOut(dot2),
            FadeOut(label1), FadeOut(label2), FadeOut(secant),
            FadeOut(run_line), FadeOut(rise_line), FadeOut(run_label),
            FadeOut(rise_label), FadeOut(formula), run_time=1.5
        )
        
        
        # SCENE 3: Making the Interval Smaller - Approaching Instantaneous
        self.clear()
        
        title3 = Text("Making the Interval Smaller", font_size=36)
        title3.to_edge(UP)
        self.play(Write(title3), run_time=1.5)
        
        axes3 = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 10, 2],
            axis_config={"include_tip": True},
            x_length=8,
            y_length=5,
        )
        axes3.shift(DOWN * 0.5)
        axes_labels3 = axes3.get_axis_labels(x_label="t", y_label="s(t)")
        
        self.play(Create(axes3), Write(axes_labels3), run_time=1.5)
        
        graph3 = axes3.plot(lambda x: x**2, x_range=[0, 3.2], color=BLUE)
        self.play(Create(graph3), run_time=1.5)
        
        fixed_point = axes3.c2p(2, 4)
        fixed_dot = Dot(fixed_point, color=RED, radius=0.1)
        fixed_label = MathTex("a=2", font_size=24, color=RED)
        fixed_label.next_to(fixed_dot, DOWN, buff=0.15)
        self.play(FadeIn(fixed_dot), Write(fixed_label), run_time=1)
        
        # Multiple h values
        h_values = [1.5, 1.0, 0.5, 0.3]
        colors_h = [GREEN, YELLOW, ORANGE, PURPLE]
        
        for h, color in zip(h_values, colors_h):
            moving_point = axes3.c2p(2 + h, (2 + h)**2)
            moving_dot = Dot(moving_point, color=color, radius=0.06)
            moving_label = MathTex(f"h={h}", font_size=20, color=color)
            moving_label.next_to(moving_dot, UP, buff=0.1)
            
            secant_h = Line(fixed_point, moving_point, color=color)
            
            self.play(
                FadeIn(moving_dot), Write(moving_label),
                Create(secant_h), run_time=0.8
            )
            
            # Calculate and show slope
            slope_val = ((2 + h)**2 - 4) / h
            slope_text = MathTex(f"slope = {slope_val:.2f}", font_size=20, color=color)
            slope_text.to_edge(RIGHT)
            slope_text.shift(UP * (1.5 - colors_h.index(color)))
            self.play(Write(slope_text), run_time=0.6)
            self.wait(0.3)
        
        observe = Text("As h gets smaller, slope approaches 4", font_size=26, color=YELLOW)
        observe.to_edge(DOWN, buff=0.3)
        self.play(Write(observe), run_time=1.5)
        
        self.wait(2)
        self.play(
            FadeOut(title3), FadeOut(axes3), FadeOut(axes_labels3),
            FadeOut(graph3), FadeOut(fixed_dot), FadeOut(fixed_label),
            FadeOut(moving_dot), FadeOut(moving_label), FadeOut(secant_h),
            FadeOut(slope_text), FadeOut(observe), run_time=1.5
        )
        
        
        # SCENE 4: The Mathematical Definition - Difference Quotient
        self.clear()
        
        title4 = Text("The Difference Quotient", font_size=36)
        title4.to_edge(UP)
        self.play(Write(title4), run_time=1.5)
        
        # Build up the formula step by step
        step1 = MathTex("s(a+h) = ", "(a+h)^2", font_size=32)
        step1.shift(UP * 2)
        self.play(Write(step1), run_time=1.5)
        
        step1_expanded = MathTex("s(a+h) = ", "a^2 + 2ah + h^2", font_size=32)
        step1_expanded.shift(UP * 2)
        self.play(TransformMatchingTex(step1, step1_expanded), run_time=1.5)
        
        step2 = MathTex("s(a) = a^2", font_size=32)
        step2.next_to(step1_expanded, DOWN, buff=0.5)
        step2.align_to(step1_expanded, LEFT)
        self.play(Write(step2), run_time=1.5)
        
        diff = MathTex("s(a+h) - s(a) = 2ah + h^2", font_size=32)
        diff.next_to(step2, DOWN, buff=0.5)
        diff.align_to(step1_expanded, LEFT)
        self.play(Write(diff), run_time=1.5)
        
        quotient = MathTex(
            "\\frac{s(a+h) - s(a)}{h} = \\frac{2ah + h^2}{h} = 2a + h",
            font_size=32, color=YELLOW
        )
        quotient.next_to(diff, DOWN, buff=0.6)
        quotient.align_to(step1_expanded, LEFT)
        self.play(Write(quotient), run_time=2)
        
        # Highlight this is average rate of change
        bracket = Brace(quotient, DOWN, color=GREEN)
        bracket_label = Text("Average rate of change", font_size=22, color=GREEN)
        bracket_label.next_to(bracket, DOWN, buff=0.15)
        self.play(Create(bracket), Write(bracket_label), run_time=1.5)
        
        self.wait(2)
        self.play(
            FadeOut(title4), FadeOut(step1_expanded), FadeOut(step2),
            FadeOut(diff), FadeOut(quotient), FadeOut(bracket),
            FadeOut(bracket_label), run_time=1.5
        )
        
        
        # SCENE 5: Taking the Limit - The Derivative Appears
        self.clear()
        
        title5 = Text("Taking the Limit as h Approaches 0", font_size=36)
        title5.to_edge(UP)
        self.play(Write(title5), run_time=1.5)
        
        formula_avg = MathTex(
            "\\frac{s(a+h) - s(a)}{h} = 2a + h",
            font_size=38, color=BLUE
        )
        formula_avg.shift(UP * 1.5)
        self.play(Write(formula_avg), run_time=2)
        
        arrow1 = Arrow(UP * 1, DOWN * 0.5, color=YELLOW)
        arrow1.next_to(formula_avg, DOWN, buff=0.3)
        self.play(Create(arrow1), run_time=1)
        
        limit_formula = MathTex(
            "\\lim_{h \\to 0}", "\\frac{s(a+h) - s(a)}{h}",
            "= \\lim_{h \\to 0}", "(2a + h)",
            font_size=38, color=GREEN
        )
        limit_formula.next_to(arrow1, DOWN, buff=0.3)
        self.play(Write(limit_formula), run_time=2.5)
        
        arrow2 = Arrow(DOWN * 1.8, DOWN * 3.2, color=YELLOW)
        self.play(Create(arrow2), run_time=1)
        
        result = MathTex("= 2a", font_size=42, color=RED)
        result.next_to(arrow2, DOWN, buff=0.3)
        self.play(Write(result), run_time=1.5)
        
        # Highlight the final form
        box = SurroundingRectangle(result, color=RED, buff=0.2)
        self.play(Create(box), run_time=1)
        
        derivative_name = Text("THE DERIVATIVE at point a", font_size=26, color=RED)
        derivative_name.to_edge(DOWN, buff=0.3)
        self.play(Write(derivative_name), run_time=1.5)
        
        self.wait(2)
        self.play(
            FadeOut(title5), FadeOut(formula_avg), FadeOut(arrow1),
            FadeOut(limit_formula), FadeOut(arrow2), FadeOut(result),
            FadeOut(box), FadeOut(derivative_name), run_time=1.5
        )
        
        
        # SCENE 6: General Definition of the Derivative
        self.clear()
        
        title6 = Text("General Definition of the Derivative", font_size=36)
        title6.to_edge(UP)
        self.play(Write(title6), run_time=1.5)
        
        # Most fundamental form
        def_general = MathTex(
            "f'(x) = \\lim_{h \\to 0}", "\\frac{f(x+h) - f(x)}{h}",
            font_size=40, color=YELLOW
        )
        def_general.shift(UP * 1)
        self.play(Write(def_general), run_time=2.5)
        
        # Alternative form with a and x
        alt_form = MathTex(
            "f'(a) = \\lim_{x \\to a}", "\\frac{f(x) - f(a)}{x - a}",
            font_size=38, color=GREEN
        )
        alt_form.next_to(def_general, DOWN, buff=1)
        self.play(Write(alt_form), run_time=2.5)
        
        # Label both forms
        label1 = Text("Standard form", font_size=22, color=YELLOW)
        label1.next_to(def_general, RIGHT, buff=0.5)
        self.play(Write(label1), run_time=1)
        
        label2 = Text("Alternative form", font_size=22, color=GREEN)
        label2.next_to(alt_form, RIGHT, buff=0.5)
        self.play(Write(label2), run_time=1)
        
        # Interpretation
        interp = Text("= instantaneous rate of change of f at point x", font_size=24, color=WHITE)
        interp.to_edge(DOWN, buff=0.5)
        self.play(Write(interp), run_time=1.5)
        
        self.wait(2)
        self.play(
            FadeOut(title6), FadeOut(def_general), FadeOut(alt_form),
            FadeOut(label1), FadeOut(label2), FadeOut(interp), run_time=1.5
        )
        
        
        # SCENE 7: Visual Interpretation - Tangent Line
        self.clear()
        
        title7 = Text("Geometric Meaning: The Tangent Line", font_size=36)
        title7.to_edge(UP)
        self.play(Write(title7), run_time=1.5)
        
        axes7 = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 10, 2],
            axis_config={"include_tip": True},
            x_length=9,
            y_length=6,
        )
        axes7.shift(DOWN * 0.3)
        axes7_labels = axes7.get_axis_labels(x_label="x", y_label="f(x)")
        
        self.play(Create(axes7), Write(axes7_labels), run_time=2)
        
        curve7 = axes7.plot(lambda x: x**2, x_range=[-0.5, 3.2], color=BLUE)
        curve7_label = MathTex("f(x) = x^2", font_size=26, color=BLUE)
        curve7_label.next_to(axes7.c2p(2.5, 6.25), RIGHT, buff=0.2)
        
        self.play(Create(curve7), Write(curve7_label), run_time=2)
        
        # Animate secant lines approaching tangent
        a_val = 1.5
        point_a = axes7.c2p(a_val, a_val**2)
        tangent_dot = Dot(point_a, color=RED, radius=0.1)
        tangent_label = MathTex("x = 1.5", font_size=22, color=RED)
        tangent_label.next_to(tangent_dot, DL, buff=0.15)
        self.play(FadeIn(tangent_dot), Write(tangent_label), run_time=1)
        
        h_vals_tangent = [2.0, 1.0, 0.5, 0.2, 0.001]
        for i, h in enumerate(h_vals_tangent):
            if h < 0.01:
                # Final tangent line
                slope = 2 * a_val  # derivative
                tangent_func = lambda x: slope * (x - a_val) + a_val**2
                
                tangent_line = axes7.plot(tangent_func, x_range=[a_val - 1.5, a_val + 1.5], color=RED)
                tangent_line_label = Text("Tangent Line = Derivative!", font_size=22, color=RED)
                tangent_line_label.to_edge(DOWN, buff=0.4)
                
                self.play(
                    Create(tangent_line), 
                    Write(tangent_line_label), run_time=1.5
                )
            else:
                other_point = axes7.c2p(a_val + h, (a_val + h)**2)
                secant_temp = Line(point_a, other_point, color=GREEN, stroke_width=2)
                opacity = max(0.3, 1 - i * 0.15)
                secant_temp.set_opacity(opacity)
                self.play(Create(secant_temp), run_time=0.6)
        
        # Show slope value
        slope_value = MathTex("f'(1.5) = 2(1.5) = 3", font_size=28, color=YELLOW)
        slope_value.shift(RIGHT * 3 + UP * 2)
        self.play(Write(slope_value), run_time=1.5)
        
        self.wait(2)
        self.play(
            FadeOut(title7), FadeOut(axes7), FadeOut(axes7_labels),
            FadeOut(curve7), FadeOut(curve7_label), FadeOut(tangent_dot),
            FadeOut(tangent_label), FadeOut(tangent_line), FadeOut(tangent_line_label),
            FadeOut(slope_value), FadeOut(secant_temp), run_time=1.5
        )
        
        
        # SCENE 8: Power Rule - A Computational Tool
        self.clear()
        
        title8 = Text("The Power Rule: Computing Derivatives Easily", font_size=36)
        title8.to_edge(UP)
        self.play(Write(title8), run_time=1.5)
        
        # Show pattern
        examples = VGroup(
            MathTex("f(x) = x^2 \\quad \\Rightarrow \\quad f'(x) = 2x", font_size=28, color=BLUE),
            MathTex("f(x) = x^3 \\quad \\Rightarrow \\quad f'(x) = 3x^2", font_size=28, color=GREEN),
            MathTex("f(x) = x^4 \\quad \\Rightarrow \\quad f'(x) = 4x^3", font_size=28, color=YELLOW),
        ).arrange(DOWN, buff=0.6)
        examples.shift(UP * 1.5)
        
        for ex in examples:
            self.play(Write(ex), run_time=1.5)
        
        rule_box = Rectangle(color=RED, height=2, width=8)
        rule_box.next_to(examples, DOWN, buff=0.8)
        
        power_rule = MathTex("\\frac{d}{dx}[x^n] = nx^{n-1}", font_size=40, color=RED)
        power_rule.move_to(rule_box)
        
        self.play(Create(rule_box), run_time=1)
        self.play(Write(power_rule), run_time=2)
        
        # Verify with our original function
        verify = Text("Verify: d/dx[x²] = 2x¹ = 2x  ✓", font_size=24, color=GREEN)
        verify.to_edge(DOWN, buff=0.3)
        self.play(Write(verify), run_time=1.5)
        
        self.wait(2)
        self.play(
            FadeOut(title8), FadeOut(examples), FadeOut(rule_box),
            FadeOut(power_rule), FadeOut(verify), run_time=1.5
        )
        
        
        # SCENE 9: Complete Example - From Function to Derivative
        self.clear()
        
        title9 = Text("Complete Example", font_size=36)
        title9.to_edge(UP)
        self.play(Write(title9), run_time=1.5)
        
        # Step by step computation for f(x) = x² at x = 3
        given = MathTex("f(x) = x^2, \\quad \\text{find } f'(3)", font_size=32, color=YELLOW)
        given.shift(UP * 2.5)
        self.play(Write(given), run_time=1.5)
        
        step1 = MathTex("f'(x) = 2x", font_size=30, color=BLUE)
        step1.next_to(given, DOWN, buff=0.8)
        step1.align_to(given, LEFT)
        self.play(Write(step1), run_time=1.5)
        
        step2 = MathTex("f'(3) = 2(3) = 6", font_size=30, color=GREEN)
        step2.next_to(step1, DOWN, buff=0.6)
        step2.align_to(given, LEFT)
        self.play(Write(step2), run_time=1.5)
        
        meaning = Text("At x = 3, the function x² changes at rate of 6 units per unit x", font_size=24, color=WHITE)
        meaning.next_to(step2, DOWN, buff=0.8)
        self.play(Write(meaning), run_time=2)
        
        # Visual confirmation
        confirm = MathTex(
            "\\lim_{h \\to 0} \\frac{(3+h)^2 - 9}{h} = \\lim_{h \\to 0} \\frac{9+6h+h^2-9}{h} = \\lim_{h \\to 0}(6+h) = 6",
            font_size=26, color=ORANGE
        )
        confirm.to_edge(DOWN, buff=0.3)
        self.play(Write(confirm), run_time=2.5)
        
        self.wait(2)
        self.play(
            FadeOut(title9), FadeOut(given), FadeOut(step1),
            FadeOut(step2), FadeOut(meaning), FadeOut(confirm), run_time=1.5
        )
        
        
        # SCENE 10: Summary and Key Takeaways
        self.clear()
        
        title10 = Text("Summary: The Derivative", font_size=40, color=YELLOW)
        title10.to_edge(UP)
        self.play(Write(title10), run_time=1.5)
        
        summary_points = VGroup(
            Text("• Derivative = instantaneous rate of change", font_size=26),
            Text("• Defined as limit of difference quotient", font_size=26),
            Text("• Geometrically: slope of tangent line", font_size=26),
            Text("• Notation: f'(x) or df/dx", font_size=26),
            Text("• Power Rule: d/dx[xⁿ] = nxⁿ⁻¹", font_size=26),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        summary_points.shift(UP * 0.5)
        
        for point in summary_points:
            self.play(Write(point), run_time=1)
        
        final_formula = MathTex(
            "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
            font_size=36, color=RED
        )
        final_formula.to_edge(DOWN, buff=0.5)
        
        box_final = SurroundingRectangle(final_formula, color=RED, buff=0.2)
        
        self.play(Write(final_formula), run_time=2)
        self.play(Create(box_final), run_time=1)
        
        self.wait(3)
        self.play(
            FadeOut(title10), FadeOut(summary_points),
            FadeOut(final_formula), FadeOut(box_final), run_time=2
        )
        
        # Final message
        end_text = Text("Calculus: Understanding Change", font_size=40, color=BLUE)
        self.play(Write(end_text), run_time=2)
        self.wait(2)
        self.play(FadeOut(end_text), run_time=1)
