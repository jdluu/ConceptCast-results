from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Vectors as directed arrows ---
        self.camera.background_color = "#181825"

        # 1. Objects
        grid_plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], color="#89b4fa"
        )
        grid_plane.set_stroke(width=2.0)

        vector_arrow = Arrow(start=[0, 0, 0], end=[2, 1, 0], color="#fab387", buff=0.0)
        vector_arrow.set_stroke(width=2.0)

        vector_label = Text("v", font="Sans", color="#a6e3a1", font_size=48)
        vector_label.next_to(vector_arrow, RIGHT, buff=0.3)

        length_label = Text("||v||", font="Sans", color="#94e2d5", font_size=36)
        length_label.next_to(vector_label, DOWN, buff=0.2)

        # Direction tick placed outside the vector_arrow bounding box (origin-centered 2.5x2.5)
        direction_tick = Arrow(
            start=[2.6, 1.3, 0], end=[3.4, 1.7, 0], color="#f38ba8", buff=0.0
        )
        direction_tick.set_stroke(width=2.0)

        # 2. Animations
        self.play(Create(grid_plane), run_time=1.5)
        self.play(Create(vector_arrow), run_time=1.5)
        self.play(FadeIn(vector_label, shift=UP), run_time=0.5)
        self.play(FadeIn(length_label, shift=UP), run_time=0.5)
        self.play(Create(direction_tick), run_time=0.5)

        # 3. Wait to match total duration 6.5s
        self.wait(2.0)
        # --- Scene 2: Linear transformation of space ---
        self.camera.background_color = "#181825"

        # Origin dot
        origin_dot = Dot(point=ORIGIN, radius=0.08, color="#fab387")

        # Source grid (regular) - LEFT
        source_grid = VGroup()
        spacing = 0.55
        rows, cols = 6, 6
        for i in range(rows):
            for j in range(cols):
                x = (i - rows / 2 + 0.5) * spacing
                y = (j - cols / 2 + 0.5) * spacing
                dot = Dot(radius=0.05, color="#89b4fa")
                dot.move_to([x, y, 0])
                source_grid.add(dot)
        source_grid.shift(LEFT * 3)

        # Target grid (sheared) - RIGHT
        target_grid = VGroup()
        shear_factor = 0.6
        for i in range(rows):
            for j in range(cols):
                x = (i - rows / 2 + 0.5) * spacing
                y = (j - cols / 2 + 0.5) * spacing
                sx = x + shear_factor * y
                sy = y
                dot = Dot(radius=0.05, color="#94e2d5")
                dot.move_to([sx, sy, 0])
                target_grid.add(dot)
        target_grid.shift(RIGHT * 3)

        # Transform arrow
        transform_arrow = Arrow(
            start=[-2, 0, 0], end=[2, 0, 0], color="#f38ba8", stroke_width=2
        )

        # Title
        title = Text("Linear transformation of space", font_size=36, color="#a6e3a1")
        title.to_edge(UP)

        # Animations - total 8.0s
        self.play(FadeIn(origin_dot, scale=0.5), run_time=0.5)
        self.play(FadeIn(source_grid, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(transform_arrow), run_time=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        self.wait(0.5)
        self.play(Transform(source_grid, target_grid), run_time=3.0)
        self.wait(2.0)
        # --- Scene 3: General effect on vectors ---
        self.clear()
        self.camera.background_color = "#181825"

        # 1. Objects
        in_arrow1 = Arrow(
            start=[-3, 1, 0], end=[-1, 1, 0], color="#89b4fa", stroke_width=2.0
        )
        in_arrow2 = Arrow(
            start=[-3, -0.5, 0], end=[-1, -0.5, 0], color="#a6e3a1", stroke_width=2.0
        )
        in_arrow3 = Arrow(
            start=[-3, 2, 0], end=[-1, 2, 0], color="#94e2d5", stroke_width=2.0
        )

        transform_box = Rectangle(
            width=1.5, height=2.5, color="#fab387", stroke_width=2.0, fill_opacity=0
        )
        transform_box.move_to(ORIGIN)

        out_arrow1 = Arrow(
            start=[1, 0.5, 0], end=[3, 1.5, 0], color="#89b4fa", stroke_width=2.0
        )
        out_arrow2 = Arrow(
            start=[1, -0.2, 0], end=[3, 0.8, 0], color="#a6e3a1", stroke_width=2.0
        )
        out_arrow3 = Arrow(
            start=[1, 1.8, 0], end=[3, 2.2, 0], color="#94e2d5", stroke_width=2.0
        )

        in_arrows = VGroup(in_arrow1, in_arrow2, in_arrow3)
        out_arrows = VGroup(out_arrow1, out_arrow2, out_arrow3)

        narration = Text(
            "Under most transformations, vectors change both their length and their direction.",
            font="Sans",
            color=WHITE,
            font_size=28,
        )
        narration.move_to(DOWN * 2.5)

        # 2. Animations
        self.play(FadeIn(transform_box, run_time=0.7))
        self.play(
            LaggedStart(
                FadeIn(in_arrow1),
                FadeIn(in_arrow2),
                FadeIn(in_arrow3),
                lag_ratio=0.2,
                run_time=1.0,
            )
        )
        self.wait(0.8)

        self.play(
            AnimationGroup(
                FadeOut(in_arrow1, shift=RIGHT * 0.5),
                FadeOut(in_arrow2, shift=RIGHT * 0.5),
                FadeOut(in_arrow3, shift=RIGHT * 0.5),
                FadeIn(out_arrow1),
                FadeIn(out_arrow2),
                FadeIn(out_arrow3),
                run_time=1.2,
            )
        )

        self.play(FadeIn(narration, run_time=0.8))
        self.wait(1.0)
        # --- Scene 4: Direction invariance ---
        self.camera.background_color = "#181825"

        # 1. Objects
        transform_box2 = Rectangle(
            width=1.2, height=2, color="#89b4fa", stroke_width=2.0, fill_opacity=0
        )
        transform_box2.move_to(ORIGIN)

        eigen_in = Arrow(
            start=[-3, 1, 0], end=[-0.5, 1, 0], color="#fab387", stroke_width=2.0
        )

        eigen_out = Arrow(
            start=[0.5, 1, 0], end=[3.5, 1, 0], color="#fab387", stroke_width=2.0
        )

        collinear_line = Line(
            start=[-3, 1, 0], end=[3.5, 1, 0], color="#f38ba8", stroke_width=2.0
        )

        direction_label = Text("direction preserved", color="#a6e3a1", font_size=36)
        direction_label.move_to(UP * 2.8)

        # 2. Animations
        self.play(Create(transform_box2), run_time=0.8)
        self.play(Create(eigen_in), run_time=0.7)
        self.wait(0.3)
        self.play(ReplacementTransform(eigen_in, eigen_out), run_time=1.5)
        self.play(Create(collinear_line), run_time=0.5)
        self.play(FadeIn(direction_label), run_time=0.7)

        # 3. Wait to match 6.0s total
        self.wait(1.5)
        # --- Scene 5: Eigenvalue as scale factor ---
        self.camera.background_color = "#181825"

        # Eigenvector (original)
        eigenvector = Arrow(start=ORIGIN, end=RIGHT * 2, color="#89b4fa")
        eigenvector.stroke_width = 2.0

        # Scaled eigenvector λ = 1.75
        scaled_vector = Arrow(start=ORIGIN, end=RIGHT * 3.5, color="#f38ba8")
        scaled_vector.stroke_width = 2.0

        # Numeric scale bar below
        scale_bar = NumberLine(x_range=[0, 4, 1], length=4, color="#94e2d5")
        scale_bar.add_numbers()
        scale_bar.stroke_width = 2.0
        scale_bar.next_to(scaled_vector, DOWN, buff=1.0)

        # Lambda label above
        lambda_label = Text("λ = 1.75", color="#fab387")
        lambda_label.next_to(eigenvector, UP, buff=0.5)

        # Brace showing the stretch length
        brace_scale = BraceBetweenPoints(
            point_1=ORIGIN + DOWN * 0.5,
            point_2=RIGHT * 3.5 + DOWN * 0.5,
            direction=UP,
            color="#a6e3a1",
        )
        brace_scale.stroke_width = 2.0

        self.play(Create(eigenvector), run_time=1.2)
        self.wait(0.3)
        self.play(ReplacementTransform(eigenvector, scaled_vector), run_time=1.5)
        self.play(FadeIn(scale_bar), run_time=1.0)
        self.play(Write(lambda_label), run_time=0.5)
        self.play(GrowFromCenter(brace_scale), run_time=0.5)
        self.wait(2.0)
        # --- Scene 6: Eigen equation ---
        self.camera.background_color = "#181825"

        # Objects
        matrix_A = Text("A", color="#89b4fa", font_size=48)
        vector_v_left = Arrow(
            start=[-1, 0, 0], end=[0.5, 0, 0], color="#fab387", stroke_width=2.0
        )
        equals_sign = Text("=", color="#a6e3a1", font_size=48)
        lambda_symbol = Text("λ", color="#f38ba8", font_size=48)
        vector_v_right = Arrow(
            start=[1, 0, 0], end=[3, 0, 0], color="#94e2d5", stroke_width=2.0
        )
        equation_tex = MathTex(r"A\mathbf{v}=\lambda\mathbf{v}", color="#89b4fa")

        # Layout to avoid overlap
        matrix_A.next_to(vector_v_left, LEFT, buff=0.3)
        equals_sign.next_to(vector_v_left, RIGHT, buff=0.8)
        lambda_symbol.next_to(equals_sign, RIGHT, buff=0.4)
        vector_v_right.next_to(lambda_symbol, RIGHT, buff=0.4)
        equation_tex.move_to(DOWN * 2.5)
        equation_tex.scale(1.2)

        # Animations
        self.play(
            FadeIn(matrix_A, shift=UP * 0.2),
            FadeIn(vector_v_left, shift=UP * 0.2),
            run_time=1.0,
        )
        self.play(FadeIn(equals_sign, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(lambda_symbol, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(vector_v_right, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(equation_tex, shift=UP * 0.2), run_time=1.0)
        self.wait(3.0)
        # --- Scene 7: Finding eigenvectors ---
        self.camera.background_color = "#181825"

        # Step 1
        step1_box = Rectangle(
            width=4,
            height=1,
            fill_color="#89b4fa",
            stroke_color="#89b4fa",
            fill_opacity=0.9,
            stroke_width=2.0,
        )
        step1_box.move_to(UP * 2.5)

        step1_text = Text("det(A - λI)=0", font="Sans", font_size=36, color="#181825")
        step1_text.move_to(step1_box.get_center())

        step1_group = VGroup(step1_box, step1_text)

        # Arrow 1
        arrow_down1 = Arrow(
            start=[0, 1, 0], end=[0, -0.5, 0], color="#f38ba8", stroke_width=2.0, buff=0
        )

        # Step 2
        step2_box = Rectangle(
            width=4,
            height=1,
            fill_color="#fab387",
            stroke_color="#fab387",
            fill_opacity=0.9,
            stroke_width=2.0,
        )
        step2_box.move_to(ORIGIN)

        step2_text = Text("Solve for λ", font="Sans", font_size=36, color="#181825")
        step2_text.move_to(step2_box.get_center())

        step2_group = VGroup(step2_box, step2_text)

        # Arrow 2
        arrow_down2 = Arrow(
            start=[0, -0.5, 0],
            end=[0, -2, 0],
            color="#f38ba8",
            stroke_width=2.0,
            buff=0,
        )

        # Step 3
        step3_box = Rectangle(
            width=5,
            height=1,
            fill_color="#a6e3a1",
            stroke_color="#a6e3a1",
            fill_opacity=0.9,
            stroke_width=2.0,
        )
        step3_box.move_to(DOWN * 2.5)

        step3_text = Text(
            "Nullspace of A - λI → v", font="Sans", font_size=32, color="#181825"
        )
        step3_text.move_to(step3_box.get_center())

        step3_group = VGroup(step3_box, step3_text)

        # Animations - total 8.5s
        self.play(GrowFromCenter(step1_group), run_time=2.0)
        self.play(Create(arrow_down1), run_time=1.0)
        self.play(GrowFromCenter(step2_group), run_time=2.0)
        self.play(Create(arrow_down2), run_time=1.0)
        self.play(GrowFromCenter(step3_group), run_time=2.0)
        self.wait(0.5)
