import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Defining the Function as a Path ---
        self.clear()

        # ── Palette (Catppuccin Mocha) ────────────────────────────
        BG = "#181825"
        GRID_COL = "#45475a"
        ACCENT = "#89b4fa"
        LABEL_COL = "#cdd6f4"
        GLOW_COL = "#74c7ec"

        # Apply background colour
        self.camera.background_color = BG

        # ── 1. Coordinate Plane ──────────────────────────────────
        coord_plane = NumberPlane(
            x_range=[-4, 10, 1],
            y_range=[-2, 10, 1],
            x_length=12,
            y_length=8,
            background_line_style={
                "stroke_color": GRID_COL,
                "stroke_width": 1,
                "stroke_opacity": 0.45,
            },
            axis_config={
                "stroke_color": "#585b70",
                "stroke_width": 2,
            },
        )

        # ── 2. Function Graph ────────────────────────────────────
        func_graph = coord_plane.plot(
            lambda x: 0.1 * x**2 - 2 * x + 5,
            x_range=[-3, 9],
            color=ACCENT,
            stroke_width=3.5,
        )

        # A faint "glow" copy behind the graph for depth
        glow_graph = coord_plane.plot(
            lambda x: 0.1 * x**2 - 2 * x + 5,
            x_range=[-3, 9],
            color=GLOW_COL,
            stroke_width=10,
            stroke_opacity=0.15,
        )

        # ── 3. Label ─────────────────────────────────────────────
        func_label = MathTex(
            r"f(x) = 0.1\,x^{2} - 2x + 5",
            font_size=36,
            color=LABEL_COL,
        )
        func_label.to_corner(UR, buff=0.5)
        label_bg = BackgroundRectangle(
            func_label, color=BG, fill_opacity=0.85, buff=0.15
        )

        # ── 4. Axis labels ───────────────────────────────────────
        x_label = MathTex("x", font_size=32, color="#a6adc8")
        x_label.next_to(coord_plane.get_right() + 0.2 * DOWN, DOWN, buff=0.2)
        y_label = MathTex("f(x)", font_size=32, color="#a6adc8")
        y_label.next_to(coord_plane.get_top() + 0.2 * LEFT, UP, buff=0.2)

        # ── Animations ───────────────────────────────────────────
        # Phase 1: Fade in the grid (2.5 s)
        self.play(FadeIn(coord_plane, run_time=2.5, rate_func=smooth))

        # Phase 2: Axis labels appear (1.0 s)
        self.play(
            FadeIn(x_label, shift=UP * 0.2),
            FadeIn(y_label, shift=RIGHT * 0.2),
            run_time=1.0,
        )

        # Phase 3: Draw the graph path left→right (5.0 s)
        self.play(
            Create(glow_graph, run_time=5.0, rate_func=linear),
            Create(func_graph, run_time=5.0, rate_func=linear),
        )

        # Phase 4: Show the formula label (2.0 s)
        self.play(
            FadeIn(label_bg, run_time=0.5),
            Write(func_label, run_time=1.5),
        )

        # Phase 5: Hold on the final image (2.0 s)
        self.wait(2.0)
        # --- Scene 2: Selecting Two Points and the Secant ---
        self.clear()

        # ── Background ──
        self.camera.background_color = "#181825"

        # ── Define curve function f(x) = 0.1x² + 1 ──
        def f(x):
            return 0.1 * x**2 + 1

        # ── Create Axes ──
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 12, 2],
            x_length=9,
            y_length=5.5,
            axis_config={
                "color": "#585b70",
                "stroke_width": 2,
                "include_tip": True,
                "tip_length": 0.2,
            },
            x_axis_config={
                "numbers_to_include": [0, 2, 4, 6, 8, 10],
                "font_size": 24,
                "color": "#6c7086",
            },
            y_axis_config={
                "numbers_to_include": [0, 2, 4, 6, 8, 10, 12],
                "font_size": 24,
                "color": "#6c7086",
            },
        )
        axes.shift(DOWN * 0.3 + LEFT * 0.3)

        # ── Axis Labels ──
        x_label = axes.get_x_axis_label(MathTex("x", color="#cdd6f4", font_size=32))
        y_label = axes.get_y_axis_label(MathTex("f(x)", color="#cdd6f4", font_size=32))

        # ── Plot the curve ──
        curve = axes.plot(
            f,
            x_range=[0.5, 9.5],
            color="#89b4fa",
            stroke_width=3,
        )

        # ── Compute points P and Q ──
        p_x, p_y = 4, f(4)
        q_x, q_y = 7, f(7)

        p_point = axes.c2p(p_x, p_y)
        q_point = axes.c2p(q_x, q_y)

        # ── Create Points ──
        point_p = Dot(p_point, radius=0.1, color="#94e2d5", z_index=5)
        point_q = Dot(q_point, radius=0.1, color="#fab387", z_index=5)

        # ── Point Labels ──
        p_label = MathTex("P", color="#94e2d5", font_size=36).next_to(
            point_p, UL, buff=0.15
        )
        q_label = MathTex("Q", color="#fab387", font_size=36).next_to(
            point_q, UR, buff=0.15
        )

        # ── Coordinate labels for points ──
        p_coords = MathTex(r"(4,\; f(4))", color="#94e2d5", font_size=26).next_to(
            point_p, DL, buff=0.15
        )
        q_coords = MathTex(r"(7,\; f(7))", color="#fab387", font_size=26).next_to(
            point_q, DR, buff=0.15
        )

        # ── Secant Line (dashed) ──
        secant_line = DashedLine(
            p_point,
            q_point,
            color="#fab387",
            dash_length=0.15,
            stroke_width=2.5,
            z_index=3,
        )

        # ── Vertical dashed lines from points to x-axis ──
        p_vertical = DashedLine(
            p_point,
            axes.c2p(p_x, 0),
            color="#94e2d5",
            dash_length=0.1,
            stroke_width=1.5,
            stroke_opacity=0.5,
        )
        q_vertical = DashedLine(
            q_point,
            axes.c2p(q_x, 0),
            color="#fab387",
            dash_length=0.1,
            stroke_width=1.5,
            stroke_opacity=0.5,
        )

        # ── Secant label ──
        mid_point = (p_point + q_point) / 2
        secant_label = Text("secant", color="#f38ba8", font_size=28, slant=ITALIC)
        secant_label.next_to(mid_point, UR, buff=0.2)

        # ── Title text ──
        title = Text("Selecting Two Points & the Secant", color="#cdd6f4", font_size=34)
        title.to_edge(UP, buff=0.35)

        # ═══════════════════════════════════════════
        # ANIMATION SEQUENCE  (total: 10.5s)
        # ═══════════════════════════════════════════

        # 1. Title + Axes + Curve  (2.5s)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.8)
        self.play(Create(curve), run_time=1.1)

        # 2. Point P appears  (2.0s)
        self.play(FadeIn(p_vertical, shift=UP * 0.3), run_time=0.4)
        self.play(
            GrowFromCenter(point_p), FadeIn(p_label, shift=DOWN * 0.2), run_time=0.7
        )
        self.play(FadeIn(p_coords), run_time=0.5)
        self.play(Indicate(point_p, color="#94e2d5", scale_factor=1.8), run_time=0.4)

        # 3. Point Q appears  (2.0s)
        self.play(FadeIn(q_vertical, shift=UP * 0.3), run_time=0.4)
        self.play(
            GrowFromCenter(point_q), FadeIn(q_label, shift=DOWN * 0.2), run_time=0.7
        )
        self.play(FadeIn(q_coords), run_time=0.5)
        self.play(Indicate(point_q, color="#fab387", scale_factor=1.8), run_time=0.4)

        # 4. Secant line draws in  (2.0s)
        self.play(Create(secant_line), run_time=1.0)
        self.play(FadeIn(secant_label, shift=LEFT * 0.2), run_time=0.6)
        self.play(
            ShowPassingFlash(
                secant_line.copy().set_color(WHITE).set_stroke(width=4),
                time_width=0.4,
            ),
            run_time=0.4,
        )

        # 5. Hold  (2.0s)
        self.wait(2.0)
        # --- Scene 3: Calculating the Average Rate of Change ---
        self.clear()

        # ── Color palette (Catppuccin Mocha) ──
        BG = "#181825"
        TEXT_COLOR = "#cdd6f4"
        DX_COLOR = "#fab387"
        DY_COLOR = "#f38ba8"
        ACCENT_BLUE = "#89b4fa"
        ACCENT_GREEN = "#a6e3a1"
        CURVE_COLOR = "#89b4fa"
        SECANT_COLOR = "#a6e3a1"

        self.camera.background_color = BG

        # ── Axes ──
        axes = Axes(
            x_range=[-0.5, 5.5, 1],
            y_range=[-0.5, 4.5, 1],
            x_length=9,
            y_length=5.5,
            axis_config={
                "color": TEXT_COLOR,
                "stroke_width": 2,
                "include_tip": True,
                "tip_length": 0.2,
            },
        ).shift(DOWN * 0.3 + LEFT * 0.3)

        x_label = axes.get_x_axis_label(
            MathTex("x", color=TEXT_COLOR, font_size=36), direction=RIGHT
        )
        y_label = axes.get_y_axis_label(
            MathTex("y", color=TEXT_COLOR, font_size=36), direction=UP
        )

        # ── Curve (concave-up function) ──
        graph = axes.plot(
            lambda x: 0.3 * x**2 + 0.5,
            x_range=[0.2, 5.2],
            color=CURVE_COLOR,
            stroke_width=3,
        )

        # ── Points P and Q ──
        p_x, p_y = 1.0, 0.3 * 1.0**2 + 0.5
        q_x, q_y = 4.0, 0.3 * 4.0**2 + 0.5

        p_point = axes.c2p(p_x, p_y)
        q_point = axes.c2p(q_x, q_y)

        dot_p = Dot(p_point, color=ACCENT_GREEN, radius=0.09, z_index=5)
        dot_q = Dot(q_point, color=ACCENT_GREEN, radius=0.09, z_index=5)

        label_p = MathTex("P", color=ACCENT_GREEN, font_size=32).next_to(
            dot_p, DL, buff=0.15
        )
        label_q = MathTex("Q", color=ACCENT_GREEN, font_size=32).next_to(
            dot_q, UR, buff=0.15
        )

        # ── Secant line ──
        secant = Line(p_point, q_point, color=SECANT_COLOR, stroke_width=2.5, z_index=3)

        # ── Right-angled triangle legs (dashed) ──
        corner_point = axes.c2p(q_x, p_y)

        h_leg = DashedLine(
            p_point,
            corner_point,
            color=DX_COLOR,
            stroke_width=2.5,
            dash_length=0.15,
            z_index=2,
        )
        v_leg = DashedLine(
            corner_point,
            q_point,
            color=DY_COLOR,
            stroke_width=2.5,
            dash_length=0.15,
            z_index=2,
        )

        # Right angle marker (small square at the corner)
        ra = 0.2
        right_angle = VGroup(
            Line(
                corner_point,
                corner_point + RIGHT * ra,
                color=TEXT_COLOR,
                stroke_width=1.5,
            ),
            Line(
                corner_point + RIGHT * ra,
                corner_point + RIGHT * ra + UP * ra,
                color=TEXT_COLOR,
                stroke_width=1.5,
            ),
            Line(
                corner_point + RIGHT * ra + UP * ra,
                corner_point + UP * ra,
                color=TEXT_COLOR,
                stroke_width=1.5,
            ),
        )

        # ── Braces for Δx and Δy ──
        dx_brace = BraceBetweenPoints(
            p_point, corner_point, direction=DOWN, color=DX_COLOR, buff=0.15
        )
        dx_label = dx_brace.get_tex(r"\Delta x")
        dx_label.set_color(DX_COLOR).scale(0.85)

        dy_brace = BraceBetweenPoints(
            corner_point, q_point, direction=RIGHT, color=DY_COLOR, buff=0.15
        )
        dy_label = dy_brace.get_tex(r"\Delta y")
        dy_label.set_color(DY_COLOR).scale(0.85)

        # ── Slope formula (floating label) ──
        slope_label = MathTex(
            r"	ext{slope}",
            r"=",
            r"\frac{\Delta y}{\Delta x}",
            color=TEXT_COLOR,
            font_size=42,
        ).to_corner(UR, buff=0.5)

        slope_label[0].set_color(TEXT_COLOR)
        slope_label[1].set_color(TEXT_COLOR)
        slope_label[2][0:2].set_color(DY_COLOR)  # Δy numerator
        slope_label[2][3:5].set_color(DX_COLOR)  # Δx denominator

        slope_box = SurroundingRectangle(
            slope_label,
            color=ACCENT_BLUE,
            buff=0.18,
            corner_radius=0.1,
            stroke_width=2,
        )

        # ── Animations ──
        # 1. Show axes + labels  (1.5 s)
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=1.5,
        )

        # 2. Draw curve  (1.0 s)
        self.play(Create(graph), run_time=1.0)

        # 3. Show P, Q + labels  (1.5 s)
        self.play(
            FadeIn(dot_p, scale=1.5),
            FadeIn(dot_q, scale=1.5),
            Write(label_p),
            Write(label_q),
            run_time=1.5,
        )

        # 4. Secant line  (1.0 s)
        self.play(Create(secant), run_time=1.0)

        # 5. Right-angle triangle legs  (2.0 s)
        self.play(Create(h_leg), run_time=1.0)
        self.play(Create(v_leg), FadeIn(right_angle), run_time=1.0)

        # 6. Braces + Δ labels  (2.0 s)
        self.play(
            GrowFromCenter(dx_brace),
            FadeIn(dx_label, shift=DOWN * 0.15),
            run_time=1.0,
        )
        self.play(
            GrowFromCenter(dy_brace),
            FadeIn(dy_label, shift=RIGHT * 0.15),
            run_time=1.0,
        )

        # 7. Slope formula + box  (2.0 s)
        self.play(
            FadeIn(slope_label, shift=DOWN * 0.3),
            Create(slope_box),
            run_time=1.5,
        )
        self.play(
            Indicate(slope_label, color=ACCENT_BLUE, scale_factor=1.08),
            run_time=0.5,
        )

        # Total run_time: 1.5+1.0+1.5+1.0+2.0+2.0+1.5+0.5 = 11.0 s ✓
        # --- Scene 4: Approaching the Limit (Point Q -> Point P) ---
        self.clear()

        # ── Color palette ──
        BG = "#181825"
        C_P = "#94e2d5"
        C_Q = "#fab387"
        C_CURVE = "#89b4fa"
        C_LINE = "#a6e3a1"
        C_TXT = "#cdd6f4"
        C_DIM = "#585b70"

        self.camera.background_color = BG

        # ── Function ──
        def f(x):
            return 0.15 * (x - 2) ** 2 + 0.5

        def f_prime(x):
            return 0.3 * (x - 2)

        # ── Axes ──
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 4, 1],
            x_length=10,
            y_length=5.5,
            axis_config={
                "color": C_DIM,
                "stroke_width": 1.5,
                "include_tip": True,
            },
            tips=True,
        ).shift(DOWN * 0.3)

        curve = axes.plot(f, x_range=[0.3, 6.7], color=C_CURVE, stroke_width=2.5)

        # ── Point P (fixed at x=4) ──
        xP, yP = 4.0, f(4.0)
        p_dot = Dot(axes.c2p(xP, yP), radius=0.1, color=C_P, z_index=5)
        p_label = MathTex("P", color=C_P, font_size=36).next_to(
            p_dot, DOWN + LEFT, buff=0.15
        )

        # ── ValueTracker for Q's x ──
        xQ_tracker = ValueTracker(6.0)

        # ── Moving dot Q ──
        q_dot = Dot(axes.c2p(6, f(6)), radius=0.1, color=C_Q, z_index=5)
        q_label = MathTex("Q", color=C_Q, font_size=36)
        q_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(xQ_tracker.get_value(), f(xQ_tracker.get_value()))
            )
        )
        q_label.add_updater(lambda m: m.next_to(q_dot, UP + RIGHT, buff=0.15))

        # ── Helper: screen-space scaling factors ──
        origin_screen = axes.c2p(0, 0)
        x_unit = axes.c2p(1, 0) - origin_screen
        y_unit = axes.c2p(0, 1) - origin_screen

        # ── Secant / Tangent line via always_redraw ──
        def get_secant_line():
            xq = xQ_tracker.get_value()
            p_screen = axes.c2p(xP, yP)
            q_screen = axes.c2p(xq, f(xq))

            dx_math = xq - xP
            dy_math = f(xq) - yP

            if abs(dx_math) < 1e-4:
                slope = f_prime(xP)
                direction = x_unit + slope * y_unit
            else:
                direction = q_screen - p_screen

            norm = np.linalg.norm(direction)
            if norm < 1e-6:
                direction = x_unit
                norm = np.linalg.norm(direction)

            u = direction / norm
            ext = 2.2
            start = p_screen - u * ext
            end = p_screen + u * ext
            return Line(start, end, color=C_LINE, stroke_width=2.5, z_index=2)

        secant_line = always_redraw(get_secant_line)

        # ── Delta-x brace & label ──
        def get_delta_brace():
            xq = xQ_tracker.get_value()
            if abs(xq - xP) < 0.25:
                return VGroup()
            p1 = axes.c2p(xP, yP)
            p2 = axes.c2p(xq, f(xq))
            return BraceBetweenPoints(p1, p2, direction=DOWN, color=C_DIM, buff=0.05)

        delta_brace = always_redraw(get_delta_brace)

        def get_delta_label():
            xq = xQ_tracker.get_value()
            if abs(xq - xP) < 0.3:
                return MathTex("", font_size=1)
            mid = axes.c2p((xP + xq) / 2, min(yP, f(xq)) - 0.55)
            lbl = MathTex(r"\Delta x", color=C_TXT, font_size=30)
            lbl.move_to(mid)
            return lbl

        delta_label = always_redraw(get_delta_label)

        # ── Slope info box (upper-right) ──
        slope_label = (
            MathTex(
                r"	ext{Slope} = \frac{\Delta y}{\Delta x}",
                color=C_LINE,
                font_size=34,
            )
            .to_corner(UR, buff=0.5)
            .shift(DOWN * 0.3)
        )
        slope_bg = BackgroundRectangle(
            slope_label, color=BG, fill_opacity=0.85, buff=0.12
        )

        tangent_label = (
            MathTex(
                r"	ext{Tangent at } P",
                color=C_LINE,
                font_size=34,
            )
            .to_corner(UR, buff=0.5)
            .shift(DOWN * 0.3)
        )
        tangent_bg = BackgroundRectangle(
            tangent_label, color=BG, fill_opacity=0.85, buff=0.12
        )

        # ── Title ──
        title = Text(
            "Approaching the Limit",
            font_size=38,
            color=C_TXT,
            weight=BOLD,
        ).to_edge(UP, buff=0.35)
        title_bg = BackgroundRectangle(title, color=BG, fill_opacity=0.9, buff=0.1)

        # ── Decorative dashed lines from P to axes ──
        p_dash_x = DashedLine(
            axes.c2p(xP, yP),
            axes.c2p(xP, 0),
            color=C_DIM,
            stroke_width=1,
            dash_length=0.1,
        )
        p_dash_y = DashedLine(
            axes.c2p(xP, yP),
            axes.c2p(0, yP),
            color=C_DIM,
            stroke_width=1,
            dash_length=0.1,
        )

        # ════════════════════════════════════════
        #  TIMELINE  (total = 11.5 s)
        # ════════════════════════════════════════

        # Phase 1 – Draw environment  (1.5 s)
        self.play(Create(axes), run_time=0.5)
        self.play(Create(curve), run_time=0.5)
        self.play(
            FadeIn(p_dot, scale=1.3),
            Write(p_label),
            Create(p_dash_x),
            Create(p_dash_y),
            run_time=0.5,
        )

        # Phase 2 – Title  (0.8 s)
        self.play(FadeIn(title_bg), Write(title), run_time=0.8)

        # Phase 3 – Introduce Q + secant + slope label  (1.0 s)
        self.play(FadeIn(q_dot, scale=1.3), Write(q_label), run_time=0.4)
        self.add(secant_line, delta_brace, delta_label)
        self.play(FadeIn(slope_bg), Write(slope_label), run_time=0.6)

        # Phase 4 – Slide Q → P  (6.5 s)
        self.play(
            xQ_tracker.animate.set_value(4.001),
            run_time=6.5,
            rate_func=smooth,
        )

        # Phase 5 – Swap label  (0.7 s)
        self.play(FadeOut(slope_bg), FadeOut(slope_label), run_time=0.3)
        self.play(FadeIn(tangent_bg), Write(tangent_label), run_time=0.4)

        # Phase 6 – Highlight tangent & hold  (1.0 s)
        self.play(
            Indicate(secant_line, color=C_P, scale_factor=1.05),
            run_time=0.5,
        )
        self.wait(0.5)
        # --- Scene 5: The Derivative as Instantaneous Slope ---
        self.clear()

        # ── Color Palette (Catppuccin Mocha inspired) ──
        BG = "#181825"
        CURVE_COL = "#89b4fa"
        TAN_COL = "#a6e3a1"
        POINT_COL = "#fab387"
        LABEL_COL = "#f38ba8"
        TICK_COL = "#94e2d5"
        AXES_COL = "#585b70"
        TEXT_COL = "#cdd6f4"

        self.camera.background_color = BG

        # ── 1. Axes ──
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[-2, 6, 1],
            x_length=9,
            y_length=5.5,
            axis_config={
                "color": AXES_COL,
                "stroke_width": 2,
                "include_tip": True,
                "tip_length": 0.2,
            },
        )
        axes_labels = (
            VGroup(
                axes.get_x_axis_label("x", direction=RIGHT, buff=0.3),
                axes.get_y_axis_label("f(x)", direction=UP, buff=0.3),
            )
            .set_color(TEXT_COL)
            .set_font_size(30)
        )

        self.play(FadeIn(axes), Write(axes_labels), run_time=0.8)

        # ── 2. Smooth curve f(x) ──
        def func(x):
            return 0.05 * (x - 1) * (x - 4) * (x - 7) + 3

        graph = axes.plot(
            func,
            x_range=[0.3, 7.7],
            color=CURVE_COL,
            stroke_width=3,
        )
        func_label = MathTex(r"y = f(x)", font_size=32, color=CURVE_COL)
        func_label.next_to(axes.c2p(7, func(7)), UR, buff=0.2)

        self.play(Create(graph), run_time=1.2)
        self.play(FadeIn(func_label, shift=UP * 0.2), run_time=0.4)

        # ── 3. Point P on the curve ──
        x_p = 4
        y_p = func(x_p)
        point_p = Dot(axes.c2p(x_p, y_p), radius=0.1, color=POINT_COL)
        point_label = MathTex(r"P", font_size=30, color=POINT_COL)
        point_label.next_to(point_p, UR, buff=0.15)

        self.play(FadeIn(point_p, scale=1.5), Write(point_label), run_time=0.6)

        # ── 4. Tangent line at P (glows green, grows) ──
        dx = 0.001
        slope = (func(x_p + dx) - func(x_p - dx)) / (2 * dx)

        t_half = 1.0
        x_start = x_p - t_half
        x_end = x_p + t_half
        y_start = y_p + slope * (x_start - x_p)
        y_end = y_p + slope * (x_end - x_p)

        tangent_short = Line(
            axes.c2p(x_start, y_start),
            axes.c2p(x_end, y_end),
            color=TAN_COL,
            stroke_width=4,
        )

        t_half_full = 3.5
        x_start_f = x_p - t_half_full
        x_end_f = x_p + t_half_full
        y_start_f = y_p + slope * (x_start_f - x_p)
        y_end_f = y_p + slope * (x_end_f - x_p)

        tangent_full = Line(
            axes.c2p(x_start_f, y_start_f),
            axes.c2p(x_end_f, y_end_f),
            color=TAN_COL,
            stroke_width=4,
        )

        tangent_glow = Line(
            axes.c2p(x_start_f, y_start_f),
            axes.c2p(x_end_f, y_end_f),
            color=TAN_COL,
            stroke_width=12,
            stroke_opacity=0.25,
        )

        self.play(Create(tangent_short), run_time=0.6)

        self.play(
            ReplacementTransform(tangent_short, tangent_full),
            FadeIn(tangent_glow),
            run_time=1.2,
        )

        self.play(
            tangent_glow.animate.set_stroke(opacity=0.45),
            rate_func=there_and_back,
            run_time=0.6,
        )

        # ── 5. Slope triangle (rise / run visual) ──
        run_len = 2.0
        rise_len = slope * run_len
        origin_pt = axes.c2p(x_p, y_p)
        run_end = axes.c2p(x_p + run_len, y_p)
        rise_end = axes.c2p(x_p + run_len, y_p + rise_len)

        run_line = Line(origin_pt, run_end, color=TICK_COL, stroke_width=2.5)
        rise_line = Line(run_end, rise_end, color=LABEL_COL, stroke_width=2.5)
        hyp_line = Line(
            origin_pt, rise_end, color=TAN_COL, stroke_width=2, stroke_opacity=0.4
        )

        angle_size = 0.15
        angle_corner = Polygon(
            run_end,
            run_end + UP * angle_size * np.sign(rise_len),
            run_end + UP * angle_size * np.sign(rise_len) + LEFT * angle_size,
            run_end + LEFT * angle_size,
            color=TICK_COL,
            stroke_width=1.5,
        )

        rise_brace = Brace(rise_line, direction=RIGHT, buff=0.1, color=LABEL_COL)
        rise_text = (
            rise_brace.get_tex(r"\Delta y").set_color(LABEL_COL).set_font_size(26)
        )

        run_brace = Brace(run_line, direction=DOWN, buff=0.1, color=TICK_COL)
        run_text = run_brace.get_tex(r"\Delta x").set_color(TICK_COL).set_font_size(26)

        self.play(
            LaggedStart(
                Create(run_line),
                Create(rise_line),
                Create(hyp_line),
                FadeIn(angle_corner),
                FadeIn(rise_brace),
                Write(rise_text),
                FadeIn(run_brace),
                Write(run_text),
                lag_ratio=0.15,
            ),
            run_time=1.5,
        )

        # ── 6. Derivative label ──
        slope_val = round(slope, 2)
        deriv_tex = MathTex(
            r"f'(" + str(x_p) + r") = " + str(slope_val),
            font_size=36,
            color=TAN_COL,
        )
        deriv_tex.next_to(tangent_full, UP, buff=0.35).shift(RIGHT * 0.3)

        deriv_bg = BackgroundRectangle(
            deriv_tex, color=BG, fill_opacity=0.85, buff=0.12
        )

        self.play(FadeIn(deriv_bg), Write(deriv_tex), run_time=0.8)

        # ── 7. Slope fraction at bottom ──
        slope_frac = MathTex(
            r"	ext{slope} = \frac{\Delta y}{\Delta x} = " + str(slope_val),
            font_size=32,
            color=TEXT_COL,
        )
        slope_frac.to_edge(DOWN, buff=0.5)
        slope_bg = BackgroundRectangle(
            slope_frac, color=BG, fill_opacity=0.85, buff=0.12
        )

        self.play(FadeIn(slope_bg), Write(slope_frac), run_time=0.8)

        # ── 8. Final emphasis ──
        self.play(
            Indicate(tangent_full, color=TAN_COL, scale_factor=1.05),
            run_time=0.7,
        )

        self.wait(1.3)
        # --- Scene 6: The Formal Limit Definition ---
        self.clear()
        # --- Color Palette (Catppuccin Mocha) ---
        BG_COLOR = "#181825"
        TEXT_PRIMARY = "#cdd6f4"
        ACCENT_YELLOW = "#f9e2af"
        ACCENT_BLUE = "#89b4fa"
        ACCENT_GREEN = "#a6e3a1"
        ACCENT_PINK = "#f38ba8"
        ACCENT_PEACH = "#fab387"

        self.camera.background_color = BG_COLOR

        # --- 1. Title at the top ---
        title = Text(
            "The Formal Definition",
            font_size=36,
            color=TEXT_PRIMARY,
            font="Sans",
        ).to_edge(UP, buff=0.6)

        # --- 2. A small graph context (showing a curve and a secant/tangent concept) ---
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 5, 1],
            x_length=5.5,
            y_length=3.2,
            axis_config={"color": TEXT_PRIMARY, "stroke_width": 1.5},
            tips=True,
        ).shift(UP * 0.3)

        # Plot a smooth curve
        curve = axes.plot(
            lambda x: 0.4 * x**2 + 0.3,
            x_range=[-0.5, 3.5],
            color=ACCENT_BLUE,
            stroke_width=3,
        )

        # Two points on the curve: x and x+h
        x_val = 1.0
        h_val = 1.2
        point_a = Dot(
            axes.coords_to_point(x_val, 0.4 * x_val**2 + 0.3),
            color=ACCENT_GREEN,
            radius=0.08,
        )
        point_b = Dot(
            axes.coords_to_point(x_val + h_val, 0.4 * (x_val + h_val) ** 2 + 0.3),
            color=ACCENT_PEACH,
            radius=0.08,
        )

        # Labels for x and x+h
        label_x = MathTex("x", font_size=28, color=ACCENT_GREEN).next_to(
            point_a, DOWN, buff=0.15
        )
        label_xh = MathTex("x+h", font_size=28, color=ACCENT_PEACH).next_to(
            point_b, DOWN, buff=0.15
        )

        # Secant line connecting the two points
        secant = Line(
            axes.coords_to_point(x_val, 0.4 * x_val**2 + 0.3),
            axes.coords_to_point(x_val + h_val, 0.4 * (x_val + h_val) ** 2 + 0.3),
            color=ACCENT_PINK,
            stroke_width=2.5,
        )

        # Vertical rise line
        rise_line = DashedLine(
            axes.coords_to_point(x_val + h_val, 0.4 * x_val**2 + 0.3),
            axes.coords_to_point(x_val + h_val, 0.4 * (x_val + h_val) ** 2 + 0.3),
            color=ACCENT_YELLOW,
            stroke_width=2,
            dash_length=0.1,
        )

        # Horizontal run line
        run_line = DashedLine(
            axes.coords_to_point(x_val, 0.4 * x_val**2 + 0.3),
            axes.coords_to_point(x_val + h_val, 0.4 * x_val**2 + 0.3),
            color=ACCENT_YELLOW,
            stroke_width=2,
            dash_length=0.1,
        )

        # Small brace labels for Δy and h
        brace_rise = BraceBetweenPoints(
            axes.coords_to_point(x_val + h_val + 0.15, 0.4 * x_val**2 + 0.3),
            axes.coords_to_point(
                x_val + h_val + 0.15, 0.4 * (x_val + h_val) ** 2 + 0.3
            ),
            direction=RIGHT,
            color=ACCENT_YELLOW,
        )
        brace_run = BraceBetweenPoints(
            axes.coords_to_point(x_val, 0.4 * x_val**2 + 0.3 - 0.2),
            axes.coords_to_point(x_val + h_val, 0.4 * x_val**2 + 0.3 - 0.2),
            direction=DOWN,
            color=ACCENT_YELLOW,
        )
        delta_y_label = brace_rise.get_tex(r"\Delta y").set_color(ACCENT_YELLOW)
        delta_y_label.font_size = 22
        h_label = brace_run.get_tex("h").set_color(ACCENT_YELLOW)
        h_label.font_size = 22

        graph_group = VGroup(
            axes,
            curve,
            point_a,
            point_b,
            label_x,
            label_xh,
            secant,
            rise_line,
            run_line,
            brace_rise,
            brace_run,
            delta_y_label,
            h_label,
        )

        # --- 3. The limit formula ---
        limit_formula = MathTex(
            r"f'(x) = \lim_{h 	o 0} \frac{f(x+h) - f(x)}{h}",
            font_size=48,
            color=TEXT_PRIMARY,
        ).to_edge(DOWN, buff=0.9)

        # Highlight box around the formula
        highlight_box = SurroundingRectangle(
            limit_formula,
            color=ACCENT_YELLOW,
            buff=0.2,
            corner_radius=0.1,
            stroke_width=2.5,
        )

        # --- 4. Annotation label near the fraction ---
        annotation = (
            Text(
                "Difference Quotient",
                font_size=22,
                color=ACCENT_PEACH,
                font="Sans",
            )
            .next_to(highlight_box, RIGHT, buff=0.3)
            .shift(UP * 0.1)
        )

        # Small arrow from annotation to the formula highlight box
        annot_arrow = Arrow(
            annotation.get_left(),
            highlight_box.get_right() + UP * 0.05,
            color=ACCENT_PEACH,
            stroke_width=2,
            buff=0.08,
            tip_length=0.15,
        )

        # --- 5. Animations ---
        # (a) Title fades in — 1.0s
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.0)

        # (b) Build the graph — 1.0s + 1.0s + 0.8s = 2.8s
        self.play(Create(axes), run_time=1.0)
        self.play(Create(curve), run_time=1.0)
        self.play(
            FadeIn(point_a, scale=1.5),
            FadeIn(point_b, scale=1.5),
            Write(label_x),
            Write(label_xh),
            run_time=0.8,
        )

        # (c) Draw secant and rise/run — 0.8s + 0.7s + 0.8s = 2.3s
        self.play(Create(secant), run_time=0.8)
        self.play(
            Create(rise_line),
            Create(run_line),
            run_time=0.7,
        )
        self.play(
            GrowFromCenter(brace_rise),
            GrowFromCenter(brace_run),
            Write(delta_y_label),
            Write(h_label),
            run_time=0.8,
        )

        # (d) The limit formula typesets — 2.0s
        self.play(Write(limit_formula), run_time=2.0)

        # (e) Highlight box — 0.8s
        self.play(Create(highlight_box), run_time=0.8)

        # (f) Annotation + arrow — 1.0s
        self.play(
            FadeIn(annotation, shift=LEFT * 0.2),
            Create(annot_arrow),
            run_time=1.0,
        )

        # (g) Indicate formula — 1.1s
        self.play(
            Indicate(limit_formula, color=ACCENT_YELLOW, scale_factor=1.05),
            run_time=1.1,
        )
        # --- Scene 7: The Derivative Function ---
        self.clear()

        # --- Color Palette ---
        BG_COLOR = "#181825"
        BLUE = "#89b4fa"
        AMBER = "#fab387"
        TEXT_COLOR = "#cdd6f4"
        MUTED_COLOR = "#585b70"

        # --- Background ---
        self.camera.background_color = BG_COLOR

        # --- Axes Setup ---
        axes = Axes(
            x_range=[-1, 12, 2],
            y_range=[-3, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={
                "color": MUTED_COLOR,
                "include_tip": True,
                "tip_length": 0.2,
                "stroke_width": 2,
            },
            tips=True,
        )
        axes_labels = axes.get_axis_labels(
            MathTex("x").set_color(TEXT_COLOR), MathTex("y").set_color(TEXT_COLOR)
        )

        # --- Original Function Graph (f(x) = 0.1(x-2)^2 - 1) ---
        original_graph = axes.plot(
            lambda x: 0.1 * (x - 2) ** 2 - 1,
            x_range=[-1, 12],
            color=BLUE,
            stroke_width=2,
            stroke_opacity=0.6,
        )
        original_label = MathTex("f(x)").set_color(BLUE).scale(0.8)
        original_label.next_to(axes.i2gp(10, original_graph), RIGHT, buff=0.3)

        # --- Derivative Function Graph (f'(x) = 0.2x - 2) ---
        derivative_graph = axes.plot(
            lambda x: 0.2 * x - 2,
            x_range=[-1, 12],
            color=AMBER,
            stroke_width=3,
        )
        derivative_label = MathTex("f'(x)").set_color(AMBER).scale(0.8)
        derivative_label.next_to(axes.i2gp(11, derivative_graph), RIGHT, buff=0.3)

        # --- Title ---
        title = Text(
            "The Derivative Function",
            font_size=36,
            color=TEXT_COLOR,
        ).to_edge(UP, buff=0.5)

        # --- Animation Timeline (Total: 11.5s) ---
        # Phase 1: Setup axes and title (2s)
        self.play(
            FadeIn(axes, shift=UP * 0.3),
            FadeIn(axes_labels),
            Write(title),
            run_time=2,
        )

        # Phase 2: Show original function (2.5s)
        self.play(
            Create(original_graph),
            FadeIn(original_label, shift=LEFT * 0.2),
            run_time=2.5,
        )
        self.wait(0.5)  # 0.5s pause

        # Phase 3: Introduce derivative function (4s)
        self.play(
            Create(derivative_graph),
            FadeIn(derivative_label, shift=LEFT * 0.2),
            run_time=4,
        )

        # Phase 4: Final emphasis (2.5s total)
        self.play(
            Circumscribe(derivative_graph, color=AMBER, time_width=1.5),
            run_time=1.5,
        )
        self.wait(1.0)

        # Total: 2 + 2.5 + 0.5 + 4 + 1.5 + 1.0 = 11.5s ✓
        # --- Scene 8: Geometric Interpretation ---
        self.clear()

        # ── Background ──
        self.camera.background_color = "#181825"

        # ── Color palette (Catppuccin Mocha + workflow palette) ──
        C_BLUE = "#89b4fa"
        C_PEACH = "#fab387"
        C_PINK = "#f38ba8"
        C_GREEN = "#a6e3a1"
        C_TEAL = "#94e2d5"
        C_YELLOW = "#f9e2af"
        C_SUBTLE = "#585b70"
        C_TEXT = "#cdd6f4"

        # ── Define f(x) = 0.5x³ − 1.5x + 1  and  f'(x) = 1.5x² − 1.5 ──
        def f_func(x):
            return 0.5 * x**3 - 1.5 * x + 1

        def df_func(x):
            return 1.5 * x**2 - 1.5

        # ═══════════════════════════════
        #  AXES  (top: f,  bottom: f')
        # ═══════════════════════════════
        ax_f = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 4, 1],
            x_length=5.5,
            y_length=2.8,
            axis_config={
                "color": C_SUBTLE,
                "stroke_width": 1.5,
                "include_numbers": False,
            },
            tips=True,
        ).shift(UP * 1.7 + LEFT * 3.0)

        ax_df = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 4, 1],
            x_length=5.5,
            y_length=2.8,
            axis_config={
                "color": C_SUBTLE,
                "stroke_width": 1.5,
                "include_numbers": False,
            },
            tips=True,
        ).shift(DOWN * 1.7 + LEFT * 3.0)

        # ── Axis labels ──
        label_f = (
            MathTex(r"f(x)", font_size=42, color=C_BLUE)
            .next_to(ax_f, UP, buff=0.15)
            .shift(LEFT * 0.5)
        )
        label_df = (
            MathTex(r"f'(x)", font_size=42, color=C_PEACH)
            .next_to(ax_df, UP, buff=0.15)
            .shift(LEFT * 0.5)
        )

        # ── Graph curves ──
        graph_f = ax_f.plot(f_func, x_range=[-2.8, 2.8], color=C_BLUE, stroke_width=2.5)
        graph_df = ax_df.plot(
            df_func, x_range=[-2.8, 2.8], color=C_PEACH, stroke_width=2.5
        )

        # ── Zero-line on derivative axes ──
        zero_line = ax_df.plot(
            lambda x: 0,
            x_range=[-2.8, 2.8],
            color=C_SUBTLE,
            stroke_width=1,
            stroke_opacity=0.5,
        )

        # ═══════════════════════════════
        #  DYNAMIC ELEMENTS  (ValueTracker)
        # ═══════════════════════════════
        tracker = ValueTracker(-2.0)

        # Dot on x-axis (top axes)
        dot_x_axis = always_redraw(
            lambda: Dot(
                ax_f.c2p(tracker.get_value(), 0),
                color=C_YELLOW,
                radius=0.07,
                z_index=5,
            )
        )

        # Dot on f(x) curve
        dot_fx = always_redraw(
            lambda: Dot(
                ax_f.c2p(tracker.get_value(), f_func(tracker.get_value())),
                color=C_GREEN,
                radius=0.1,
                z_index=5,
            )
        )

        # Tangent line on f(x)
        tangent_line = always_redraw(
            lambda: ax_f.plot(
                lambda x: (
                    f_func(tracker.get_value())
                    + df_func(tracker.get_value()) * (x - tracker.get_value())
                ),
                x_range=[
                    max(-2.8, tracker.get_value() - 0.7),
                    min(2.8, tracker.get_value() + 0.7),
                ],
                color=C_TEAL,
                stroke_width=2.5,
            )
        )

        # Vertical dashed link connecting both plots
        vertical_link = always_redraw(
            lambda: DashedLine(
                ax_f.c2p(tracker.get_value(), ax_f.y_range[0]),
                ax_df.c2p(tracker.get_value(), ax_df.y_range[1]),
                color=C_SUBTLE,
                stroke_width=1.2,
                dash_length=0.07,
            )
        )

        # Dot on f'(x) curve
        dot_dfx = always_redraw(
            lambda: Dot(
                ax_df.c2p(tracker.get_value(), df_func(tracker.get_value())),
                color=C_PINK,
                radius=0.1,
                z_index=5,
            )
        )

        # Horizontal dashed: y-axis → dot on f'(x)  (shows derivative value)
        h_link_df = always_redraw(
            lambda: DashedLine(
                ax_df.c2p(0, df_func(tracker.get_value())),
                ax_df.c2p(tracker.get_value(), df_func(tracker.get_value())),
                color=C_SUBTLE,
                stroke_width=1.0,
                dash_length=0.06,
            )
        )

        # Slope value label near tangent
        slope_label = always_redraw(
            lambda: MathTex(
                f"\	ext{{slope}} = {df_func(tracker.get_value()):.2f}",
                font_size=28,
                color=C_TEAL,
            ).next_to(
                ax_f.c2p(tracker.get_value(), f_func(tracker.get_value())),
                UR,
                buff=0.12,
            )
        )

        # ═══════════════════════════════
        #  NARRATION TEXT  (right side)
        # ═══════════════════════════════
        narr1 = Text("Where f(x) is steep…", font_size=22, color=C_TEXT)
        narr2 = Text("…f′(x) is high.", font_size=22, color=C_PEACH)
        narr3 = Text("Where f(x) is flat…", font_size=22, color=C_TEXT)
        narr4 = Text("…f′(x) crosses zero.", font_size=22, color=C_PINK)

        narr_top = VGroup(narr1, narr2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        narr_bot = VGroup(narr3, narr4).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        narr_group = VGroup(narr_top, narr_bot).arrange(DOWN, buff=0.4)
        narr_group.move_to(RIGHT * 3.8)

        # Decorative boxes around text groups
        box_top = SurroundingRectangle(
            narr_top, color=C_TEAL, buff=0.12, stroke_width=1.2, corner_radius=0.08
        )
        box_bot = SurroundingRectangle(
            narr_bot, color=C_PINK, buff=0.12, stroke_width=1.2, corner_radius=0.08
        )

        # Small accent dots before each line
        d1 = Dot(color=C_TEAL, radius=0.04).next_to(narr1, LEFT, buff=0.08)
        d2 = Dot(color=C_PEACH, radius=0.04).next_to(narr2, LEFT, buff=0.08)
        d3 = Dot(color=C_PINK, radius=0.04).next_to(narr3, LEFT, buff=0.08)
        d4 = Dot(color=C_PINK, radius=0.04).next_to(narr4, LEFT, buff=0.08)

        # ══════════════════════════════════════════════
        #  ANIMATION SEQUENCE  — total 12 s
        # ══════════════════════════════════════════════

        # ── 0.0 – 1.8 s: Draw axes, labels, graphs ──
        self.play(
            LaggedStart(
                FadeIn(ax_f, shift=DOWN * 0.2),
                FadeIn(ax_df, shift=DOWN * 0.2),
                FadeIn(label_f),
                FadeIn(label_df),
                lag_ratio=0.15,
            ),
            run_time=0.8,
        )
        self.play(
            Create(graph_f, run_time=0.8),
            Create(graph_df, run_time=0.8),
        )
        self.play(Create(zero_line, run_time=0.2))
        # t = 1.8

        # ── 1.8 – 2.8 s: Reveal dynamic tracker elements ──
        self.play(
            FadeIn(dot_x_axis, scale=1.5),
            FadeIn(dot_fx, scale=1.5),
            FadeIn(tangent_line),
            FadeIn(vertical_link),
            FadeIn(dot_dfx, scale=1.5),
            FadeIn(h_link_df),
            FadeIn(slope_label),
            run_time=0.8,
        )
        self.wait(0.2)
        # t = 2.8

        # ── 2.8 – 5.0 s: Sweep to steep region (x ≈ 2) ──
        self.play(tracker.animate.set_value(2.0), run_time=2.2, rate_func=smooth)
        # t = 5.0

        # ── 5.0 – 5.8 s: Show "steep → high" narration ──
        self.play(
            FadeIn(narr1, shift=LEFT * 0.2, run_time=0.3),
            FadeIn(d1, run_time=0.2),
        )
        self.play(
            FadeIn(narr2, shift=LEFT * 0.2, run_time=0.3),
            FadeIn(d2, run_time=0.2),
        )
        self.play(FadeIn(box_top, run_time=0.2))
        # t = 5.8

        # ── 5.8 – 6.2 s: Brief pulse on steep tangent ──
        self.play(
            Indicate(tangent_line, color=C_TEAL, scale_factor=1.15, run_time=0.2),
            Indicate(dot_dfx, color=C_PINK, scale_factor=1.4, run_time=0.2),
        )
        # t = 6.2

        # ── 6.2 – 8.4 s: Sweep to flat region (x ≈ −1 where f' ≈ 0) ──
        self.play(tracker.animate.set_value(-1.0), run_time=2.2, rate_func=smooth)
        # t = 8.4

        # ── 8.4 – 9.4 s: Show "flat → zero" narration ──
        self.play(
            FadeIn(narr3, shift=LEFT * 0.2, run_time=0.3),
            FadeIn(d3, run_time=0.2),
        )
        self.play(
            FadeIn(narr4, shift=LEFT * 0.2, run_time=0.3),
            FadeIn(d4, run_time=0.2),
        )
        self.play(FadeIn(box_bot, run_time=0.2))
        # t = 9.4

        # ── 9.4 – 9.8 s: Pulse on flat region ──
        self.play(
            Indicate(tangent_line, color=C_YELLOW, scale_factor=1.1, run_time=0.2),
            Indicate(dot_dfx, color=C_YELLOW, scale_factor=1.3, run_time=0.2),
        )
        # t = 9.8

        # ── 9.8 – 11.2 s: Grand tour sweep ──
        self.play(tracker.animate.set_value(2.5), run_time=0.7, rate_func=smooth)
        self.play(tracker.animate.set_value(-2.5), run_time=0.7, rate_func=smooth)
        # t = 11.2

        # ── 11.2 – 11.6 s: Settle to a calm middle position ──
        self.play(tracker.animate.set_value(0.5), run_time=0.4, rate_func=smooth)
        # t = 11.6

        # ── 11.6 – 12.0 s: Final gentle hold ──
        self.wait(0.4)
        # t = 12.0
