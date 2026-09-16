from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # --- SCENE 1: Introduction to the Concept ---
        title = Text("What is a Derivative?", font_size=48).to_edge(UP)
        desc = Text("The instantaneous rate of change of a function", font_size=32).next_to(title, DOWN)
        desc2 = Text("with respect to its input.", font_size=32).next_to(desc, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(desc), FadeIn(desc2))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(desc), FadeOut(desc2))
        self.clear()

        # --- SCENE 2: Visualizing a Function ---
        axes = Axes(x_range=[-1, 5], y_range=[-1, 10], axis_config={"include_tip": True})
        func = lambda x: 0.5 * x**2
        graph = axes.plot(func, color=BLUE)
        graph_label = axes.get_graph_label(graph, label="f(x) = \\frac{1}{2}x^2")
        
        self.play(Create(axes), Create(graph))
        self.play(Write(graph_label))
        self.wait(1)
        
        # Define point P
        dot_p = Dot(axes.c2p(1, func(1)), color=YELLOW)
        label_p = MathTex("P(x, f(x))").next_to(dot_p, UL)
        
        self.play(FadeIn(dot_p), Write(label_p))
        self.wait(2)
        self.play(FadeOut(graph_label), FadeOut(label_p), FadeOut(dot_p), FadeOut(graph), FadeOut(axes))
        self.clear()

        # --- SCENE 3: Average Rate of Change (Secant Line) ---
        axes = Axes(x_range=[-1, 5], y_range=[-1, 10], axis_config={"include_tip": True})
        graph = axes.plot(func, color=BLUE)
        
        x1, x2 = 1, 3
        p1 = axes.c2p(x1, func(x1))
        p2 = axes.c2p(x2, func(x2))
        dot1 = Dot(p1, color=YELLOW)
        dot2 = Dot(p2, color=YELLOW)
        
        secant = Line(p1, p2, color=RED)
        
        slope_text = MathTex("Avg Rate = \\frac{f(x+h) - f(x)}{h}", color=RED).to_edge(UP)
        
        self.play(Create(axes), Create(graph))
        self.play(FadeIn(dot1), FadeIn(dot2))
        self.play(Create(secant), Write(slope_text))
        self.wait(2)
        
        self.play(FadeOut(secant), FadeOut(dot1), FadeOut(dot2), FadeOut(slope_text), FadeOut(graph), FadeOut(axes))
        self.clear()

        # --- SCENE 4: The Limit Process (h approaching 0) ---
        axes = Axes(x_range=[-1, 5], y_range=[-1, 10], axis_config={"include_tip": True})
        graph = axes.plot(func, color=BLUE)
        self.add(axes, graph)
        
        x_val = 1
        # Dynamic points for animation
        h_tracker = ValueTracker(2)
        
        def get_secant():
            h = h_tracker.get_value()
            p1 = axes.c2p(x_val, func(x_val))
            p2 = axes.c2p(x_val + h, func(x_val + h))
            return Line(p1, p2, color=RED)

        def get_dots():
            h = h_tracker.get_value()
            return VGroup(
                Dot(axes.c2p(x_val, func(x_val)), color=YELLOW),
                Dot(axes.c2p(x_val + h, func(x_val + h)), color=YELLOW)
            )

        secant = always_redraw(get_secant)
        dots = always_redraw(get_dots)
        
        h_label = MathTex("h = ").shift(UP*3 + LEFT*2)
        h_val = DecimalNumber(2, num_decimal_places=2).next_to(h_label, RIGHT)
        h_val.add_updater(lambda d: d.set_value(h_tracker.get_value()))
        
        self.play(Write(h_label), Write(h_val))
        self.play(Create(dots), Create(secant))
        self.wait(1)
        
        # Animate h moving toward 0
        self.play(h_tracker.animate.set_value(0.01), run_time=4, rate_func=linear)
        self.wait(1)
        
        self.play(FadeOut(secant), FadeOut(dots), FadeOut(h_label), FadeOut(h_val), FadeOut(graph), FadeOut(axes))
        self.clear()

        # --- SCENE 5: The Tangent Line (Instantaneous Rate) ---
        axes = Axes(x_range=[-1, 5], y_range=[-1, 10], axis_config={"include_tip": True})
        graph = axes.plot(func, color=BLUE)
        
        # Tangent at x=1: f'(x) = x, so f'(1) = 1. Eq: y - 0.5 = 1(x - 1) => y = x - 0.5
        tangent_line = axes.plot(lambda x: x - 0.5, x_range=[0, 2], color=YELLOW)
        tangent_point = Dot(axes.c2p(1, func(1)), color=YELLOW)
        
        label_tangent = Text("Tangent Line", color=YELLOW, font_size=24).next_to(tangent_line, RIGHT)
        
        self.play(Create(axes), Create(graph))
        self.play(Create(tangent_point))
        self.play(Create(tangent_line), Write(label_tangent))
        
        desc_instant = Text("Instantaneous rate of change", font_size=32).to_edge(UP)
        self.play(Write(desc_instant))
        self.wait(2)
        
        self.play(FadeOut(tangent_line), FadeOut(tangent_point), FadeOut(label_tangent), FadeOut(desc_instant), FadeOut(graph), FadeOut(axes))
        self.clear()

        # --- SCENE 6: The Formal Definition ---
        formula = MathTex(
            "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}", 
            font_size=60
        )
        
        parts = VGroup(
            MathTex("f'(x)", font_size=60),
            MathTex("=", font_size=60),
            MathTex("\\lim_{h \\to 0}", font_size=60),
            MathTex("\\frac{f(x+h) - f(x)}{h}", font_size=60)
        ).arrange(RIGHT)
        
        self.play(Write(parts[0]))
        self.play(Write(parts[1]))
        self.play(Write(parts[2]))
        self.play(Write(parts[3]))
        self.wait(2)
        
        # Highlight components
        box = SurroundingRectangle(parts[3], color=YELLOW)
        box_text = Text("Difference Quotient", font_size=24, color=YELLOW).next_to(box, DOWN)
        
        self.play(Create(box), Write(box_text))
        self.wait(2)
        
        self.play(FadeOut(box), FadeOut(box_text))
        self.play(parts.animate.scale(1.2).set_color(BLUE))
        self.wait(2)
        
        # Final Conclusion
        conclusion = Text("The derivative is the limit of the average rate of change\nas the interval h shrinks to zero.", 
                          font_size=30, t2c={"limit": BLUE}).to_edge(DOWN)
        
        self.play(Write(conclusion))
        self.wait(3)
