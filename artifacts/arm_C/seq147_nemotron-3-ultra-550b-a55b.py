import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Linear Transformation Visualization ---
        self.clear()
        self.camera.background_color = "#181825"

        # Create a NumberPlane with subtle grid lines
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={
                "stroke_color": "#89b4fa",
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "stroke_color": "#89b4fa",
                "stroke_width": 2,
                "include_tip": True,
            },
            faded_line_ratio=4,
        )

        # Create basis vectors e1 and e2
        e1_start = grid.c2p(0, 0)
        e1_end = grid.c2p(1, 0)
        e2_start = grid.c2p(0, 0)
        e2_end = grid.c2p(0, 1)

        # Vector e1 (x-axis basis)
        vec_e1 = Arrow(
            start=e1_start,
            end=e1_end,
            buff=0,
            color="#fab387",
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15,
        )
        label_e1 = MathTex(r"\vec{e}_1", color="#fab387").next_to(
            vec_e1.get_end(), RIGHT, buff=0.1
        )

        # Vector e2 (y-axis basis)
        vec_e2 = Arrow(
            start=e2_start,
            end=e2_end,
            buff=0,
            color="#a6e3a1",
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15,
        )
        label_e2 = MathTex(r"\vec{e}_2", color="#a6e3a1").next_to(
            vec_e2.get_end(), UP, buff=0.1
        )

        basis_group = VGroup(vec_e1, label_e1, vec_e2, label_e2)

        # Transformation matrix [[2, 1], [1, 2]]
        transform_matrix = np.array([[2, 1], [1, 2]])

        # Show initial state
        self.play(Create(grid), run_time=1.0)
        self.play(
            GrowFromCenter(vec_e1),
            Write(label_e1),
            GrowFromCenter(vec_e2),
            Write(label_e2),
            run_time=1.0,
        )
        self.wait(0.5)

        # Apply transformation to grid and vectors
        self.play(
            ApplyMatrix(transform_matrix, grid),
            ApplyMatrix(transform_matrix, vec_e1),
            ApplyMatrix(transform_matrix, vec_e2),
            run_time=3.0,
        )

        # Update labels to follow transformed vectors
        new_e1_end = grid.c2p(2, 1)  # First column of matrix
        new_e2_end = grid.c2p(1, 2)  # Second column of matrix

        # Animate labels to new positions
        self.play(
            label_e1.animate.next_to(new_e1_end, RIGHT, buff=0.1),
            label_e2.animate.next_to(new_e2_end, UP, buff=0.1),
            run_time=1.0,
        )

        self.wait(0.5)
        # --- Scene 2: Eigenvector Invariance ---
        self.camera.background_color = "#181825"

        # Create coordinate grid
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={
                "stroke_color": "#585b70",
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
        )

        # Transformation matrix
        A = [[2, 1], [1, 2]]
        A_np = np.array(A)

        # Create random vectors (non-eigenvectors) as 3D points for Manim
        vectors_data = [
            (np.array([1, 0.5, 0]), "#F38BA8"),  # Red/pink
            (np.array([0.5, 1, 0]), "#FAB387"),  # Orange
            (np.array([-1, 0.5, 0]), "#89B4FA"),  # Blue
            (np.array([0.5, -1, 0]), "#94E2D5"),  # Teal
        ]

        random_vectors = VGroup()
        random_vectors_transformed = VGroup()

        for vec_coords, color in vectors_data:
            # vec_coords is now a 3D numpy array
            vec = Arrow(ORIGIN, vec_coords * 1.5, buff=0, color=color, stroke_width=3)
            random_vectors.add(vec)

            # Transformed version (apply matrix to x,y components)
            transformed_xy = A_np @ vec_coords[:2]
            transformed_end = np.array([transformed_xy[0], transformed_xy[1], 0])
            vec_transformed = Arrow(
                ORIGIN, transformed_end * 1.5, buff=0, color=color, stroke_width=3
            )
            random_vectors_transformed.add(vec_transformed)

        # Eigenvector (stays on same line) - 3D array
        eigenvector_dir = np.array([1, 1, 0])  # Eigenvector for eigenvalue 3
        eigenvector = Arrow(
            ORIGIN, eigenvector_dir * 2, buff=0, color="#A6E3A1", stroke_width=5
        )
        eigenvector_transformed = Arrow(
            ORIGIN, eigenvector_dir * 6, buff=0, color="#A6E3A1", stroke_width=5
        )

        # Glow effect for eigenvector
        eigenvector_glow = Arrow(
            ORIGIN,
            eigenvector_dir * 2,
            buff=0,
            color="#A6E3A1",
            stroke_width=15,
            stroke_opacity=0.3,
        )
        eigenvector_glow_transformed = Arrow(
            ORIGIN,
            eigenvector_dir * 6,
            buff=0,
            color="#A6E3A1",
            stroke_width=15,
            stroke_opacity=0.3,
        )

        # Label
        eigen_label = MathTex(
            r"\vec{v}_{eigen}", color="#A6E3A1", font_size=36
        ).next_to(eigenvector.get_end(), UR, buff=0.2)
        eigen_label_transformed = MathTex(
            r"\vec{v}_{eigen}", color="#A6E3A1", font_size=36
        ).next_to(eigenvector_transformed.get_end(), UR, buff=0.2)

        # Animation sequence
        # 1. Show grid
        self.play(Create(grid), run_time=1.0)

        # 2. Show random vectors
        self.play(
            LaggedStart(*[GrowFromCenter(v) for v in random_vectors], lag_ratio=0.1),
            run_time=1.0,
        )

        # 3. Show eigenvector with glow
        self.play(
            GrowFromCenter(eigenvector),
            GrowFromCenter(eigenvector_glow),
            Write(eigen_label),
            run_time=1.0,
        )

        # 4. Transform everything
        self.play(
            ApplyMethod(grid.apply_matrix, A),
            *[
                Transform(v, vt)
                for v, vt in zip(random_vectors, random_vectors_transformed)
            ],
            Transform(eigenvector, eigenvector_transformed),
            Transform(eigenvector_glow, eigenvector_glow_transformed),
            Transform(eigen_label, eigen_label_transformed),
            run_time=2.5,
        )

        # 5. Emphasize eigenvector invariance
        self.play(
            Indicate(eigenvector, color="#A6E3A1", scale_factor=1.1), run_time=1.0
        )

        self.wait(0.5)
        # --- Scene 3: Eigenvalue Scaling ---
        self.camera.background_color = "#1E1E2E"

        # Palette
        ACCENT_1 = "#CBA6F7"  # eigenvalue label
        ACCENT_4 = "#A6E3A1"  # eigenvector 1 (stretch)
        ACCENT_5 = "#89B4FA"  # eigenvector 2 (shrink)

        # Basis vectors as numpy arrays for arithmetic
        e1 = np.array([1.0, 0.0, 0.0])
        e2 = np.array([0.0, 1.0, 0.0])

        # Initial eigenvectors (length 1 and 0.5)
        v1 = Arrow(ORIGIN, e1, buff=0, color=ACCENT_4, stroke_width=6)
        v2 = Arrow(ORIGIN, e2 * 0.5, buff=0, color=ACCENT_5, stroke_width=6)

        # Braces and eigenvalue labels (FIXED: separate color application)
        brace1 = Brace(v1, direction=UP, color=ACCENT_1)
        lambda1 = brace1.get_tex(r"\lambda = 2")
        lambda1.set_color(ACCENT_1)

        brace2 = Brace(v2, direction=UP, color=ACCENT_1)
        lambda2 = brace2.get_tex(r"\lambda = 0.5")
        lambda2.set_color(ACCENT_1)

        # Number line for scaling factor
        num_line = NumberLine(
            x_range=[0, 2.5, 0.5],
            length=6,
            include_numbers=True,
            label_direction=DOWN,
            color=ACCENT_1,
        ).shift(DOWN * 2.5)

        # Dots tracking scaling on number line
        dot1 = Dot(num_line.n2p(1), color=ACCENT_4)
        dot2 = Dot(num_line.n2p(0.5), color=ACCENT_5)

        # Show initial state
        self.add(v1, v2, brace1, lambda1, brace2, lambda2, num_line, dot1, dot2)

        # Create target vectors for animation
        v1_target = Arrow(ORIGIN, e1 * 2, buff=0, color=ACCENT_4, stroke_width=6)
        v2_target = Arrow(ORIGIN, e2 * 0.25, buff=0, color=ACCENT_5, stroke_width=6)

        # Create target braces for animation
        brace1_target = Brace(v1_target, direction=UP, color=ACCENT_1)
        brace2_target = Brace(v2_target, direction=UP, color=ACCENT_1)

        # Animate scaling
        self.play(
            Transform(v1, v1_target),
            Transform(brace1, brace1_target),
            lambda1.animate.move_to(brace1_target.get_tip() + UP * 0.3),
            dot1.animate.move_to(num_line.n2p(2)),
            Transform(v2, v2_target),
            Transform(brace2, brace2_target),
            lambda2.animate.move_to(brace2_target.get_tip() + UP * 0.3),
            dot2.animate.move_to(num_line.n2p(0.25)),
            run_time=4,
        )
        self.wait(3)
        # --- Scene 4: Characteristic Equation ---
        self.clear()
        self.camera.background_color = "#181825"

        # Color palette
        ACCENT_1 = "#89b4fa"
        ACCENT_2 = "#fab387"
        ACCENT_3 = "#f38ba8"
        ACCENT_4 = "#a6e3a1"
        ACCENT_5 = "#94e2d5"

        # Title
        title = Text(
            "Characteristic Equation", font="Sans", font_size=48, color=ACCENT_1
        )
        title.to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # Matrix A = [[2, 1], [1, 2]]
        matrix_A = Matrix([[2, 1], [1, 2]], element_to_mobject_config={"color": WHITE})
        label_A = MathTex("A", "=", color=WHITE).next_to(matrix_A, LEFT)
        group_A = VGroup(label_A, matrix_A)

        # Identity matrix I
        matrix_I = Matrix([[1, 0], [0, 1]], element_to_mobject_config={"color": WHITE})
        label_I = MathTex("I", color=WHITE).next_to(matrix_I, LEFT)
        group_I = VGroup(label_I, matrix_I)

        # Lambda symbol
        lambda_sym = MathTex(r"\lambda", color=ACCENT_2)

        # Expression: A - λI
        minus = MathTex("-", color=WHITE)
        expr_group = VGroup(group_A, minus, lambda_sym, group_I).arrange(
            RIGHT, buff=0.3
        )
        expr_group.center()

        # Determinant bars and equals zero
        det_left = MathTex(r"\det(", color=WHITE)
        det_right = MathTex(r")", color=WHITE)
        equals_zero = MathTex("= 0", color=WHITE)
        full_eq = VGroup(det_left, expr_group.copy(), det_right, equals_zero).arrange(
            RIGHT, buff=0.2
        )
        full_eq.center()

        # Show initial expression
        self.play(
            FadeIn(group_A, shift=UP * 0.2),
            FadeIn(group_I, shift=UP * 0.2),
            Write(minus),
            Write(lambda_sym),
            run_time=1.5,
        )
        self.wait(0.5)

        # Show determinant equation
        self.play(
            ReplacementTransform(expr_group.copy(), full_eq[1]),
            Write(det_left),
            Write(det_right),
            Write(equals_zero),
            run_time=1.5,
        )
        self.wait(0.5)

        # Show explicit matrix subtraction: [[2-λ, 1], [1, 2-λ]]
        matrix_A_minus_lambda_I = Matrix(
            [[r"2-\lambda", 1], [1, r"2-\lambda"]],
            element_to_mobject_config={"color": WHITE},
        )
        det_explicit = (
            VGroup(
                MathTex(r"\det(", color=WHITE),
                matrix_A_minus_lambda_I,
                MathTex(r")", color=WHITE),
                MathTex("= 0", color=WHITE),
            )
            .arrange(RIGHT, buff=0.2)
            .center()
        )

        self.play(ReplacementTransform(full_eq, det_explicit), run_time=1.5)
        self.wait(0.5)

        # Compute determinant: (2-λ)^2 - 1 = 0
        step1 = MathTex(r"(2-\lambda)^2 - 1 = 0", color=WHITE).next_to(
            det_explicit, DOWN, buff=0.5
        )
        self.play(Write(step1), run_time=1.0)
        self.wait(0.5)

        # Expand: λ^2 - 4λ + 3 = 0
        step2 = MathTex(r"\lambda^2 - 4\lambda + 3 = 0", color=ACCENT_4).next_to(
            step1, DOWN, buff=0.3
        )
        self.play(Write(step2), run_time=1.0)
        self.wait(0.5)

        # Highlight final polynomial
        rect = SurroundingRectangle(step2, color=ACCENT_1, buff=0.1)
        self.play(Create(rect), run_time=0.5)
        self.wait(0.5)

        # Fade out
        self.play(
            FadeOut(VGroup(title, det_explicit, step1, step2, rect)), run_time=1.0
        )
        self.wait(0.5)
        # --- Scene 5: Invariant Axes ---
        self.clear()

        # Background color (Catppuccin Mocha)
        self.camera.background_color = "#1E1E2E"

        # Palette Colors
        ACCENT_1 = "#CBA6F7"  # Mauve - Eigenvector 1
        ACCENT_2 = "#F38BA8"  # Red - Eigenvector 2
        ACCENT_3 = "#FAB387"  # Peach - Grid lines
        ACCENT_4 = "#A6E3A1"  # Green - Labels/Flash
        ACCENT_5 = "#89B4FA"  # Blue - Title
        TEXT_COLOR = "#CDD6F4"

        # Create the Eigenbasis Grid (NumberPlane aligned to eigenvectors)
        # Standard basis aligned grid (no shear)
        eigen_plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={
                "stroke_color": ACCENT_3,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={
                "color": TEXT_COLOR,
                "include_tip": True,
                "stroke_width": 2,
            },
            faded_line_ratio=4,  # Show fewer faded lines for cleaner look
        )

        # Eigenvectors as thick arrows along the new axes (x' and y')
        # Since grid is axis-aligned, eigenvectors are just standard basis vectors scaled
        v1 = Arrow(
            ORIGIN,
            eigen_plane.c2p(3, 0),
            buff=0,
            color=ACCENT_1,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15,
        )
        v2 = Arrow(
            ORIGIN,
            eigen_plane.c2p(0, 2),
            buff=0,
            color=ACCENT_2,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15,
        )

        eigenvectors = VGroup(v1, v2)

        # Labels for eigenvectors / new axes
        label_v1 = MathTex(r"\vec{v}_1", color=ACCENT_1).next_to(v1.get_end(), RIGHT)
        label_v2 = MathTex(r"\vec{v}_2", color=ACCENT_2).next_to(v2.get_end(), UP)

        # Axis labels for new coordinate system (x', y')
        x_label = MathTex(r"x'", color=TEXT_COLOR).next_to(
            eigen_plane.x_axis.get_end(), DR
        )
        y_label = MathTex(r"y'", color=TEXT_COLOR).next_to(
            eigen_plane.y_axis.get_end(), UL
        )

        # Title
        title = (
            Text(
                "Invariant Axes (Eigenbasis)", font="Sans", color=ACCENT_5, weight=BOLD
            )
            .scale(0.8)
            .to_edge(UP)
        )

        # Animation Sequence (Total 7 seconds)
        # 1. Fade in Title (0.5s)
        self.play(FadeIn(title), run_time=0.5)

        # 2. Create Grid (2.0s) - "snaps into a clean, axis-aligned grid"
        self.play(Create(eigen_plane), run_time=2.0)

        # 3. Grow Eigenvectors (1.5s) - "shown as thick arrows along x' and y' axes"
        self.play(GrowFromCenter(v1), GrowFromCenter(v2), run_time=1.5)

        # 4. Write Labels (1.0s)
        self.play(
            Write(label_v1),
            Write(label_v2),
            Write(x_label),
            Write(y_label),
            run_time=1.0,
        )

        # 5. Hold/Emphasize invariant lines (grid lines) (1.5s)
        # Flash along axes to show invariance
        self.play(
            ShowPassingFlash(
                v1.copy().set_color(ACCENT_4).set_stroke(width=8), time_width=0.5
            ),
            ShowPassingFlash(
                v2.copy().set_color(ACCENT_4).set_stroke(width=8), time_width=0.5
            ),
            run_time=1.5,
        )

        # Final wait to match duration exactly (7.0 - 0.5 - 2.0 - 1.5 - 1.0 - 1.5 = 0.5s)
        self.wait(0.5)
        # --- Scene 6: Diagonalization ---
        self.clear()
        # Set background color
        self.camera.background_color = "#181825"

        # Color palette from workflow
        PALETTE = [
            "#89b4fa",  # Blue
            "#fab387",  # Peach
            "#f38ba8",  # Red
            "#a6e3a1",  # Green
            "#94e2d5",  # Teal
        ]

        # Original matrix A (from previous scenes context)
        matrix_A = Matrix(
            [["2", "1"], ["1", "2"]], element_to_mobject_config={"color": WHITE}
        )
        matrix_A_label = MathTex("A", "=", color=WHITE).next_to(matrix_A, LEFT)
        matrix_A_group = VGroup(matrix_A_label, matrix_A).to_edge(UP, buff=1)

        # Diagonal matrix D with eigenvalues 3 and 1
        diag_matrix = Matrix(
            [["3", "0"], ["0", "1"]], element_to_mobject_config={"color": WHITE}
        )
        diag_matrix_label = MathTex("D", "=", color=WHITE).next_to(diag_matrix, LEFT)
        diag_matrix_group = VGroup(diag_matrix_label, diag_matrix).move_to(ORIGIN)

        # Change of basis matrices P and P^{-1}
        P_matrix = Matrix(
            [["1", "1"], ["1", "-1"]],
            element_to_mobject_config={"color": WHITE, "font_size": 36},
        )
        P_label = MathTex("P", color=WHITE).next_to(P_matrix, LEFT)
        P_group = (
            VGroup(P_label, P_matrix)
            .next_to(diag_matrix_group, LEFT, buff=1.5)
            .shift(UP * 0.5)
        )

        P_inv_matrix = Matrix(
            [["0.5", "0.5"], ["0.5", "-0.5"]],
            element_to_mobject_config={"color": WHITE, "font_size": 36},
        )
        P_inv_label = MathTex("P^{-1}", color=WHITE).next_to(P_inv_matrix, LEFT)
        P_inv_group = (
            VGroup(P_inv_label, P_inv_matrix)
            .next_to(diag_matrix_group, RIGHT, buff=1.5)
            .shift(UP * 0.5)
        )

        # Arrows indicating transformation
        arrow1 = Arrow(
            P_group.get_right(),
            diag_matrix_group.get_left(),
            color=PALETTE[0],
            buff=0.2,
        )
        arrow2 = Arrow(
            diag_matrix_group.get_right(),
            P_inv_group.get_left(),
            color=PALETTE[0],
            buff=0.2,
        )

        # Equation: A = PDP^{-1}
        equation = (
            MathTex("A", "=", "P", "D", "P^{-1}", color=WHITE)
            .scale(0.8)
            .to_edge(DOWN, buff=1)
        )

        # Animation sequence (total 7.5 seconds)
        # 1. Show original matrix A (1.5s)
        self.play(FadeIn(matrix_A_group), run_time=1.5)

        # 2. Transform A to diagonal form D (2s)
        self.play(
            FadeOut(matrix_A_group, shift=UP),
            FadeIn(diag_matrix_group, shift=UP),
            run_time=2.0,
        )

        # 3. Show P and P^{-1} matrices with arrows (2s)
        self.play(
            FadeIn(P_group),
            FadeIn(P_inv_group),
            Create(arrow1),
            Create(arrow2),
            run_time=2.0,
        )

        # 4. Show diagonalization equation (1.5s)
        self.play(Write(equation), run_time=1.5)

        # 5. Hold final frame (0.5s)
        self.wait(0.5)
