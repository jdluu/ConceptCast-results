import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Linear Transformations as Space Warping ---
        # 1. Setup Colors and Styles
        self.camera.background_color = "#181825"
        COLOR_GRID = "#A6ADC8"
        COLOR_AXES = "#CDD6F4"
        COLOR_TEXT = "#CBA6F7"
        COLOR_BASIS_I = "#89b4fa"  # accent_5
        COLOR_BASIS_J = "#fab387"  # accent_3

        # 2. Objects Definition
        # NumberPlane for the grid
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-7, 7, 1],
            background_line_style={
                "stroke_color": COLOR_GRID,
                "stroke_width": 1.0,
                "stroke_opacity": 0.4,
            },
        )

        # Axes on top of the grid
        # FIX: 'include_tip' is not a valid keyword argument for Axes in the current Manim version.
        # Tips are enabled by default or controlled via axis_config.
        axes = Axes(
            x_range=[-7, 7, 1],
            y_range=[-7, 7, 1],
            axis_config={"color": COLOR_AXES, "stroke_width": 2.0},
        )

        # Basis vectors to visually demonstrate the transformation
        basis_i = Arrow(ORIGIN, RIGHT, color=COLOR_BASIS_I, buff=0)
        basis_j = Arrow(ORIGIN, UP, color=COLOR_BASIS_J, buff=0)

        # FIX: Use raw strings (r"...") for LaTeX to avoid SyntaxWarnings regarding escape sequences like \h
        label_i = MathTex(r"\hat{i}", color=COLOR_BASIS_I).next_to(
            basis_i, RIGHT, buff=0.1
        )
        label_j = MathTex(r"\hat{j}", color=COLOR_BASIS_J).next_to(
            basis_j, UP, buff=0.1
        )

        # Transformation Label
        transformation_label = Text(
            "Linear Transformation", font="Sans", color=COLOR_TEXT, font_size=42
        ).to_edge(UP)

        # 3. Animations
        # Stage 1: Introduction (0.0 - 3.0s)
        self.play(FadeIn(grid), Create(axes), Write(transformation_label), run_time=2.0)
        self.play(
            GrowFromCenter(basis_i),
            GrowFromCenter(basis_j),
            Write(label_i),
            Write(label_j),
            run_time=1.0,
        )
        self.wait(1.0)

        # Define the transformation matrix: [1.5 0.8; 0.5 1.2]
        matrix = [[1.5, 0.8], [0.5, 1.2]]

        # Stage 2: The Warp (4.0 - 8.0s)
        # Animate the basis vectors and the grid simultaneously
        # Note: apply_matrix is a method of VMobject that transforms coordinates.
        self.play(
            grid.animate.apply_matrix(matrix),
            axes.animate.apply_matrix(matrix),
            basis_i.animate.apply_matrix(matrix),
            basis_j.animate.apply_matrix(matrix),
            label_i.animate.apply_matrix(matrix).shift(RIGHT * 0.2),
            label_j.animate.apply_matrix(matrix).shift(UP * 0.2),
            run_time=4.0,
            rate_func=slow_into,
        )

        # Stage 3: Conclusion (8.0 - 10.0s)
        self.play(
            Indicate(transformation_label, scale_factor=1.1, color=COLOR_TEXT),
            run_time=1.0,
        )
        self.wait(1.0)
        # --- Scene 2: The Concept of Directional Invariance ---
        # Configuration from Style Guidelines
        self.camera.background_color = "#181825"
        COLOR_GRID = "#A6ADC8"
        COLOR_VECTORS = "#F38BA8"
        COLOR_INVARIANT = "#A6E3A1"

        # 1. Objects definition
        # Create a number plane to represent the space
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-7, 7, 1],
            background_line_style={"stroke_color": COLOR_GRID, "stroke_width": 1.0},
        )

        # We define a linear transformation matrix.
        # Matrix [[1.5, 0.5], [0, 1]] has an eigenvector [1, 0] with eigenvalue 1.5.
        # This is a shear mapping.
        matrix = np.array([[1.5, 0.5], [0, 1]])

        # Random vectors that will change direction
        # CRITICAL FIX: Manim coordinates must be 3D (x, y, z).
        # The previous error "ValueError: operands could not be broadcast together with shapes (2,) (3,)"
        # occurred because np.array([x, y]) was used where Manim expected [x, y, z].
        random_dirs = [[1, 2, 0], [-1, 1, 0], [2, -1, 0], [-2, -2, 0], [0, 2, 0]]
        random_vectors = VGroup(
            *[
                Arrow(start=ORIGIN, end=np.array(d), color=COLOR_VECTORS, buff=0)
                for d in random_dirs
            ]
        )

        # The invariant vector (along the x-axis for our chosen matrix)
        # Vector [2, 0, 0] stays on the x-axis span
        invariant_vector = Arrow(
            start=ORIGIN, end=[2, 0, 0], color=COLOR_INVARIANT, buff=0
        )

        # The span line
        span_line = Line(
            start=[-4, 0, 0], end=[4, 0, 0], color=COLOR_INVARIANT, stroke_width=2
        )
        span_label = Text(
            "Invariant Span", font="Sans", color=COLOR_INVARIANT, font_size=24
        )
        span_label.next_to(span_line, DOWN, buff=0.2)

        # 2. Animations
        # Initial State
        self.add(grid)
        self.play(
            Create(span_line), Write(span_label), FadeIn(invariant_vector), run_time=2.0
        )
        self.play(
            LaggedStart(*[GrowFromCenter(v) for v in random_vectors], lag_ratio=0.1),
            run_time=2.0,
        )
        self.wait(1.0)

        # The Transformation (Grid Warp and Vector Rotation)
        # Manim's apply_matrix expects a 2x2 or 3x3 matrix.
        # Since we are in a 2D-like plane, apply_matrix handles the 2x2 mapping to the 3D space.
        self.play(
            grid.animate.apply_matrix(matrix),
            random_vectors.animate.apply_matrix(matrix),
            invariant_vector.animate.apply_matrix(matrix),
            span_line.animate.apply_matrix(matrix),
            run_time=4.0,
        )

        # Highlight the fact that the invariant vector is still on the line
        self.play(
            Indicate(invariant_vector, color=COLOR_INVARIANT, scale_factor=1.2),
            run_time=1.0,
        )

        # Final hold to match total duration (11.0s)
        self.wait(1.0)
        # --- Scene 3: Defining the Eigenvector ---
        # --- Configuration & Styles ---
        # Using provided style guidelines
        BG_COLOR = "#181825"
        COLOR_EIGEN = "#A6E3A1"
        COLOR_FADED = "#45475a"

        self.camera.background_color = BG_COLOR

        # --- Objects ---
        # Create a set of background vectors (faded)
        # Explicitly using 3-element lists [x, y, z] to avoid broadcasting errors
        random_dirs = [
            [1.5, 1.0, 0],
            [-1.0, 1.5, 0],
            [2.0, -1.0, 0],
            [-1.5, -1.5, 0],
            [0.5, 2.0, 0],
        ]

        faded_vectors = VGroup(
            *[
                Arrow(
                    start=ORIGIN, end=np.array(d), color=COLOR_FADED, stroke_width=2.0
                )
                for d in random_dirs
            ]
        )

        # Create the 'Invariant' Eigenvector (The hero of the scene)
        # Positioned along a specific diagonal
        eigen_dir = np.array([2.5, 0.5, 0])
        eigenvector_highlight = Arrow(
            start=ORIGIN, end=eigen_dir, color=COLOR_EIGEN, stroke_width=4.0
        )

        # Label for the eigenvector using the primary font 'Sans'
        label_eigenvector = Text(
            "Eigenvector", font="Sans", color=COLOR_EIGEN, font_size=36
        ).next_to(eigenvector_highlight.get_end(), UR, buff=0.2)

        # --- Animation Sequence ---
        # Total target duration: 11.0 seconds.

        # 1. Initial state: all vectors are present
        self.add(faded_vectors, eigenvector_highlight)
        self.wait(1.0)

        # 2. Background vectors fade out to emphasize the invariant one
        # Duration: 2.0s
        self.play(
            faded_vectors.animate.set_color(COLOR_FADED).set_stroke(opacity=0.3),
            run_time=2.0,
        )

        # 3. The Eigenvector "glows" and is labeled
        # Duration: 2.0s
        self.play(
            Indicate(eigenvector_highlight, color=COLOR_EIGEN, scale_factor=1.2),
            Write(label_eigenvector),
            run_time=2.0,
        )

        # 4. Reinforce the "axis" concept with a circumference
        # Duration: 2.0s
        self.play(Circumscribe(label_eigenvector, color=COLOR_EIGEN), run_time=2.0)

        # 5. Final hold to match narration and total duration
        # Total elapsed: 1 + 2 + 2 + 2 = 7.0s. Need 4.0s more.
        self.wait(4.0)
        # --- Scene 4: The Eigenvalue (Scaling Factor) ---
        self.clear()
        # --- Scene 4: The Eigenvalue (Scaling Factor) ---
        # Set background color based on style guidelines
        self.camera.background_color = "#181825"

        # Colors from the provided palette
        COLOR_VEC = "#a6e3a1"  # Greenish
        COLOR_VAL = "#fab387"  # Peach/Orange
        COLOR_LINE = "#89b4fa"  # Soft Blue

        # 1. Objects Setup
        # Eigenvector direction: [1, 1] (diagonal)
        span_dir = np.array([1, 1, 0])

        # The span line: the line along which the eigenvector lives
        span_line = Line(
            start=-span_dir * 2.5,
            end=span_dir * 2.5,
            color=COLOR_LINE,
            stroke_opacity=0.3,
        )

        # Tracker for the scaling factor (lambda)
        lambda_tracker = ValueTracker(1.0)

        # The Eigenvector: Dynamic arrow updating with the tracker
        eigenvector = always_redraw(
            lambda: Arrow(
                start=ORIGIN,
                end=lambda_tracker.get_value() * span_dir,
                color=COLOR_VEC,
                buff=0,
                stroke_width=5,
            )
        )

        # The eigenvalue label positioned at the Top Right
        lbl_prefix = MathTex(r"\lambda = ", color=COLOR_VAL).to_corner(UR, buff=1)
        lbl_value = always_redraw(
            lambda: DecimalNumber(
                lambda_tracker.get_value(), color=COLOR_VAL, num_decimal_places=2
            ).next_to(lbl_prefix, RIGHT)
        )

        # The Brace: Scales with the vector
        scaling_brace = always_redraw(
            lambda: BraceBetweenPoints(
                ORIGIN,
                lambda_tracker.get_value() * span_dir,
                direction=DL,
                color=COLOR_VAL,
            )
        )

        # --- Animation Sequence ---
        # Total duration: 11.5s

        # 1. Initial state introduction (2.0s)
        self.play(Create(span_line), run_time=1)
        self.play(
            GrowFromCenter(eigenvector),
            Write(lbl_prefix),
            FadeIn(lbl_value),
            run_time=1,
        )
        self.wait(1)

        # 2. First Scaling: Extend (3.0s)
        # FIX: In modern Manim, to animate a ValueTracker,
        # we must wrap the set_value call in a lambda or a custom function
        # if passed to play, or simply call set_value inside a
        # value-updating context. The most reliable method for simultaneous
        # animation of a ValueTracker and Mobjects is to use a
        # custom Animation or a simple loop, but for standard Scene.play,
        # we can animate a dummy Mobject and use its update to drive the tracker.

        # Alternatively, we use a simple lambda function inside play that
        # updates the tracker's value incrementally.

        # Create a dummy object to anchor the animation duration
        dummy = Dot(point=ORIGIN, radius=0).add_to_back()

        self.add(
            scaling_brace
        )  # Add the brace first to avoid Create() errors with always_redraw
        self.play(
            FadeIn(scaling_brace),
            # Animate the tracker using a simple function logic inside a play call
            # by creating a value-changing animation on a proxy object.
            dummy.animate.shift(RIGHT * 0),
            run_time=2.0,
            rate_func=smooth,
        )
        # Since set_value is an instant change, to achieve a smooth transition
        # while other things animate, we use the ValueTracker's target_value
        # if supported, or we use the 'animate' approach via an updater.

        # Correct pattern for animating ValueTracker in Community Edition:
        # We can't put .set_value in play(). We should use a ValueTracker
        # in combination with an animation that lasts the same duration.

        # Redefining Scaling animations using a custom update loop logic
        # for absolute compatibility:

        # 2. Extend (2.0s animation + 1.0s wait)
        self.play(
            lambda_tracker.animate.set_value(2.2),
            # We remove Create(scaling_brace) because it's already redrawable
            # and instead just make it appear.
            run_time=2.0,
            rate_func=smooth,
        )
        self.wait(1.0)

        # 3. Second Scaling: Shrink (2.0s animation + 1.0s wait)
        self.play(lambda_tracker.animate.set_value(0.5), run_time=2.0, rate_func=smooth)
        self.wait(1.0)

        # 4. Final Scaling: Expand (1.5s animation + 1.0s wait)
        self.play(lambda_tracker.animate.set_value(1.5), run_time=1.5, rate_func=smooth)
        self.wait(1.0)
        # --- Scene 5: The Fundamental Equation ---
        # Set background color based on style guidelines
        self.camera.background_color = "#181825"

        # Color Palette from guidelines
        COLOR_EQUATION = "#CDD6F4"
        COLOR_MATRIX_A = "#CBA6F7"
        COLOR_LAMBDA = "#FAB387"

        # 1. Objects
        # The fundamental equation Ax = λx
        # We use a list for the equation to easily index parts for labels
        equation = MathTex(
            "A", "x", "=", "\\lambda", "x", font_size=72, color=COLOR_EQUATION
        )
        equation.set_color_by_tex("A", COLOR_MATRIX_A)
        equation.set_color_by_tex("\\lambda", COLOR_LAMBDA)

        # Fix: Using ORIGIN or explicit coordinates instead of CENTER if CENTER is giving issues,
        # although CENTER is standard. In some environments, explicit vectors are safer.
        equation.move_to([0, 0, 0])

        # Labels for the components
        # matrix_a_label: Below 'A'
        matrix_a_label = Text(
            "Linear Transformation", font="Sans", font_size=24, color=COLOR_MATRIX_A
        )
        matrix_a_label.next_to(equation[0], DOWN, buff=0.5)

        # lambda_label: Below '\lambda'
        lambda_label = Text(
            "Scaling Factor", font="Sans", font_size=24, color=COLOR_LAMBDA
        )
        lambda_label.next_to(equation[3], DOWN, buff=0.5)

        # 2. Animations
        # Transition into the scene
        # Since the narration is "Mathematically, applying matrix A to vector x...",
        # we start by writing the equation.

        # Write the equation (4s)
        self.play(Write(equation), run_time=4.0)
        self.wait(1.0)

        # Indicate the specific parts mentioned in the narration
        # Highlight 'A' first, then 'lambda' (3s total)
        self.play(
            FadeIn(matrix_a_label, shift=UP * 0.3),
            Indicate(equation[0], color=COLOR_MATRIX_A),
            run_time=1.5,
        )
        self.play(
            FadeIn(lambda_label, shift=UP * 0.3),
            Indicate(equation[3], color=COLOR_LAMBDA),
            run_time=1.5,
        )

        # Final hold to let the viewer absorb the relationship (3.0s)
        # Total duration = 4.0 (Write) + 1.0 (Wait) + 1.5 (A label) + 1.5 (L label) + 3.0 (Wait) = 11.0s
        self.wait(3.0)
        # --- Scene 6: Characteristic Equation (Finding λ) ---
        # Configuration from style guidelines
        self.camera.background_color = "#181825"
        primary_color = "#89b4fa"  # Blue-ish
        secondary_color = "#fab387"  # Orange-ish
        accent_color = "#CBA6F7"  # Purple (from storyboard)
        text_color = "#CDD6F4"  # Light grey/white
        axis_color = "#A6ADC8"  # Muted blue-grey

        # 1. Objects
        # The characteristic equation at the top
        char_equation = MathTex(
            r"\det(A - \lambda I) = 0", font_size=54, color=text_color
        ).to_edge(UP, buff=1.5)

        # Number line for lambda (bottom)
        # x_range: [-4, 4, 1]
        lambda_axis = NumberLine(
            x_range=[-4, 4, 1],
            length=10,
            color=axis_color,
            include_numbers=True,
            label_direction=DOWN,
            font_size=24,
        ).shift(DOWN * 2)

        # Add lambda label to the axis
        lambda_label = MathTex(r"\lambda", color=axis_color, font_size=36).next_to(
            lambda_axis, RIGHT, buff=0.5
        )

        # The characteristic polynomial graph
        # Let's use a simple quadratic for demonstration: f(lambda) = (lambda - 1)(lambda + 2) = lambda^2 + lambda - 2
        axes = (
            Axes(
                x_range=[-4, 4, 1],
                y_range=[-3, 5, 1],
                x_length=10,
                y_length=5,
                axis_config={"include_tip": False, "include_numbers": False},
                color=axis_color,
            )
            .move_to(ORIGIN)
            .shift(DOWN * 0.5)
        )

        # We align the x-axis of the 'axes' object with the 'lambda_axis'
        # lambda_axis is at DOWN*2, axes is at DOWN*0.5.
        # To make them overlap or align, let's just use one Axes object for the graph
        # and treat the NumberLine as the label for the X axis.

        def poly_func(x):
            return (x - 1) * (x + 2)

        characteristic_poly = axes.plot(
            poly_func, color=accent_color, x_range=[-3, 2], stroke_width=4
        )

        # Roots (dots where the graph hits the x-axis)
        root1 = Dot(axes.c2p(1, 0), color=secondary_color)
        root2 = Dot(axes.c2p(-2, 0), color=secondary_color)

        root_labels = VGroup(
            MathTex(r"\lambda_1 = 1", font_size=30, color=secondary_color).next_to(
                root1, UP, buff=0.2
            ),
            MathTex(r"\lambda_2 = -2", font_size=30, color=secondary_color).next_to(
                root2, UP, buff=0.2
            ),
        )

        # 2. Animations
        # Sequence total duration: 11.0s

        # Step 1: Write the equation (2.0s)
        self.play(Write(char_equation), run_time=2.0)
        self.wait(0.5)

        # Step 2: Transition to Graph (3.0s)
        # We fade the equation slightly and bring in the axes/graph
        self.play(
            char_equation.animate.set_opacity(0.5).scale(0.8).to_edge(UP, buff=0.5),
            Create(axes),
            Create(lambda_axis),
            Write(lambda_label),
            run_time=3.0,
        )

        # Step 3: Draw the polynomial curve (2.0s)
        self.play(Create(characteristic_poly), run_time=2.0)
        self.wait(0.5)

        # Step 4: Highlight roots (3.0s)
        # Indicate the points where det(A-lambda I) = 0
        self.play(
            LaggedStart(
                FadeIn(root1, scale=0.5), FadeIn(root2, scale=0.5), lag_ratio=0.5
            ),
            run_time=1.0,
        )
        self.play(
            Write(root_labels),
            Indicate(root1, color=secondary_color),
            Indicate(root2, color=secondary_color),
            run_time=2.0,
        )

        # Total time: 2.0 + 0.5 + 3.0 + 2.0 + 0.5 + 1.0 + 2.0 = 11.0s
        # The wait(0.5) is part of the pacing.
        # Let's adjust the final wait if needed.
        # Current sum = 11.0.
        # --- Scene 7: Solving for the Eigenvector ---
        self.clear()

        # --- Style Configuration ---
        # Using colors from the workflow context
        BG_COLOR = "#181825"
        COLOR_EQ = "#CDD6F4"
        COLOR_LINE = "#A6E3A1"
        COLOR_PLANE = "#45475a"
        COLOR_ACCENT = "#89b4fa"

        self.camera.background_color = BG_COLOR

        # 1. Objects
        # Equation (A - λI)x = 0
        substitution_eq = MathTex(
            "(A - \lambda I)\mathbf{x} = 0", color=COLOR_EQ, font_size=72
        ).to_edge(UP, buff=1.5)

        # NumberPlane as the background for the "collapse" visual
        collapse_visual = (
            NumberPlane(
                x_range=[-4, 4, 1],
                y_range=[-4, 4, 1],
                background_line_style={
                    "stroke_color": COLOR_PLANE,
                    "stroke_width": 2,
                    "stroke_opacity": 0.5,
                },
                axis_config={"color": COLOR_PLANE},
            )
            .scale(0.8)
            .shift(DOWN * 0.5)
        )

        # The "collapse" effect is best represented by a set of points or a grid
        # that flattens onto a line.
        # Create a grid of dots to visualize the space
        dots = (
            VGroup(
                *[
                    Dot(
                        point=[x, y, 0],
                        radius=0.05,
                        color=COLOR_ACCENT,
                        fill_opacity=0.6,
                    )
                    for x in range(-3, 4)
                    for y in range(-3, 4)
                ]
            )
            .scale(0.5)
            .move_to(collapse_visual.get_center())
        )

        # The target eigenspace line
        eigenspace_line = (
            Line(start=[-2, -2, 0], end=[2, 2, 0], color=COLOR_LINE, stroke_width=6)
            .scale(0.8)
            .move_to(collapse_visual.get_center())
        )

        # Label for the line
        line_label = MathTex("Eigenspace", color=COLOR_LINE, font_size=36).next_to(
            eigenspace_line, UR, buff=0.1
        )

        # 2. Animations
        # Step 1: Write the equation (2.0s)
        self.play(Write(substitution_eq), run_time=2.0)
        self.wait(0.5)

        # Step 2: Show the coordinate plane and the initial "space" (2.0s)
        self.play(Create(collapse_visual), FadeIn(dots, scale=0.5), run_time=2.0)
        self.wait(1.0)

        # Step 3: Visual Metaphor - The collapse of the plane into the line (3.0s)
        # We simulate the transformation by moving dots onto the line
        # For a simple visual, we can just transition the dots into the line
        # or move them linearly.

        # To create a "collapsing" feel, we transform the dots into the line
        # and fade in the line simultaneously.
        self.play(
            ReplacementTransform(dots, eigenspace_line),
            Write(line_label),
            run_time=3.0,
            rate_func=smooth,
        )

        # Final pause to let the viewer absorb the visual metaphor (2.5s)
        # Total time: 2.0 + 0.5 + 2.0 + 1.0 + 3.0 + 2.5 = 11.0s
        self.wait(2.5)
        # --- Scene 8: Application: Principal Components ---
        # --- Setup Background and Palette ---
        self.camera.background_color = "#181825"
        COLOR_DATA = "#CDD6F4"
        COLOR_AXES = "#A6E3A1"
        COLOR_PC1 = "#FAB387"
        COLOR_PC2 = "#89B4FA"

        # --- 1. Objects Definition ---

        # Generate a synthetic data cloud (elongated ellipse)
        # We'll create points that are spread more along a specific diagonal
        np.random.seed(42)
        points = []
        for _ in range(60):
            # Create a distribution with higher variance along x' (rotated)
            x_prime = np.random.normal(0, 2.5)
            y_prime = np.random.normal(0, 0.8)

            # Rotate by 30 degrees
            theta = 30 * DEGREES
            x = x_prime * np.cos(theta) - y_prime * np.sin(theta)
            y = x_prime * np.sin(theta) + y_prime * np.cos(theta)
            points.append([x, y, 0])

        data_cloud = VGroup(
            *[Dot(point=p, radius=0.06, color=COLOR_DATA) for p in points]
        )

        # Coordinate System (Standard Axes)
        pca_axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": COLOR_AXES, "include_tip": True},
        )

        # Principal Components (Arrows)
        # PC1: direction of maximum variance (along the cloud's long axis)
        pc1_vector = np.array([np.cos(30 * DEGREES), np.sin(30 * DEGREES), 0])
        pc1_arrow = Arrow(
            start=ORIGIN, end=pc1_vector * 3, color=COLOR_PC1, buff=0, stroke_width=6
        )

        # PC2: orthogonal to PC1
        pc2_vector = np.array([-np.sin(30 * DEGREES), np.cos(30 * DEGREES), 0])
        pc2_arrow = Arrow(
            start=ORIGIN, end=pc2_vector * 2, color=COLOR_PC2, buff=0, stroke_width=6
        )

        # Labels
        label_pc1 = MathTex("PC_1", color=COLOR_PC1).next_to(
            pc1_arrow.get_end(), RIGHT, buff=0.1
        )
        label_pc2 = MathTex("PC_2", color=COLOR_PC2).next_to(
            pc2_arrow.get_end(), UP, buff=0.1
        )

        # --- 2. Animations ---

        # Duration Breakdown (Total: 11.0s)
        # 0-2s: Fade in data cloud
        # 2-4s: Create axes
        # 4-7s: Reveal PC1 and explain variance
        # 7-9s: Reveal PC2 and rotate the frame
        # 9-11s: Final hold/outro

        # Step 1: Show Data (2.0s)
        self.play(FadeIn(data_cloud, lag_ratio=0.05), run_time=2.0)

        # Step 2: Create Base Coordinate System (2.0s)
        self.play(Create(pca_axes), run_time=2.0)

        # Step 3: Principal Component 1 (3.0s)
        # We simulate the "finding" of the eigenvector by growing the arrow
        self.play(GrowFromCenter(pc1_arrow), Write(label_pc1), run_time=1.5)
        self.play(Indicate(pc1_arrow, color=COLOR_PC1, scale_factor=1.1), run_time=1.5)

        # Step 4: Principal Component 2 & Rotation (2.0s)
        # Transform the axes to align with the data (representing the change of basis)
        # We rotate the axes by 30 degrees to match the data spread
        target_axes = pca_axes.copy().rotate(30 * DEGREES)

        self.play(
            ReplacementTransform(pca_axes, target_axes),
            GrowFromCenter(pc2_arrow),
            Write(label_pc2),
            run_time=2.0,
        )

        # Final Hold (2.0s)
        # Correcting duration sum: 2 + 2 + 3 + 2 + 2 = 11.0
        self.wait(2.0)
