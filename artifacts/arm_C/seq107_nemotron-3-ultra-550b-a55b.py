from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Average Rate of Change ---
        self.clear()
        # Colors from style guidelines
        BG_COLOR = "#181825"
        AXES_COLOR = "#89b4fa"  # Blue
        GRAPH_COLOR = "#94e2d5"  # Teal
        POINT_A_COLOR = "#a6e3a1"  # Green
        POINT_B_COLOR = "#f38ba8"  # Red
        SECANT_COLOR = "#fab387"  # Peach
        TRIANGLE_COLOR_1 = "#a6e3a1"  # Green for run
        TRIANGLE_COLOR_2 = "#f38ba8"  # Red for rise
        TEXT_COLOR = "#cdd6f4"  # Text (Catppuccin Mocha Text)

        self.camera.background_color = BG_COLOR

        # 1. Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": AXES_COLOR, "include_numbers": True, "font_size": 24},
            tips=False,
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        axes_labels.set_color(TEXT_COLOR)

        # 2. Graph f(x) = x^3 - 3x
        graph = axes.plot(lambda x: x**3 - 3 * x, color=GRAPH_COLOR, stroke_width=3)

        # 3. Points A(-1, 2) and B(1, -2)
        point_a_coords = (-1, 2)
        point_b_coords = (1, -2)
        point_a = Dot(axes.c2p(*point_a_coords), color=POINT_A_COLOR, radius=0.1)
        point_b = Dot(axes.c2p(*point_b_coords), color=POINT_B_COLOR, radius=0.1)
        label_a = MathTex("A(-1, 2)", color=TEXT_COLOR, font_size=28).next_to(
            point_a, UL, buff=0.1
        )
        label_b = MathTex("B(1, -2)", color=TEXT_COLOR, font_size=28).next_to(
            point_b, DR, buff=0.1
        )

        # 4. Secant Line
        secant_line = Line(
            axes.c2p(*point_a_coords),
            axes.c2p(*point_b_coords),
            color=SECANT_COLOR,
            stroke_width=3,
        )

        # 5. Slope Triangle (Right Triangle)
        p_a = axes.c2p(*point_a_coords)
        p_b = axes.c2p(*point_b_coords)
        p_corner = axes.c2p(point_b_coords[0], point_a_coords[1])  # (x_B, y_A)

        # Triangle vertices: A, Corner, B
        slope_triangle = Polygon(
            p_a, p_corner, p_b, color=TRIANGLE_COLOR_1, fill_opacity=0.3, stroke_width=0
        )

        # Leg lines for labeling
        run_line = Line(p_a, p_corner, color=TRIANGLE_COLOR_1, stroke_width=4)
        rise_line = Line(p_corner, p_b, color=TRIANGLE_COLOR_2, stroke_width=4)

        # 6. Labels Rise/Run
        run_label = MathTex(
            "\\Delta x = 2", color=TRIANGLE_COLOR_1, font_size=32
        ).next_to(run_line, DOWN, buff=0.2)
        rise_label = MathTex(
            "\\Delta y = -4", color=TRIANGLE_COLOR_2, font_size=32
        ).next_to(rise_line, RIGHT, buff=0.2)

        # 7. Slope Formula - Fixed escape sequence
        slope_formula = MathTex(
            r"\text{Average Rate of Change} = \frac{\Delta y}{\Delta x} = \frac{-4}{2} = -2",
            color=TEXT_COLOR,
            font_size=36,
        )
        slope_formula.to_corner(UR, buff=0.5)

        # Animations
        self.play(Create(axes), Write(axes_labels), run_time=1.5)
        self.play(Create(graph), run_time=2.0)
        self.play(
            FadeIn(point_a, point_b), Write(label_a), Write(label_b), run_time=1.0
        )
        self.play(Create(secant_line), run_time=1.0)
        self.play(
            FadeIn(slope_triangle), Create(run_line), Create(rise_line), run_time=1.5
        )
        self.play(Write(run_label), Write(rise_label), run_time=1.0)
        self.play(Write(slope_formula), run_time=1.5)
        self.wait(0.5)  # Fixed: wait time must be positive
        # --- Scene 2: Limit of the Secant Line ---
        self.camera.background_color = "#1E1E2E"

        # Setup axes
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": "#CDD6F4", "include_tip": True},
        )

        # Define function f(x) = -(x-2)^2 + 4 (parabola with vertex at (2,4))
        def func(x):
            return -((x - 2) ** 2) + 4

        # Create graph
        graph = axes.plot(func, x_range=[0, 4], color="#89B4FA", stroke_width=3)

        # Fixed point A at x=1
        x_a = 1
        y_a = func(x_a)
        point_a = Dot(axes.c2p(x_a, y_a), color="#A6E3A1", radius=0.1)
        label_a = MathTex("A", color="#CDD6F4", font_size=36).next_to(
            point_a, UL, buff=0.1
        )

        # ValueTracker for point B's x-coordinate (starts at x=3, moves to x=1)
        b_tracker = ValueTracker(3)

        # Moving point B
        point_b = always_redraw(
            lambda: Dot(
                axes.c2p(b_tracker.get_value(), func(b_tracker.get_value())),
                color="#FAB387",
                radius=0.1,
            )
        )
        label_b = always_redraw(
            lambda: MathTex("B", color="#CDD6F4", font_size=36).next_to(
                point_b, UR, buff=0.1
            )
        )

        # Dynamic secant line
        secant_line = always_redraw(
            lambda: Line(
                axes.c2p(x_a, y_a),
                axes.c2p(b_tracker.get_value(), func(b_tracker.get_value())),
                color="#F38BA8",
                stroke_width=2,
            )
        )

        # Tangent line at A (derivative at x=1 is 2)
        # Tangent: y - 3 = 2(x - 1) => y = 2x + 1
        tangent_line = Line(
            axes.c2p(0, 1), axes.c2p(3, 7), color="#89B4FA", stroke_width=4
        )
        tangent_line.set_opacity(0)  # Start invisible

        # Slope triangle (dynamic)
        slope_triangle = always_redraw(
            lambda: Polygon(
                axes.c2p(x_a, y_a),
                axes.c2p(b_tracker.get_value(), y_a),
                axes.c2p(b_tracker.get_value(), func(b_tracker.get_value())),
                fill_color="#CBA6F7",
                fill_opacity=0.3,
                stroke_color="#CBA6F7",
                stroke_width=1,
            )
        )

        # Delta x and Delta y labels
        delta_x_label = always_redraw(
            lambda: MathTex(r"\Delta x", color="#CDD6F4", font_size=24).move_to(
                axes.c2p((x_a + b_tracker.get_value()) / 2, y_a - 0.3)
            )
        )
        delta_y_label = always_redraw(
            lambda: MathTex(r"\Delta y", color="#CDD6F4", font_size=24).move_to(
                axes.c2p(
                    b_tracker.get_value() + 0.2, (y_a + func(b_tracker.get_value())) / 2
                )
            )
        )

        # Animation sequence
        self.play(Create(axes), Create(graph), run_time=1.5)
        self.play(FadeIn(point_a), Write(label_a), run_time=0.5)
        self.play(
            FadeIn(point_b),
            Write(label_b),
            Create(secant_line),
            Create(slope_triangle),
            run_time=1.0,
        )
        self.play(Write(delta_x_label), Write(delta_y_label), run_time=0.5)

        # Animate B moving towards A (x: 3 -> 1) over 4 seconds
        self.play(
            b_tracker.animate.set_value(
                1.001
            ),  # Approach but not equal to avoid division by zero
            run_time=4,
            rate_func=smooth,
        )

        # Fade out slope triangle and labels, show tangent line
        self.play(
            FadeOut(slope_triangle),
            FadeOut(delta_x_label),
            FadeOut(delta_y_label),
            tangent_line.animate.set_opacity(1),
            run_time=1.0,
        )

        # Glow effect on tangent line
        self.play(
            tangent_line.animate.set_stroke(width=6, color="#89B4FA"), run_time=0.5
        )
        self.play(
            tangent_line.animate.set_stroke(width=4, color="#89B4FA"), run_time=0.5
        )

        # Final wait to reach total 9.5 seconds
        self.wait(0.5)
        # --- Scene 3: The Difference Quotient ---
        self.clear()
        self.camera.background_color = "#181825"

        # Color palette
        BLUE = "#89b4fa"
        ORANGE = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"

        # 1. Create Axes and Function Graph
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 10, 2],
            x_length=8,
            y_length=5,
            axis_config={"color": WHITE, "stroke_width": 2},
        ).shift(DOWN * 0.5)

        # Define function f(x) = x^2
        graph = axes.plot(lambda x: x**2, color=BLUE, x_range=[-1, 3.5])
        graph_label = MathTex("f(x) = x^2", color=BLUE).next_to(
            graph.get_end(), UP + RIGHT, buff=0.2
        )

        # 2. Points and Secant Line Setup (initial h=2)
        x_val = 1
        h_val = 2
        tracker = ValueTracker(h_val)

        # Points
        dot1 = Dot(color=ORANGE)
        dot2 = Dot(color=PINK)

        # Secant line
        secant = Line(color=GREEN)

        # Updaters for dynamic movement
        def update_dot1(mob):
            mob.move_to(axes.c2p(x_val, x_val**2))

        def update_dot2(mob):
            h = tracker.get_value()
            mob.move_to(axes.c2p(x_val + h, (x_val + h) ** 2))

        def update_secant(mob):
            p1 = axes.c2p(x_val, x_val**2)
            p2 = axes.c2p(
                x_val + tracker.get_value(), (x_val + tracker.get_value()) ** 2
            )
            mob.put_start_and_end_on(p1, p2)

        dot1.add_updater(update_dot1)
        dot2.add_updater(update_dot2)
        secant.add_updater(update_secant)

        # Labels for points
        x_label = MathTex("x", color=ORANGE).next_to(dot1, DOWN, buff=0.1)
        xh_label = MathTex("x+h", color=PINK).next_to(dot2, UP + RIGHT, buff=0.1)

        # Make labels follow dots
        x_label.add_updater(lambda m: m.next_to(dot1, DOWN, buff=0.1))
        xh_label.add_updater(lambda m: m.next_to(dot2, UP + RIGHT, buff=0.1))

        # 3. Horizontal Brace for 'h' on x-axis
        # Brace connects x to x+h on the x-axis
        h_brace = Brace(
            Line(axes.c2p(x_val, 0), axes.c2p(x_val + h_val, 0)), DOWN, color=TEAL
        )
        h_text = MathTex("h", color=TEAL).next_to(h_brace, DOWN, buff=0.1)

        def update_brace(mob):
            h = tracker.get_value()
            new_line = Line(axes.c2p(x_val, 0), axes.c2p(x_val + h, 0))
            mob.become(Brace(new_line, DOWN, color=TEAL))

        def update_h_text(mob):
            mob.next_to(h_brace, DOWN, buff=0.1)

        h_brace.add_updater(update_brace)
        h_text.add_updater(update_h_text)

        # 4. Difference Quotient Formula (Top Left)
        quot_formula = (
            MathTex(r"\lim_{h 	o 0} \frac{f(x+h) - f(x)}{h}", font_size=48)
            .to_corner(UL)
            .shift(DOWN * 0.5 + RIGHT * 0.5)
        )

        # 5. Derivative Notation (Hidden initially)
        deriv_notation = MathTex("f'(x) = 2x", font_size=48, color=GREEN).move_to(
            quot_formula
        )

        # --- ANIMATION SEQUENCE (Total 11.0s) ---

        # 1. Intro: Show Graph and Formula (2.0 + 1.0 + 0.5 = 3.5s)
        self.play(Create(axes), Create(graph), Write(graph_label), run_time=2.0)
        self.play(Write(quot_formula), run_time=1.0)
        self.wait(0.5)

        # 2. Show Secant Line and Points (1.5 + 0.5 + 0.5 = 2.5s) -> Total 6.0s
        self.play(FadeIn(dot1), FadeIn(dot2), Create(secant), run_time=1.5)
        self.play(Write(x_label), Write(xh_label), run_time=0.5)
        self.wait(0.5)

        # 3. Show Brace 'h' (1.0 + 0.5 = 1.5s) -> Total 7.5s
        self.play(GrowFromCenter(h_brace), Write(h_text), run_time=1.0)
        self.wait(0.5)

        # 4. Animate h -> 0 (2.5s) -> Total 10.0s
        self.play(tracker.animate.set_value(0.01), run_time=2.5, rate_func=smooth)

        # 5. Transform Formula to Derivative (1.0s) -> Total 11.0s
        self.play(ReplacementTransform(quot_formula, deriv_notation), run_time=1.0)
        # --- Scene 4: Instantaneous Rate of Change ---
        self.clear()
        # Set background color
        self.camera.background_color = "#181825"

        # Define palette colors
        accent_4 = "#a6e3a1"  # Green from palette
        accent_1 = "#89b4fa"  # Blue from palette

        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"stroke_width": 2, "color": WHITE},
        )

        # Define function f(x) = x^3 - 3x
        def func(x):
            return x**3 - 3 * x

        # Plot the curve
        curve = axes.plot(func, color=accent_1, stroke_width=3)

        # Point A at x = -1
        x_a = -1
        y_a = func(x_a)
        point_a = Dot(axes.c2p(x_a, y_a), color=YELLOW, radius=0.1)

        # Tangent line at x = -1 (derivative f'(x) = 3x^2 - 3, f'(-1) = 0)
        # Tangent line: y = y_a + f'(x_a)(x - x_a) = 2 + 0*(x+1) = 2
        tangent_line = axes.plot(lambda x: y_a, color=accent_4, stroke_width=3)

        # Slope triangle on tangent line (infinitesimally small but visible)
        # Horizontal leg: dx = 0.5, Vertical leg: dy = 0 (since slope = 0)
        dx = 0.5
        p1 = axes.c2p(x_a, y_a)
        p2 = axes.c2p(x_a + dx, y_a)
        p3 = axes.c2p(x_a + dx, y_a)
        slope_triangle = Polygon(
            p1, p2, p3, color=accent_4, fill_opacity=0.3, stroke_width=2
        )

        # Derivative label f'(x) = 0
        derivative_label = MathTex("f'(x) = 0", font_size=36, color=accent_4)
        derivative_label.next_to(point_a, UP + RIGHT, buff=0.3)

        # Slope value label (DecimalNumber showing 0)
        slope_value = DecimalNumber(
            0, num_decimal_places=1, color=accent_4, font_size=36
        )
        slope_value.next_to(derivative_label, DOWN, buff=0.2)

        # Group for pulsing animation
        tangent_group = VGroup(
            tangent_line, slope_triangle, derivative_label, slope_value
        )

        # Animations
        self.play(Create(axes), Create(curve), run_time=1.5)
        self.play(FadeIn(point_a), run_time=0.5)
        self.play(Create(tangent_line), run_time=1.0)
        self.play(FadeIn(slope_triangle), Write(derivative_label), run_time=1.0)
        self.play(FadeIn(slope_value), run_time=0.5)

        # Pulse animation (indicate instantaneous rate)
        self.play(
            Indicate(tangent_line, color=accent_4, scale_factor=1.1), run_time=1.0
        )
        self.play(Indicate(slope_value, color=accent_4, scale_factor=1.2), run_time=1.0)
        self.play(
            Indicate(derivative_label, color=accent_4, scale_factor=1.1), run_time=1.0
        )

        # Wait to match duration 8.5 seconds
        # Sum: 1.5+0.5+1.0+1.0+0.5+1.0+1.0+1.0 = 7.5, need 1.0 more
        self.wait(1.0)
        # --- Scene 5: Derivative as a Function ---
        # Nord palette colors
        BACKGROUND = "#2E3440"
        ACCENT_1 = "#88C0D0"  # For derivative curve
        ACCENT_2 = "#81A1C1"  # For tangent line
        ACCENT_4 = "#A3BE8C"  # For tracker dot
        ACCENT_5 = "#EBCB8B"  # For derivative point
        PRIMARY_TEXT = "#ECEFF4"

        self.camera.background_color = BACKGROUND

        # Define functions
        def f(x):
            return x**3 - 3 * x

        def f_prime(x):
            return 3 * x**2 - 3

        # Set up original axes (top)
        original_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-6, 6, 2],
            x_length=10,
            y_length=5,
            axis_config={"color": PRIMARY_TEXT, "stroke_width": 2},
        ).to_edge(UP, buff=0.5)

        original_graph = original_axes.plot(f, color=PRIMARY_TEXT, stroke_width=3)
        original_label = MathTex(
            "f(x) = x^3 - 3x", color=PRIMARY_TEXT, font_size=36
        ).next_to(original_axes, UP)

        # Set up derivative axes (bottom)
        derivative_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-6, 10, 2],
            x_length=10,
            y_length=5,
            axis_config={"color": PRIMARY_TEXT, "stroke_width": 2},
        ).to_edge(DOWN, buff=0.5)

        derivative_graph = derivative_axes.plot(f_prime, color=ACCENT_1, stroke_width=3)
        derivative_label = MathTex(
            "f'(x) = 3x^2 - 3", color=ACCENT_1, font_size=36
        ).next_to(derivative_axes, DOWN)

        # ValueTracker for x position
        x_tracker = ValueTracker(-2.5)

        # Tracker dot on original curve
        tracker_dot = always_redraw(
            lambda: Dot(
                original_axes.c2p(x_tracker.get_value(), f(x_tracker.get_value())),
                color=ACCENT_4,
                radius=0.12,
            )
        )

        # Tangent line on original curve
        tangent_line = always_redraw(
            lambda: original_axes.get_secant_slope_group(
                x=x_tracker.get_value(),
                graph=original_graph,
                dx=0.01,
                secant_line_color=ACCENT_2,
                secant_line_length=4,
            )
        )

        # Derivative point on derivative axes
        derivative_point = always_redraw(
            lambda: Dot(
                derivative_axes.c2p(
                    x_tracker.get_value(), f_prime(x_tracker.get_value())
                ),
                color=ACCENT_5,
                radius=0.1,
            )
        )

        # Traced path for derivative curve drawing
        derivative_curve_drawing = TracedPath(
            derivative_point.get_center,
            stroke_color=ACCENT_1,
            stroke_width=3,
            stroke_opacity=1,
        )

        # Initial setup
        self.add(original_axes, original_graph, original_label)
        self.add(derivative_axes, derivative_label)

        # Fade original graph to lighter opacity
        self.play(original_graph.animate.set_opacity(0.3), run_time=1.0)

        # Add tracker elements
        self.add(tracker_dot, tangent_line, derivative_point, derivative_curve_drawing)

        # Animate tracker from x=-2.5 to x=2.5
        self.play(x_tracker.animate.set_value(2.5), run_time=7.0, rate_func=linear)

        # Show final derivative graph
        self.play(Create(derivative_graph), run_time=1.5)

        # Final wait to match exact duration - use a small positive duration
        self.wait(0.001)  # Total: 1.0 + 7.0 + 1.5 = 9.5 (approximately)
