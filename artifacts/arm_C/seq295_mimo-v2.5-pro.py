import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: The Vector ---
        # Background color
        self.camera.background_color = "#181825"

        # 1. NumberPlane grid
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={
                "stroke_color": "#313244",
                "stroke_opacity": 0.4,
                "stroke_width": 1,
            },
            axis_config={
                "stroke_color": "#45475a",
                "stroke_width": 1.5,
            },
            faded_line_style={
                "stroke_color": "#313244",
                "stroke_opacity": 0.2,
            },
        )

        # 2. Vector arrow from origin to (2, 1)
        vec_arrow = Arrow(
            start=grid.c2p(0, 0),
            end=grid.c2p(2, 1),
            buff=0,
            color="#89b4fa",
            stroke_width=4,
            tip_length=0.25,
        )

        # 3. Dot at arrowhead
        vec_tip = Dot(
            point=grid.c2p(2, 1),
            radius=0.08,
            color="#89b4fa",
        )

        # 4. Label for the vector
        vec_label = MathTex(
            r"\vec{v}",
            color="#89b4fa",
            font_size=36,
        ).next_to(vec_arrow.get_center(), UP + LEFT, buff=0.15)

        # 5. Origin dot
        origin_dot = Dot(
            point=grid.c2p(0, 0),
            radius=0.06,
            color="#a6adc8",
        )

        # 6. Coordinate label at tip
        coord_label = MathTex(
            r"(2,\,1)",
            color="#cdd6f4",
            font_size=28,
        ).next_to(vec_tip, UR, buff=0.12)

        # --- Animations ---
        # Phase 1: Fade in the grid (0.8s)
        self.play(FadeIn(grid), run_time=0.8)

        # Phase 2: Grow origin dot (0.3s)
        self.play(GrowFromCenter(origin_dot), run_time=0.3)

        # Phase 3: Draw the vector arrow (1.2s)
        self.play(Create(vec_arrow), run_time=1.2)

        # Phase 4: Dot appears at tip + label writes in (0.7s)
        self.play(
            GrowFromCenter(vec_tip),
            Write(vec_label),
            run_time=0.7,
        )

        # Phase 5: Coordinate label fades in (0.5s)
        self.play(FadeIn(coord_label, shift=DOWN * 0.2), run_time=0.5)

        # Phase 6: Hold the scene (1.5s)
        self.wait(1.5)

        # Total: 0.8 + 0.3 + 1.2 + 0.7 + 0.5 + 1.5 = 5.0s ✓
        # --- Scene 2: The Transformation ---
        # Color palette (Catppuccin Mocha)
        BG = "#181825"
        GRID_COLOR = "#313244"
        ACCENT_BLUE = "#89b4fa"
        ACCENT_PEACH = "#fab387"
        ACCENT_PINK = "#f38ba8"
        ACCENT_GREEN = "#a6e3a1"
        TEXT_COLOR = "#cdd6f4"

        self.camera.background_color = BG

        # 1. Create the NumberPlane grid
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={
                "stroke_color": GRID_COLOR,
                "stroke_width": 1.5,
                "stroke_opacity": 0.6,
            },
            axis_config={
                "stroke_color": GRID_COLOR,
                "stroke_width": 2,
            },
        )

        # 2. Create the blue vector (arrow)
        vec = Arrow(
            start=grid.c2p(0, 0),
            end=grid.c2p(2, 1),
            buff=0,
            color=ACCENT_BLUE,
            stroke_width=4,
            tip_length=0.2,
        )
        vec_label = MathTex(r"\vec{v}", color=ACCENT_BLUE, font_size=32).next_to(
            vec.get_end(), UR, buff=0.15
        )

        # 3. Create the matrix display in the top-right
        matrix_tex = MathTex(
            r"A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}",
            color=ACCENT_PEACH,
            font_size=36,
        ).to_corner(UR, buff=0.5)
        matrix_box = SurroundingRectangle(
            matrix_tex,
            color=ACCENT_PEACH,
            buff=0.15,
            stroke_width=1.5,
            corner_radius=0.1,
        )

        # 4. Narration text at the bottom
        narration = Text(
            "A linear transformation changes the space,\nscaling or rotating vectors.",
            color=TEXT_COLOR,
            font_size=24,
        ).to_edge(DOWN, buff=0.4)

        # === ANIMATIONS ===

        # Phase 1: Show the grid and vector
        self.play(Create(grid), run_time=0.8)
        self.play(GrowArrow(vec), FadeIn(vec_label, shift=UP * 0.2), run_time=0.5)

        # Phase 2: Show the matrix and narration
        self.play(
            FadeIn(matrix_box),
            Write(matrix_tex),
            FadeIn(narration, shift=UP * 0.2),
            run_time=0.6,
        )
        self.wait(0.4)

        # Phase 3: Apply the matrix transformation [[2,1],[1,2]]
        new_grid = grid.copy()
        new_grid.apply_matrix([[2, 1], [1, 2]])

        # Transformed vector: [[2,1],[1,2]] @ [2,1] = [5, 4]
        new_vec = Arrow(
            start=grid.c2p(0, 0),
            end=grid.c2p(5, 4),
            buff=0,
            color=ACCENT_BLUE,
            stroke_width=4,
            tip_length=0.2,
        )
        new_vec_label = MathTex(r"A\vec{v}", color=ACCENT_PINK, font_size=32).next_to(
            new_vec.get_end(), UR, buff=0.15
        )

        self.play(
            Transform(grid, new_grid),
            Transform(vec, new_vec),
            ReplacementTransform(vec_label, new_vec_label),
            run_time=2.2,
        )

        # Phase 4: Highlight the result
        self.play(
            Indicate(new_vec_label, color=ACCENT_GREEN, scale_factor=1.3), run_time=0.5
        )
        # --- Scene 3: The Anchor ---
        # Background color
        self.camera.background_color = "#181825"

        # Color palette
        BG_GRID = "#313244"
        ACCENT_GREEN = "#a6e3a1"
        ACCENT_BLUE = "#89b4fa"
        ACCENT_PEACH = "#fab387"
        ACCENT_PINK = "#f38ba8"
        ACCENT_TEAL = "#94e2d5"
        GUIDE_LINE_COLOR = "#45475a"
        SUBTLE_TEXT = "#6c7086"

        # --- 1. OBJECTS ---

        # NumberPlane (stable grid)
        stable_grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={
                "stroke_color": BG_GRID,
                "stroke_width": 1.5,
                "stroke_opacity": 0.6,
            },
            axis_config={
                "stroke_color": "#585b70",
                "stroke_width": 2,
            },
        )

        # Dashed guide line along y=x
        guide_line = DashedLine(
            start=stable_grid.c2p(-2.5, -2.5),
            end=stable_grid.c2p(2.5, 2.5),
            color=GUIDE_LINE_COLOR,
            stroke_width=2,
            dash_length=0.15,
        )

        # Eigenvector arrow along y=x direction
        eigenvector = Arrow(
            start=stable_grid.c2p(0, 0),
            end=stable_grid.c2p(1.2, 1.2),
            color=ACCENT_GREEN,
            buff=0,
            stroke_width=5,
            tip_length=0.25,
        )

        # Label for the eigenvector
        eig_label = MathTex(r"\vec{v}", color=ACCENT_GREEN, font_size=42)
        eig_label.next_to(eigenvector.get_end(), UR, buff=0.15)

        # Title text
        title_text = Text("Eigenvector", font_size=32, color=ACCENT_GREEN, weight=BOLD)
        title_text.to_corner(UL, buff=0.5)

        # Eigenvector property text
        prop_text = Text(
            "Direction preserved after transformation",
            font_size=20,
            color=SUBTLE_TEXT,
        )
        prop_text.next_to(title_text, DOWN, aligned_edge=LEFT, buff=0.2)

        # Formula
        formula = MathTex(
            r"A\vec{v}",
            r"=",
            r"\lambda",
            r"\vec{v}",
            font_size=38,
        )
        formula[0].set_color(ACCENT_BLUE)
        formula[1].set_color(WHITE)
        formula[2].set_color(ACCENT_PEACH)
        formula[3].set_color(ACCENT_GREEN)
        formula.to_corner(UR, buff=0.5)

        # Lambda (eigenvalue) label
        lam_label = MathTex(
            r"\lambda = 4",
            color=ACCENT_PEACH,
            font_size=34,
        )
        lam_label.next_to(formula, DOWN, aligned_edge=RIGHT, buff=0.25)

        # --- 2. ANIMATIONS ---
        # Total duration target: ~7.0 seconds

        # Phase 1: Show grid and guide line (0.0s - 1.2s)
        self.play(FadeIn(stable_grid), run_time=0.8)
        self.play(Create(guide_line), run_time=0.4)

        # Phase 2: Show eigenvector with labels (1.2s - 2.6s)
        self.play(GrowFromCenter(eigenvector), run_time=0.8)
        self.play(
            FadeIn(eig_label, shift=UR * 0.1),
            FadeIn(title_text),
            FadeIn(prop_text),
            run_time=0.6,
        )

        # Phase 3: Show formula (2.6s - 3.4s)
        self.play(Write(formula), run_time=0.8)

        # Phase 4: Apply matrix transformation — grid distorts (3.4s - 5.4s)
        # Matrix [[3,1],[1,3]]: eigenvalues 4 (eigenvector (1,1)) and 2 (eigenvector (1,-1))
        transform_matrix = np.array(
            [
                [3, 1],
                [1, 3],
            ]
        )

        self.play(
            stable_grid.animate.apply_matrix(transform_matrix),
            run_time=2.0,
            rate_func=smooth,
        )

        # Phase 5: Eigenvector transforms — stays on the same line (5.4s - 6.4s)
        self.play(
            eigenvector.animate.apply_matrix(transform_matrix),
            FadeOut(eig_label),
            run_time=0.6,
        )

        # Show scaled label
        scaled_label = MathTex(r"4\vec{v}", color=ACCENT_PEACH, font_size=42)
        scaled_label.next_to(eigenvector.get_end(), UR, buff=0.15)

        self.play(
            FadeIn(scaled_label, shift=UR * 0.1),
            FadeIn(lam_label),
            run_time=0.4,
        )

        # Phase 6: Emphasize the guide line still contains the vector (6.4s - 7.0s)
        self.play(
            guide_line.animate.set_stroke(ACCENT_GREEN, width=3, opacity=0.9),
            run_time=0.3,
        )
        self.play(
            guide_line.animate.set_stroke(GUIDE_LINE_COLOR, width=2, opacity=1.0),
            run_time=0.3,
        )

        # Final pause (must be positive)
        self.wait(0.5)
        # --- Scene 4: The Scalar ---
        # Color palette from workflow
        BG = "#181825"
        GREEN_VEC = "#a6e3a1"
        ORANGE_LABEL = "#fab387"

        self.camera.background_color = BG

        # Small origin dot
        origin_dot = Dot(ORIGIN, radius=0.06, color=WHITE)

        # The eigenvector arrow (green) — the full scaled vector
        scaled_vec = Arrow(
            start=ORIGIN,
            end=3 * RIGHT + 3 * UP,
            color=GREEN_VEC,
            stroke_width=3.5,
            buff=0,
        )

        # Original shorter vector (unit eigenvector) to show the scaling
        original_vec = Arrow(
            start=ORIGIN,
            end=1 * RIGHT + 1 * UP,
            color=GREEN_VEC,
            stroke_width=2.5,
            buff=0,
        )

        # Dashed eigenline showing direction extends beyond
        eigenline = DashedLine(
            start=-0.5 * RIGHT - 0.5 * UP,
            end=4.5 * RIGHT + 4.5 * UP,
            color=GREEN_VEC,
            stroke_width=1.2,
            dash_length=0.15,
        )
        eigenline.set_opacity(0.3)

        # Dots at key positions
        unit_dot = Dot(1 * RIGHT + 1 * UP, radius=0.05, color=GREEN_VEC)
        scaled_dot = Dot(3 * RIGHT + 3 * UP, radius=0.05, color=GREEN_VEC)

        # Brace along the FULL scaled vector (from origin to tip)
        scale_brace = Brace(scaled_vec, direction=UP + RIGHT, buff=0.2)
        scale_brace.set_color(ORANGE_LABEL)

        # Lambda label from brace
        lambda_label = scale_brace.get_tex(r"\lambda = 3")
        lambda_label.set_color(ORANGE_LABEL)
        lambda_label.scale(1.1)

        # Title text
        title = Text("The Scalar", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.4)
        title.set_opacity(0.7)

        # --- Animation Sequence ---

        # Phase 1 (0.0 - 0.8): Show title and eigenline
        self.play(
            FadeIn(title, shift=DOWN * 0.3),
            Create(eigenline),
            FadeIn(origin_dot),
            run_time=0.8,
        )

        # Phase 2 (0.8 - 1.5): Grow the original eigenvector
        self.play(
            GrowFromCenter(original_vec),
            FadeIn(unit_dot),
            run_time=0.7,
        )

        # Phase 3 (1.5 - 3.2): Elongate the vector by factor 3
        self.play(
            Transform(original_vec, scaled_vec),
            FadeIn(scaled_dot),
            run_time=1.7,
        )

        # Phase 4 (3.2 - 4.0): Show the brace measuring the stretch
        self.play(
            GrowFromCenter(scale_brace),
            run_time=0.8,
        )

        # Phase 5 (4.0 - 4.8): Show the lambda = 3 label
        self.play(
            Write(lambda_label),
            run_time=0.8,
        )

        # Phase 6 (4.8 - 5.4): Highlight the label with a pulse
        self.play(
            Indicate(lambda_label, color=ORANGE_LABEL, scale_factor=1.25),
            run_time=0.6,
        )

        # Phase 7 (5.4 - 6.0): Hold on screen
        self.wait(0.6)
        # --- Scene 5: The Definition ---
        # Color palette from Catppuccin Mocha
        BG_COLOR = "#181825"
        TEXT_COLOR = "#cdd6f4"
        MATRIX_COLOR = "#89b4fa"  # Blue - matches matrix A
        EIGENVECTOR_COLOR = "#a6e3a1"  # Green - matches eigenvector v
        EIGENVALUE_COLOR = "#fab387"  # Orange - matches eigenvalue lambda
        ACCENT_COLOR = "#f38ba8"  # Pink accent

        # 1. Background rectangle for the equation
        equation_bg = Rectangle(
            width=8,
            height=3,
            fill_color=BG_COLOR,
            fill_opacity=0.85,
            stroke_color=TEXT_COLOR,
            stroke_width=1.5,
            stroke_opacity=0.3,
        ).round_corners(radius=0.3)

        # 2. Main equation: A v = lambda v
        eq_main = MathTex(
            r"A",
            r"\vec{v}",
            r"=",
            r"\lambda",
            r"\vec{v}",
            font_size=72,
        )
        # Color each part: A=blue, v=green, lambda=orange
        eq_main[0].set_color(MATRIX_COLOR)  # A
        eq_main[1].set_color(EIGENVECTOR_COLOR)  # v (left)
        eq_main[2].set_color(TEXT_COLOR)  # =
        eq_main[3].set_color(EIGENVALUE_COLOR)  # lambda
        eq_main[4].set_color(EIGENVECTOR_COLOR)  # v (right)

        # 3. Subtle underline for emphasis
        underline_a = Underline(
            eq_main[0], color=MATRIX_COLOR, buff=0.15, stroke_width=3
        )
        underline_v = Underline(
            eq_main[1], color=EIGENVECTOR_COLOR, buff=0.15, stroke_width=3
        )
        underline_lambda = Underline(
            eq_main[3], color=EIGENVALUE_COLOR, buff=0.15, stroke_width=3
        )

        # ---- Animations ----

        # Step 1: Fade in background panel (0.8s)
        self.play(FadeIn(equation_bg, scale=0.95), run_time=0.8)

        # Step 2: Write the equation with a satisfying reveal (2.0s)
        self.play(Write(eq_main), run_time=2.0)

        # Step 3: Briefly highlight each colored component (0.5s each = 1.5s)
        self.play(
            Indicate(eq_main[0], color=MATRIX_COLOR, scale_factor=1.15),
            Create(underline_a),
            run_time=0.5,
        )
        self.play(
            Indicate(eq_main[1], color=EIGENVECTOR_COLOR, scale_factor=1.15),
            FadeOut(underline_a),
            Create(underline_v),
            run_time=0.5,
        )
        self.play(
            Indicate(eq_main[3], color=EIGENVALUE_COLOR, scale_factor=1.15),
            FadeOut(underline_v),
            Create(underline_lambda),
            run_time=0.5,
        )

        # Step 4: Final hold (0.2s)
        self.play(FadeOut(underline_lambda), run_time=0.2)

        # Total: 0.8 + 2.0 + 0.5 + 0.5 + 0.5 + 0.2 + 0.5 = 5.0s
        self.wait(0.5)
        # --- Scene 6: Geometric Interpretation ---
        # === Color palette ===
        bg_color = "#181825"
        grid_color = "#313244"
        chaos_color = "#f38ba8"
        eigen_color = "#94e2d5"
        text_color = "#cdd6f4"
        accent_color = "#89b4fa"

        # === 1. Background grid plane ===
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": grid_color,
                "stroke_width": 1,
                "stroke_opacity": 0.6,
            },
            axis_config={"stroke_color": grid_color, "stroke_width": 1.5},
        )

        # === 2. Chaos arrows (random vectors scattered across the plane) ===
        np.random.seed(42)
        chaos_arrows = VGroup()
        for _ in range(12):
            x = np.random.uniform(-3, 3)
            y = np.random.uniform(-2.5, 2.5)
            angle = np.random.uniform(0, TAU)
            dx = 0.7 * np.cos(angle)
            dy = 0.7 * np.sin(angle)
            arrow = Arrow(
                start=np.array([x, y, 0]),
                end=np.array([x + dx, y + dy, 0]),
                buff=0,
                color=chaos_color,
                stroke_width=2.5,
                tip_length=0.15,
                max_tip_length_to_length_ratio=0.35,
            )
            chaos_arrows.add(arrow)

        # === 3. Eigenvector lines (stable axes through the origin) ===
        eigen_line_1 = Line(
            start=[-4, -4, 0],
            end=[4, 4, 0],
            color=eigen_color,
            stroke_width=4,
        )
        eigen_line_2 = Line(
            start=[-4, 2, 0],
            end=[4, -2, 0],
            color=eigen_color,
            stroke_width=4,
        )

        # Labels for eigenvectors
        eigen_label_1 = MathTex(r"\vec{e}_1", color=eigen_color, font_size=32)
        eigen_label_1.next_to(eigen_line_1.get_end(), UR, buff=0.15)
        eigen_label_2 = MathTex(r"\vec{e}_2", color=eigen_color, font_size=32)
        eigen_label_2.next_to(eigen_line_2.get_end(), DR, buff=0.15)

        # Title text
        title = Text("Geometric Interpretation", font_size=28, color=text_color)
        title.to_edge(UP, buff=0.35)

        subtitle = Text(
            "Eigenvectors: axes that remain stable under transformation",
            font_size=20,
            color=accent_color,
        )
        subtitle.next_to(title, DOWN, buff=0.15)

        # === ANIMATION SEQUENCE ===
        # Total duration: 6.5 seconds

        # Step 1: Fade in the plane (0.6s)
        self.play(FadeIn(plane, shift=DOWN * 0.3), run_time=0.6)

        # Step 2: Show the title (0.5s)
        self.play(Write(title), run_time=0.5)

        # Step 3: Scatter in the chaos arrows (0.9s)
        self.play(
            LaggedStart(
                *[GrowFromCenter(a) for a in chaos_arrows],
                lag_ratio=0.06,
            ),
            run_time=0.9,
        )

        # Step 4: Draw eigenvector lines (1.0s)
        eigen_group = VGroup(eigen_line_1, eigen_line_2)
        self.play(
            Create(eigen_line_1),
            Create(eigen_line_2),
            run_time=1.0,
        )

        # Step 5: Add eigenvector labels and subtitle (0.5s)
        self.play(
            FadeIn(eigen_label_1, scale=0.8),
            FadeIn(eigen_label_2, scale=0.8),
            Write(subtitle),
            run_time=0.5,
        )

        # Step 6: Distort the scene — chaos arrows shift/rotate randomly,
        #         eigenvectors stay perfectly still (2.0s)
        np.random.seed(99)
        distortion_anims = []
        for arrow in chaos_arrows:
            dx = np.random.uniform(-0.6, 0.6)
            dy = np.random.uniform(-0.6, 0.6)
            rotation = np.random.uniform(-0.5, 0.5)
            distortion_anims.append(
                arrow.animate.shift([dx, dy, 0]).rotate(
                    rotation, about_point=arrow.get_center()
                )
            )

        # Slightly warp the grid to show the transformation
        plane_target = plane.copy()
        plane_target.apply_matrix(
            [[1.1, 0.3, 0], [0.2, 0.9, 0], [0, 0, 1]],
        )

        self.play(
            Transform(plane, plane_target),
            *distortion_anims,
            run_time=2.0,
        )

        # Step 7: Hold — eigenvectors unmoved while chaos settles (1.0s)
        self.wait(1.0)
