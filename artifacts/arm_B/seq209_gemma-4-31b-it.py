from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # -------------------------------------------------------------------------
        # STEP 1: Introduction to the function
        # -------------------------------------------------------------------------
        title = Text("The Derivative: Instantaneous Rate of Change", font_size=40).to_edge(UP)
        axes = Axes(
            x_range=[-1, 5], y_range=[-1, 10], 
            axis_config={"include_tip": True}
        ).scale(0.8).shift(DOWN * 0.5)
        
        func = lambda x: 0.5 * x**2
        graph = axes.plot(func, color=BLUE)
        graph_label = axes.get_graph_label(graph, label="f(x) = \\frac{1}{2}x^2")

        self.play(Write(title))
        self.play(Create(axes), Create(graph), Write(graph_label))
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(graph_label), FadeOut(graph), FadeOut(axes))
        self.clear()

        # -------------------------------------------------------------------------
        # STEP 2: Average Rate of Change (The Secant Line)
        # -------------------------------------------------------------------------
        title2 = Text("Step 1: Average Rate of Change", font_size=36).to_edge(UP)
        axes2 = Axes(x_range=[-1, 5], y_range=[-1, 10], axis_config={"include_tip": True}).scale(0.8).shift(DOWN * 0.5)
        graph2 = axes2.plot(func, color=BLUE)
        
        x1 = 1
        x2 = 3
        p1 = axes2.coords_to_point(x1, func(x1))
        p2 = axes2.coords_to_point(x2, func(x2))
        
        dot1 = Dot(p1, color=YELLOW)
        dot2 = Dot(p2, color=YELLOW)
        
        secant = Line(p1, p2, color=RED)
        secant_label = MathTex("m_{sec} = \\frac{f(x+h) - f(x)}{h}", color=RED).to_edge(RIGHT).shift(UP * 2)

        self.play(Write(title2))
        self.play(Create(axes2), Create(graph2))
        self.play(FadeIn(dot1), FadeIn(dot2))
        self.play(Create(secant))
        self.play(Write(secant_label))
        self.wait(2)

        self.play(FadeOut(title2), FadeOut(secant_label), FadeOut(secant), FadeOut(dot1), FadeOut(dot2), FadeOut(graph2), FadeOut(axes2))
        self.clear()

        # -------------------------------------------------------------------------
        # STEP 3: The concept of 'h' (The gap)
        # -------------------------------------------------------------------------
        title3 = Text("Step 2: Shrinking the Gap", font_size=36).to_edge(UP)
        axes3 = Axes(x_range=[-1, 5], y_range=[-1, 10], axis_config={"include_tip": True}).scale(0.8).shift(DOWN * 0.5)
        graph3 = axes3.plot(func, color=BLUE)
        
        x_val = 1
        p_fixed = axes3.coords_to_point(x_val, func(x_val))
        dot_fixed = Dot(p_fixed, color=YELLOW)
        
        self.play(Write(title3))
        self.play(Create(axes3), Create(graph3), FadeIn(dot_fixed))
        
        h_tracker = ValueTracker(2.0)
        
        # Dynamic secant line based on tracker
        secant_line = always_redraw(lambda: 
            Line(
                p_fixed, 
                axes3.coords_to_point(x_val + h_tracker.get_value(), func(x_val + h_tracker.get_value())), 
                color=RED
            )
        )
        
        # Dynamic text based on tracker
        h_text = always_redraw(lambda: 
            MathTex(f"h = {h_tracker.get_value():.2f}", color=RED)
            .to_edge(RIGHT).shift(UP * 2)
        )
        
        self.add(secant_line, h_text)
        
        # Animation sequence of h approaching 0
        self.play(h_tracker.animate.set_value(0.1), run_time=4, rate_func=linear)

        self.wait(1)
        self.play(FadeOut(title3), FadeOut(h_text), FadeOut(secant_line), FadeOut(dot_fixed), FadeOut(graph3), FadeOut(axes3))
        self.clear()

        # -------------------------------------------------------------------------
        # STEP 4: Defining the Limit (The Formalism)
        # -------------------------------------------------------------------------
        title4 = Text("Step 3: The Limit Definition", font_size=36).to_edge(UP)
        
        # Using a single MathTex object for stability and correct spacing
        full_formula = MathTex(
            "f'(x) = ", 
            "\\lim_{h \\to 0}", 
            "\\left( \\frac{f(x+h) - f(x)}{h} \\right)", 
            color=WHITE
        ).shift(UP * 1)
        full_formula[1].set_color(YELLOW)
        full_formula[2].set_color(RED)

        desc = Text("As the distance between points (h) vanishes,\nthe secant line becomes a tangent line.", 
                    font_size=24, color=GRAY).next_to(full_formula, DOWN, buff=1)

        self.play(Write(title4))
        self.play(Write(full_formula))
        self.play(Write(desc))
        self.wait(3)
        
        self.play(FadeOut(title4), FadeOut(full_formula), FadeOut(desc))
        self.clear()

        # -------------------------------------------------------------------------
        # STEP 5: The Tangent Line (The Derivative Result)
        # -------------------------------------------------------------------------
        title5 = Text("Final Result: The Tangent Line", font_size=36).to_edge(UP)
        axes5 = Axes(x_range=[-1, 5], y_range=[-1, 10], axis_config={"include_tip": True}).scale(0.8).shift(DOWN * 0.5)
        graph5 = axes5.plot(func, color=BLUE)
        
        x_target = 2
        p_target = axes5.coords_to_point(x_target, func(x_target))
        dot_target = Dot(p_target, color=YELLOW)
        
        # To avoid plot errors, we use the specific tangent line helper 
        # or define points for a Line. The derivative of 0.5x^2 at x=2 is 2.
        # Point 1: (2, 2), Point 2: (3, 4) -> Slope 2
        p_start = axes5.coords_to_point(1, 0) # y = 2(1) - 2 = 0
        p_end = axes5.coords_to_point(3, 4)   # y = 2(3) - 2 = 4
        tangent = Line(p_start, p_end, color=RED)
        
        slope_text = MathTex("f'(2) = 2", color=RED).to_edge(RIGHT).shift(UP * 2)
        meaning_text = Text("The slope of the tangent line is the\ninstantaneous rate of change.", 
                            font_size=24).to_edge(LEFT).shift(UP * 2)

        self.play(Write(title5))
        self.play(Create(axes5), Create(graph5))
        self.play(FadeIn(dot_target))
        self.play(Create(tangent))
        self.play(Write(slope_text), Write(meaning_text))
        self.wait(3)
        
        # Final wrap up: transform to a conclusion
        self.play(
            FadeOut(title5), FadeOut(axes5), FadeOut(graph5), 
            FadeOut(dot_target), FadeOut(tangent), FadeOut(slope_text), FadeOut(meaning_text)
        )
        
        final_text = Text("Derivative = Instantaneous Rate of Change", color=BLUE, font_size=32)
        self.play(Write(final_text))
        self.play(final_text.animate.scale(1.5).set_color(YELLOW))
        self.wait(2)
