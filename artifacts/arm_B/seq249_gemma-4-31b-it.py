from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # --- SCENE 1: Introduction to Linear Transformations ---
        title = Text("Linear Transformations", color=WHITE).to_edge(UP)
        plane = NumberPlane()
        vec = Arrow(start=ORIGIN, end=[1, 1, 0], color=YELLOW)
        vec_label = MathTex(r"\vec{v}").next_to(vec.get_end(), DR, buff=0.1)
        
        self.play(Write(title), Create(plane))
        self.play(Create(vec), Write(vec_label))
        self.wait(1)
        
        # Apply a transformation matrix [[2, 1], [1, 1]]
        matrix = np.array([[2, 1], [1, 1]])
        new_vec_coords = np.dot(matrix, [1, 1])
        # Convert (2,) array to [x, y, 0] for Manim
        new_vec_end = [new_vec_coords[0], new_vec_coords[1], 0]
        new_vec = Arrow(start=ORIGIN, end=new_vec_end, color=BLUE)
        new_label = MathTex(r"T(\vec{v})").next_to(new_vec.get_end(), DR, buff=0.1)
        
        self.play(
            Transform(vec, new_vec),
            Transform(vec_label, new_label),
            run_time=2
        )
        self.wait(2)
        self.play(FadeOut(title), FadeOut(plane), FadeOut(vec), FadeOut(vec_label))

        # --- SCENE 2: The General Case (Rotation/Scaling) ---
        title2 = Text("Most vectors change direction", color=WHITE).to_edge(UP)
        plane2 = NumberPlane()
        
        v1 = Arrow(start=ORIGIN, end=[1, 0, 0], color=YELLOW)
        v2 = Arrow(start=ORIGIN, end=[0, 1, 0], color=YELLOW)
        
        # Matrix that shears and scales: [[1, 1], [0, 1]]
        m_shear = np.array([[1, 1], [0, 1]])
        
        v1_coords = np.dot(m_shear, [1, 0])
        v1_new = Arrow(start=ORIGIN, end=[v1_coords[0], v1_coords[1], 0], color=BLUE)
        
        v2_coords = np.dot(m_shear, [0, 1])
        v2_new = Arrow(start=ORIGIN, end=[v2_coords[0], v2_coords[1], 0], color=BLUE)
        
        self.play(Write(title2), Create(plane2))
        self.play(Create(v1), Create(v2))
        self.wait(1)
        
        self.play(
            Transform(v1, v1_new),
            Transform(v2, v2_new),
            run_time=2
        )
        self.wait(2)
        self.play(FadeOut(title2), FadeOut(plane2), FadeOut(v1), FadeOut(v2))

        # --- SCENE 3: The Special Case (Eigenvectors) ---
        title3 = Text("The Special Case: Eigenvectors", color=WHITE).to_edge(UP)
        plane3 = NumberPlane()
        
        # Matrix [[2, 0], [0, 1]] - Scale X by 2, Y by 1
        # Eigenvectors are [1,0] and [0,1]
        v_eigen = Arrow(start=ORIGIN, end=[1, 0, 0], color=GREEN)
        v_other = Arrow(start=ORIGIN, end=[1, 1, 0], color=YELLOW)
        
        v_eigen_new = Arrow(start=ORIGIN, end=[2, 0, 0], color=GREEN)
        v_other_new = Arrow(start=ORIGIN, end=[2, 1, 0], color=BLUE)
        
        self.play(Write(title3), Create(plane3))
        self.play(Create(v_eigen), Create(v_other))
        self.wait(1)
        
        self.play(
            Transform(v_eigen, v_eigen_new),
            Transform(v_other, v_other_new),
            run_time=2
        )
        
        note = Text("The green vector stayed on its own span!", font_size=24).to_edge(DOWN)
        self.play(Write(note))
        self.wait(2)
        self.play(FadeOut(title3), FadeOut(plane3), FadeOut(v_eigen), FadeOut(v_other), FadeOut(note))

        # --- SCENE 4: The Mathematical Definition ---
        title4 = Text("The Eigenvalue Equation", color=WHITE).to_edge(UP)
        eq = MathTex(r"A\vec{v} = \lambda\vec{v}", color=YELLOW, font_size=72).shift(UP*0.5)
        
        desc1 = Text("A: Transformation Matrix", font_size=30).next_to(eq, DOWN, buff=0.5).shift(LEFT*2)
        desc2 = Text("v: Eigenvector", font_size=30).next_to(eq, DOWN, buff=0.5).shift(RIGHT*1)
        desc3 = Text("λ: Eigenvalue (Scalar)", font_size=30).next_to(desc2, DOWN, buff=0.3)
        
        self.play(Write(title4))
        self.play(Write(eq))
        self.wait(1)
        self.play(FadeIn(desc1), FadeIn(desc2))
        self.wait(1)
        self.play(FadeIn(desc3))
        self.wait(3)
        self.play(FadeOut(title4), FadeOut(eq), FadeOut(desc1), FadeOut(desc2), FadeOut(desc3))

        # --- SCENE 5: Visualizing the Scalar Factor ---
        title5 = Text("Scaling by Eigenvalue λ", color=WHITE).to_edge(UP)
        plane5 = NumberPlane()
        
        # Let λ = 3
        v_base = Arrow(start=ORIGIN, end=[1, 1, 0], color=GREEN)
        v_scaled = Arrow(start=ORIGIN, end=[3, 3, 0], color=GREEN)
        
        lambda_text = MathTex(r"\lambda = 3", color=YELLOW).to_edge(RIGHT).shift(UP)
        
        self.play(Write(title5), Create(plane5))
        self.play(Create(v_base))
        self.play(Write(lambda_text))
        self.wait(1)
        
        self.play(Transform(v_base, v_scaled), run_time=2)
        self.play(Indicate(v_base))
        
        conclusion = Text("Direction is preserved, magnitude is scaled.", font_size=30).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(title5), FadeOut(plane5), FadeOut(v_base), FadeOut(lambda_text), FadeOut(conclusion))

        # --- SCENE 6: Summary Visual ---
        title6 = Text("Summary: Eigenvectors", color=WHITE).to_edge(UP)
        plane6 = NumberPlane()
        
        # Matrix [[1, 1], [0, 1]]
        # Eigenvector [1,0] eigenvalue 1
        v1_eig = Arrow(start=ORIGIN, end=[1, 0, 0], color=GREEN)
        v1_eig_new = Arrow(start=ORIGIN, end=[1, 0, 0], color=GREEN) # No change
        
        v2_non = Arrow(start=ORIGIN, end=[0, 1, 0], color=YELLOW)
        v2_non_new = Arrow(start=ORIGIN, end=[1, 1, 0], color=BLUE) # Changed direction
        
        self.play(Write(title6), Create(plane6))
        self.play(Create(v1_eig), Create(v2_non))
        self.wait(1)
        
        self.play(
            Transform(v1_eig, v1_eig_new),
            Transform(v2_non, v2_non_new),
            run_time=2
        )
        
        label_eig = Text("Eigenvector", font_size=20, color=GREEN).next_to(v1_eig.get_end(), DR)
        label_non = Text("Non-Eigenvector", font_size=20, color=BLUE).next_to(v2_non.get_end(), DR)
        
        self.play(Write(label_eig), Write(label_non))
        self.wait(3)
        
        # Final fade out
        self.play(FadeOut(title6), FadeOut(plane6), FadeOut(v1_eig), FadeOut(v2_non), FadeOut(label_eig), FadeOut(label_non))
