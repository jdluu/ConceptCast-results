#!/usr/bin/env python3
"""
Educational animation: Derivative of a function — instantaneous rate of change.
Manim CE v0.20.1 script. Single Scene subclass with ~8 lesson steps.
"""

from manim import *

class SceneGen(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Scene 1: Function as a process / input-output mapping
        # ------------------------------------------------------------
        title1 = Text("The derivative of a function", font_size=42, color=YELLOW)
        subtitle1 = Text("Instantaneous rate of change", font_size=32, color=BLUE)
        subtitle1.next_to(title1, DOWN)
        self.play(Write(title1), Write(subtitle1))
        self.wait(1)

        # Show a simple function: f(x) = x^2
        axes1 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"include_numbers": True},
        )
        axes1.next_to(subtitle1, DOWN, buff=0.5)
        func1 = axes1.plot(lambda x: x**2, color=GREEN)
        func_label1 = MathTex("f(x)=x^2", color=GREEN).next_to(axes1, DR, buff=0.3)

        self.play(Create(axes1), Create(func1), Write(func_label1))
        self.wait(2)

        # Clear for next scene
        self.clear()

        # ------------------------------------------------------------
        # Scene 2: Average rate of change / secant line
        # ------------------------------------------------------------
        title2 = Text("Average rate of change (secant line)", font_size=36, color=ORANGE)
        self.play(Write(title2))
        self.wait(0.5)

        axes2 = Axes(
            x_range=[-1, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"include_numbers": True},
        )
        axes2.next_to(title2, DOWN, buff=0.5)
        func2 = axes2.plot(lambda x: x**2, color=GREEN)
        func_label2 = MathTex("f(x)=x^2", color=GREEN).next_to(axes2, DR, buff=0.3)

        # Two points for secant: a=1 and b=2.5
        a = 1.0
        b = 2.5
        dotA = Dot(axes2.c2p(a, a**2), color=RED)
        dotB = Dot(axes2.c2p(b, b**2), color=RED)
        labelA = MathTex("(a,f(a))", color=RED, font_size=28).next_to(dotA, UL)
        labelB = MathTex("(b,f(b))", color=RED, font_size=28).next_to(dotB, UR)

        # Secant line
        secant = Line(
            axes2.c2p(a, a**2),
            axes2.c2p(b, b**2),
            color=PURPLE,
            stroke_width=3,
        )
        delta_x = b - a
        delta_y = b**2 - a**2
        avg_rate = delta_y / delta_x
        rate_text = MathTex(
            f"\\text{{avg rate}} = \\frac{{f(b)-f(a)}}{{b-a}} = {avg_rate:.2f}",
            color=PURPLE,
            font_size=28,
        )
        rate_text.next_to(axes2, DOWN, buff=0.4)

        self.play(Create(axes2), Create(func2), Write(func_label2))
        self.play(Create(dotA), Create(dotB), Write(labelA), Write(labelB))
        self.play(Create(secant))
        self.play(Write(rate_text))
        self.wait(2)

        self.clear()

        # ------------------------------------------------------------
        # Scene 3: Shrinking the interval — b → a
        # ------------------------------------------------------------
        title3 = Text("Making the interval smaller ...", font_size=36, color=ORANGE)
        self.play(Write(title3))
        self.wait(0.5)

        axes3 = Axes(
            x_range=[-1, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"include_numbers": True},
        )
        axes3.next_to(title3, DOWN, buff=0.5)
        func3 = axes3.plot(lambda x: x**2, color=GREEN)
        func_label3 = MathTex("f(x)=x^2", color=GREEN).next_to(axes3, DR, buff=0.3)

        a_fixed = 1.0
        b_start = 2.5
        dotA3 = Dot(axes3.c2p(a_fixed, a_fixed**2), color=RED)
        labelA3 = MathTex("a", color=RED, font_size=28).next_to(dotA3, UL)

        dotB3 = Dot(axes3.c2p(b_start, b_start**2), color=RED)
        labelB3 = MathTex("b", color=RED, font_size=28).next_to(dotB3, UR)
        secant3 = Line(
            axes3.c2p(a_fixed, a_fixed**2),
            axes3.c2p(b_start, b_start**2),
            color=PURPLE,
            stroke_width=3,
        )

        self.play(Create(axes3), Create(func3), Write(func_label3))
        self.play(Create(dotA3), Create(dotB3), Write(labelA3), Write(labelB3))
        self.play(Create(secant3))

        # Animate b moving toward a
        self.play(
            dotB3.animate.move_to(axes3.c2p(2.0, 4.0)),
            labelB3.animate.next_to(axes3.c2p(2.0, 4.0), UR),
            secant3.animate.put_start_and_end_on(
                axes3.c2p(a_fixed, a_fixed**2),
                axes3.c2p(2.0, 4.0),
            ),
            run_time=1.5,
        )
        self.wait(0.5)
        self.play(
            dotB3.animate.move_to(axes3.c2p(1.5, 2.25)),
            labelB3.animate.next_to(axes3.c2p(1.5, 2.25), UR),
            secant3.animate.put_start_and_end_on(
                axes3.c2p(a_fixed, a_fixed**2),
                axes3.c2p(1.5, 2.25),
            ),
            run_time=1.5,
        )
        self.wait(0.5)
        self.play(
            dotB3.animate.move_to(axes3.c2p(1.2, 1.44)),
            labelB3.animate.next_to(axes3.c2p(1.2, 1.44), UR),
            secant3.animate.put_start_and_end_on(
                axes3.c2p(a_fixed, a_fixed**2),
                axes3.c2p(1.2, 1.44),
            ),
            run_time=1.5,
        )
        self.wait(1.5)

        self.clear()

        # ------------------------------------------------------------
        # Scene 4: Limit concept — secant becomes tangent
        # ------------------------------------------------------------
        title4 = Text("As b → a, the secant approaches the tangent", font_size=32, color=YELLOW)
        self.play(Write(title4))
        self.wait(0.5)

        axes4 = Axes(
            x_range=[-1, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"include_numbers": True},
        )
        axes4.next_to(title4, DOWN, buff=0.5)
        func4 = axes4.plot(lambda x: x**2, color=GREEN)
        func_label4 = MathTex("f(x)=x^2", color=GREEN).next_to(axes4, DR, buff=0.3)

        a4 = 1.0
        dotA4 = Dot(axes4.c2p(a4, a4**2), color=RED)
        labelA4 = MathTex("a", color=RED, font_size=28).next_to(dotA4, UL)

        # Tangent line slope at a=1: derivative 2*1=2
        tangent_line = axes4.plot(lambda x: 2 * (x - a4) + a4**2, x_range=[0.2, 2.0], color=PURPLE)
        tangent_label = MathTex("\\text{tangent line}", color=PURPLE, font_size=28)
        tangent_label.next_to(axes4, DOWN, buff=0.5)

        self.play(Create(axes4), Create(func4), Write(func_label4))
        self.play(Create(dotA4), Write(labelA4))
        self.play(Create(tangent_line))
        self.play(Write(tangent_label))
        self.wait(2)

        self.clear()

        # ------------------------------------------------------------
        # Scene 5: Limit definition symbolically
        # ------------------------------------------------------------
        title5 = Text("The limit definition", font_size=36, color=YELLOW)
        self.play(Write(title5))
        self.wait(0.5)

        limit_def = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            font_size=44,
            color=BLUE,
        )
        limit_def.next_to(title5, DOWN, buff=0.8)

        explanation = Text(
            "Instantaneous rate of change = derivative",
            font_size=28,
            color=WHITE,
        )
        explanation.next_to(limit_def, DOWN, buff=0.5)

        self.play(Write(limit_def))
        self.play(Write(explanation))
        self.wait(2)

        self.clear()

        # ------------------------------------------------------------
        # Scene 6: Geometric interpretation — slope of tangent = derivative
        # ------------------------------------------------------------
        title6 = Text("Derivative = slope of tangent line", font_size=34, color=YELLOW)
        self.play(Write(title6))
        self.wait(0.5)

        axes6 = Axes(
            x_range=[-1, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"include_numbers": True},
        )
        axes6.next_to(title6, DOWN, buff=0.5)
        func6 = axes6.plot(lambda x: x**2, color=GREEN)
        func_label6 = MathTex("f(x)=x^2", color=GREEN).next_to(axes6, DR, buff=0.3)

        a6 = 1.5
        dotA6 = Dot(axes6.c2p(a6, a6**2), color=RED)
        labelA6 = MathTex("(x, f(x))", color=RED, font_size=28).next_to(dotA6, UL)

        # tangent slope = 2*1.5 = 3
        tangent_line6 = axes6.plot(lambda x: 3 * (x - a6) + a6**2, x_range=[0.5, 2.5], color=PURPLE)
        slope_label6 = MathTex(r"f'(x) = 3", color=PURPLE, font_size=30)
        slope_label6.next_to(axes6, DOWN, buff=0.5)

        self.play(Create(axes6), Create(func6), Write(func_label6))
        self.play(Create(dotA6), Write(labelA6))
        self.play(Create(tangent_line6))
        self.play(Write(slope_label6))
        self.wait(2)

        self.clear()

        # ------------------------------------------------------------
        # Scene 7: Derivative as a function (graphical)
        # ------------------------------------------------------------
        title7 = Text("Derivative as a function", font_size=34, color=YELLOW)
        self.play(Write(title7))
        self.wait(0.5)

        axes7 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-6, 6, 1],
            axis_config={"include_numbers": True},
        )
        axes7.next_to(title7, DOWN, buff=0.5)

        func7 = axes7.plot(lambda x: x**2, color=GREEN, x_range=[-2.5, 2.5])
        deriv7 = axes7.plot(lambda x: 2 * x, color=ORANGE, x_range=[-2.5, 2.5])

        func_label7 = MathTex("f(x)=x^2", color=GREEN).next_to(axes7, UL, buff=0.2)
        deriv_label7 = MathTex("f'(x)=2x", color=ORANGE).next_to(axes7, UR, buff=0.2)

        self.play(Create(axes7))
        self.play(Create(func7), Write(func_label7))
        self.play(Create(deriv7), Write(deriv_label7))
        self.wait(2)

        self.clear()

        # ------------------------------------------------------------
        # Scene 8: Real world intuition — velocity
        # ------------------------------------------------------------
        title8 = Text("Real-world example: velocity", font_size=36, color=YELLOW)
        self.play(Write(title8))
        self.wait(0.5)

        example = MathTex(
            r"\text{If } s(t) = t^2 \text{ (position)}, \quad v(t) = s'(t) = 2t",
            font_size=38, color=BLUE,
        )
        example.next_to(title8, DOWN, buff=0.8)

        note = Text(
            "Derivative gives instantaneous velocity at any time t",
            font_size=28,
            color=WHITE,
        )
        note.next_to(example, DOWN, buff=0.5)

        self.play(Write(example))
        self.play(Write(note))
        self.wait(2)

        self.clear()

        # ------------------------------------------------------------
        # Scene 9: Summary of the concept
        # ------------------------------------------------------------
        title9 = Text("Derivative: The Instantaneous Rate of Change", font_size=38, color=YELLOW)
        self.play(Write(title9))
        self.wait(0.5)

        summary_items = VGroup(
            Text("• Secant line → average rate", font_size=28, color=ORANGE),
            Text("• As interval shrinks → tangent line", font_size=28, color=ORANGE),
            Text("• Slope of tangent = derivative", font_size=28, color=ORANGE),
            Text("• Limit of difference quotient", font_size=28, color=ORANGE),
        )
        summary_items.arrange(DOWN, buff=0.3)
        summary_items.next_to(title9, DOWN, buff=0.8)

        final_formula = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}",
            font_size=40,
            color=BLUE,
        )
        final_formula.next_to(summary_items, DOWN, buff=0.5)

        self.play(Write(summary_items))
        self.play(Write(final_formula))
        self.wait(3)

        self.clear()

        # ------------------------------------------------------------
        # Scene 10: Closing animation
        # ------------------------------------------------------------
        closing = Text(
            "Calculus: the study of change",
            font_size=42,
            color=TEAL,
        )
        self.play(Write(closing))
        self.wait(1.5)
        closing2 = Text(
            "Derivative = foundation of calculus",
            font_size=32,
            color=GRAY,
        )
        closing2.next_to(closing, DOWN, buff=0.5)
        self.play(Write(closing2))
        self.wait(2)
