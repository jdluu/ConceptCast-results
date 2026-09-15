import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Linear transformations as matrix multiplication ---
        self.clear()
        self.camera.background_color = "#181825"

        # ---- Palette (Catppuccin Mocha accents) ----
        BLUE = "#89b4fa"  # main formula text
        PEACH = "#fab387"  # original vector
        GREEN = "#a6e3a1"  # transformed vector
        PINK = "#f38ba8"  # matrix A
        TEAL = "#94e2d5"  # axes
        GRID = "#45475a"  # grid lines

        # ---- Title ----
        title_1 = Text(
            "Linear transformations as matrix multiplication", font_size=36, color=WHITE
        )
        title_1.move_to(UP * 3)

        # ---- Main formula text ----
        main_1 = Text("A · v = v′", font_size=48, color=BLUE)
        main_1.move_to(DOWN * 2.5)

        # ---- Coordinate grid (the "space") ----
        plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-1, 2, 1],
            x_length=5,
            y_length=3,
            background_line_style={"stroke_color": GRID, "stroke_width": 1},
            axis_config={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "include_ticks": False,
            },
        ).shift(DOWN * 0.35)
        origin_dot = Dot(plane.c2p(0, 0), radius=0.05, color=WHITE)

        # ---- Original vector v ----
        v_arrow = Arrow(
            plane.c2p(0, 0), plane.c2p(1, 1), buff=0, color=PEACH, stroke_width=5
        )
        v_label = MathTex(r"\vec{v}", color=PEACH).next_to(v_arrow, UR, buff=0.1)

        # ---- Matrix A ----
        mat_A = Matrix([["0", "-1"], ["1.2", "0.6"]], h_buff=0.9).set_color(PINK)
        A_name = MathTex("A", color=PINK).next_to(mat_A, UP, buff=0.2)
        mat_group = VGroup(mat_A, A_name).move_to(RIGHT * 4.4 + UP * 0.2)

        # ---- Transformed vector v' = A v ----
        v_prime = Arrow(
            plane.c2p(0, 0), plane.c2p(-1, 1.8), buff=0, color=GREEN, stroke_width=5
        )
        ghost = DashedLine(
            plane.c2p(0, 0),
            plane.c2p(1, 1),
            dash_length=0.15,
            stroke_width=2,
            color=PEACH,
        ).set_opacity(0.6)
        vprime_label = (
            MathTex(r"\vec{v}\,' = A\vec{v}", color=GREEN)
            .scale(0.8)
            .next_to(v_prime, UL, buff=0.1)
        )

        # ---- Animations ----
        self.play(Write(title_1), run_time=1.2)
        self.play(
            Create(plane),
            FadeIn(origin_dot),
            GrowFromCenter(main_1),
            run_time=1.4,
        )
        self.play(
            GrowFromCenter(v_arrow),
            FadeIn(v_label, shift=0.2 * DOWN),
            FadeIn(mat_group),
            run_time=1.4,
        )
        self.play(
            Transform(v_arrow, v_prime),
            FadeOut(v_label),
            FadeIn(ghost),
            FadeIn(vprime_label, shift=0.2 * DOWN),
            Circumscribe(mat_A, color=PEACH, buff=0.15),
            run_time=2.0,
        )
        self.play(Indicate(main_1, scale_factor=1.15, color=PEACH), run_time=1.0)
        self.wait(1.0)
        # --- Scene 2: Step 2: Most vectors change direction under transformation ---
        self.clear()

        # -- Palette (Catppuccin Mocha accents) --
        BG = "#181825"
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"

        self.camera.background_color = BG

        # -- Title --
        title_2 = Text(
            "Most vectors change direction under transformation",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # -- Axes --
        main_2 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=7.2,
            y_length=4.8,
            axis_config={
                "color": PEACH,
                "stroke_width": 2.0,
                "include_tip": True,
            },
        )

        # -- Vectors before the transformation --
        vecs = [
            ((1.0, 0.5), BLUE),
            ((2.0, 0.3), PINK),
            ((0.5, 1.5), GREEN),
            ((-1.5, 0.5), TEAL),
            ((1.5, -1.0), BLUE),
            ((-0.5, -1.5), PINK),
        ]

        arrows = VGroup(
            *[
                Arrow(
                    start=main_2.c2p(0, 0),
                    end=main_2.c2p(x, y),
                    buff=0,
                    color=c,
                    stroke_width=5,
                )
                for (x, y), c in vecs
            ]
        )

        # Faint ghost copies that stay behind at the original directions
        ghosts = VGroup(*[a.copy().set_opacity(0.25) for a in arrows])

        # -- Linear transformation: rotation (~58 degrees) + slight scale --
        T = [[0.5, -0.8], [0.8, 0.5]]

        # -- Animations --
        self.play(Write(title_2), run_time=1.0)
        self.play(Create(main_2), run_time=1.0)
        self.play(
            LaggedStart(*[GrowFromCenter(a) for a in arrows], lag_ratio=0.2),
            run_time=1.2,
        )
        self.play(FadeIn(ghosts), run_time=0.5)
        self.play(ApplyMatrix(T, arrows, about_point=ORIGIN), run_time=2.0)

        # Curved arrows swinging from the old directions to the new ones
        movers = [(ghosts[i], arrows[i]) for i in (0, 3, 5)]
        curved = VGroup(
            *[
                CurvedArrow(
                    g.get_end(),
                    a.get_end(),
                    angle=-TAU / 8,
                    color=a.get_color(),
                )
                for g, a in movers
            ]
        )
        map_label = MathTex(
            r"\vec{v} \;\mapsto\; A\vec{v}", font_size=40, color=WHITE
        ).move_to(DOWN * 3)

        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in curved], lag_ratio=0.25),
            FadeIn(map_label),
            run_time=1.0,
        )
        self.wait(0.3)
        # --- Scene 3: Step 3: Definition of eigenvectors: vectors that keep their direction ---
        self.clear()
        # --- Scene 3: Definition of eigenvectors: vectors that keep their direction ---

        BG = "#181825"
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"

        self.camera.background_color = BG

        # Title
        title = Text(
            "Definition of eigenvectors: vectors that keep their direction",
            font_size=30,
            color=WHITE,
        ).move_to(UP * 3)
        self.play(Write(title), run_time=1.0)

        # NumberLine used as a lambda-meter at the bottom edge
        main_3 = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
            include_tip=True,
            color=PINK,
        ).move_to(DOWN * 2.6)
        self.play(Create(main_3), run_time=1.0)

        lambda_dot = Dot(
            point=main_3.number_to_point(1.0),
            radius=0.1,
            color=BLUE,
        )
        self.play(FadeIn(lambda_dot), run_time=0.5)

        # Contrast: an ordinary vector that rotates under the transformation
        ordinary_vec = Arrow(
            start=ORIGIN,
            end=np.array([2.0, 1.0, 0.0]),
            buff=0.0,
            stroke_width=4,
            color=PEACH,
        )
        push_hint = CurvedArrow(
            start_point=ordinary_vec.get_end(),
            end_point=ordinary_vec.get_end() + np.array([-1.0, 1.0, 0.0]),
            color=BLUE,
        )
        self.play(GrowFromCenter(ordinary_vec), run_time=0.8)
        self.play(FadeIn(push_hint), run_time=0.3)
        self.play(
            Rotate(ordinary_vec, angle=-PI / 3, about_point=ORIGIN),
            FadeOut(push_hint),
            run_time=1.2,
        )
        self.play(FadeOut(ordinary_vec), run_time=0.5)

        # Payoff: an eigenvector only stretches, keeping its direction
        eigenline = DashedLine(
            start=np.array([-4.0, -2.0, 0.0]),
            end=np.array([4.0, 2.0, 0.0]),
            dash_length=0.2,
            color=GREEN,
        )
        eigenvector = Arrow(
            start=ORIGIN,
            end=np.array([2.0, 1.0, 0.0]),
            buff=0.0,
            stroke_width=4,
            color=GREEN,
        )
        self.play(Create(eigenline), run_time=0.7)
        self.play(GrowFromCenter(eigenvector), run_time=0.8)

        stretched = Arrow(
            start=ORIGIN,
            end=np.array([4.0, 2.0, 0.0]),
            buff=0.0,
            stroke_width=4,
            color=GREEN,
        )
        ghost = DashedLine(
            start=ORIGIN,
            end=np.array([2.0, 1.0, 0.0]),
            dash_length=0.15,
            color=TEAL,
        )
        self.play(ReplacementTransform(eigenvector, stretched), run_time=1.0)
        self.add(ghost)
        self.play(FadeOut(ghost), run_time=0.3)

        lambda_label = MathTex(r"\lambda = 2", color=BLUE).scale(0.8)
        lambda_label.next_to(main_3, UP, buff=0.2)
        lambda_label.to_edge(LEFT, buff=1.0)
        self.play(FadeIn(lambda_label), run_time=0.5)
        self.play(
            lambda_dot.animate.move_to(main_3.number_to_point(2.0)),
            run_time=1.0,
        )

        flash = ShowPassingFlash(
            eigenline.copy().set_color(TEAL),
            time_width=0.5,
        )
        self.play(flash, run_time=1.0)
        self.wait(0.2)
        # --- Scene 4: Step 4: Eigenvalues as the scaling factor ---
        self.clear()
        self.camera.background_color = "#181825"

        GREEN_C = "#a6e3a1"
        ORANGE_C = "#fab387"

        # Title
        title = Text("Eigenvalues as the scaling factor", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Main VGroup: original eigenvector arrow with dot at origin
        v_orig = Arrow(
            ORIGIN,
            RIGHT * 1.5 + UP * 0.75,
            buff=0,
            color=GREEN_C,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.5,
        )
        v_label = MathTex(r"\mathbf{v}", font_size=48, color=GREEN_C)
        v_label.next_to(v_orig.get_end(), UP, buff=0.2)
        origin_dot = Dot(ORIGIN, radius=0.08, color=WHITE)
        main_4 = VGroup(v_orig, v_label, origin_dot)
        main_4.move_to(ORIGIN + DOWN * 0.3)

        # Scaled eigenvector (eigenvalue lambda = 2)
        start_pt = v_orig.get_start()
        scaled_end = start_pt + v_orig.get_vector() * 2
        v_scaled = Arrow(
            start_pt,
            scaled_end,
            buff=0,
            color=ORANGE_C,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.3,
        )

        lam_label = MathTex(
            r"A\mathbf{v} = \lambda \mathbf{v}", font_size=48, color=WHITE
        )
        lam_label.move_to(DOWN * 2.5)
        lam_val = MathTex(r"\lambda = 2", font_size=48, color=ORANGE_C)
        lam_val.next_to(lam_label, RIGHT, buff=0.6)

        # Timeline (7.0s total)
        self.play(Write(title), run_time=1.0)  # 1.0
        self.play(
            GrowFromCenter(v_orig), FadeIn(v_label), FadeIn(origin_dot), run_time=1.2
        )  # 2.2
        self.wait(0.8)  # 3.0
        self.play(TransformFromCopy(v_orig, v_scaled), run_time=1.5)  # 4.5
        self.play(FadeIn(lam_label, shift=UP * 0.3), run_time=1.0)  # 5.5
        self.play(FadeIn(lam_val, shift=UP * 0.3), run_time=0.5)  # 6.0
        self.play(Circumscribe(lam_label, color=ORANGE_C), run_time=0.8)  # 6.8
        self.wait(0.2)  # 7.0
        # --- Scene 5: Step 5: The eigenvalue equation Av = λv ---
        self.clear()
        # --- Scene 5: Step 5: The eigenvalue equation Av = λv ---
        self.camera.background_color = "#181825"

        # Title
        title = Text("The eigenvalue equation Av = \u03bbv", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Color-coded central equation: A v = lambda v
        eq = MathTex(r"A", r"\vec{v}", r"=", r"\lambda", r"\vec{v}")
        eq[0].set_color("#89b4fa")  # A
        eq[1].set_color("#fab387")  # v
        eq[3].set_color("#f38ba8")  # lambda
        eq[4].set_color("#fab387")  # v
        eq.scale(2.0)
        eq.move_to(UP * 0.5)

        # Main Table (as specified in the storyboard)
        table = Table(
            [
                [
                    r"A = \begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}",
                    r"\vec{v}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}",
                    r"\lambda_1 = 2",
                ]
            ],
            include_outer_lines=True,
            line_config={"stroke_color": "#94e2d5", "stroke_width": 2.0},
            element_to_mobject=MathTex,
        ).scale(0.9)
        table.move_to(DOWN * 2)

        # Apply entry colors after construction (Table indexing is 1-based)
        table.get_entries((1, 1)).set_color("#a6e3a1")  # Matrix A
        table.get_entries((1, 2)).set_color("#fab387")  # Eigenvector
        table.get_entries((1, 3)).set_color("#f38ba8")  # Eigenvalue

        # Supporting column labels
        col_labels = VGroup(
            Text("Matrix A", font_size=24, color="#94e2d5"),
            Text("Eigenvector", font_size=24, color="#94e2d5"),
            Text("Eigenvalue", font_size=24, color="#94e2d5"),
        ).arrange(RIGHT, buff=1.8)
        col_labels.move_to(table.get_top() + UP * 0.5)

        # Curved arrow connecting the equation to its concrete example
        arrow = CurvedArrow(
            eq.get_bottom() + LEFT * 0.2,
            table.get_top() + LEFT * 2.6,
            color="#94e2d5",
            angle=-TAU / 6,
        )

        # Animations (total = 10s)
        self.play(Write(title), run_time=2.0)
        self.play(GrowFromCenter(eq), run_time=2.0)
        self.play(Create(arrow), run_time=1.0)
        self.play(FadeIn(col_labels, shift=DOWN * 0.3), run_time=1.0)
        self.play(GrowFromCenter(table), run_time=2.0)
        self.wait(2.0)
        # --- Scene 6: Step 6: Deriving the characteristic equation ---
        self.clear()
        self.camera.background_color = "#181825"

        C_TEXT = "#cdd6f4"
        C_BLUE = "#89b4fa"
        C_ORANGE = "#fab387"
        C_RED = "#f38ba8"
        C_GREEN = "#a6e3a1"
        C_TEAL = "#94e2d5"

        # Title
        title = Text("Deriving the characteristic equation", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Starting eigenvalue equation
        eq_start = MathTex(r"A\vec{v}", r"=", r"\lambda\vec{v}", font_size=60)
        eq_start[0].set_color(C_BLUE)
        eq_start[2].set_color(C_ORANGE)
        eq_start.move_to(UP * 1.4)

        # Step 1: move lambda*v to the left
        eq_step1 = MathTex(
            r"A\vec{v}",
            r"-",
            r"\lambda\vec{v}",
            r"=",
            r"\vec{0}",
            font_size=60,
        )
        eq_step1[0].set_color(C_BLUE)
        eq_step1[2].set_color(C_ORANGE)
        eq_step1[4].set_color(C_RED)
        eq_step1.move_to(UP * 1.4)

        # Step 2: factor out v
        eq_step2 = MathTex(
            r"(A",
            r"-",
            r"\lambda I",
            r")\vec{v}",
            r"=",
            r"\vec{0}",
            font_size=60,
        )
        eq_step2[0].set_color(C_BLUE)
        eq_step2[2].set_color(C_ORANGE)
        eq_step2[3].set_color(C_GREEN)
        eq_step2[5].set_color(C_RED)
        eq_step2.move_to(UP * 1.4)

        # Main arrow at ORIGIN (storyboard object main_6)
        main_arrow = Arrow(
            start=LEFT * 4.5,
            end=RIGHT * 4.5,
            buff=0,
            stroke_width=6,
            color=C_TEXT,
        )
        main_arrow.move_to(ORIGIN)
        condition = MathTex(r"\vec{v}", r"\neq", r"\vec{0}", font_size=44)
        condition[0].set_color(C_GREEN)
        condition[2].set_color(C_RED)
        condition.next_to(main_arrow, DOWN, buff=0.25)
        label_left = Text("nonzero solutions", font_size=26, color=C_TEAL)
        label_left.next_to(main_arrow, UP, buff=0.25).shift(LEFT * 1.8)
        label_right = Text("require", font_size=26, color=C_TEAL)
        label_right.next_to(main_arrow, UP, buff=0.25).shift(RIGHT * 1.8)

        # Final characteristic equation
        eq_final = MathTex(
            r"\det(A",
            r"-",
            r"\lambda I",
            r")",
            r"=",
            r"0",
            font_size=72,
        )
        eq_final[0].set_color(C_BLUE)
        eq_final[2].set_color(C_ORANGE)
        eq_final[4].set_color(C_RED)
        eq_final.move_to(DOWN * 1.6)

        box = SurroundingRectangle(eq_final, color=C_GREEN, buff=0.35)
        caption = Text("the characteristic equation", font_size=28, color=C_GREEN)
        caption.next_to(box, DOWN, buff=0.3)

        # --- Animations (total 11.0s) ---
        self.play(Write(title), run_time=0.5)
        self.play(Write(eq_start), run_time=1.0)
        self.wait(0.5)

        self.play(ReplacementTransform(eq_start, eq_step1), run_time=1.5)
        self.wait(0.5)

        self.play(ReplacementTransform(eq_step1, eq_step2), run_time=1.5)
        self.play(Indicate(eq_step2[0:3], color=C_TEAL), run_time=0.5)

        # Build the arrow: derivation -> requirement
        self.play(
            GrowFromCenter(main_arrow),
            FadeIn(condition),
            run_time=1.5,
        )
        self.play(FadeIn(label_left), FadeIn(label_right), run_time=0.5)
        self.wait(0.5)

        # Reveal determinant condition
        self.play(Write(eq_final), run_time=1.5)
        self.play(Create(box), FadeIn(caption), run_time=0.5)
        self.wait(0.5)
        # --- Scene 7: Step 7: Solving the characteristic polynomial ---
        self.clear()

        # Palette
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"

        self.camera.background_color = "#181825"

        # --- Objects ---
        title_7 = Text(
            "Solving the characteristic polynomial",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        main_7 = Text(
            "det(A - \u03bbI) = 0",
            font_size=48,
            color=BLUE,
        ).move_to(ORIGIN)

        poly = MathTex(
            r"\lambda^2",
            r"-",
            r"5\lambda",
            r"+",
            r"6",
            r"=",
            r"0",
        ).move_to(ORIGIN)
        poly[0].set_color(BLUE)

        factored = MathTex(
            r"(\lambda - 2)",
            r"(\lambda - 3)",
            r"= 0",
        ).move_to(ORIGIN)
        factored[0].set_color(PEACH)
        factored[1].set_color(PINK)

        ev_label = Text("Eigenvalues of A", font_size=30, color=GREEN)
        ev1 = MathTex(r"\lambda_1 = 2", color=PEACH)
        ev2 = MathTex(r"\lambda_2 = 3", color=PINK)
        eigen_row = VGroup(ev1, ev2).arrange(RIGHT, buff=1.4)
        eigen_block = VGroup(ev_label, eigen_row).arrange(DOWN, buff=0.4)
        eigen_block.move_to(DOWN * 2.2)

        arrow1 = CurvedArrow(
            factored[0].get_bottom() + DOWN * 0.05,
            ev1.get_top() + UP * 0.05,
            angle=TAU / 8,
            color=PEACH,
            stroke_width=2,
            tip_length=0.15,
        )
        arrow2 = CurvedArrow(
            factored[1].get_bottom() + DOWN * 0.05,
            ev2.get_top() + UP * 0.05,
            angle=TAU / 8,
            color=PINK,
            stroke_width=2,
            tip_length=0.15,
        )

        # --- Animations ---
        self.play(Write(title_7), run_time=1.0)
        self.play(GrowFromCenter(main_7), run_time=1.0)
        self.wait(0.3)
        self.play(ReplacementTransform(main_7, poly), run_time=1.2)
        self.wait(0.3)
        self.play(ReplacementTransform(poly, factored), run_time=1.2)
        self.wait(0.2)
        self.play(
            LaggedStart(
                GrowFromCenter(ev_label),
                GrowFromCenter(ev1),
                GrowFromCenter(ev2),
                Create(arrow1),
                Create(arrow2),
                lag_ratio=0.25,
            ),
            run_time=1.5,
        )
        self.play(Circumscribe(eigen_row, color=GREEN), run_time=0.9)
        self.wait(1.4)
        # --- Scene 8: Step 8: Finding eigenvectors for each eigenvalue ---
        self.clear()
        # --- Scene 8: Step 8: Finding eigenvectors for each eigenvalue ---
        self.camera.background_color = "#181825"

        # ---------- Palette ----------
        blue = "#89b4fa"
        peach = "#fab387"
        red = "#f38ba8"
        green = "#a6e3a1"
        teal = "#94e2d5"

        # ---------- Title ----------
        title = Text(
            "Finding eigenvectors for each eigenvalue",
            font_size=36,
            color=WHITE,
        )
        title.move_to(UP * 3)

        # ---------- Main Axes ----------
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=9,
            y_length=5,
            axis_config={
                "color": peach,
                "stroke_width": 2.0,
                "include_tip": True,
                "tip_width": 0.18,
                "tip_height": 0.18,
            },
        )
        axes.move_to(ORIGIN + DOWN * 0.2)
        x_label = MathTex("x", font_size=30, color=peach)
        x_label.next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = MathTex("y", font_size=30, color=peach)
        y_label.next_to(axes.y_axis.get_end(), UP, buff=0.2)

        # ---------- Key equation (the "recipe") ----------
        eq = MathTex(
            r"(A - \lambda I)\,\vec{v} = \vec{0}",
            font_size=44,
            color=WHITE,
        )
        eq.to_corner(DL, buff=0.5)

        # ---------- Eigenvalue 1: lambda_1 = 3, direction (1, 1) ----------
        # Dashed infinite line = the null space line for lambda_1
        line1 = DashedLine(
            axes.c2p(-2.4, -1.6),
            axes.c2p(2.4, 1.6),
            dash_length=0.12,
            color=blue,
            stroke_width=2.0,
        )
        vec1 = Arrow(
            ORIGIN,
            axes.c2p(1.6, 1.07),
            buff=0,
            color=blue,
            stroke_width=6,
            tip_length=0.25,
        )
        label1 = MathTex(
            r"\lambda_1 = 3:\;\; \vec{v}_1 \propto \begin{bmatrix} 1 \\ 1 \end{bmatrix}",
            font_size=34,
            color=blue,
        )
        label1.next_to(vec1.get_end(), UR, buff=0.15)

        # ---------- Eigenvalue 2: lambda_2 = 1, direction (1, -1) ----------
        line2 = DashedLine(
            axes.c2p(-2.4, 1.6),
            axes.c2p(2.4, -1.6),
            dash_length=0.12,
            color=red,
            stroke_width=2.0,
        )
        vec2 = Arrow(
            ORIGIN,
            axes.c2p(1.6, -1.07),
            buff=0,
            color=red,
            stroke_width=6,
            tip_length=0.25,
        )
        label2 = MathTex(
            r"\lambda_2 = 1:\;\; \vec{v}_2 \propto \begin{bmatrix} 1 \\ -1 \end{bmatrix}",
            font_size=34,
            color=red,
        )
        label2.next_to(vec2.get_end(), DR, buff=0.15)

        # ---------- Null space annotation ----------
        null_note = Text(
            "Solve the null space for each lambda",
            font_size=24,
            color=green,
        )
        null_note.to_corner(DR, buff=0.5)

        origin_dot = Dot(ORIGIN + DOWN * 0.2, radius=0.07, color=teal)

        # ---------- Animation sequence (total = 9.0s) ----------
        # 1.0 + 1.5 + 1.0 + 2.0 + 1.0 + 1.0 + 0.5 + 0.5 + 0.5 = 9.0
        self.play(Write(title), run_time=1.0)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.5)
        self.play(GrowFromCenter(origin_dot), FadeIn(eq, shift=UP * 0.3), run_time=1.0)

        # Lambda 1: substitute back, get null-space line and eigenvector
        self.play(
            Create(line1),
            GrowFromCenter(vec1),
            Write(label1),
            run_time=2.0,
        )
        self.play(Circumscribe(eq, color=blue), run_time=1.0)

        # Lambda 2: substitute back, get second null-space line
        self.play(
            Create(line2),
            GrowFromCenter(vec2),
            Write(label2),
            run_time=1.0,
        )
        self.play(FadeIn(null_note, shift=LEFT * 0.5), run_time=0.5)
        self.play(
            Circumscribe(label1, color=blue),
            Circumscribe(label2, color=red),
            run_time=0.5,
        )
        self.wait(0.5)
        # --- Scene 9: Step 9: Eigenbasis and diagonalization ---
        self.clear()
        self.camera.background_color = "#181825"

        blue = "#89b4fa"
        peach = "#fab387"
        red = "#f38ba8"
        green = "#a6e3a1"
        teal = "#94e2d5"

        # ---------- Title ----------
        title = Text("Eigenbasis and diagonalization", font_size=36, color=WHITE)
        title.move_to(UP * 3)
        self.play(Write(title), run_time=1.0)

        # ---------- Eigenbasis: two eigenvectors spanning the space ----------
        origin = LEFT * 3.2 + DOWN * 0.2
        v1 = Arrow(
            origin,
            origin + RIGHT * 1.6 + UP * 1.6,
            buff=0,
            stroke_width=4.0,
            color=blue,
            tip_length=0.25,
        )
        v2 = Arrow(
            origin,
            origin + LEFT * 1.6 + UP * 1.6,
            buff=0,
            stroke_width=4.0,
            color=peach,
            tip_length=0.25,
        )
        v1_label = MathTex(r"\vec{v}_1", font_size=36, color=blue)
        v1_label.next_to(v1.get_end(), RIGHT, buff=0.15)
        v2_label = MathTex(r"\vec{v}_2", font_size=36, color=peach)
        v2_label.next_to(v2.get_end(), LEFT, buff=0.15)

        self.play(
            LaggedStart(GrowFromCenter(v1), GrowFromCenter(v2), lag_ratio=0.5),
            run_time=1.0,
        )
        self.play(FadeIn(v1_label), FadeIn(v2_label), run_time=0.5)

        eb_caption = Text("eigenbasis", font_size=28, color=teal)
        eb_caption.next_to(VGroup(v1, v2), DOWN, buff=0.25)
        self.play(FadeIn(eb_caption), run_time=0.5)

        # ---------- Number line with eigenvalues as scale factors ----------
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            color=red,
            include_numbers=False,
            stroke_width=2.0,
            font_size=24,
        )
        number_line.move_to(DOWN * 2.3)
        self.play(Create(number_line), run_time=1.0)

        dot1 = Dot(number_line.n2p(2), radius=0.1, color=green)
        dot2 = Dot(number_line.n2p(3), radius=0.1, color=green)
        lam1 = MathTex(r"\lambda_1 = 2", font_size=30, color=green)
        lam1.next_to(dot1, UP, buff=0.15).shift(LEFT * 0.7)
        lam2 = MathTex(r"\lambda_2 = 3", font_size=30, color=green)
        lam2.next_to(dot2, UP, buff=0.15).shift(RIGHT * 0.7)
        self.play(
            FadeIn(dot1, scale=0.1),
            FadeIn(dot2, scale=0.1),
            GrowFromCenter(lam1),
            GrowFromCenter(lam2),
            run_time=1.0,
        )

        # ---------- Diagonalization equation ----------
        eq = MathTex(r"A", "=", "P", "D", "P^{-1}", font_size=48)
        eq.move_to(RIGHT * 2.9 + UP * 1.3)
        self.play(Write(eq), run_time=1.0)

        d_matrix = MathTex(
            r"D = \begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}",
            font_size=44,
            color=green,
        )
        d_matrix.next_to(eq, DOWN, buff=0.6)
        self.play(Write(d_matrix), run_time=1.0)

        # Highlight: D is just scaling along the eigenbasis
        self.play(Indicate(d_matrix, color=green, scale_factor=1.1), run_time=1.0)
        self.play(
            Circumscribe(VGroup(v1, v2, eb_caption), color=teal, buff=0.15),
            run_time=1.0,
        )

        self.wait(1.0)
        # --- Scene 10: Step 10: Applications of eigenvectors ---
        self.clear()
        self.camera.background_color = "#181825"

        # Catppuccin-style palette
        blue = "#89b4fa"
        peach = "#fab387"
        pink = "#f38ba8"
        green = "#a6e3a1"
        teal = "#94e2d5"
        text_color = "#cdd6f4"

        # ---------- Title ----------
        title = Text("Applications of eigenvectors", font_size=36, color=WHITE)
        title.move_to(UP * 3)
        underline = Line(LEFT * 3.2, RIGHT * 3.2, color=green, stroke_width=3)
        underline.next_to(title, DOWN, buff=0.18)

        # ---------- Card builder ----------
        def make_card(icon, name, subtitle, color):
            label = Text(name, font_size=26, color=color)
            sub = Text(subtitle, font_size=17, color=text_color)
            content = VGroup(icon, label, sub).arrange(DOWN, buff=0.3)
            box = SurroundingRectangle(
                content, color=color, buff=0.35, corner_radius=0.15, stroke_width=2
            )
            return VGroup(box, content)

        # ---------- Icon 1: PCA (data cloud + principal axis) ----------
        pts = [
            (-1.0, -0.62),
            (-0.72, -0.35),
            (-0.45, -0.52),
            (-0.2, -0.12),
            (0.05, 0.02),
            (0.3, 0.3),
            (0.6, 0.18),
            (0.9, 0.5),
        ]
        pca_dots = VGroup(
            *[Dot(point=np.array([x, y, 0.0]), radius=0.06, color=blue) for x, y in pts]
        )
        pca_axis = DashedLine(
            start=np.array([-1.15, -0.78, 0.0]),
            end=np.array([1.05, 0.68, 0.0]),
            color=green,
            stroke_width=3,
            dash_length=0.12,
        )
        pca_icon = VGroup(pca_dots, pca_axis)

        # ---------- Icon 2: PageRank (web graph) ----------
        a_pos = np.array([-0.95, -0.45, 0.0])
        b_pos = np.array([0.95, -0.45, 0.0])
        c_pos = np.array([0.0, 0.75, 0.0])
        node_a = Circle(radius=0.26, color=peach, stroke_width=2.5).move_to(a_pos)
        node_b = Circle(radius=0.26, color=peach, stroke_width=2.5).move_to(b_pos)
        node_c = Circle(radius=0.26, color=peach, stroke_width=2.5).move_to(c_pos)
        node_a.set_fill(peach, opacity=0.25)
        node_b.set_fill(peach, opacity=0.25)
        node_c.set_fill(peach, opacity=0.25)
        link_ab = CurvedArrow(
            a_pos + np.array([0.3, 0.0, 0.0]),
            b_pos + np.array([-0.3, 0.0, 0.0]),
            angle=-TAU / 8,
            color=peach,
            stroke_width=2.5,
            tip_length=0.15,
        )
        link_bc = CurvedArrow(
            b_pos + np.array([-0.2, 0.25, 0.0]),
            c_pos + np.array([0.35, -0.1, 0.0]),
            angle=TAU / 8,
            color=peach,
            stroke_width=2.5,
            tip_length=0.15,
        )
        link_ca = CurvedArrow(
            c_pos + np.array([-0.35, -0.1, 0.0]),
            a_pos + np.array([0.2, 0.25, 0.0]),
            angle=TAU / 8,
            color=peach,
            stroke_width=2.5,
            tip_length=0.15,
        )
        pagerank_icon = VGroup(node_a, node_b, node_c, link_ab, link_bc, link_ca)

        # ---------- Icon 3: Stability (vectors converging to equilibrium) ----------
        stable_center = Dot(ORIGIN, radius=0.09, color=teal)
        stable_arrows = VGroup(
            *[
                Arrow(
                    np.array([dx, dy, 0.0]) * 1.15,
                    np.array([dx, dy, 0.0]) * 0.22,
                    buff=0,
                    color=pink,
                    stroke_width=3,
                    tip_length=0.15,
                )
                for dx, dy in [(1.0, 0.6), (-1.0, 0.6), (1.0, -0.6), (-1.0, -0.6)]
            ]
        )
        stable_icon = VGroup(stable_arrows, stable_center)

        # ---------- Assemble the three application cards ----------
        card_pca = make_card(pca_icon, "PCA", "Principal Component Analysis", blue)
        card_pagerank = make_card(
            pagerank_icon, "PageRank", "Google's web ranking", peach
        )
        card_stability = make_card(stable_icon, "Stability", "Dynamical systems", teal)

        main_10 = VGroup(card_pca, card_pagerank, card_stability)
        main_10.arrange(RIGHT, buff=0.55)
        main_10.move_to(DOWN * 0.55)

        # ---------- Animations (total = 7.0 s) ----------
        self.play(Write(title), Create(underline), run_time=1.0)
        self.play(
            LaggedStart(
                GrowFromCenter(card_pca),
                GrowFromCenter(card_pagerank),
                GrowFromCenter(card_stability),
                lag_ratio=0.35,
            ),
            run_time=2.0,
        )
        self.play(
            LaggedStart(
                Indicate(card_pca, color=WHITE, scale_factor=1.06),
                Indicate(card_pagerank, color=WHITE, scale_factor=1.06),
                Indicate(card_stability, color=WHITE, scale_factor=1.06),
                lag_ratio=0.5,
            ),
            run_time=2.5,
        )
        self.wait(1.5)
