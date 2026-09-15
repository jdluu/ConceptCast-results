from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Functions and Slope ---
        self.clear()

        # === Color Palette (Catppuccin Mocha) ===
        BG = "#1E1E2E"
        TEXT_COLOR = "#CDD6F4"
        CURVE_COLOR = "#89B4FA"
        POINT_A_COLOR = "#F38BA8"
        POINT_B_COLOR = "#FAB387"
        TRIANGLE_COLOR = "#A6E3A1"
        ACCENT = "#CBA6F7"

        # === Background ===
        bg = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BG,
            fill_opacity=1,
            stroke_width=0,
        )
        self.add(bg)

        # === 1. Axes ===
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "color": TEXT_COLOR,
                "include_numbers": True,
                "font_size": 24,
            },
            tips=True,
        )
        axes_labels = axes.get_axis_labels(
            MathTex("x", color=TEXT_COLOR, font_size=30),
            MathTex("f(x)", color=TEXT_COLOR, font_size=30),
        )

        # === 2. Function Curve ===
        curve = axes.plot(
            lambda x: 0.1 * (x - 2) ** 3 - 0.5 * x + 2,
            x_range=[-0.5, 4.8],
            color=CURVE_COLOR,
            stroke_width=3,
        )
        func_label = MathTex(
            r"f(x) = 0.1(x-2)^3 - 0.5x + 2",
            color=CURVE_COLOR,
            font_size=26,
        ).to_corner(UR, buff=0.4)

        # === 3. Points A and B ===
        a_x, b_x = 0.5, 3.5
        a_y = 0.1 * (a_x - 2) ** 3 - 0.5 * a_x + 2
        b_y = 0.1 * (b_x - 2) ** 3 - 0.5 * b_x + 2

        point_a = Dot(axes.c2p(a_x, a_y), radius=0.1, color=POINT_A_COLOR)
        point_b = Dot(axes.c2p(b_x, b_y), radius=0.1, color=POINT_B_COLOR)

        label_a = MathTex("A(a, f(a))", color=POINT_A_COLOR, font_size=26).next_to(
            point_a, UL, buff=0.15
        )
        label_b = MathTex("B(b, f(b))", color=POINT_B_COLOR, font_size=26).next_to(
            point_b, UR, buff=0.15
        )

        # === 4. Slope Triangle ===
        corner_point = axes.c2p(b_x, a_y)
        triangle = Polygon(
            axes.c2p(a_x, a_y),
            corner_point,
            axes.c2p(b_x, b_y),
            color=TRIANGLE_COLOR,
            stroke_width=2.5,
            fill_color=TRIANGLE_COLOR,
            fill_opacity=0.15,
        )

        # Right angle marker
        right_angle_size = 0.2
        right_angle = VGroup(
            Line(
                corner_point,
                corner_point + right_angle_size * RIGHT,
                color=TRIANGLE_COLOR,
                stroke_width=1.5,
            ),
            Line(
                corner_point + right_angle_size * RIGHT,
                corner_point + right_angle_size * RIGHT + right_angle_size * UP,
                color=TRIANGLE_COLOR,
                stroke_width=1.5,
            ),
            Line(
                corner_point + right_angle_size * RIGHT + right_angle_size * UP,
                corner_point + right_angle_size * UP,
                color=TRIANGLE_COLOR,
                stroke_width=1.5,
            ),
        )

        # === 5. Braces for rise and run ===
        rise_brace = BraceBetweenPoints(
            axes.c2p(b_x, a_y),
            axes.c2p(b_x, b_y),
            direction=RIGHT,
            color=TRIANGLE_COLOR,
        )
        rise_label = MathTex(
            r"\Delta y = f(b) - f(a)",
            color=TRIANGLE_COLOR,
            font_size=22,
        ).next_to(rise_brace, RIGHT, buff=0.1)

        run_brace = BraceBetweenPoints(
            axes.c2p(a_x, a_y),
            axes.c2p(b_x, a_y),
            direction=DOWN,
            color=TRIANGLE_COLOR,
        )
        run_label = MathTex(
            r"\Delta x = b - a",
            color=TRIANGLE_COLOR,
            font_size=22,
        ).next_to(run_brace, DOWN, buff=0.1)

        # === 6. Slope Formula ===
        slope_formula = MathTex(
            r"	ext{slope} = \frac{\Delta y}{\Delta x} = \frac{f(b) - f(a)}{b - a}",
            color=ACCENT,
            font_size=32,
        ).to_edge(DOWN, buff=0.35)

        # ============================================================
        # === ANIMATIONS (total duration: 6.0s) ===
        # ============================================================

        # Phase 1: Draw axes and curve (0 → 2.0s)
        self.play(FadeIn(axes), run_time=0.5)
        self.play(FadeIn(axes_labels), run_time=0.3)
        self.play(Create(curve), run_time=1.0)
        self.play(FadeIn(func_label, shift=UP * 0.2), run_time=0.2)
        # 2.0s

        # Phase 2: Show points A and B (2.0 → 3.2s)
        self.play(
            GrowFromCenter(point_a),
            FadeIn(label_a, shift=LEFT * 0.2),
            run_time=0.6,
        )
        self.play(
            GrowFromCenter(point_b),
            FadeIn(label_b, shift=RIGHT * 0.2),
            run_time=0.6,
        )
        # 3.2s

        # Phase 3: Draw slope triangle with braces (3.2 → 5.0s)
        self.play(Create(triangle), run_time=0.6)
        self.play(Create(right_angle), run_time=0.3)
        self.play(
            FadeIn(rise_brace),
            FadeIn(rise_label),
            run_time=0.5,
        )
        self.play(
            FadeIn(run_brace),
            FadeIn(run_label),
            run_time=0.4,
        )
        # 5.0s

        # Phase 4: Display slope formula (5.0 → 6.0s)
        self.play(Write(slope_formula), run_time=0.8)
        self.wait(0.2)
        # 6.0s
        # --- Scene 2: Approaching the Limit ---
        self.clear()

        # ─── Color palette ───
        BG = "#181825"
        CURVE_COLOR = "#89b4fa"
        POINT_A_COLOR = "#f38ba8"
        POINT_B_COLOR = "#fab387"
        SECANT_COLOR = "#cba6f7"
        TRIANGLE_COLOR = "#a6e3a1"
        AXIS_COLOR = "#cdd6f4"
        DELTA_COLOR = "#fab387"
        GHOST_COLOR = "#585b70"
        self.camera.background_color = BG

        # ─── Axes ───
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=5.5,
            axis_config={
                "color": AXIS_COLOR,
                "include_tip": True,
                "stroke_width": 2,
            },
            tips=True,
        )
        axes_labels = VGroup(
            axes.get_x_axis_label("x", direction=RIGHT),
            axes.get_y_axis_label("f(x)", direction=UP),
        )

        # ─── Function: a cubic with interesting curvature ───
        def f(x):
            return 0.1 * (x - 2) ** 3 - 0.5 * x + 2

        curve = axes.plot(f, x_range=[-0.5, 4.8], color=CURVE_COLOR, stroke_width=3)

        # ─── Fixed point A at x=1 ───
        a_x = 1.0
        a_pt = axes.c2p(a_x, f(a_x))
        dot_a = Dot(a_pt, color=POINT_A_COLOR, radius=0.1)
        label_a = MathTex("A", color=POINT_A_COLOR, font_size=36).next_to(
            dot_a, DL, buff=0.15
        )
        coord_a = MathTex(r"x = a", color=POINT_A_COLOR, font_size=28).next_to(
            label_a, DOWN, buff=0.1
        )

        # ─── ValueTracker for point B position ───
        # h = B_x - a_x, starts at 3 (B at x=4), moves toward 0.15
        h_tracker = ValueTracker(3.0)

        # ─── Point B (moving, redrawn every frame) ───
        dot_b = always_redraw(
            lambda: Dot(
                axes.c2p(a_x + h_tracker.get_value(), f(a_x + h_tracker.get_value())),
                color=POINT_B_COLOR,
                radius=0.1,
            )
        )
        label_b = always_redraw(
            lambda: MathTex("B", color=POINT_B_COLOR, font_size=36).next_to(
                dot_b, UR, buff=0.15
            )
        )

        # ─── Secant line connecting A and B ───
        secant = always_redraw(
            lambda: Line(
                a_pt,
                axes.c2p(a_x + h_tracker.get_value(), f(a_x + h_tracker.get_value())),
                color=SECANT_COLOR,
                stroke_width=3,
            )
        )

        # ─── Dynamic right triangle (Δx horizontal, Δy vertical) ───
        def make_triangle():
            b_x = a_x + h_tracker.get_value()
            b_y = f(b_x)
            a_y = f(a_x)
            b_pt = axes.c2p(b_x, b_y)
            corner_pt = axes.c2p(b_x, a_y)
            return Polygon(
                a_pt,
                corner_pt,
                b_pt,
                color=TRIANGLE_COLOR,
                fill_color=TRIANGLE_COLOR,
                fill_opacity=0.15,
                stroke_width=2,
            )

        triangle = always_redraw(make_triangle)

        # ─── Δx and Δy labels following the triangle ───
        def make_delta_x():
            b_x = a_x + h_tracker.get_value()
            a_y = f(a_x)
            left = axes.c2p(a_x, a_y)
            right = axes.c2p(b_x, a_y)
            mid = (left + right) / 2
            label = MathTex(r"\Delta x", color=DELTA_COLOR, font_size=28)
            label.move_to(mid + DOWN * 0.3)
            return label

        def make_delta_y():
            b_x = a_x + h_tracker.get_value()
            b_y = f(b_x)
            a_y = f(a_x)
            bottom = axes.c2p(b_x, a_y)
            top = axes.c2p(b_x, b_y)
            mid = (bottom + top) / 2
            label = MathTex(r"\Delta y", color="#94e2d5", font_size=28)
            label.move_to(mid + RIGHT * 0.35)
            return label

        delta_x_label = always_redraw(make_delta_x)
        delta_y_label = always_redraw(make_delta_y)

        # ─── Slope display at top ───
        slope_label = always_redraw(
            lambda: MathTex(
                r"	ext{slope} = \frac{\Delta y}{\Delta x} = \frac{f(a+h) - f(a)}{h}",
                color=SECANT_COLOR,
                font_size=30,
            ).to_edge(UP, buff=0.4)
        )

        h_val_display = always_redraw(
            lambda: MathTex(
                "h = " + f"{h_tracker.get_value():.2f}",
                color=DELTA_COLOR,
                font_size=32,
            ).next_to(slope_label, DOWN, buff=0.2)
        )

        # ─── Ghost trail: faint traces of previous B positions ───
        ghost_positions = [4.0, 3.0, 2.5, 2.0, 1.7, 1.5, 1.3]
        ghosts = VGroup()
        for gx in ghost_positions:
            gp = axes.c2p(gx, f(gx))
            ghost_dot = Dot(gp, radius=0.05, color=GHOST_COLOR, fill_opacity=0.4)
            ghost_line = Line(
                a_pt, gp, color=GHOST_COLOR, stroke_width=1, stroke_opacity=0.25
            )
            ghosts.add(ghost_dot, ghost_line)

        # ─── "h → 0" callout in bottom-right ───
        h_arrow_text = MathTex(r"h 	o 0", color=DELTA_COLOR, font_size=40)
        h_arrow_text.to_corner(DR, buff=0.5)
        h_arrow_box = SurroundingRectangle(
            h_arrow_text, color=DELTA_COLOR, buff=0.15, stroke_width=1.5
        )

        # ═══════════════════════════════════════════════════════
        #  ANIMATIONS — total duration = 7.5s
        #  0.5+0.5=1.0  (axes + curve)
        #  0.3+0.2=0.5  (point A)
        #  0.5+0.3=0.8  (point B + secant + triangle)
        #  0.3+0.2=0.5  (slope display + h→0)
        #  0.5           (ghost trail)
        #  3.5           (B glides toward A)
        #  0.7           (final hold)
        #  TOTAL: 7.5s
        # ═══════════════════════════════════════════════════════

        # 1. Draw axes and curve
        self.play(Create(axes), Write(axes_labels), run_time=0.5)
        self.play(Create(curve), run_time=0.5)

        # 2. Fixed point A
        self.play(FadeIn(dot_a, scale=1.5), Write(label_a), run_time=0.3)
        self.play(FadeIn(coord_a, shift=UP * 0.2), run_time=0.2)

        # 3. Moving point B, secant, triangle
        self.play(
            FadeIn(dot_b, scale=1.5), Write(label_b), Create(secant), run_time=0.5
        )
        self.play(
            Create(triangle), FadeIn(delta_x_label), FadeIn(delta_y_label), run_time=0.3
        )

        # 4. Slope formula + h display
        self.play(
            FadeIn(slope_label, shift=DOWN * 0.2),
            FadeIn(h_val_display, shift=DOWN * 0.2),
            run_time=0.3,
        )
        self.play(FadeIn(h_arrow_text), FadeIn(h_arrow_box), run_time=0.2)

        # 5. Ghost trail of prior positions
        self.play(
            LaggedStart(*[FadeIn(g, shift=DOWN * 0.1) for g in ghosts], lag_ratio=0.04),
            run_time=0.5,
        )

        # 6. THE MAIN EVENT: B glides toward A, triangle shrinks, secant rotates
        self.play(h_tracker.animate.set_value(0.15), run_time=3.5, rate_func=smooth)

        # 7. Final contemplative hold
        self.wait(0.7)
        # --- Scene 3: Secant to Tangent ---
        # Catppuccin Mocha colors
        BG = "#1E1E2E"
        TEXT = "#CDD6F4"
        BLUE = "#89B4FA"
        PINK = "#F38BA8"
        GREEN = "#A6E3A1"
        GRAY = "#585B70"

        self.camera.background_color = BG

        # Create axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": TEXT, "include_tip": True},
        )

        # Define function
        curve = axes.plot(
            lambda x: 0.1 * (x - 2) ** 3 - 0.5 * x + 2,
            x_range=[-0.5, 4.8],
            color=BLUE,
            stroke_width=3,
        )

        # Point of tangency at x = 1
        x0 = 1.0
        y0 = 0.1 * (x0 - 2) ** 3 - 0.5 * x0 + 2
        point = Dot(axes.c2p(x0, y0), color=PINK, radius=0.1)

        # Tangent line at x0
        # Derivative: 0.3*(x-2)^2 - 0.5
        slope = 0.3 * (x0 - 2) ** 2 - 0.5
        tangent = axes.plot(
            lambda x: slope * (x - x0) + y0,
            x_range=[-0.5, 3.0],
            color=GREEN,
            stroke_width=3,
        )

        # Ghost secant line (dashed) between x=1 and x=3
        x_a, x_b = 1.0, 3.0
        y_a = 0.1 * (x_a - 2) ** 3 - 0.5 * x_a + 2
        y_b = 0.1 * (x_b - 2) ** 3 - 0.5 * x_b + 2
        secant_ghost = DashedLine(
            axes.c2p(x_a, y_a),
            axes.c2p(x_b, y_b),
            color=GRAY,
            stroke_width=2,
        )

        # Labels
        tangent_label = Text("Tangent Line", font_size=28, color=GREEN)
        tangent_label.next_to(tangent, UP, buff=0.2)

        point_label = Text("Point of Tangency", font_size=24, color=PINK)
        point_label.next_to(point, DOWN + RIGHT, buff=0.15)

        concept_text = Text("Instantaneous Rate of Change", font_size=30, color=TEXT)
        concept_text.to_edge(UP, buff=0.4)

        derivative_formula = MathTex(
            r"f'(x_0) = \lim_{h 	o 0} \frac{f(x_0+h) - f(x_0)}{h}",
            font_size=36,
            color=TEXT,
        )
        derivative_formula.to_edge(DOWN, buff=0.5)

        # --- Animations ---

        # Step 1: Axes and curve fade in
        self.play(FadeIn(axes), run_time=0.6)
        self.play(Create(curve), run_time=0.7)

        # Step 2: Ghost secant appears
        self.play(Create(secant_ghost), run_time=0.7)

        # Step 3: Secant vanishes, tangent grows
        self.play(
            FadeOut(secant_ghost),
            Create(tangent),
            run_time=1.0,
        )

        # Step 4: Point and labels
        self.play(
            GrowFromCenter(point),
            run_time=0.5,
        )
        self.play(
            Write(tangent_label),
            Write(point_label),
            run_time=0.7,
        )

        # Step 5: Highlight tangent, show concept
        self.play(
            Indicate(tangent, color=GREEN, scale_factor=1.1),
            Write(concept_text),
            run_time=0.8,
        )

        # Step 6: Derivative formula
        self.play(Write(derivative_formula), run_time=0.9)

        # Step 7: Hold
        self.wait(0.8)
        # --- Scene 4: The Difference Quotient ---
        self.clear()

        # Define color palette from style guidelines
        BG_COLOR = "#181825"
        ACCENT_1 = "#89b4fa"  # Blue for curve
        ACCENT_2 = "#fab387"  # Orange for run (h)
        ACCENT_3 = "#f38ba8"  # Pink for emphasis
        ACCENT_4 = "#a6e3a1"  # Green for rise
        TEXT_COLOR = "#CDD6F4"

        # Set background color
        self.camera.background_color = BG_COLOR

        # 1. Create axes (positioned left)
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=5,
            y_length=4,
            axis_config={
                "color": TEXT_COLOR,
                "include_tip": True,
                "stroke_width": 2,
            },
            tips=True,
        ).shift(LEFT * 2.5)

        # Add axis labels
        x_label = axes.get_x_axis_label("x", direction=RIGHT)
        y_label = axes.get_y_axis_label("y", direction=UP)

        # 2. Create a smooth curve (parabola-like)
        curve = axes.plot(
            lambda x: 0.3 * x**2 + 0.5,
            x_range=[0, 3.5],
            color=ACCENT_1,
            stroke_width=3,
        )

        # Define two points on the curve
        x_val = 1.0
        h_val = 1.5
        x_plus_h = x_val + h_val

        y_at_x = 0.3 * x_val**2 + 0.5
        y_at_x_plus_h = 0.3 * (x_plus_h) ** 2 + 0.5

        # Points on the curve
        point_x = axes.c2p(x_val, y_at_x)
        point_xh = axes.c2p(x_plus_h, y_at_x_plus_h)

        # Dots at the two points
        dot_x = Dot(point_x, color=ACCENT_3, radius=0.07)
        dot_xh = Dot(point_xh, color=ACCENT_3, radius=0.07)

        # Labels for the dots
        label_fx = MathTex("f(x)", font_size=28, color=ACCENT_4).next_to(
            dot_x, LEFT, buff=0.15
        )
        label_fxh = MathTex("f(x+h)", font_size=28, color=ACCENT_4).next_to(
            dot_xh, RIGHT, buff=0.15
        )

        # 3. Rise line (vertical): from (x+h, f(x)) to (x+h, f(x+h))
        rise_start = axes.c2p(x_plus_h, y_at_x)
        rise_end = axes.c2p(x_plus_h, y_at_x_plus_h)
        rise_line = Line(rise_start, rise_end, color=ACCENT_4, stroke_width=4)

        # 4. Run line (horizontal): from (x, f(x)) to (x+h, f(x))
        run_start = axes.c2p(x_val, y_at_x)
        run_end = axes.c2p(x_plus_h, y_at_x)
        run_line = Line(run_start, run_end, color=ACCENT_2, stroke_width=4)

        # Labels for rise and run
        label_rise = MathTex("f(x+h) - f(x)", font_size=24, color=ACCENT_4).next_to(
            rise_line, RIGHT, buff=0.15
        )
        label_run = MathTex("h", font_size=24, color=ACCENT_2).next_to(
            run_line, DOWN, buff=0.15
        )

        # Secant line connecting the two points
        secant_line = Line(point_x, point_xh, color=ACCENT_3, stroke_width=3)

        # Vertical dashed lines from points to x-axis
        dash_x = DashedLine(
            point_x,
            axes.c2p(x_val, 0),
            color=TEXT_COLOR,
            stroke_width=1.5,
            dash_length=0.1,
        )
        dash_xh = DashedLine(
            point_xh,
            axes.c2p(x_plus_h, 0),
            color=TEXT_COLOR,
            stroke_width=1.5,
            dash_length=0.1,
        )

        # x-axis labels
        label_x = MathTex("x", font_size=26, color=TEXT_COLOR).next_to(
            axes.c2p(x_val, 0), DOWN, buff=0.15
        )
        label_xh = MathTex("x+h", font_size=26, color=TEXT_COLOR).next_to(
            axes.c2p(x_plus_h, 0), DOWN, buff=0.15
        )

        # 5. Difference quotient equation (positioned right)
        equation = MathTex(
            r"\frac{f(x+h) - f(x)}{h}",
            font_size=56,
            color=WHITE,
        ).shift(RIGHT * 3)

        # Surrounding rectangle for equation
        eq_rect = SurroundingRectangle(
            equation, color=ACCENT_1, buff=0.2, corner_radius=0.1, stroke_width=2
        )

        # Group graph elements for scaling
        graph_group = VGroup(
            axes,
            curve,
            dot_x,
            dot_xh,
            secant_line,
            rise_line,
            run_line,
            label_fx,
            label_fxh,
            label_rise,
            label_run,
            dash_x,
            dash_xh,
            label_x,
            label_xh,
            x_label,
            y_label,
        )

        # ===== ANIMATIONS =====
        # Total target: 6.0 seconds

        # Phase 1: Draw axes and curve (1.2s)
        self.play(Create(axes), run_time=0.6)
        self.play(Create(curve), Write(x_label), Write(y_label), run_time=0.6)

        # Phase 2: Show the two points, labels, and secant line (1.3s)
        self.play(FadeIn(dot_x), FadeIn(dot_xh), run_time=0.4)
        self.play(Write(label_fx), Write(label_fxh), run_time=0.5)
        self.play(Create(secant_line), run_time=0.4)

        # Phase 3: Draw rise and run lines with labels (1.8s)
        self.play(
            Create(dash_x),
            Create(dash_xh),
            Write(label_x),
            Write(label_xh),
            run_time=0.5,
        )
        self.play(Create(run_line), run_time=0.4)
        self.play(Write(label_run), run_time=0.3)
        self.play(Create(rise_line), run_time=0.3)
        self.play(Write(label_rise), run_time=0.3)

        # Phase 4: Camera zooms out slightly, show equation (1.7s)
        self.play(
            graph_group.animate.scale(0.85).shift(LEFT * 0.3),
            run_time=0.5,
        )
        self.play(Write(equation), run_time=0.6)
        self.play(Create(eq_rect), run_time=0.4)

        # Final hold (0.2s)
        self.wait(0.2)
        # --- Scene 5: The Limit Definition ---
        self.clear()

        # Catppuccin Mocha palette
        BG_COLOR = "#181825"
        TEXT_COLOR = "#CDD6F4"
        RED_ACCENT = "#F38BA8"
        ORANGE_ACCENT = "#FAB387"
        GREEN_ACCENT = "#A6E3A1"
        BLUE_ACCENT = "#89B4FA"

        # Set background
        self.camera.background_color = BG_COLOR

        # --- OBJECTS ---

        # The equation WITHOUT the limit operator (start state)
        eq_no_limit = MathTex(
            r"f'(x)", r"=", r"\frac{f(x+h) - f(x)}{h}", font_size=44, color=TEXT_COLOR
        )
        eq_no_limit.move_to(ORIGIN)

        # The full limit definition equation (end state)
        limit_def = MathTex(
            r"f'(x)",
            r"=",
            r"\lim_{h 	o 0}",
            r"\frac{f(x+h) - f(x)}{h}",
            font_size=44,
            color=TEXT_COLOR,
        )
        limit_def.move_to(ORIGIN)

        # Fraction part reference (index 2 in eq_no_limit)
        fraction_part = eq_no_limit[2]

        # h -> 0 label below the equation
        h_label = MathTex(r"h 	o 0", font_size=36, color=RED_ACCENT)
        h_label.next_to(eq_no_limit, DOWN, buff=0.5)

        # Arrow from h_label to the fraction
        arrow_to_h = Arrow(
            start=h_label.get_top() + UP * 0.05,
            end=fraction_part.get_bottom() + DOWN * 0.05,
            buff=0.05,
            color=ORANGE_ACCENT,
            stroke_width=3,
            tip_length=0.18,
        )

        # === TIMELINE (total = 7.5s) ===
        # Phase 1: Write equation (0.0 - 1.8s) = 1.8s
        # Phase 2: Pulse h variables red (1.8 - 2.9s) = 1.1s
        # Phase 3: Show h->0 label + arrow (2.9 - 4.2s) = 1.3s
        # Phase 4: Transform to limit def (4.2 - 5.9s) = 1.7s
        # Phase 5: Highlight f'(x) (5.9 - 6.9s) = 1.0s
        # Wait 0.6s

        # --- Phase 1: Write the base equation ---
        self.play(Write(eq_no_limit), run_time=1.8)

        # --- Phase 2: Pulse the h variables in the fraction ---
        h_highlight = SurroundingRectangle(
            fraction_part, color=RED_ACCENT, buff=0.08, stroke_width=3
        )
        self.play(
            Create(h_highlight),
            fraction_part.animate.set_color(RED_ACCENT),
            run_time=0.35,
        )
        self.play(FadeOut(h_highlight), fraction_part.animate.scale(1.08), run_time=0.4)
        self.play(fraction_part.animate.scale(1.0 / 1.08), run_time=0.35)

        # --- Phase 3: Show h->0 label and arrow ---
        self.play(FadeIn(h_label, shift=UP * 0.2), run_time=0.65)
        self.play(GrowArrow(arrow_to_h), run_time=0.65)

        # --- Phase 4: Transition to full limit definition ---
        self.play(FadeOut(h_label), FadeOut(arrow_to_h), run_time=0.5)
        self.play(ReplacementTransform(eq_no_limit, limit_def), run_time=1.2)

        # --- Phase 5: Highlight the final f'(x) notation ---
        fprime = limit_def[0]
        self.play(Indicate(fprime, color=GREEN_ACCENT, scale_factor=1.3), run_time=1.0)

        # --- Hold the final frame ---
        self.wait(0.6)
        # --- Scene 6: Tangent Line Slope ---
        # Background
        self.camera.background_color = "#181825"

        # Title
        title = Text("Tangent Line Slope", font_size=48, color="#89B4FA").to_edge(UP)
        self.play(FadeIn(title), run_time=0.5)

        # Axes
        axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-4, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": "#585B70", "stroke_width": 2},
            tips=True,
        ).shift(DOWN * 0.3)
        self.play(FadeIn(axes), run_time=0.5)

        # Curve f(x) = 0.2x^3 - 1.5x^2 + 2x
        def func(x):
            return 0.2 * x**3 - 1.5 * x**2 + 2 * x

        curve = axes.plot(func, x_range=[-0.5, 5.5], color="#89B4FA", stroke_width=4)
        glow = axes.plot(
            func,
            x_range=[-0.5, 5.5],
            color="#89B4FA",
            stroke_width=12,
            stroke_opacity=0.3,
        )
        self.play(Create(glow), Create(curve), run_time=1.5)

        # Derivative formula
        deriv = MathTex(r"f'(x) = 0.6x^2 - 3x + 2", font_size=36, color="#CDD6F4")
        deriv.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(deriv), run_time=0.8)

        # Tangent line helper
        def tangent_line(x0, color, slope_val, length=2.5):
            y0 = func(x0)
            point = axes.coords_to_point(x0, y0)
            m = slope_val
            dx = length / 2
            dy = m * dx
            start = axes.coords_to_point(x0 - dx, y0 - dy)
            end = axes.coords_to_point(x0 + dx, y0 + dy)
            line = Line(start, end, color=color, stroke_width=3)
            dot = Dot(point, radius=0.08, color=color)
            label = DecimalNumber(
                slope_val, num_decimal_places=1, font_size=32, color=color
            )
            label.next_to(dot, UR, buff=0.15)
            return line, dot, label

        # Point 1: x=0.88, slope≈0
        tl1, dot1, lbl1 = tangent_line(0.88, "#A6E3A1", 0.0)
        self.play(Create(tl1), FadeIn(dot1), run_time=0.6)
        self.play(FadeIn(lbl1), run_time=0.4)

        # Point 2: x=3.39, slope≈-2
        tl2, dot2, lbl2 = tangent_line(3.39, "#FAB387", -2.0)
        self.play(Create(tl2), FadeIn(dot2), run_time=0.6)
        self.play(FadeIn(lbl2), run_time=0.4)

        # Point 3: x=4.5, slope≈3.1
        tl3, dot3, lbl3 = tangent_line(4.5, "#CBA6F7", 3.1)
        self.play(Create(tl3), FadeIn(dot3), run_time=0.6)
        self.play(FadeIn(lbl3), run_time=0.4)

        # Emphasize all slope labels
        self.play(
            Indicate(lbl1, color="#A6E3A1", scale_factor=1.3),
            Indicate(lbl2, color="#FAB387", scale_factor=1.3),
            Indicate(lbl3, color="#CBA6F7", scale_factor=1.3),
            run_time=0.9,
        )

        self.wait(0.8)
        # --- Scene 7: Velocity Example ---
        # --- Scene 7: Velocity Example ---

        # Background
        self.camera.background_color = "#181825"

        # Create axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=7,
            y_length=4,
            axis_config={"include_numbers": True, "color": "#CDD6F4"},
        ).shift(UP * 1.5)

        x_label = axes.get_x_axis_label("t").set_color("#CDD6F4")
        y_label = axes.get_y_axis_label("s(t)").set_color("#CDD6F4")

        # Create position curve s(t) = t^2
        curve = axes.plot(
            lambda x: x**2, x_range=[0, 2.2], color="#89b4fa", stroke_width=3
        )
        curve_label = (
            MathTex("s(t) = t^2", color="#89b4fa")
            .scale(0.7)
            .next_to(axes, UP, buff=0.2)
        )

        # Value tracker for time t
        t_tracker = ValueTracker(0.5)

        # Dot that moves along curve
        dot = always_redraw(
            lambda: Dot(
                axes.coords_to_point(t_tracker.get_value(), t_tracker.get_value() ** 2),
                color="#F38BA8",
                radius=0.08,
            )
        )

        # Tangent arrow showing slope (derivative)
        tangent_arrow = always_redraw(
            lambda: Arrow(
                start=axes.coords_to_point(
                    t_tracker.get_value(), t_tracker.get_value() ** 2
                ),
                end=axes.coords_to_point(
                    t_tracker.get_value() + 0.8,
                    t_tracker.get_value() ** 2 + 2 * t_tracker.get_value() * 0.8,
                ),
                color="#FAB387",
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.2,
            )
        )

        # Velocity display
        velocity_label = (
            MathTex("v(t) = s'(t) = 2t", color="#A6E3A1")
            .scale(0.8)
            .to_edge(DOWN, buff=1.5)
        )
        velocity_label.shift(LEFT * 2)

        velocity_value = always_redraw(
            lambda: DecimalNumber(
                2 * t_tracker.get_value(),
                num_decimal_places=2,
                color="#A6E3A1",
                font_size=40,
            ).next_to(velocity_label, RIGHT, buff=0.3)
        )

        # Create animations
        # Step 1: Draw axes (1.5s)
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)

        # Step 2: Draw curve (1.0s)
        self.play(Create(curve), Write(curve_label), run_time=1.0)

        # Step 3: Add interactive elements (0.5s)
        self.play(
            FadeIn(dot),
            FadeIn(tangent_arrow),
            FadeIn(velocity_label),
            FadeIn(velocity_value),
            run_time=0.5,
        )

        # Step 4: Animate t from 0.5 to 4.5 (2.5s)
        self.play(t_tracker.animate.set_value(4.5), run_time=2.5, rate_func=linear)

        # Step 5: Pause (0.5s)
        self.wait(0.5)
