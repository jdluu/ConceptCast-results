from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction to linear transformations
        title = Text("Eigenvectors & Eigenvalues", font_size=48, color=YELLOW)
        subtitle = Text("The Secret of Transformations", font_size=28, color=BLUE)
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(subtitle))
        
        # Show a simple transformation: scaling
        grid = NumberPlane(
            x_range=[-4, 4], y_range=[-4, 4],
            x_length=6, y_length=6,
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(grid), runtime=2)
        
        vec = Vector([1, 2], color=RED)
        label = MathTex(r"\vec{v}", font_size=36, color=RED)
        label.next_to(vec.get_end(), UR)
        
        self.play(GrowArrow(vec), Write(label))
        self.wait()
        
        # Apply scaling transformation
        scale_mat = [[2, 0], [0, 2]]
        scaled_vec = Vector([2, 4], color=PURPLE)
        scaled_label = MathTex(r"2\vec{v}", font_size=36, color=PURPLE)
        scaled_label.next_to(scaled_vec.get_end(), UR)
        
        self.play(
            vec.animate.set_opacity(0.3),
            Transform(vec.copy(), scaled_vec),
            FadeIn(scaled_label)
        )
        self.wait(2)
        self.clear()
        
        # Scene 2: General linear transformation
        title2 = Text("What happens to most vectors?", font_size=36, color=YELLOW)
        self.play(Write(title2))
        self.wait(1)
        self.play(FadeOut(title2))
        
        grid2 = NumberPlane(
            x_range=[-4, 4], y_range=[-4, 4],
            x_length=6, y_length=6,
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(grid2))
        
        # Show multiple vectors
        vectors = []
        for i, (x, y) in enumerate([(1,0), (0,1), (1,1), (-1,2)]):
            color = [RED, GREEN, BLUE, ORANGE][i]
            vec = Vector([x, y], color=color)
            vectors.append(vec)
            self.play(GrowArrow(vec), runtime=0.3)
        
        self.wait()
        
        # Apply a rotation + shear transformation [1, 1; 0, 1]
        transform_mat = [[1, 1], [0, 1]]
        for vec in vectors:
            start = vec.get_start()
            end = vec.get_end()
            vec_vals = np.array([end[0]-start[0], end[1]-start[1]])
            new_vec = transform_mat @ vec_vals
            new_vector = Vector(new_vec, color=vec.get_color())
            self.play(
                vec.animate.shift(new_vector.get_start() - vec.get_start()),
                vec.animate.set_opacity(0.2),
                runtime=0.5
            )
        
        self.wait(2)
        self.clear()
        
        # Scene 3: The special vector
        title3 = Text("But some vectors are special...", font_size=36, color=YELLOW)
        self.play(Write(title3))
        self.wait(1)
        self.play(FadeOut(title3))
        
        grid3 = NumberPlane(
            x_range=[-4, 4], y_range=[-4, 4],
            x_length=6, y_length=6,
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(grid3))
        
        # Show eigenvector for shear transformation: [1, 1; 0, 1]
        # eigenvector [1, 0] with eigenvalue 1
        eig_vec = Vector([1, 0], color=YELLOW)
        eig_label = MathTex(r"\vec{v}", font_size=36, color=YELLOW)
        eig_label.next_to(eig_vec.get_end(), UR)
        
        self.play(GrowArrow(eig_vec), Write(eig_label))
        self.wait()
        
        # Apply same transformation, eigenvector only scales (stays same here)
        new_eig_vec = Vector([1, 0], color=ORANGE)
        new_eig_label = MathTex(r"\lambda\vec{v}", font_size=36, color=ORANGE)
        new_eig_label.next_to(new_eig_vec.get_end(), UR)
        
        self.play(
            eig_vec.animate.set_opacity(0.3).set_color(GRAY),
            Transform(eig_vec.copy(), new_eig_vec),
            FadeIn(new_eig_label)
        )
        self.wait(2)
        self.clear()
        
        # Scene 4: Definition of eigenvector
        title4 = Text("Definition: Eigenvector", font_size=36, color=YELLOW)
        self.play(Write(title4))
        self.wait(0.5)
        
        definition = MathTex(
            r"A\vec{v} = \lambda \vec{v}",
            font_size=60,
            color=BLUE
        )
        definition.next_to(title4, DOWN, buff=0.5)
        self.play(Write(definition))
        self.wait()
        
        annot1 = Text("Non-zero vector → only scaled", font_size=24, color=GREEN)
        annot1.next_to(definition, DOWN, buff=0.3)
        self.play(FadeIn(annot1))
        self.wait(2)
        self.clear()
        
        # Scene 5: Finding eigenvectors visually - rotation example
        title5 = Text("Rotation: No real eigenvectors", font_size=36, color=RED)
        self.play(Write(title5))
        self.wait(0.5)
        self.play(FadeOut(title5))
        
        grid5 = NumberPlane(
            x_range=[-4, 4], y_range=[-4, 4],
            x_length=6, y_length=6,
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(grid5))
        
        ref_vec = Vector([1, 0], color=BLUE)
        ref_label = MathTex(r"\vec{v}", font_size=36, color=BLUE)
        ref_label.next_to(ref_vec.get_end(), UR)
        self.play(GrowArrow(ref_vec), Write(ref_label))
        
        # Rotate by 90 degrees
        rotated_vec = Vector([0, 1], color=PURPLE)
        rotated_label = MathTex(r"R\vec{v}", font_size=36, color=PURPLE)
        rotated_label.next_to(rotated_vec.get_end(), UR)
        
        self.play(
            ref_vec.animate.set_opacity(0.3),
            Transform(ref_vec.copy(), rotated_vec),
            FadeIn(rotated_label)
        )
        self.wait()
        
        note = Text("Direction changed → not eigenvector", font_size=24, color=RED)
        note.next_to(rotated_label, DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(2)
        self.clear()
        
        # Scene 6: Stretching example with clear eigenvector
        title6 = Text("Stretching: Clear eigenvector", font_size=36, color=YELLOW)
        self.play(Write(title6))
        self.wait(0.5)
        self.play(FadeOut(title6))
        
        grid6 = NumberPlane(
            x_range=[-4, 4], y_range=[-4, 4],
            x_length=6, y_length=6,
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(grid6))
        
        # Eigenvector along y-axis for stretching
        eig_vec_y = Vector([0, 1], color=RED)
        eig_label_y = MathTex(r"\vec{e}_y", font_size=36, color=RED)
        eig_label_y.next_to(eig_vec_y.get_end(), RIGHT)
        self.play(GrowArrow(eig_vec_y), Write(eig_label_y))
        
        # Apply stretch matrix [[1, 0], [0, 3]]
        stretched = Vector([0, 3], color=ORANGE)
        stretched_label = MathTex(r"3\vec{e}_y", font_size=36, color=ORANGE)
        stretched_label.next_to(stretched.get_end(), RIGHT)
        
        self.play(
            eig_vec_y.animate.set_opacity(0.3),
            Transform(eig_vec_y.copy(), stretched),
            FadeIn(stretched_label)
        )
        self.wait(2)
        self.clear()
        
        # Scene 7: Multiple eigenvectors in one transformation
        title7 = Text("Multiple eigenvectors possible", font_size=36, color=YELLOW)
        self.play(Write(title7))
        self.wait(0.5)
        self.play(FadeOut(title7))
        
        grid7 = NumberPlane(
            x_range=[-4, 4], y_range=[-4, 4],
            x_length=6, y_length=6,
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(grid7))
        
        # Diagonal matrix [[2, 0], [0, 3]] - both axes are eigenvectors
        vec1 = Vector([1, 0], color=RED)
        vec2 = Vector([0, 1], color=GREEN)
        label1 = MathTex(r"\vec{e}_x", font_size=36, color=RED)
        label2 = MathTex(r"\vec{e}_y", font_size=36, color=GREEN)
        label1.next_to(vec1.get_end(), UR)
        label2.next_to(vec2.get_end(), RIGHT)
        
        self.play(GrowArrow(vec1), Write(label1))
        self.play(GrowArrow(vec2), Write(label2))
        self.wait()
        
        # Apply diagonal transformation
        diag_vec1 = Vector([2, 0], color=ORANGE)
        diag_vec2 = Vector([0, 3], color=PURPLE)
        diag_label1 = MathTex(r"2\vec{e}_x", font_size=36, color=ORANGE)
        diag_label2 = MathTex(r"3\vec{e}_y", font_size=36, color=PURPLE)
        diag_label1.next_to(diag_vec1.get_end(), UR)
        diag_label2.next_to(diag_vec2.get_end(), RIGHT)
        
        self.play(
            vec1.animate.set_opacity(0.3),
            vec2.animate.set_opacity(0.3),
            Transform(vec1.copy(), diag_vec1),
            Transform(vec2.copy(), diag_vec2),
            FadeIn(diag_label1),
            FadeIn(diag_label2)
        )
        self.wait(2)
        self.clear()
        
        # Scene 8: Negative eigenvalues
        title8 = Text("Can eigenvalues be negative?", font_size=36, color=YELLOW)
        self.play(Write(title8))
        self.wait(0.5)
        self.play(FadeOut(title8))
        
        grid8 = NumberPlane(
            x_range=[-4, 4], y_range=[-4, 4],
            x_length=6, y_length=6,
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(grid8))
        
        vec_neg = Vector([1, 0], color=RED)
        label_neg = MathTex(r"\vec{v}", font_size=36, color=RED)
        label_neg.next_to(vec_neg.get_end(), UR)
        self.play(GrowArrow(vec_neg), Write(label_neg))
        
        # Reflection matrix [[-1, 0], [0, 1]]
        reflected = Vector([-1, 0], color=BLUE)
        reflected_label = MathTex(r"-\vec{v}", font_size=36, color=BLUE)
        reflected_label.next_to(reflected.get_end(), UL)
        
        self.play(
            vec_neg.animate.set_opacity(0.3),
            Transform(vec_neg.copy(), reflected),
            FadeIn(reflected_label)
        )
        self.wait(2)
        self.clear()
        
        # Scene 9: Complex eigenvalues preview
        title9 = Text("Complex eigenvalues", font_size=36, color=YELLOW)
        self.play(Write(title9))
        self.wait(0.5)
        
        text9 = Text("Some transformations have no real eigenvectors", font_size=24, color=RED)
        text9.next_to(title9, DOWN)
        self.play(FadeIn(text9))
        
        rotation_circle = Circle(radius=1.5, color=BLUE, stroke_opacity=0.5)
        self.play(Create(rotation_circle))
        self.wait()
        
        arrow = Vector([1, 0], color=GREEN)
        self.play(GrowArrow(arrow))
        self.play(Rotate(arrow, angle=2*PI, about_point=ORIGIN), runtime=3)
        self.wait(2)
        self.clear()
        
        # Scene 10: Final summary
        title10 = Text("Summary", font_size=48, color=YELLOW)
        self.play(Write(title10))
        self.wait(0.5)
        
        points = VGroup(
            Text("• Non-zero vectors that stay in direction", font_size=24, color=BLUE),
            Text("• Only scaled by eigenvalue λ", font_size=24, color=BLUE),
            Text("• Aᵥ = λᵥ", font_size=36, color=RED),
            Text("• Key concept for: PCA, Quantum mechanics, Vibrations", font_size=20, color=GREEN)
        )
        points.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        points.next_to(title10, DOWN, buff=0.5)
        
        for point in points:
            self.play(FadeIn(point, shift=UP), runtime=0.5)
        
        self.wait(3)
        
        # Final reveal
        final_eq = MathTex(
            r"A\vec{v} = \lambda \vec{v}",
            font_size=72,
            color=YELLOW
        )
        final_eq.move_to(ORIGIN)
        self.play(FadeOut(points), FadeOut(title10))
        self.play(Write(final_eq))
        self.wait(2)
        self.play(FadeOut(final_eq))
