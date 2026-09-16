from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: A function curve - introducing the concept of change
        title = Text("Understanding Change in Functions", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True, "numbers_to_exclude": []},
        )
        axes.shift(DOWN * 0.5)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        self.play(Create(axes), Write(axes_labels))
        
        graph = axes.plot(lambda x: 0.5 * x**2, x_range=[0, 4], color=BLUE)
        graph_label = MathTex("f(x) = \\frac{1}{2}x^2", color=BLUE).to_corner(UR)
        graph_label.shift(DOWN * 0.5)
        
        self.play(Create(graph), Write(graph_label))
        
        # Show two points and the change between them
        x1, x2 = 1, 3
        p1 = axes.c2p(x1, 0.5 * x1**2)
        p2 = axes.c2p(x2, 0.5 * x2**2)
        
        dot1 = Dot(p1, color=RED)
        dot2 = Dot(p2, color=RED)
        label1 = MathTex("A", color=RED).next_to(dot1, DL, buff=0.1)
        label2 = MathTex("B", color=RED).next_to(dot2, UR, buff=0.1)
        
        self.play(FadeIn(dot1), FadeIn(dot2), Write(label1), Write(label2))
        
        # Draw secant line
        secant_line = Line(p1, p2, color=YELLOW)
        self.play(Create(secant_line))
        
        # Show the change
        brace_x = Brace(Line(axes.c2p(x1, -0.3), axes.c2p(x2, -0.3)), DOWN, color=GREEN)
        brace_y = Brace(Line(axes.c2p(4.3, 0.5*x1**2), axes.c2p(4.3, 0.5*x2**2)), RIGHT, color=GREEN)
        delta_x = MathTex("\\Delta x", color=GREEN).next_to(brace_x, DOWN)
        delta_y = MathTex("\\Delta y", color=GREEN).next_to(brace_y, RIGHT)
        
        self.play(
            GrowFromCenter(brace_x), 
            GrowFromCenter(brace_y),
            Write(delta_x), 
            Write(delta_y)
        )
        
        average_rate = MathTex("\\text{Average rate} = \\frac{\\Delta y}{\\Delta x}", color=YELLOW)
        average_rate.to_corner(DR)
        self.play(Write(average_rate))
        
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Scene 2: The problem with average rate - we want instantaneous
        title2 = Text("The Problem: We Want Instantaneous Rate", font_size=36)
        title2.to_edge(UP)
        self.play(Write(title2))
        
        axes2 = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True},
        )
        axes2.shift(DOWN * 0.5)
        
        self.play(Create(axes2))
        
        graph2 = axes2.plot(lambda x: 0.5 * x**2, x_range=[0, 4], color=BLUE)
        self.play(Create(graph2))
        
        # Fixed point P
        x_p = 2
        p_point = axes2.c2p(x_p, 0.5 * x_p**2)
        dot_p = Dot(p_point, color=RED)
        label_p = MathTex("P", color=RED).next_to(dot_p, DOWN, buff=0.15)
        
        self.play(FadeIn(dot_p), Write(label_p))
        
        # Moving point Q that gets closer to P
        x_q_values = [3.5, 3.0, 2.5, 2.2, 2.1, 2.05]
        colors = [GREEN, YELLOW, ORANGE, PURPLE, PINK, WHITE]
        
        secant_lines = VGroup()
        dots_q = VGroup()
        
        for i, x_q in enumerate(x_q_values):
            q_point = axes2.c2p(x_q, 0.5 * x_q**2)
            dot_q = Dot(q_point, color=colors[i])
            label_q = MathTex(f"Q_{i+1}", color=colors[i]).next_to(dot_q, UR, buff=0.1)
            
            secant = Line(p_point, q_point, color=colors[i])
            
            self.play(
                FadeIn(dot_q), 
                Write(label_q),
                Create(secant),
                run_time=0.8
            )
            
            if i < len(x_q_values) - 1:
                self.play(
                    FadeOut(dot_q),
                    FadeOut(label_q),
                    secant.animate.set_stroke(opacity=0.3),
                    run_time=0.3
                )
                secant_lines.add(secant)
        
        tangent_approx = MathTex("Q \\to P \\text{ : secant } \\to \\text{ tangent?}", color=YELLOW)
        tangent_approx.next_to(title2, DOWN)
        self.play(Write(tangent_approx))
        
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Scene 3: Introducing h as the small change
        title3 = Text("Step 1: Define the Small Change h", font_size=36)
        title3.to_edge(UP)
        self.play(Write(title3))
        
        axes3 = Axes(
            x_range=[-0.5, 4, 1],
            y_range=[-0.5, 4, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True},
        )
        axes3.shift(DOWN * 0.5)
        self.play(Create(axes3))
        
        graph3 = axes3.plot(lambda x: 0.5 * x**2, x_range=[0, 3.5], color=BLUE)
        graph_label3 = MathTex("f(x) = \\frac{1}{2}x^2", color=BLUE).to_corner(UR)
        graph_label3.shift(DOWN * 0.5)
        self.play(Create(graph3), Write(graph_label3))
        
        # Point at x
        x_val = 1.5
        point_x = axes3.c2p(x_val, 0.5 * x_val**2)
        dot_x = Dot(point_x, color=RED)
        label_x = MathTex("x", color=RED).next_to(dot_x, DOWN, buff=0.15)
        
        self.play(FadeIn(dot_x), Write(label_x))
        
        # Show x + h
        h_val = 1.5
        point_xh = axes3.c2p(x_val + h_val, 0.5 * (x_val + h_val)**2)
        
        # Draw h bracket
        h_brace = Brace(
            Line(axes3.c2p(x_val, -0.2), axes3.c2p(x_val + h_val, -0.2)), 
            DOWN, color=GREEN
        )
        h_label = MathTex("h", color=GREEN).next_to(h_brace, DOWN)
        
        self.play(GrowFromCenter(h_brace), Write(h_label))
        
        dot_xh = Dot(point_xh, color=PURPLE)
        label_xh = MathTex("x+h", color=PURPLE).next_to(dot_xh, UR, buff=0.1)
        
        self.play(FadeIn(dot_xh), Write(label_xh))
        
        # Function values
        fx_label = MathTex("f(x)", color=RED).next_to(dot_x, LEFT, buff=0.3)
        fxh_label = MathTex("f(x+h)", color=PURPLE).next_to(dot_xh, RIGHT, buff=0.3)
        
        self.play(Write(fx_label), Write(fxh_label))
        
        # Secant line
        secant3 = Line(point_x, point_xh, color=YELLOW)
        self.play(Create(secant3))
        
        # Show the rise over run
        rise_line = DashedLine(
            axes3.c2p(x_val + h_val, 0.5 * x_val**2),
            point_xh,
            color=GREEN
        )
        run_line = DashedLine(
            point_x,
            axes3.c2p(x_val + h_val, 0.5 * x_val**2),
            color=GREEN
        )
        
        self.play(Create(rise_line), Create(run_line))
        
        slope_formula = MathTex(
            "\\text{slope} = \\frac{f(x+h) - f(x)}{h}",
            color=YELLOW
        )
        slope_formula.to_corner(DR)
        self.play(Write(slope_formula))
        
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Scene 4: The difference quotient with actual function
        title4 = Text("Step 2: Compute the Difference Quotient", font_size=36)
        title4.to_edge(UP)
        self.play(Write(title4))
        
        # Show the algebraic computation
        diff_quotient = MathTex(
            "\\frac{f(x+h) - f(x)}{h} =",
            "\\frac{\\frac{1}{2}(x+h)^2 - \\frac{1}{2}x^2}{h}",
        )
        diff_quotient.scale(0.9)
        diff_quotient.shift(UP * 2)
        
        self.play(Write(diff_quotient))
        
        step1 = MathTex(
            "= \\frac{\\frac{1}{2}(x^2 + 2xh + h^2) - \\frac{1}{2}x^2}{h}",
        )
        step1.scale(0.9)
        step1.next_to(diff_quotient, DOWN, aligned_edge=LEFT)
        
        self.play(Write(step1))
        
        step2 = MathTex(
            "= \\frac{\\frac{1}{2}x^2 + xh + \\frac{1}{2}h^2 - \\frac{1}{2}x^2}{h}",
        )
        step2.scale(0.9)
        step2.next_to(step1, DOWN, aligned_edge=LEFT)
        
        self.play(Write(step2))
        
        step3 = MathTex(
            "= \\frac{xh + \\frac{1}{2}h^2}{h}",
        )
        step3.scale(0.9)
        step3.next_to(step2, DOWN, aligned_edge=LEFT)
        
        self.play(Write(step3))
        
        step4 = MathTex(
            "= x + \\frac{1}{2}h",
        )
        step4.scale(0.9)
        step4.next_to(step3, DOWN, aligned_edge=LEFT)
        step4.set_color(GREEN)
        
        self.play(Write(step4))
        
        box = SurroundingRectangle(step4, color=YELLOW, buff=0.2)
        self.play(Create(box))
        
        explanation = Text(
            "This is the slope of the secant line for any h",
            font_size=24,
            color=YELLOW
        )
        explanation.to_edge(DOWN)
        self.play(Write(explanation))
        
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Scene 5: The limit as h approaches 0
        title5 = Text("Step 3: Take the Limit as h approaches 0", font_size=36)
        title5.to_edge(UP)
        self.play(Write(title5))
        
        limit_def = MathTex(
            "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
        )
        limit_def.shift(UP * 1.5)
        limit_def.set_color(BLUE)
        
        self.play(Write(limit_def))
        
        # Visual of h getting smaller
        axes5 = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 3, 1],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True},
        )
        axes5.shift(DOWN * 0.5 + LEFT * 2)
        
        self.play(Create(axes5))
        
        graph5 = axes5.plot(lambda x: 0.5 * x**2, x_range=[0, 3], color=BLUE)
        self.play(Create(graph5))
        
        x_val5 = 1.5
        point_p5 = axes5.c2p(x_val5, 0.5 * x_val5**2)
        dot_p5 = Dot(point_p5, color=RED)
        label_p5 = MathTex("P", color=RED).next_to(dot_p5, DOWN, buff=0.1)
        
        self.play(FadeIn(dot_p5), Write(label_p5))
        
        # Show h values getting smaller
        h_values = [2.0, 1.0, 0.5, 0.25, 0.1]
        h_texts = VGroup()
        
        for h in h_values:
            q_point = axes5.c2p(x_val5 + h, 0.5 * (x_val5 + h)**2)
            dot_q = Dot(q_point, color=GREEN)
            secant = Line(point_p5, q_point, color=YELLOW)
            
            h_text = MathTex(f"h = {h}", color=GREEN)
            h_text.to_corner(UR)
            h_text.shift(DOWN * 0.5)
            
            self.play(
                FadeIn(dot_q),
                Create(secant),
                Write(h_text),
                run_time=0.6
            )
            
            h_texts.add(h_text)
            
            slope_val = x_val5 + 0.5 * h
            slope_text = MathTex(f"\\text{{slope}} = {slope_val:.3f}", color=YELLOW)
            slope_text.next_to(h_text, DOWN)
            
            self.play(Write(slope_text), run_time=0.4)
            
            if h != h_values[-1]:
                self.play(
                    FadeOut(dot_q),
                    FadeOut(secant),
                    FadeOut(slope_text),
                    FadeOut(h_text),
                    run_time=0.3
                )
        
        # Final tangent line
        tangent = axes5.plot(
            lambda t: 0.5 * x_val5**2 + x_val5 * (t - x_val5),
            x_range=[0, 3],
            color=RED
        )
        
        tangent_label = MathTex("\\text{Tangent: slope } = x = 1.5", color=RED)
        tangent_label.to_corner(UR)
        tangent_label.shift(DOWN * 0.5)
        
        self.play(
            Create(tangent),
            Write(tangent_label)
        )
        
        limit_result = MathTex(
            "f'(x) = \\lim_{h \\to 0} \\left(x + \\frac{1}{2}h\\right) = x",
            color=GREEN
        )
        limit_result.next_to(limit_def, DOWN, buff=0.8)
        
        self.play(Write(limit_result))
        
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Scene 6: The formal derivative definition
        title6 = Text("The Derivative: Formal Definition", font_size=36)
        title6.to_edge(UP)
        self.play(Write(title6))
        
        formal_def = MathTex(
            "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
        )
        formal_def.shift(UP * 2)
        formal_def.set_color(BLUE)
        
        self.play(Write(formal_def))
        
        # Alternative notations
        notations_title = Text("Common Notations:", font_size=28, color=YELLOW)
        notations_title.next_to(formal_def, DOWN, buff=0.8)
        notations_title.shift(LEFT * 3)
        
        self.play(Write(notations_title))
        
        notation1 = MathTex("\\frac{df}{dx}", color=GREEN)
        notation1.next_to(notations_title, DOWN, aligned_edge=LEFT)
        
        notation2 = MathTex("\\frac{d}{dx}f(x)", color=GREEN)
        notation2.next_to(notation1, DOWN, aligned_edge=LEFT)
        
        notation3 = MathTex("y' \\text{ if } y = f(x)", color=GREEN)
        notation3.next_to(notation2, DOWN, aligned_edge=LEFT)
        
        notation4 = MathTex("\\dot{y} \\text{ (Newton's notation)}", color=GREEN)
        notation4.next_to(notation3, DOWN, aligned_edge=LEFT)
        
        self.play(
            Write(notation1),
            Write(notation2),
            Write(notation3),
            Write(notation4)
        )
        
        # Meaning explanation
        meaning = Text(
            "Read as: \"dee f dee x\" or \"derivative of f with respect to x\"",
            font_size=24,
            color=WHITE
        )
        meaning.to_edge(DOWN, buff=0.5)
        
        self.play(Write(meaning))
        
        # Highlight key aspects
        aspects = VGroup()
        aspect1 = Text("• Instantaneous rate of change", font_size=22, color=YELLOW)
        aspect2 = Text("• Slope of the tangent line", font_size=22, color=YELLOW)
        aspect3 = Text("• Limit of slopes of secant lines", font_size=22, color=YELLOW)
        
        aspect1.to_corner(DR)
        aspect1.shift(UP * 1.5 + LEFT * 2)
        aspect2.next_to(aspect1, DOWN, aligned_edge=LEFT)
        aspect3.next_to(aspect2, DOWN, aligned_edge=LEFT)
        
        self.play(
            Write(aspect1),
            Write(aspect2),
            Write(aspect3)
        )
        
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Scene 7: Geometric interpretation
        title7 = Text("Geometric Interpretation", font_size=36)
        title7.to_edge(UP)
        self.play(Write(title7))
        
        axes7 = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 5, 1],
            x_length=9,
            y_length=5,
            axis_config={"include_tip": True},
        )
        axes7.shift(DOWN * 0.3)
        
        self.play(Create(axes7))
        
        # A generic curve
        graph7 = axes7.plot(
            lambda x: 0.15 * (x - 1) * (x - 2) * (x - 5) + 2.5,
            x_range=[0.5, 5.5],
            color=BLUE
        )
        self.play(Create(graph7))
        
        # Multiple points with tangent lines
        x_points = [1.5, 3.0, 4.5]
        colors_tangent = [RED, GREEN, PURPLE]
        
        for i, x_pt in enumerate(x_points):
            y_pt = 0.15 * (x_pt - 1) * (x_pt - 2) * (x_pt - 5) + 2.5
            
            # Approximate derivative numerically
            h_small = 0.001
            y_plus = 0.15 * (x_pt + h_small - 1) * (x_pt + h_small - 2) * (x_pt + h_small - 5) + 2.5
            slope = (y_plus - y_pt) / h_small
            
            point = axes7.c2p(x_pt, y_pt)
            dot = Dot(point, color=colors_tangent[i])
            
            # Tangent line
            tangent_func = lambda t, s=slope, px=x_pt, py=y_pt: py + s * (t - px)
            tangent = axes7.plot(
                tangent_func,
                x_range=[x_pt - 1, x_pt + 1],
                color=colors_tangent[i]
            )
            
            label = MathTex(f"P_{i+1}", color=colors_tangent[i])
            label.next_to(dot, UP if i % 2 == 0 else DOWN, buff=0.15)
            
            slope_label = MathTex(f"f'(x_{i+1})", color=colors_tangent[i])
            slope_label.next_to(tangent, RIGHT if i < 2 else LEFT, buff=0.1)
            slope_label.shift(UP * 0.5)
            
            self.play(
                FadeIn(dot),
                Write(label),
                Create(tangent),
                Write(slope_label)
            )
        
        interpretation = Text(
            "Derivative = slope of tangent at each point",
            font_size=26,
            color=YELLOW
        )
        interpretation.to_edge(DOWN, buff=0.3)
        
        self.play(Write(interpretation))
        
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Scene 8: Summary and final formula
        title8 = Text("Summary: The Derivative", font_size=40)
        title8.to_edge(UP)
        self.play(Write(title8))
        
        # Central formula
        central = MathTex(
            "\\frac{df}{dx} = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
        )
        central.scale(1.3)
        central.set_color(BLUE)
        
        self.play(Write(central))
        
        # Key points
        points_title = Text("Key Ideas:", font_size=28, color=YELLOW)
        points_title.next_to(central, DOWN, buff=0.8)
        points_title.shift(LEFT * 3)
        
        self.play(Write(points_title))
        
        point_lines = VGroup()
        p1 = Text("1. Start with average rate of change", font_size=22)
        p2 = Text("2. Let the interval shrink (h → 0)", font_size=22)
        p3 = Text("3. The limit gives instantaneous rate", font_size=22)
        p4 = Text("4. Geometrically: slope of tangent line", font_size=22)
        
        p1.next_to(points_title, DOWN, aligned_edge=LEFT)
        p2.next_to(p1, DOWN, aligned_edge=LEFT)
        p3.next_to(p2, DOWN, aligned_edge=LEFT)
        p4.next_to(p3, DOWN, aligned_edge=LEFT)
        
        self.play(
            Write(p1),
            Write(p2),
            Write(p3),
            Write(p4)
        )
        
        # Final emphasis
        final_box = SurroundingRectangle(central, color=YELLOW, buff=0.3)
        self.play(Create(final_box))
        
        final_text = Text(
            "The foundation of differential calculus",
            font_size=24,
            color=GREEN
        )
        final_text.to_edge(DOWN, buff=0.5)
        
        self.play(Write(final_text))
        
        self.wait(3)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # End with credits
        thanks = Text("End of Lesson", font_size=48, color=BLUE)
        self.play(Write(thanks))
        self.wait(1)
        self.play(FadeOut(thanks))
