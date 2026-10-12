from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction to function
        title1 = Text("Derivative: Instantaneous Rate of Change", font_size=36)
        title1.to_edge(UP)
        axes1 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"color": BLUE}
        ).to_edge(DOWN).scale(0.8)
        graph1 = axes1.plot(lambda x: x**2, color=GREEN)
        label1 = axes1.get_graph_label(graph1, label="f(x)=x^2", direction=UP)
        point1 = Dot(axes1.c2p(1, 1), color=YELLOW)
        self.play(FadeIn(title1), Create(axes1), Create(graph1), Write(label1))
        self.play(GrowFromCenter(point1))
        self.wait(1)
        self.play(FadeOut(title1), FadeOut(axes1), FadeOut(graph1), FadeOut(label1), FadeOut(point1))

        # Scene 2: Average rate of change with secant
        axes2 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"color": BLUE}
        ).to_edge(DOWN).scale(0.8)
        graph2 = axes2.plot(lambda x: x**2, color=GREEN)
        a_val = -1
        b_val = 2
        point_a = Dot(axes2.c2p(a_val, a_val**2), color=RED)
        point_b = Dot(axes2.c2p(b_val, b_val**2), color=RED)
        secant = Line(axes2.c2p(a_val, a_val**2), axes2.c2p(b_val, b_val**2), color=RED)
        label_sec = MathTex(r"\text{Secant line}").next_to(secant, UP)
        avg_text = Text("Average rate of change between two points", font_size=28).to_edge(UP)
        self.play(Create(axes2), Create(graph2))
        self.play(FadeIn(avg_text))
        self.play(GrowFromCenter(point_a), GrowFromCenter(point_b))
        self.play(Create(secant), Write(label_sec))
        self.wait(1.5)
        self.play(FadeOut(avg_text), FadeOut(axes2), FadeOut(graph2), FadeOut(point_a), FadeOut(point_b), FadeOut(secant), FadeOut(label_sec))

        # Scene 3: Moving point B closer to A
        axes3 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"color": BLUE}
        ).to_edge(DOWN).scale(0.8)
        graph3 = axes3.plot(lambda x: x**2, color=GREEN)
        a_val = 1
        point_a3 = Dot(axes3.c2p(a_val, a_val**2), color=RED)
        point_b3 = Dot(axes3.c2p(2.5, 2.5**2), color=RED)
        secant3 = Line(axes3.c2p(a_val, a_val**2), axes3.c2p(2.5, 2.5**2), color=RED)
        moving_text = Text("Move B closer to A", font_size=28).to_edge(UP)
        self.play(Create(axes3), Create(graph3), GrowFromCenter(point_a3))
        self.play(GrowFromCenter(point_b3), Create(secant3))
        self.play(FadeIn(moving_text))
        for b in [2.2, 1.8, 1.4, 1.2]:
            new_b_dot = Dot(axes3.c2p(b, b**2), color=RED)
            new_sec = Line(axes3.c2p(a_val, a_val**2), axes3.c2p(b, b**2), color=RED)
            self.play(Transform(point_b3, new_b_dot), Transform(secant3, new_sec))
        self.wait(1)
        self.play(FadeOut(moving_text), FadeOut(axes3), FadeOut(graph3), FadeOut(point_a3), FadeOut(point_b3), FadeOut(secant3))

        # Scene 4: Tangent emerges as limit
        axes4 = Axes(
            x_range=[-1.5, 2.5, 0.5],
            y_range=[0, 7, 1],
            axis_config={"color": BLUE}
        ).to_edge(DOWN).scale(0.8)
        graph4 = axes4.plot(lambda x: x**2, color=GREEN)
        a_val = 1
        point_a4 = Dot(axes4.c2p(a_val, a_val**2), color=YELLOW)
        # Manual tangent line through point with slope 2
        line_start = axes4.c2p(0, 0)
        line_end = axes4.c2p(2.5, 5)
        tangent_line2 = Line(line_start, line_end, color=ORANGE)
        label_tan = Text("Tangent line").next_to(tangent_line2, UP)
        limit_text = Text("As B → A, secant → tangent", font_size=28).to_edge(UP)
        self.play(Create(axes4), Create(graph4), GrowFromCenter(point_a4))
        self.play(FadeIn(limit_text))
        self.play(Create(tangent_line2), Write(label_tan))
        self.wait(1.5)
        self.play(FadeOut(limit_text), FadeOut(axes4), FadeOut(graph4), FadeOut(point_a4), FadeOut(tangent_line2), FadeOut(label_tan))

        # Scene 5: Difference quotient formula
        formula1 = MathTex(r"\text{Average rate} = \frac{f(x+h)-f(x)}{h}").scale(1.2)
        formula1.to_edge(UP)
        formula2 = MathTex(r"f'(x)=\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}").scale(1.2)
        formula2.next_to(formula1, DOWN, buff=0.8)
        arrow = Arrow(formula1.get_bottom(), formula2.get_top(), buff=0.1, color=YELLOW)
        desc = Text("Difference quotient → limit", font_size=28).to_edge(DOWN)
        self.play(Write(formula1))
        self.play(GrowArrow(arrow))
        self.play(Write(formula2))
        self.play(FadeIn(desc))
        self.wait(1.5)
        self.play(FadeOut(formula1), FadeOut(formula2), FadeOut(arrow), FadeOut(desc))

        # Scene 6: Instantaneous slope interpretation
        axes6 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"color": BLUE}
        ).to_edge(DOWN).scale(0.8)
        graph6 = axes6.plot(lambda x: x**2, color=GREEN)
        point6 = Dot(axes6.c2p(1.5, 1.5**2), color=YELLOW)
        tangent6 = Line(axes6.c2p(0, -1.5), axes6.c2p(3, 4.5), color=ORANGE)
        slope_text = Text("Slope at a point = instantaneous rate", font_size=28).to_edge(UP)
        fprime_text = MathTex(r"f'(x)=2x").next_to(slope_text, DOWN)
        self.play(Create(axes6), Create(graph6))
        self.play(GrowFromCenter(point6), Create(tangent6))
        self.play(FadeIn(slope_text), Write(fprime_text))
        self.wait(2)
        self.play(FadeOut(axes6), FadeOut(graph6), FadeOut(point6), FadeOut(tangent6), FadeOut(slope_text), FadeOut(fprime_text))

        # Scene 7: Final summary
        summary = Text("Derivative = instantaneous rate of change", font_size=40).scale(1.1)
        definition = MathTex(r"f'(x)=\lim_{x_2\to x_1}\frac{f(x_2)-f(x_1)}{x_2-x_1}").scale(0.9)
        summary.to_edge(UP)
        definition.next_to(summary, DOWN, buff=0.8)
        self.play(FadeIn(summary), Write(definition))
        self.wait(2)
        self.play(FadeOut(summary), FadeOut(definition))
