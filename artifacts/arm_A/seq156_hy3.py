from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Function and average rate of change
        axes = Axes(x_range=[-1, 4, 1], y_range=[-1, 10, 1], x_length=6, y_length=6).shift(LEFT * 3)
        graph = axes.plot(lambda x: x ** 2, color=BLUE)
        label = axes.get_graph_label(graph, "f(x)=x^2")
        self.play(Create(axes), Create(graph), Write(label))
        x0 = 1.0
        x1 = 3.0
        p0 = axes.coords_to_point(x0, x0 ** 2)
        p1 = axes.coords_to_point(x1, x1 ** 2)
        dot0 = Dot(p0, color=RED)
        dot1 = Dot(p1, color=RED)
        secant = Line(p0, p1, color=YELLOW)
        self.play(FadeIn(dot0), FadeIn(dot1), Create(secant))
        avg_rate = MathTex(r"\frac{f(x_1)-f(x_0)}{x_1-x_0}", color=YELLOW).to_corner(UR)
        self.play(Write(avg_rate))
        self.wait(1)
        self.clear()

        # Scene 2: Difference quotient with h
        axes2 = Axes(x_range=[-1, 4, 1], y_range=[-1, 10, 1], x_length=6, y_length=6).shift(LEFT * 3)
        graph2 = axes2.plot(lambda x: x ** 2, color=BLUE)
        self.play(Create(axes2), Create(graph2))
        x_val = 1.0
        h_val = 2.0
        p_x = axes2.coords_to_point(x_val, x_val ** 2)
        p_xh = axes2.coords_to_point(x_val + h_val, (x_val + h_val) ** 2)
        dot_x = Dot(p_x, color=RED)
        dot_xh = Dot(p_xh, color=GREEN)
        secant2 = Line(p_x, p_xh, color=YELLOW)
        self.play(FadeIn(dot_x), FadeIn(dot_xh), Create(secant2))
        dq = MathTex(r"\frac{f(x+h)-f(x)}{h}", color=YELLOW).to_corner(UR)
        self.play(Write(dq))
        self.wait(1)
        self.clear()

        # Scene 3: Decrease h to approach tangent
        axes3 = Axes(x_range=[-1, 4, 1], y_range=[-1, 10, 1], x_length=6, y_length=6).shift(LEFT * 3)
        graph3 = axes3.plot(lambda x: x ** 2, color=BLUE)
        self.play(Create(axes3), Create(graph3))
        x_fixed = 1.0
        dot_fixed = Dot(axes3.coords_to_point(x_fixed, x_fixed ** 2), color=RED)
        self.play(FadeIn(dot_fixed))
        dot_mov = Dot(axes3.coords_to_point(x_fixed + 2.0, (x_fixed + 2.0) ** 2), color=GREEN)
        secant_line = Line(axes3.coords_to_point(x_fixed, x_fixed ** 2), dot_mov.get_center(), color=YELLOW)
        self.play(FadeIn(dot_mov), Create(secant_line))
        for h in [1.5, 1.0, 0.5, 0.2, 0.05]:
            p_mov = axes3.coords_to_point(x_fixed + h, (x_fixed + h) ** 2)
            new_sec = Line(axes3.coords_to_point(x_fixed, x_fixed ** 2), p_mov, color=YELLOW)
            self.play(dot_mov.animate.move_to(p_mov), Transform(secant_line, new_sec))
            self.wait(0.5)
        self.clear()

        # Scene 4: Limit as h->0, tangent line
        axes4 = Axes(x_range=[-1, 4, 1], y_range=[-1, 10, 1], x_length=6, y_length=6).shift(LEFT * 3)
        graph4 = axes4.plot(lambda x: x ** 2, color=BLUE)
        self.play(Create(axes4), Create(graph4))
        x_t = 1.0
        p_t = axes4.coords_to_point(x_t, x_t ** 2)
        dot_t = Dot(p_t, color=RED)
        tangent = axes4.plot(lambda x: 2 * x_t * (x - x_t) + x_t ** 2, x_range=[0, 2.5], color=GREEN)
        self.play(FadeIn(dot_t), Create(tangent))
        limit_tex = MathTex(r"\lim_{h \to 0} \frac{f(x+h)-f(x)}{h}", color=GREEN).to_corner(UR)
        self.play(Write(limit_tex))
        self.wait(1)
        self.clear()

        # Scene 5: Derivative notation
        title = Text("Derivative Notation", color=WHITE)
        self.play(Write(title))
        self.wait(0.5)
        fprime = MathTex(r"f'(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}", color=YELLOW)
        dy_dx = MathTex(r"\frac{dy}{dx} = \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x}", color=BLUE)
        group = VGroup(fprime, dy_dx).arrange(DOWN, buff=0.8).shift(UP * 0.5)
        self.play(Write(fprime))
        self.wait(0.5)
        self.play(Write(dy_dx))
        self.wait(1)
        self.clear()

        # Scene 6: Derivative of x^2 is 2x
        axes6 = Axes(x_range=[-1, 4, 1], y_range=[-1, 10, 1], x_length=6, y_length=6).shift(LEFT * 3)
        graph6 = axes6.plot(lambda x: x ** 2, color=BLUE)
        deriv = axes6.plot(lambda x: 2 * x, color=GREEN)
        self.play(Create(axes6), Create(graph6))
        self.wait(0.5)
        self.play(Create(deriv))
        tex6 = MathTex(r"f(x)=x^2 \implies f'(x)=2x", color=YELLOW).to_corner(UR)
        self.play(Write(tex6))
        self.wait(1)
        self.clear()

        # Scene 7: Recap
        axes7 = Axes(x_range=[-1, 4, 1], y_range=[-1, 10, 1], x_length=5, y_length=5).shift(LEFT * 3)
        graph7 = axes7.plot(lambda x: x ** 2, color=BLUE)
        tangent7 = axes7.plot(lambda x: 2 * 1 * (x - 1) + 1, x_range=[0, 2.5], color=GREEN)
        dot7 = Dot(axes7.coords_to_point(1, 1), color=RED)
        self.play(Create(axes7), Create(graph7), Create(tangent7), FadeIn(dot7))
        recap = Text(
            "Derivative = Instantaneous Rate of Change\n= Slope of Tangent Line\n= Limit of Difference Quotient",
            color=WHITE,
        ).to_corner(UR)
        self.play(Write(recap))
        self.wait(2)
        self.clear()