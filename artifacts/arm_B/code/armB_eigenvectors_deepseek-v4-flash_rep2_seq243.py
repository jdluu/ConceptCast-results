from manim import *

class EigenvectorAnimation(Scene):
    def construct(self):
        # Title
        title = Text("Eigenvectors & Diagonal Matrices", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        
        # Create grid
        grid1 = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_opacity": 0.4,
                "stroke_width": 1,
            }
        )
        self.play(Create(grid1))
        self.wait(0.5)
        
        # First eigenvector on x-axis
        evec1 = Arrow(start=ORIGIN, end=2*RIGHT, color=YELLOW)
        evec1_label = MathTex(r"\vec{e}_1", color=YELLOW).next_to(evec1.get_end(), DOWN)
        self.play(GrowArrow(evec1), Write(evec1_label))
        self.wait(0.5)
        
        # Transformations: stretch x, compress y (diagonal matrix)
        diag_matrix = [[2.0, 0], [0, 0.5]]
        self.play(
            grid1.animate.apply_matrix(diag_matrix),
            evec1.animate.apply_matrix(diag_matrix),
            evec1_label.animate.move_to(evec1.get_end() + DOWN*0.4)
        )
        self.wait(1)
        
        # Reset
        self.play(
            grid1.animate.apply_matrix(np.linalg.inv(diag_matrix)),
            evec1.animate.apply_matrix(np.linalg.inv(diag_matrix)),
            evec1_label.animate.next_to(evec1.get_end(), DOWN)
        )
        self.wait(0.5)
        
        # Second eigenvector on y-axis
        evec2 = Arrow(start=ORIGIN, end=2*UP, color=PURPLE)
        evec2_label = MathTex(r"\vec{e}_2", color=PURPLE).next_to(evec2.get_end(), RIGHT)
        self.play(GrowArrow(evec2), Write(evec2_label))
        self.wait(0.5)
        self.play(
            evec2.animate.apply_matrix(diag_matrix),
            evec2_label.animate.move_to(evec2.get_end() + RIGHT*0.4)
        )
        self.wait(1)
        
        # Show both eigenvectors
        self.play(
            evec1.animate.apply_matrix(diag_matrix),
            evec1_label.animate.move_to(evec1.get_end() + DOWN*0.4),
            evec2.animate.apply_matrix(diag_matrix),
            evec2_label.animate.move_to(evec2.get_end() + RIGHT*0.4)
        )
        self.wait(2)
