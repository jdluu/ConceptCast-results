from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # --- SCENE 1: Introduction to Linear Transformations ---
        # Goal: Establish that matrices move vectors.
        title = Text("Linear Transformations", color=BLUE).to_edge(UP)
        grid = NumberPlane()
        vec = Arrow(start=ORIGIN, end=[1, 1, 0], color=YELLOW)
        vec_label = MathTex(r"\vec{v}", color=YELLOW).next_to(vec.get_end(), RIGHT)
        
        self.play(Write(title))
        self.play(Create(grid))
        self.play(GrowFromCenter(vec), Write(vec_label))
        self.wait(1)

        # Apply a shear transformation matrix [[1, 1], [0, 1]]
        matrix = [[1, 1], [0, 1]]
        self.play(
            title.animate.set_text("Transforming the Space"),
            grid.animate.apply_matrix(matrix),
            vec.animate.apply_matrix(matrix),
            vec_label.animate.shift(RIGHT * 1),
            run_time=2
        )
        self.wait(2)
        self.play(FadeOut(title), FadeOut(grid), FadeOut(vec), FadeOut(vec_label))
        self.clear()

        # --- SCENE 2: The Concept of Directional Change ---
        # Goal: Show that most vectors change direction.
        title = Text("Do all vectors change direction?", color=WHITE).to_edge(UP)
        grid = NumberPlane()
        
        v1 = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED)
        v2 = Arrow(start=ORIGIN, end=[0, 1, 0], color=GREEN)
        v3 = Arrow(start=ORIGIN, end=[-1, 1, 0], color=PURPLE)
        
        self.play(Write(title))
        self.play(Create(grid))
        self.play(GrowFromCenter(v1), GrowFromCenter(v2), GrowFromCenter(v3))
        self.wait(1)

        # Apply a scaling/shear: [[2, 1], [0, 1]]
        mat2 = [[2, 1], [0, 1]]
        self.play(
            grid.animate.apply_matrix(mat2),
            v1.animate.apply_matrix(mat2),
            v2.animate.apply_matrix(mat2),
            v3.animate.apply_matrix(mat2),
            run_time=2
        )
        
        # Highlighting that v1 stayed on its line, v2 and v3 rotated
        self.play(v2.animate.set_color(GRAY), v3.animate.set_color(GRAY))
        self.play(v1.animate.set_color(YELLOW), run_time=1)
        
        self.wait(2)
        self.play(FadeOut(title), FadeOut(grid), FadeOut(v1), FadeOut(v2), FadeOut(v3))
        self.clear()

        # --- SCENE 3: Defining the Eigenvector ---
        # Goal: Formal definition of an eigenvector.
        title = Text("The Eigenvector", color=YELLOW).to_edge(UP)
        formula = MathTex(r"A\vec{v} = \lambda\vec{v}", font_size=72).shift(UP * 0.5)
        desc = Text("The vector only scales; it does not rotate.", font_size=30).next_to(formula, DOWN)
        
        self.play(Write(title))
        self.play(Write(formula))
        self.play(FadeIn(desc))
        self.wait(2)
        
        # Visualizing the equality
        grid = NumberPlane()
        v_orig = Arrow(start=ORIGIN, end=[1, 0, 0], color=YELLOW)
        v_trans = Arrow(start=ORIGIN, end=[3, 0, 0], color=ORANGE)
        v_label_orig = MathTex(r"\vec{v}", color=YELLOW).next_to(v_orig.get_end(), RIGHT)
        v_label_trans = MathTex(r"\lambda\vec{v}", color=ORANGE).next_to(v_trans.get_end(), RIGHT)
        
        self.play(Create(grid))
        self.play(GrowFromCenter(v_orig), Write(v_label_orig))
        self.play(Transform(v_orig.copy(), v_trans), Write(v_label_trans))
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(formula), FadeOut(desc), FadeOut(grid), FadeOut(v_orig), FadeOut(v_trans), FadeOut(v_label_orig), FadeOut(v_label_trans))
        self.clear()

        # --- SCENE 4: Understanding the Eigenvalue (Lambda) ---
        # Goal: Show that lambda can be > 1, < 1, or negative.
        title = Text("The Eigenvalue: $\lambda$", color=BLUE).to_edge(UP)
        grid = NumberPlane()
        v_base = Arrow(start=ORIGIN, end=[1, 1, 0], color=WHITE)
        
        self.play(Write(title), Create(grid), GrowFromCenter(v_base))
        
        # Case 1: lambda = 2
        l1 = MathTex(r"\lambda = 2", color=GREEN).shift(RIGHT * 4 + UP * 1)
        v_scale1 = Arrow(start=ORIGIN, end=[2, 2, 0], color=GREEN)
        self.play(Write(l1), TransformFromCopy(v_base, v_scale1))
        self.wait(1)
        self.play(FadeOut(l1), FadeOut(v_scale1))

        # Case 2: lambda = 0.5
        l2 = MathTex(r"\lambda = 0.5", color=RED).shift(RIGHT * 4 + UP * 1)
        v_scale2 = Arrow(start=ORIGIN, end=[0.5, 0.5, 0], color=RED)
        self.play(Write(l2), TransformFromCopy(v_base, v_scale2))
        self.wait(1)
        self.play(FadeOut(l2), FadeOut(v_scale2))

        # Case 3: lambda = -1
        l3 = MathTex(r"\lambda = -1", color=PURPLE).shift(RIGHT * 4 + UP * 1)
        v_scale3 = Arrow(start=ORIGIN, end=[-1, -1, 0], color=PURPLE)
        self.play(Write(l3), TransformFromCopy(v_base, v_scale3))
        self.wait(1)
        
        self.play(FadeOut(title), FadeOut(grid), FadeOut(v_base), FadeOut(v_scale3), FadeOut(l3))
        self.clear()

        # --- SCENE 5: Finding Eigenvectors Graphically ---
        # Goal: Demonstrate a real matrix and its eigenvectors.
        title = Text("Example: A = [[2, 1], [1, 2]]", color=WHITE).to_edge(UP)
        grid = NumberPlane()
        
        # For this matrix, eigenvectors are [1,1] (lambda=3) and [1,-1] (lambda=1)
        ev1 = Arrow(start=ORIGIN, end=[1, 1, 0], color=YELLOW)
        ev2 = Arrow(start=ORIGIN, end=[1, -1, 0], color=BLUE)
        label1 = MathTex(r"\vec{v}_1", color=YELLOW).next_to(ev1.get_end(), UR)
        label2 = MathTex(r"\vec{v}_2", color=BLUE).next_to(ev2.get_end(), DR)
        
        self.play(Write(title), Create(grid))
        self.play(GrowFromCenter(ev1), GrowFromCenter(ev2), Write(label1), Write(label2))
        self.wait(1)
        
        matrix = [[2, 1], [1, 2]]
        self.play(
            grid.animate.apply_matrix(matrix),
            ev1.animate.apply_matrix(matrix),
            ev2.animate.apply_matrix(matrix),
            label1.animate.shift(UP * 2 + RIGHT * 2),
            label2.animate.shift(DOWN * 2 + RIGHT * 2),
            run_time=3
        )
        
        # Visual proof: they stayed on their lines
        line1 = Line(start=[-2, -2, 0], end=[2, 2, 0], color=YELLOW, stroke_opacity=0.3)
        line2 = Line(start=[-2, 2, 0], end=[2, -2, 0], color=BLUE, stroke_opacity=0.3)
        self.play(Create(line1), Create(line2))
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(grid), FadeOut(ev1), FadeOut(ev2), FadeOut(label1), FadeOut(label2), FadeOut(line1), FadeOut(line2))
        self.clear()

        # --- SCENE 6: Summary and Final Takeaway ---
        # Goal: Wrap up the concepts.
        summary_title = Text("Summary", color=BLUE).to_edge(UP)
        point1 = Text("1. Linear transformations move vectors.", font_size=32).shift(UP * 1)
        point2 = Text("2. Most vectors change direction.", font_size=32).next_to(point1, DOWN, buff=0.5)
        point3 = Text("3. Eigenvectors STAY on their span.", font_size=32, color=YELLOW).next_to(point2, DOWN, buff=0.5)
        point4 = Text("4. The scaling factor is the Eigenvalue.", font_size=32, color=GREEN).next_to(point3, DOWN, buff=0.5)
        
        self.play(Write(summary_title))
        self.play(Write(point1))
        self.wait(1)
        self.play(Write(point2))
        self.wait(1)
        self.play(Write(point3))
        self.wait(1)
        self.play(Write(point4))
        self.wait(3)
        
        self.play(FadeOut(summary_title), FadeOut(point1), FadeOut(point2), FadeOut(point3), FadeOut(point4))
