from manim import *

class SceneGen(Scene):
    def construct(self):
        # SCENE 1: Introduction to Average Speed with a Car
        self.camera.background_color = "#1a1a2e"
        
        title = Text("Understanding Derivatives", font_size=48, color=YELLOW)
        subtitle = Text("From Average to Instantaneous Rate of Change", font_size=28, color=GRAY_B)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(1)
        
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Car and road setup
        road = Line(LEFT * 5, RIGHT * 5, color=GRAY, stroke_width=8)
        road_label = Text("Road (distance in miles)", font_size=20, color=GRAY_C).next_to(road, DOWN, buff=0.3)
        
        car = SVGMobject("car").scale(0.4) if False else Rectangle(height=0.5, width=0.8, color=RED, fill_opacity=0.8)
        car = VGroup(
            Polygon([-0.4, 0, 0], [0.4, 0, 0], [0.3, 0.3, 0], [-0.3, 0.3, 0], color=RED, fill_opacity=0.9),
            Circle(radius=0.12, color=BLACK, fill_opacity=0.8).move_to([-0.2, -0.1, 0]),
            Circle(radius=0.12, color=BLACK, fill_opacity=0.8).move_to([0.2, -0.1, 0])
        )
        car.move_to(LEFT * 4 + UP * 0.4)
        
        start_flag = VGroup(
            Line(DOWN * 0.3, UP * 0.5, color=GREEN),
            Triangle(color=GREEN, fill_opacity=0.8).scale(0.2).move_to(UP * 0.5 + RIGHT * 0.2).rotate(-PI/2)
        ).move_to(LEFT * 4 + DOWN * 0.6)
        
        end_flag = VGroup(
            Line(DOWN * 0.3, UP * 0.5, color=RED),
            Triangle(color=RED, fill_opacity=0.8).scale(0.2).move_to(UP * 0.5 + RIGHT * 0.2).rotate(-PI/2)
        ).move_to(RIGHT * 3 + DOWN * 0.6)
        
        start_time = Text("t = 1 hour", font_size=20, color=GREEN).next_to(start_flag, DOWN)
        end_time = Text("t = 3 hours", font_size=20, color=RED).next_to(end_flag, DOWN)
        
        distance_brace = BraceBetweenPoints(LEFT * 4, RIGHT * 3, direction=UP, color=YELLOW)
        distance_text = distance_brace.get_text("120 miles")
        
        self.play(Create(road), Write(road_label), run_time=1)
        self.play(Create(start_flag), Create(end_flag), run_time=0.8)
        self.play(Write(start_time), Write(end_time), run_time=0.8)
        self.play(Create(distance_brace), Write(distance_text), run_time=1)
        
        # Animate car moving
        self.play(car.animate.move_to(RIGHT * 3 + UP * 0.4), run_time=2, rate_func=linear)
        
        avg_speed = MathTex(r"\text{Average Speed} = \frac{120 \text{ miles}}{2 \text{ hours}} = 60 \text{ mph}", color=YELLOW)
        avg_speed.to_edge(DOWN, buff=0.8)
        
        self.play(Write(avg_speed), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.clear()
        self.wait(0.5)
        
        # SCENE 2: The Problem with Average Speed
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 150, 30],
            x_length=9,
            y_length=5,
            axis_config={"include_numbers":True, "color":WHITE},
            tips=False
        ).to_edge(DOWN, buff=1)
        
        x_label = MathTex("t \text{ (hours)}", color=BLUE).next_to(axes.x_axis, RIGHT)
        y_label = MathTex("s \text{ (miles)}", color=GREEN).next_to(axes.y_axis, UP)
        
        # Position function s(t) = 20t^2 (non-constant velocity)
        graph = axes.plot(lambda t: 20 * t**2, color=YELLOW, x_range=[0, 5.5])
        graph_label = MathTex("s(t) = 20t^2", color=YELLOW).next_to(axes.c2p(4, 120), UR)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)
        self.play(Create(graph), Write(graph_label), run_time=1.5)
        
        # Two points for average rate
        dot_a = Dot(axes.c2p(1, 20), color=GREEN)
        dot_b = Dot(axes.c2p(3, 180), color=RED)
        label_a = MathTex("A(1, 20)", color=GREEN, font_size=28).next_to(dot_a, LEFT + DOWN)
        label_b = MathTex("B(3, 180)", color=RED, font_size=28).next_to(dot_b, RIGHT)
        
        secant_line = Line(dot_a.get_center(), dot_b.get_center(), color=ORANGE)
        
        self.play(Create(dot_a), Create(dot_b), run_time=0.8)
        self.play(Write(label_a), Write(label_b), run_time=0.8)
        self.play(Create(secant_line), run_time=1)
        
        # Show slope calculation
        slope_calc = MathTex(r"\text{Slope} = \frac{180-20}{3-1} = \frac{160}{2} = 80", color=ORANGE)
        slope_calc.to_edge(UP, buff=0.5)
        
        self.play(Write(slope_calc), run_time=1.5)
        self.wait(1)
        
        # The problem: what about at exactly t=2?
        question = Text("But what is the speed at EXACTLY t = 2?", color=RED, font_size=32)
        question.next_to(slope_calc, DOWN)
        
        cursor_dot = Dot(axes.c2p(2, 80), color=RED)
        cursor_label = MathTex("t=2", color=RED, font_size=24).next_to(axes.c2p(2, 0), DOWN)
        
        self.play(Write(question), run_time=1)
        self.play(Create(cursor_dot), Create(cursor_label), run_time=0.8)
        self.wait(2)
        
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.clear()
        self.wait(0.5)
        
        # SCENE 3: Zooming In - Secant Lines Approach Tangent
        axes2 = Axes(
            x_range=[0, 5, 0.5],
            y_range=[0, 120, 20],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 1}, "color": WHITE},
            tips=False
        ).to_edge(DOWN, buff=0.8)
        
        x_label2 = MathTex("t", color=BLUE).next_to(axes2.x_axis, RIGHT)
        y_label2 = MathTex("s(t)", color=GREEN).next_to(axes2.y_axis, UP)
        
        graph2 = axes2.plot(lambda t: 15 * t**2, color=YELLOW, x_range=[0, 4.5])
        
        self.play(Create(axes2), Write(x_label2), Write(y_label2), run_time=1.5)
        self.play(Create(graph2), run_time=1.5)
        
        # Fixed point P at t=2
        p_x = 2
        p_y = 15 * p_x**2
        point_p = Dot(axes2.c2p(p_x, p_y), color=YELLOW)
        label_p = MathTex("P(2, 60)", color=YELLOW, font_size=28).next_to(point_p, UP)
        
        self.play(Create(point_p), Write(label_p), run_time=1)
        
        # Multiple secant lines with Q approaching P
        h_values = [2, 1, 0.5, 0.25, 0.1]
        colors = [RED, ORANGE, GREEN, BLUE, PURPLE]
        
        prev_secant = None
        prev_dot_q = None
        prev_label_q = None
        
        for i, h in enumerate(h_values):
            q_x = p_x + h
            q_y = 15 * q_x**2
            
            dot_q = Dot(axes2.c2p(q_x, q_y), color=colors[i])
            label_q = MathTex(f"Q(2+h, s(2+h))", color=colors[i], font_size=22).next_to(dot_q, RIGHT + UP * 0.3)
            label_q_small = MathTex(f"h = {h}", color=colors[i], font_size=24).next_to(dot_q, RIGHT + DOWN * 0.2)
            
            secant = Line(axes2.c2p(p_x, p_y), axes2.c2p(q_x, q_y), color=colors[i])
            
            # Calculate slope
            slope = (q_y - p_y) / h
            slope_text = MathTex(f"\\text{{Slope}} = {slope:.1f}", color=colors[i], font_size=28)
            slope_text.to_edge(UP, buff=0.3)
            
            if prev_secant:
                self.play(
                    Transform(prev_secant, secant),
                    Transform(prev_dot_q, dot_q),
                    Transform(prev_label_q, VGroup(label_q_small)),
                    FadeIn(slope_text),
                    FadeOut(prev_slope_text) if 'prev_slope_text' in dir() or i > 0 else FadeOut(slope_text) if i == 0 else FadeOut(prev_slope_text),
                    run_time=1.5
                )
            else:
                self.play(Create(dot_q), Create(secant), Write(label_q_small), run_time=1)
                self.play(Write(slope_text), run_time=1)
            
            prev_secant = secant
            prev_dot_q = dot_q
            prev_label_q = label_q_small
            prev_slope_text = slope_text
            
            self.wait(0.8)
        
        # Emphasize h getting closer to 0
        limit_text = MathTex(r"\text{As } h \to 0, \text{ slope approaches } 60", color=WHITE, font_size=30)
        limit_text.to_edge(UP, buff=0.3)
        
        self.play(
            Transform(prev_slope_text, limit_text),
            run_time=1.5
        )
        self.wait(2)
        
        # The tangent line appears
        tangent_line = axes2.get_secant_slope_group(
            x=2,
            graph=graph2,
            dx=0.001,
            secant_line_color=WHITE,
            secant_line_length=6
        ).secant_line
        
        self.play(
            FadeOut(prev_secant),
            FadeOut(prev_dot_q),
            FadeOut(prev_label_q),
            FadeOut(prev_slope_text),
            run_time=0.5
        )
        
        tangent_label = MathTex(r"\text{Tangent Line at } P", color=WHITE, font_size=28).next_to(point_p, DOWN + LEFT)
        
        self.play(Create(tangent_line), Write(tangent_label), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.clear()
        self.wait(0.5)
        
        # SCENE 4: Formal Definition - The Difference Quotient
        title_dq = Text("The Difference Quotient", font_size=40, color=YELLOW)
        title_dq.to_edge(UP, buff=0.5)
        
        self.play(Write(title_dq), run_time=1)
        
        # Visual setup with two points
        axes3 = Axes(
            x_range=[0, 6, 1],
            y_range=[-5, 80, 20],
            x_length=9,
            y_length=5,
            axis_config={"include_numbers": True, "color": WHITE},
            tips=False
        ).move_to(DOWN * 0.5)
        
        x_label3 = MathTex("x", color=BLUE).next_to(axes3.x_axis, RIGHT)
        y_label3 = MathTex("f(x)", color=GREEN).next_to(axes3.y_axis, UP)
        
        # A cubic function for variety
        graph3 = axes3.plot(lambda x: x**3 - 6*x**2 + 11*x, color=YELLOW, x_range=[0, 5])
        
        self.play(Create(axes3), Write(x_label3), Write(y_label3), run_time=1.5)
        self.play(Create(graph3), run_time=1.5)
        
        # General points
        a_val = 2
        a_y = a_val**3 - 6*a_val**2 + 11*a_val
        
        dot_a = Dot(axes3.c2p(a_val, a_y), color=YELLOW)
        label_a = MathTex("x", color=YELLOW, font_size=28).next_to(dot_a, DOWN + LEFT)
        
        h_val = 1.5
        dot_b = Dot(axes3.c2p(a_val + h_val, (a_val+h_val)**3 - 6*(a_val+h_val)**2 + 11*(a_val+h_val)), color=RED)
        label_b = MathTex("x+h", color=RED, font_size=28).next_to(dot_b, RIGHT)
        
        secant = Line(dot_a.get_center(), dot_b.get_center(), color=ORANGE)
        
        # Rise and run visualization
        run_line = DashedLine(dot_a.get_center(), axes3.c2p(a_val + h_val, a_y), color=GREEN)
        rise_line = DashedLine(axes3.c2p(a_val + h_val, a_y), dot_b.get_center(), color=BLUE)
        
        run_brace = Brace(run_line, direction=DOWN, color=GREEN)
        rise_brace = Brace(rise_line, direction=RIGHT, color=BLUE)
        
        run_label = MathTex("h", color=GREEN, font_size=24).next_to(run_brace, DOWN, buff=0.1)
        rise_label = MathTex(r"f(x+h)-f(x)", color=BLUE, font_size=24).next_to(rise_brace, RIGHT, buff=0.1)
        
        self.play(Create(dot_a), Write(label_a), run_time=0.8)
        self.play(Create(dot_b), Write(label_b), run_time=0.8)
        self.play(Create(secant), run_time=0.8)
        self.play(Create(run_line), Create(rise_line), run_time=0.8)
        self.play(Create(run_brace), Create(rise_brace), Write(run_label), Write(rise_label), run_time=1)
        
        # Build up the formula step by step
        formula_parts = VGroup()
        
        step1 = MathTex(r"\text{Slope}", color=WHITE)
        step1.to_edge(UP, buff=1.5)
        
        step2 = MathTex(r"= \frac{\text{Rise}}{\text{Run}}", color=WHITE)
        step2.next_to(step1, RIGHT)
        
        step3 = MathTex(r"= \frac{f(x+h) - f(x)}{h}", color=ORANGE)
        step3.next_to(step2, RIGHT)
        
        self.play(Write(step1), run_time=1)
        self.play(Write(step2), run_time=1)
        self.play(Write(step3), run_time=1.5)
        
        formula_group = VGroup(step1, step2, step3)
        
        self.wait(2)
        
        # Reveal this is the difference quotient
        dq_title = MathTex(r"\text{Difference Quotient: } \frac{f(x+h) - f(x)}{h}", color=YELLOW, font_size=36)
        dq_title.to_edge(UP, buff=1.5)
        
        self.play(
            Transform(formula_group, dq_title),
            run_time=1.5
        )
        self.wait(2)
        
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.clear()
        self.wait(0.5)
        
        # SCENE 5: The Limit - From Difference Quotient to Derivative
        title_limit = Text("Taking the Limit", font_size=40, color=YELLOW)
        title_limit.to_edge(UP, buff=0.5)
        
        self.play(Write(title_limit), run_time=1)
        
        # Big formula display
        diff_quotient = MathTex(r"\frac{f(x+h) - f(x)}{h}", color=ORANGE, font_size=48)
        diff_quotient.move_to(UP * 1.5)
        
        limit_notation = MathTex(r"\lim_{h \to 0}", color=BLUE, font_size=48)
        limit_notation.next_to(diff_quotient, LEFT, buff=0.3)
        
        equals = MathTex(r"= \; ?", color=WHITE, font_size=48)
        equals.next_to(diff_quotient, RIGHT, buff=0.3)
        
        self.play(Write(diff_quotient), run_time=1)
        self.play(Write(limit_notation), run_time=1)
        self.play(Write(equals), run_time=1)
        
        self.wait(1)
        
        # Visual demonstration with shrinking h
        axes4 = Axes(
            x_range=[0, 4, 0.5],
            y_range=[0, 10, 2],
            x_length=8,
            y_length=4.5,
            axis_config={"include_numbers": True, "color": WHITE},
            tips=False
        ).to_edge(DOWN, buff=0.8)
        
        graph4 = axes4.plot(lambda x: x**2, color=YELLOW, x_range=[0, 3.5])
        graph_label = MathTex("f(x) = x^2", color=YELLOW, font_size=24).next_to(axes4.c2p(3, 9), UR)
        
        self.play(Create(axes4), Create(graph4), Write(graph_label), run_time=1.5)
        
        # Point at x=2
        a_point = axes4.c2p(2, 4)
        fixed_dot = Dot(a_point, color=YELLOW)
        fixed_label = MathTex("x", color=YELLOW, font_size=24).next_to(fixed_dot, DOWN + LEFT)
        
        self.play(Create(fixed_dot), Write(fixed_label), run_time=0.8)
        
        # Series of h values showing convergence
        h_vals_demo = [1.0, 0.5, 0.25, 0.1, 0.05, 0.01]
        prev_elements = None
        
        for j, h_demo in enumerate(h_vals_demo):
            b_x = 2 + h_demo
            b_y = b_x**2
            b_point = axes4.c2p(b_x, b_y)
            
            moving_dot = Dot(b_point, color=RED)
            moving_label = MathTex(f"h={h_demo}", color=RED, font_size=18).next_to(moving_dot, UR)
            
            secant_demo = Line(a_point, b_point, color=ORANGE)
            
            # Calculate actual slope
            slope_val = (b_y - 4) / h_demo
            slope_display = MathTex(f"\\text{{Slope}} = {slope_val:.4f}", color=ORANGE, font_size=26)
            slope_display.to_edge(DOWN, buff=0.3)
            
            # Derivative value
            deriv_display = MathTex(r"f'(2) = 4", color=GREEN, font_size=26).next_to(slope_display, RIGHT, buff=1)
            
            current_elements = VGroup(moving_dot, moving_label, secant_demo, slope_display)
            
            if prev_elements:
                self.play(
                    FadeOut(prev_elements),
                    run_time=0.3
                )
            
            if j == len(h_vals_demo) - 1:
                # Final: tangent line
                tangent = axes4.get_secant_slope_group(
                    x=2, graph=graph4, dx=0.001,
                    secant_line_color=GREEN, secant_line_length=6
                ).secant_line
                
                final_slope = MathTex(r"\text{Slope} \to 4", color=GREEN, font_size=28)
                final_slope.to_edge(DOWN, buff=0.3)
                
                self.play(
                    Create(moving_dot),
                    Write(moving_label),
                    Create(secant_demo),
                    run_time=0.6
                )
                self.play(
                    Transform(secant_demo, tangent),
                    Transform(moving_dot, Dot(a_point, color=GREEN)),
                    FadeOut(moving_label),
                    Write(final_slope),
                    run_time=1
                )
                self.play(Write(deriv_display), run_time=0.8)
            else:
                self.play(
                    Create(moving_dot),
                    Write(moving_label),
                    Create(secant_demo),
                    Write(slope_display),
                    run_time=0.8 if j == 0 else 0.5
                )
            
            prev_elements = current_elements
            self.wait(0.3 if j < len(h_vals_demo) - 1 else 2)
        
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.clear()
        self.wait(0.5)
        
        # SCENE 6: The Derivative Definition
        title_deriv = Text("The Derivative", font_size=44, color=YELLOW)
        title_deriv.to_edge(UP, buff=0.5)
        
        self.play(Write(title_deriv), run_time=1)
        
        # Full definition
        def1 = MathTex(r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}", color=WHITE, font_size=42)
        def1.move_to(UP * 1)
        
        self.play(Write(def1), run_time=2)
        self.wait(1)
        
        # Alternative notation
        def2 = MathTex(r"\frac{df}{dx} = \lim_{\Delta x \to 0} \frac{\Delta f}{\Delta x} = \lim_{\Delta x \to 0} \frac{f(x+\Delta x) - f(x)}{\Delta x}", color=ORANGE, font_size=32)
        def2.next_to(def1, DOWN, buff=0.8)
        
        self.play(Write(def2), run_time=2)
        self.wait(1)
        
        # Leibniz notation explanation
        leibniz = MathTex(r"\frac{df}{dx} \text{ means ''the rate of change of } f \text{ with respect to } x\text{''}", color=GREEN, font_size=28)
        leibniz.next_to(def2, DOWN, buff=0.8)
        
        self.play(Write(leibniz), run_time=1.5)
        self.wait(2)
        
        # Key insight box
        box = Rectangle(height=2, width=10, color=YELLOW, fill_opacity=0.1)
        box.to_edge(DOWN, buff=0.5)
        
        key_insight = Text("KEY INSIGHT:", font_size=28, color=YELLOW)
        key_insight.next_to(box.get_top(), DOWN, buff=0.2)
        
        insight_text = Text("The derivative is the slope of the tangent line", font_size=24, color=WHITE)
        insight_text.next_to(key_insight, DOWN, buff=0.2)
        
        insight_text2 = Text("at a single point — the instantaneous rate of change", font_size=24, color=WHITE)
        insight_text2.next_to(insight_text, DOWN, buff=0.1)
        
        self.play(Create(box), run_time=1)
        self.play(Write(key_insight), run_time=0.8)
        self.play(Write(insight_text), run_time=1)
        self.play(Write(insight_text2), run_time=1)
        self.wait(2)
        
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.clear()
        self.wait(0.5)
        
        # SCENE 7: Concrete Example - Computing f'(x) for f(x) = x²
        title_example = Text("Example: Finding the Derivative of f(x) = x²", font_size=36, color=YELLOW)
        title_example.to_edge(UP, buff=0.5)
        
        self.play(Write(title_example), run_time=1)
        
        # Step by step calculation
        step1 = MathTex(r"f(x) = x^2", color=WHITE, font_size=32)
        step1.to_edge(LEFT, buff=1)
        step1.shift(UP * 2)
        
        self.play(Write(step1), run_time=1)
        
        step2 = MathTex(r"f(x+h) = (x+h)^2 = x^2 + 2xh + h^2", color=GREEN, font_size=28)
        step2.next_to(step1, DOWN, buff=0.6)
        step2.to_edge(LEFT, buff=1)
        
        self.play(Write(step2), run_time=1.5)
        
        step3 = MathTex(r"f(x+h) - f(x) = (x^2 + 2xh + h^2) - x^2 = 2xh + h^2", color=ORANGE, font_size=28)
        step3.next_to(step2, DOWN, buff=0.6)
        step3.to_edge(LEFT, buff=1)
        
        self.play(Write(step3), run_time=1.5)
        
        step4 = MathTex(r"\frac{f(x+h) - f(x)}{h} = \frac{2xh + h^2}{h} = 2x + h", color=YELLOW, font_size=28)
        step4.next_to(step3, DOWN, buff=0.6)
        step4.to_edge(LEFT, buff=1)
        
        self.play(Write(step4), run_time=1.5)
        
        step5 = MathTex(r"f'(x) = \lim_{h \to 0} (2x + h) = 2x", color=RED, font_size=32)
        step5.next_to(step4, DOWN, buff=0.8)
        step5.to_edge(LEFT, buff=1)
        
        self.play(Write(step5), run_time=1.5)
        
        # Visual confirmation
        axes5 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 8, 2],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True, "color": WHITE},
            tips=False
        ).to_edge(RIGHT, buff=1).shift(UP * 0.5)
        
        graph_f = axes5.plot(lambda x: x**2, color=YELLOW, x_range=[-2.5, 2.5])
        graph_f_label = MathTex("f(x)=x^2", color=YELLOW, font_size=20).next_to(axes5.c2p(2, 4), UR)
        
        graph_df = axes5.plot(lambda x: 2*x, color=GREEN, x_range=[-2.5, 2.5])
        graph_df_label = MathTex("f'(x)=2x", color=GREEN, font_size=20).next_to(axes5.c2p(2, 4), RIGHT)
        
        self.play(Create(axes5), Create(graph_f), Write(graph_f_label), run_time=1.5)
        
        # Show tangent slopes at various points
        test_points = [(1, 1), (0, 0), (-1, 2)]
        colors_tp = [RED, BLUE, PURPLE]
        
        for k, (tx, ty) in enumerate(test_points):
            actual_y = tx**2
            point = Dot(axes5.c2p(tx, actual_y), color=colors_tp[k])
            tangent = axes5.get_secant_slope_group(
                x=tx, graph=graph_f, dx=0.001,
                secant_line_color=colors_tp[k], secant_line_length=3
            ).secant_line
            
            slope_label = MathTex(f"f'({tx})={2*tx}", color=colors_tp[k], font_size=20)
            slope_label.next_to(point, UP if tx >= 0 else DOWN, buff=0.2)
            
            self.play(
                Create(point),
                Create(tangent),
                Write(slope_label),
                run_time=1
            )
        
        self.wait(1)
        
        # Add derivative graph
        self.play(Create(graph_df), Write(graph_df_label), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.clear()
        self.wait(0.5)
        
        # SCENE 8: Interpretation - Position, Velocity, Acceleration
        title_phys = Text("Physical Interpretation", font_size=40, color=YELLOW)
        title_phys.to_edge(UP, buff=0.5)
        
        self.play(Write(title_phys), run_time=1)
        
        # Three levels
        level1 = MathTex(r"s(t) = \text{position (miles)}", color=BLUE, font_size=28)
        level1.move_to(UP * 2)
        
        arrow1 = Arrow(UP * 1.3, UP * 0.3, color=GREEN)
        deriv_label1 = MathTex(r"\frac{d}{dt}", color=GREEN, font_size=24).next_to(arrow1, RIGHT)
        
        level2 = MathTex(r"v(t) = s'(t) = \text{velocity (mph)}", color=GREEN, font_size=28)
        level2.move_to(DOWN * 0)
        
        arrow2 = Arrow(DOWN * 0.7, DOWN * 1.7, color=RED)
        deriv_label2 = MathTex(r"\frac{d}{dt}", color=RED, font_size=24).next_to(arrow2, RIGHT)
        
        level3 = MathTex(r"a(t) = v'(t) = s''(t) = \text{acceleration (mph}^2\text{)}", color=RED, font_size=28)
        level3.move_to(DOWN * 2.5)
        
        self.play(Write(level1), run_time=1)
        self.play(Create(arrow1), Write(deriv_label1), run_time=0.8)
        self.play(Write(level2), run_time=1)
        self.play(Create(arrow2), Write(deriv_label2), run_time=0.8)
        self.play(Write(level3), run_time=1)
        
        self.wait(2)
        
        # Concrete example with motion
        example_title = Text("Example: A Falling Object", font_size=28, color=WHITE)
        example_title.to_edge(DOWN, buff=1.5)
        
        height_eq = MathTex(r"h(t) = -4.9t^2 + 100 \text{ (meters)}", color=YELLOW, font_size=24)
        height_eq.next_to(example_title, DOWN, buff=0.3)
        
        velocity_eq = MathTex(r"v(t) = h'(t) = -9.8t \text{ (m/s)}", color=GREEN, font_size=24)
        velocity_eq.next_to(height_eq, DOWN, buff=0.3)
        
        accel_eq = MathTex(r"a(t) = v'(t) = -9.8 \text{ (m/s}^2\text{)} = \text{constant gravity}", color=RED, font_size=24)
        accel_eq.next_to(velocity_eq, DOWN, buff=0.3)
        
        self.play(Write(example_title), run_time=1)
        self.play(Write(height_eq), run_time=1)
        self.play(Write(velocity_eq), run_time=1)
        self.play(Write(accel_eq), run_time=1)
        self.wait(2)
        
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.clear()
        self.wait(0.5)
        
        # SCENE 9: Geometric Meaning - Tangent Lines and Function Behavior
        title_geo = Text("What the Derivative Tells Us", font_size=40, color=YELLOW)
        title_geo.to_edge(UP, buff=0.5)
        
        self.play(Write(title_geo), run_time=1)
        
        axes6 = Axes(
            x_range=[-3, 4, 1],
            y_range=[-5, 10, 2],
            x_length=10,
            y_length=5.5,
            axis_config={"include_numbers": True, "color": WHITE},
            tips=False
        ).to_edge(DOWN, buff=0.6)
        
        # Interesting function with multiple features
        graph6 = axes6.plot(lambda x: 0.5*x**3 - 2*x**2 + x + 3, color=YELLOW, x_range=[-2.5, 3.5])
        graph6_label = MathTex("f(x)", color=YELLOW, font_size=24).next_to(axes6.c2p(3, 4), UR)
        
        self.play(Create(axes6), Create(graph6), Write(graph6_label), run_time=1.5)
        
        # Show various tangent behaviors
        # Positive slope (increasing)
        pos_point = 2.5
        pos_dot = Dot(axes6.c2p(pos_point, 0.5*pos_point**3 - 2*pos_point**2 + pos_point + 3), color=GREEN)
        pos_tangent = axes6.get_secant_slope_group(
            x=pos_point, graph=graph6, dx=0.001,
            secant_line_color=GREEN, secant_line_length=4
        ).secant_line
        pos_label = Text("f' > 0: Increasing", color=GREEN, font_size=20).next_to(axes6.c2p(pos_point, 0.5*pos_point**3 - 2*pos_point**2 + pos_point + 3), UP)
        
        self.play(Create(pos_dot), Create(pos_tangent), Write(pos_label), run_time=1)
        self.wait(0.5)
        
        # Negative slope (decreasing)
        neg_point = 1.5
        neg_dot = Dot(axes6.c2p(neg_point, 0.5*neg_point**3 - 2*neg_point**2 + neg_point + 3), color=RED)
        neg_tangent = axes6.get_secant_slope_group(
            x=neg_point, graph=graph6, dx=0.001,
            secant_line_color=RED, secant_line_length=4
        ).secant_line
        neg_label = Text("f' < 0: Decreasing", color=RED, font_size=20).next_to(axes6.c2p(neg_point, 0.5*neg_point**3 - 2*neg_point**2 + neg_point + 3), DOWN)
        
        self.play(Create(neg_dot), Create(neg_tangent), Write(neg_label), run_time=1)
        self.wait(0.5)
        
        # Critical point where f' = 0
        crit_point = 2 + (4/3)**0.5  # local minimum approx
        # Actually let's use the exact critical point
        crit_x = 2 + (4/3)**0.5  # Actually solve: 1.5x^2 - 4x + 1 = 0
        # Use quadratic formula approximation
        crit_x = 2.387  # approximate local min
        
        # Better: find where derivative is zero: 1.5x^2 - 4x + 1 = 0
        import math
        a_q, b_q, c_q = 1.5, -4, 1
        crit_x2 = (-b_q + math.sqrt(b_q**2 - 4*a_q*c_q)) / (2*a_q)
        
        crit_dot = Dot(axes6.c2p(crit_x2, 0.5*crit_x2**3 - 2*crit_x2**2 + crit_x2 + 3), color=BLUE)
        crit_tangent = axes6.get_secant_slope_group(
            x=crit_x2, graph=graph6, dx=0.001,
            secant_line_color=BLUE, secant_line_length=4
        ).secant_line
        crit_label = Text("f' = 0: Critical Point (Horizontal Tangent)", color=BLUE, font_size=20)
        crit_label.next_to(crit_dot, UP + LEFT)
        
        self.play(Create(crit_dot), Create(crit_tangent), Write(crit_label), run_time=1)
        self.wait(2)
        
        # Summary table of derivative information
        self.play(
            FadeOut(pos_dot), FadeOut(pos_tangent), FadeOut(pos_label),
            FadeOut(neg_dot), FadeOut(neg_tangent), FadeOut(neg_label),
            FadeOut(crit_dot), FadeOut(crit_tangent), FadeOut(crit_label),
            run_time=0.8
        )
        
        summary = VGroup(
            MathTex(r"f'(x) > 0 \iff f \text{ is increasing}", color=GREEN, font_size=24),
            MathTex(r"f'(x) < 0 \iff f \text{ is decreasing}", color=RED, font_size=24),
            MathTex(r"f'(x) = 0 \iff \text{ possible local max/min}", color=BLUE, font_size=24),
            MathTex(r"|f'(x)| \text{ large} \iff \text{ steep (rapid change)}", color=ORANGE, font_size=24),
            MathTex(r"|f'(x)| \text{ small} \iff \text{ flat (slow change)}", color=YELLOW, font_size=24)
        ).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=0.5).shift(UP * 0.5)
        
        for item in summary:
            self.play(Write(item), run_time=0.8)
            self.wait(0.2)
        
        self.wait(2)
        
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.clear()
        self.wait(0.5)
        
        # SCENE 10: Summary and Key Takeaways
        final_title = Text("Summary: The Derivative", font_size=44, color=YELLOW)
        
        self.play(Write(final_title), run_time=1)
        
        # Central formula
        central = MathTex(r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}", color=WHITE, font_size=40)
        central.move_to(UP * 1)
        
        self.play(FadeOut(final_title), run_time=0.5)
        final_title_small = Text("Summary: The Derivative", font_size=32, color=YELLOW)
        final_title_small.to_edge(UP, buff=0.5)
        self.play(Write(final_title_small), run_time=0.5)
        self.play(Write(central), run_time=2)
        
        # Four key ideas arranged around
        idea1 = VGroup(
            MathTex(r"\text{1. Limit of}", font_size=22, color=BLUE),
            MathTex(r"\text{difference quotients}", font_size=22, color=BLUE)
        ).arrange(DOWN, buff=0.1)
        idea1.move_to(LEFT * 4 + UP * 2.5)
        
        idea2 = VGroup(
            MathTex(r"\text{2. Slope of}", font_size=22, color=GREEN),
            MathTex(r"\text{tangent line}", font_size=22, color=GREEN)
        ).arrange(DOWN, buff=0.1)
        idea2.move_to(RIGHT * 4 + UP * 2.5)
        
        idea3 = VGroup(
            MathTex(r"\text{3. Instantaneous}", font_size=22, color=ORANGE),
            MathTex(r"\text{rate of change}", font_size=22, color=ORANGE)
        ).arrange(DOWN, buff=0.1)
        idea3.move_to(LEFT * 4 + DOWN * 2)
        
        idea4 = VGroup(
            MathTex(r"\text{4. Linear}", font_size=22, color=PURPLE),
            MathTex(r"\text{approximation}", font_size=22, color=PURPLE)
        ).arrange(DOWN, buff=0.1)
        idea4.move_to(RIGHT * 4 + DOWN * 2)
        
        arrows = VGroup(
            Arrow(central.get_corner(UL) + LEFT * 0.3 + UP * 0.3, idea1.get_right(), color=BLUE),
            Arrow(central.get_corner(UR) + RIGHT * 0.3 + UP * 0.3, idea2.get_left(), color=GREEN),
            Arrow(central.get_corner(DL) + LEFT * 0.3 + DOWN * 0.3, idea3.get_right(), color=ORANGE),
            Arrow(central.get_corner(DR) + RIGHT * 0.3 + DOWN * 0.3, idea4.get_left(), color=PURPLE)
        )
        
        for idea in [idea1, idea2, idea3, idea4]:
            self.play(Write(idea), run_time=1)
        
        self.play(Create(arrows), run_time=1.5)
        self.wait(2)
        
        # Final visual: everything together
        self.play(
            FadeOut(idea1), FadeOut(idea2), FadeOut(idea3), FadeOut(idea4),
            FadeOut(arrows),
            central.animate.move_to(ORIGIN).scale(1.2),
            run_time=1.5
        )
        
        # Notation variants appear
        notations = VGroup(
            MathTex(r"f'(x)", color=YELLOW, font_size=32),
            MathTex(r"\frac{df}{dx}", color=GREEN, font_size=32),
            MathTex(r"\frac{d}{dx}f(x)", color=ORANGE, font_size=32),
            MathTex(r"D_x f", color=PURPLE, font_size=32)
        ).arrange(RIGHT, buff=1).next_to(central, DOWN, buff=1)
        
        notation_text = Text("Equivalent notations:", font_size=24, color=GRAY).next_to(notations, UP, buff=0.3)
        
        self.play(Write(notation_text), run_time=0.8)
        for note in notations:
            self.play(Write(note), run_time=0.6)
        
        self.wait(2)
        
        # Fade everything and show final message
        self.play(*[FadeOut(mobj) for mobj in self.mobjects], run_time=1)
        
        thanks = Text("Derivatives: The Mathematics of Change", font_size=36, color=YELLOW)
        thanks.move_to(UP * 0.5)
        
        subtitle_end = Text("Foundation for understanding how everything changes", font_size=24, color=GRAY)
        subtitle_end.next_to(thanks, DOWN, buff=0.5)
        
        self.play(Write(thanks), run_time=1.5)
        self.play(FadeIn(subtitle_end), run_time=1)
        self.wait(3)
        
        self.play(FadeOut(thanks), FadeOut(subtitle_end), run_time=1)
        self.clear()
