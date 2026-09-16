from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introducing a function and its graph
        title = Text("The Derivative: Instantaneous Rate of Change", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 10, 1],
            x_length=6,
            y_length=5,
            axis_config={"include_tip": True}
        )
        axes.shift(DOWN * 0.5)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        self.play(Create(axes), Write(axes_labels))
        
        func_graph = axes.plot(lambda x: x**2, x_range=[0, 3], color=BLUE)
        func_label = MathTex("f(x) = x^2", color=BLUE)
        func_label.next_to(axes, RIGHT, buff=0.3)
        
        self.play(Create(func_graph), Write(func_label))
        
        # Show a specific point
        x_val = 2
        point = axes.c2p(x_val, x_val**2)
        dot = Dot(point, color=RED)
        dot_label = MathTex("(2, 4)", color=RED)
        dot_label.next_to(dot, UR, buff=0.2)
        
        self.play(FadeIn(dot), Write(dot_label))
        
        #motion description
        question = Text("How fast is f changing at x=2?", font_size=28)
        question.next_to(title, DOWN, buff=0.3)
        self.play(Write(question))
        
        self.wait(2)
        self.clear()
        
        # Scene 2: Average rate of change (secant line)
        title2 = Text("Step 1: Average Rate of Change", font_size=36)
        title2.to_edge(UP)
        self.play(Write(title2))
        
        axes2 = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 10, 1],
            x_length=6,
            y_length=5,
            axis_config={"include_tip": True}
        )
        axes2.shift(DOWN * 0.5)
        axes_labels2 = axes2.get_axis_labels(x_label="x", y_label="f(x)")
        
        self.play(Create(axes2), Write(axes_labels2))
        
        func_graph2 = axes2.plot(lambda x: x**2, x_range=[0, 3], color=BLUE)
        self.play(Create(func_graph2))
        
        # Two points for secant
        x1, x2 = 2, 3
        p1 = axes2.c2p(x1, x1**2)
        p2 = axes2.c2p(x2, x2**2)
        
        dot1 = Dot(p1, color=RED)
        dot2 = Dot(p2, color=GREEN)
        label1 = MathTex("P", color=RED).next_to(dot1, LEFT, buff=0.2)
        label2 = MathTex("Q", color=GREEN).next_to(dot2, RIGHT, buff=0.2)
        
        self.play(FadeIn(dot1), FadeIn(dot2), Write(label1), Write(label2))
        
        # Secant line
        secant = Line(p1, p2, color=YELLOW)
        self.play(Create(secant))
        
        # Rise and run
        run_line = DashedLine(p1, axes2.c2p(x2, x1**2), color=WHITE)
        rise_line = DashedLine(axes2.c2p(x2, x1**2), p2, color=WHITE)
        
        run_brace = Brace(run_line, DOWN, buff=0.1)
        rise_brace = Brace(rise_line, RIGHT, buff=0.1)
        
        run_label = MathTex("\\Delta x", color=WHITE).next_to(run_brace, DOWN, buff=0.1)
        rise_label = MathTex("\\Delta y", color=WHITE).next_to(rise_brace, RIGHT, buff=0.1)
        
        self.play(
            Create(run_line), 
            Create(rise_line),
            Create(run_brace), 
            Create(rise_brace),
            Write(run_label), 
            Write(rise_label)
        )
        
        slope_formula = MathTex(
            "\\text{slope} = \\frac{\\Delta y}{\\Delta x} = \\frac{f(x+h)-f(x)}{h}",
            color=YELLOW
        )
        slope_formula.next_to(axes2, DOWN, buff=0.5)
        self.play(Write(slope_formula))
        
        self.wait(2)
        self.clear()
        
        # Scene 3: The difference quotient
        title3 = Text("Step 2: The Difference Quotient", font_size=36)
        title3.to_edge(UP)
        self.play(Write(title3))
        
        formula = MathTex(
            "\\frac{f(x+h) - f(x)}{h}",
            font_size=60
        )
        formula.move_to(UP * 1.5)
        self.play(Write(formula))
        
        # Labels for each part
        f_xh = MathTex("f(x+h): \\text{ function at } x+h", color=BLUE)
        f_x = MathTex("f(x): \\text{ function at } x", color=RED)
        h = MathTex("h: \\text{ the distance between inputs}", color=GREEN)
        
        f_xh.next_to(formula, DOWN, buff=0.8)
        f_x.next_to(f_xh, DOWN, buff=0.4)
        h.next_to(f_x, DOWN, buff=0.4)
        
        self.play(Write(f_xh))
        self.play(Write(f_x))
        self.play(Write(h))
        
        # Example with numbers
        example_title = Text("Example: f(x) = x² at x = 2, h = 1", font_size=28)
        example_title.to_edge(DOWN, buff=1.5)
        self.play(Write(example_title))
        
        example_calc = MathTex(
            "\\frac{(2+1)^2 - 2^2}{1} = \\frac{9-4}{1} = 5",
            color=YELLOW
        )
        example_calc.next_to(example_title, DOWN, buff=0.3)
        self.play(Write(example_calc))
        
        self.wait(2)
        self.clear()
        
        # Scene 4: Visualizing h getting smaller
        title4 = Text("Step 3: What Happens as h → 0?", font_size=36)
        title4.to_edge(UP)
        self.play(Write(title4))
        
        axes4 = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 10, 1],
            x_length=6,
            y_length=5,
            axis_config={"include_tip": True}
        )
        axes4.shift(DOWN * 0.5)
        self.play(Create(axes4))
        
        func_graph4 = axes4.plot(lambda x: x**2, x_range=[0, 3], color=BLUE)
        self.play(Create(func_graph4))
        
        fixed_point = axes4.c2p(2, 4)
        fixed_dot = Dot(fixed_point, color=RED)
        fixed_label = MathTex("P(2,4)", color=RED).next_to(fixed_dot, LEFT, buff=0.2)
        self.play(FadeIn(fixed_dot), Write(fixed_label))
        
        # Animate secant lines with decreasing h
        h_values = [1.5, 1.0, 0.5, 0.25, 0.1]
        secant_lines = []
        moving_dots = []
        
        prev_secant = None
        prev_moving_dot = None
        prev_label = None
        
        for i, h_val in enumerate(h_values):
            x_moving = 2 + h_val
            moving_point = axes4.c2p(x_moving, x_moving**2)
            
            moving_dot = Dot(moving_point, color=GREEN)
            moving_label = MathTex(f"Q", color=GREEN).next_to(moving_dot, UR, buff=0.1)
            
            secant = Line(fixed_point, moving_point, color=YELLOW)
            
            h_text = MathTex(f"h = {h_val}", color=WHITE)
            h_text.to_edge(RIGHT, buff=0.5)
            h_text.shift(UP)
            
            animations = []
            if prev_secant is not None:
                animations.extend([
                    FadeOut(prev_secant),
                    FadeOut(prev_moving_dot),
                    FadeOut(prev_label)
                ])
            
            animations.extend([
                Create(secant),
                FadeIn(moving_dot),
                Write(moving_label),
                Write(h_text) if i == 0 else Transform(prev_h_text, h_text)
            ])
            
            self.play(*animations, run_time=1.5)
            
            if i == 0:
                prev_h_text = h_text
            
            prev_secant = secant
            prev_moving_dot = moving_dot
            prev_label = moving_label
        
        # Final state: Q approaches P
        arrow = Arrow(
            moving_point,
            fixed_point,
            color=WHITE,
            buff=0.2
        )
        approach_text = Text("Q → P as h → 0", font_size=24, color=WHITE)
        approach_text.next_to(arrow, RIGHT, buff=0.2)
        
        self.play(
            FadeOut(prev_secant),
            FadeOut(prev_moving_dot),
            FadeOut(prev_label),
            Create(arrow),
            Write(approach_text),
            FadeOut(prev_h_text)
        )
        
        self.wait(2)
        self.clear()
        
        # Scene 5: The tangent line emerges
        title5 = Text("Step 4: The Tangent Line", font_size=36)
        title5.to_edge(UP)
        self.play(Write(title5))
        
        axes5 = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 10, 1],
            x_length=6,
            y_length=5,
            axis_config={"include_tip": True}
        )
        axes5.shift(DOWN * 0.5)
        self.play(Create(axes5))
        
        func_graph5 = axes5.plot(lambda x: x**2, x_range=[0, 3], color=BLUE)
        self.play(Create(func_graph5))
        
        # Show tangent line at x=2
        # derivative of x^2 is 2x, so slope at x=2 is 4
        tangent_point = axes5.c2p(2, 4)
        tangent_dot = Dot(tangent_point, color=RED)
        self.play(FadeIn(tangent_dot))
        
        # Draw tangent line with slope 4: y - 4 = 4(x - 2), so y = 4x - 4
        tangent_line = axes5.plot(lambda x: 4*x - 4, x_range=[0.5, 3], color=GREEN)
        tangent_label = Text("Tangent Line", color=GREEN, font_size=24)
        tangent_label.next_to(axes5, RIGHT, buff=0.3)
        tangent_label.shift(UP)
        
        self.play(Create(tangent_line), Write(tangent_label))
        
        # Show that it touches at exactly one point
        touch_text = MathTex("\\text{slope of tangent} = f'(2)", color=YELLOW)
        touch_text.next_to(axes5, DOWN, buff=0.5)
        self.play(Write(touch_text))
        
        # Show the "zooming in" effect - looks linear
        zoom_box = Rectangle(height=2, width=2, color=WHITE)
        zoom_box.move_to(tangent_point)
        
        self.play(Create(zoom_box))
        
        # Transform to show zoomed view concept
        zoom_text = Text("Zooming in: curve looks like its tangent", font_size=22)
        zoom_text.next_to(touch_text, DOWN, buff=0.3)
        self.play(Write(zoom_text))
        
        self.wait(2)
        self.clear()
        
        # Scene 6: The limit definition
        title6 = Text("Step 5: The Derivative as a Limit", font_size=36)
        title6.to_edge(UP)
        self.play(Write(title6))
        
        limit_def = MathTex(
            "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
            font_size=48
        )
        limit_def.move_to(UP * 1)
        self.play(Write(limit_def))
        
        # Break it down
        box1 = SurroundingRectangle(limit_def[0][5:22], color=BLUE, buff=0.15)
        self.play(Create(box1))
        
        dq_text = Text("The difference quotient", font_size=24, color=BLUE)
        dq_text.next_to(box1, DOWN, buff=0.3)
        self.play(Write(dq_text))
        
        self.wait(1)
        
        box2 = SurroundingRectangle(limit_def[0][0:5], color=RED, buff=0.15)
        self.play(Create(box2))
        
        lim_text = Text("The limit as h approaches 0", font_size=24, color=RED)
        lim_text.next_to(limit_def, UP, buff=0.5)
        self.play(Write(lim_text))
        
        self.wait(1)
        
        # Result
        result = MathTex(
            "= \\text{instantaneous rate of change}",
            color=GREEN,
            font_size=36
        )
        result.next_to(limit_def, DOWN, buff=1)
        self.play(Write(result))
        
        # Arrow showing conceptual flow
        concept_arrow = Arrow(
            limit_def.get_bottom(),
            result.get_top(),
            color=YELLOW,
            buff=0.3
        )
        self.play(Create(concept_arrow))
        
        self.wait(2)
        self.clear()
        
        # Scene 7: Computing the derivative of x²
        title7 = Text("Step 6: Example - Find f'(x) for f(x) = x²", font_size=32)
        title7.to_edge(UP)
        self.play(Write(title7))
        
        step1 = MathTex(
            "f'(x) = \\lim_{h \\to 0} \\frac{(x+h)^2 - x^2}{h}",
            font_size=36
        )
        step1.to_edge(LEFT, buff=1)
        step1.shift(UP * 2)
        self.play(Write(step1))
        
        step2 = MathTex(
            "= \\lim_{h \\to 0} \\frac{x^2 + 2xh + h^2 - x^2}{h}",
            font_size=36
        )
        step2.next_to(step1, DOWN, buff=0.5)
        step2.align_to(step1, LEFT)
        self.play(Write(step2))
        
        step3 = MathTex(
            "= \\lim_{h \\to 0} \\frac{2xh + h^2}{h}",
            font_size=36
        )
        step3.next_to(step2, DOWN, buff=0.5)
        step3.align_to(step1, LEFT)
        self.play(Write(step3))
        
        step4 = MathTex(
            "= \\lim_{h \\to 0} (2x + h)",
            font_size=36
        )
        step4.next_to(step3, DOWN, buff=0.5)
        step4.align_to(step1, LEFT)
        self.play(Write(step4))
        
        # Highlight the key step
        key_box = SurroundingRectangle(step3, color=YELLOW, buff=0.2)
        key_text = Text("h ≠ 0, so we can divide!", font_size=22, color=YELLOW)
        key_text.next_to(step3, RIGHT, buff=1)
        self.play(Create(key_box), Write(key_text))
        
        self.wait(1)
        self.play(FadeOut(key_box), FadeOut(key_text))
        
        final = MathTex(
            "= 2x",
            color=GREEN,
            font_size=48
        )
        final.next_to(step4, DOWN, buff=0.5)
        final.align_to(step1, LEFT)
        self.play(Write(final))
        
        check = MathTex("f'(2) = 4 \\checkmark", color=GREEN)
        check.next_to(final, RIGHT, buff=2)
        self.play(Write(check))
        
        self.wait(2)
        self.clear()
        
        # Scene 8: Geometric interpretation summary
        title8 = Text("Step 7: Summary - What f'(x) Tells Us", font_size=32)
        title8.to_edge(UP)
        self.play(Write(title8))
        
        axes8 = Axes(
            x_range=[-1, 5, 1],
            y_range=[-2, 10, 1],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": True}
        )
        axes8.to_edge(LEFT, buff=0.5)
        axes8.shift(DOWN * 0.5)
        self.play(Create(axes8))
        
        # f(x) = x^2 and its derivative f'(x) = 2x
        graph_f = axes8.plot(lambda x: x**2, x_range=[-0.5, 3], color=BLUE)
        graph_f_label = MathTex("f(x)=x^2", color=BLUE)
        graph_f_label.next_to(axes8, UP, buff=0.1)
        graph_f_label.shift(LEFT)
        
        self.play(Create(graph_f), Write(graph_f_label))
        
        # Show tangent at various points with slopes
        x_vals = [0.5, 1, 1.5, 2]
        colors = [GREEN, YELLOW, ORANGE, RED]
        
        for xv, col in zip(x_vals, colors):
            point = axes8.c2p(xv, xv**2)
            slope = 2 * xv  # derivative value
            # tangent line: y - xv^2 = slope*(x - xv), so y = slope*x - slope*xv + xv^2
            tangent = axes8.plot(
                lambda x, s=slope, xv=xv: s*(x - xv) + xv**2,
                x_range=[xv - 0.4, xv + 0.4],
                color=col
            )
            dot = Dot(point, color=col, radius=0.08)
            slope_text = MathTex(f"f'({xv})={slope}", color=col, font_size=20)
            slope_text.next_to(axes8, RIGHT, buff=0.3)
            slope_text.shift(UP * (2 - xv))
            
            self.play(Create(tangent), FadeIn(dot), Write(slope_text), run_time=0.8)
        
        # Key insight box
        insight = VGroup(
            Text("Key Insight:", font_size=24, color=YELLOW),
            Text("f'(x) > 0: function increasing", font_size=22),
            Text("f'(x) < 0: function decreasing", font_size=22),
            Text("f'(x) = 0: critical point", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        insight.next_to(axes8, RIGHT, buff=0.5)
        insight.shift(DOWN * 1.5)
        
        self.play(Write(insight))
        
        self.wait(2)
        self.clear()
        
        # Scene 9: Final unified view
        title9 = Text("The Derivative: A Complete Picture", font_size=36)
        title9.to_edge(UP)
        self.play(Write(title9))
        
        # Three perspectives
        perspectives = VGroup(
            VGroup(
                Text("Algebraic", font_size=28, color=BLUE),
                MathTex("f'(x) = \\lim_{h \\to 0}\\frac{f(x+h)-f(x)}{h}", font_size=28)
            ).arrange(DOWN, buff=0.3),
            VGroup(
                Text("Geometric", font_size=28, color=GREEN),
                Text("Slope of tangent line", font_size=24)
            ).arrange(DOWN, buff=0.3),
            VGroup(
                Text("Physical", font_size=28, color=RED),
                Text("Instantaneous rate of change", font_size=24)
            ).arrange(DOWN, buff=0.3)
        ).arrange(DOWN, buff=0.8)
        
        perspectives.move_to(ORIGIN)
        
        for p in perspectives:
            self.play(Write(p), run_time=1)
        
        self.wait(1)
        
        # Unifying arrow and formula
        unify = MathTex(
            "\\frac{df}{dx} = f'(x) = \\lim_{h \\to 0}\\frac{\\Delta y}{\\Delta x}",
            font_size=40,
            color=YELLOW
        )
        unify.to_edge(DOWN, buff=1)
        
        arrows_to_unify = VGroup(
            Arrow(perspectives[0][0].get_bottom(), unify.get_top(), color=BLUE, buff=0.3),
            Arrow(perspectives[1][0].get_bottom(), unify.get_top(), color=GREEN, buff=0.3),
            Arrow(perspectives[2][0].get_bottom(), unify.get_top(), color=RED, buff=0.3)
        )
        
        self.play(Create(arrows_to_unify))
        self.play(Write(unify))
        
        self.wait(2)
        self.clear()
        
        # Scene 10: Conclusion
        conclusion = Text("The Derivative", font_size=48, color=BLUE)
        self.play(Write(conclusion))
        
        self.wait(0.5)
        
        big_formula = MathTex(
            "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
            font_size=60,
            color=YELLOW
        )
        big_formula.next_to(conclusion, DOWN, buff=0.8)
        self.play(Write(big_formula))
        
        tagline = Text(
            "The instantaneous rate of change",
            font_size=32,
            color=GREEN
        )
        tagline.next_to(big_formula, DOWN, buff=0.8)
        self.play(Write(tagline))
        
        self.wait(1)
        
        # Final fade with emphasis
        surrounding = SurroundingRectangle(big_formula, color=WHITE, buff=0.3)
        self.play(Create(surrounding))
        
        self.wait(2)
