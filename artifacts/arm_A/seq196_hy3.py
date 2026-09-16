from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Vectors and basis in 2D
        plane = NumberPlane()
        self.play(Create(plane))
        ax = Vector([1, 0], color=RED)
        ay = Vector([0, 1], color=GREEN)
        v = Vector([2, 1], color=YELLOW)
        self.play(GrowArrow(ax), GrowArrow(ay))
        self.play(Write(Text("Basis vectors and a vector v").to_edge(UP)))
        self.play(GrowArrow(v))
        self.play(v.animate.scale(1.3), run_time=1)
        self.play(v.animate.scale(1 / 1.3), run_time=1)
        self.wait()

        self.clear()

        # Scene 2: General linear transformation changes most vectors
        plane = NumberPlane()
        self.add(plane)
        v = Vector([1, 1.5], color=YELLOW)
        self.play(GrowArrow(v))
        self.play(Write(Text("Linear transformation (shear) changes most vectors").to_edge(UP)))
        self.play(ApplyMatrix(np.array([[1, 1], [0, 1]]), v, run_time=2))
        self.play(v.animate.set_color(RED))
        self.wait()

        self.clear()

        # Scene 3: Some vectors keep their direction under transformation
        plane = NumberPlane()
        self.add(plane)
        ex = Vector([2, 0], color=GREEN)
        self.play(GrowArrow(ex))
        self.play(Write(Text("But some vectors keep their line (x-axis under shear)").to_edge(UP)))
        self.play(ApplyMatrix(np.array([[1, 1], [0, 1]]), ex, run_time=2))
        self.play(ex.animate.set_color(BLUE))
        self.wait()

        self.clear()

        # Scene 4: Formal definition of eigenvectors and eigenvalues
        title = Text("Eigenvectors & Eigenvalues").to_edge(UP)
        eq = MathTex(r"A\mathbf{v} = \lambda\mathbf{v}", r",\ \mathbf{v}\neq \mathbf{0}").scale(1.2)
        self.play(Write(title))
        self.play(Write(eq))
        self.play(eq.animate.shift(UP * 0.3))
        sub = Text("v is eigenvector, λ is eigenvalue (scalar factor)").scale(0.7)
        self.play(Write(sub.next_to(eq, DOWN)))
        self.wait()

        self.clear()

        # Scene 5: Example with a scaling matrix
        plane = NumberPlane()
        self.add(plane)
        mt = Matrix([[2, 0], [0, 0.5]]).to_corner(UL)
        self.play(Write(mt))
        vx = Vector([1.5, 0], color=GREEN)
        vy = Vector([0, 1.5], color=RED)
        self.play(GrowArrow(vx), GrowArrow(vy))
        self.play(Write(Text("Axes are eigenvectors: λ=2 (x), λ=0.5 (y)").to_edge(DOWN)))
        self.play(ApplyMatrix(np.array([[2, 0], [0, 0.5]]), vx, run_time=2),
                  ApplyMatrix(np.array([[2, 0], [0, 0.5]]), vy, run_time=2))
        self.wait()

        self.clear()

        # Scene 6: Many vectors, only eigenvectors stay collinear
        plane = NumberPlane()
        self.add(plane)
        vecs = VGroup(*[Vector(p, color=BLUE) for p in [(1, 1), (2, 0.5), (1.5, 0), (0, 1.5), (-1, 1)]])
        self.play(*[GrowArrow(v) for v in vecs])
        self.play(Write(Text("Only vectors on eigen-directions stay collinear").to_edge(UP)))
        self.play(ApplyMatrix(np.array([[2, 0], [0, 0.5]]), vecs, run_time=2))
        self.play(vecs[2].animate.set_color(GREEN), vecs[3].animate.set_color(GREEN))
        self.wait()

        self.clear()

        # Scene 7: Negative eigenvalue
        plane = NumberPlane()
        self.add(plane)
        self.play(Write(Matrix([[-1, 0], [0, 1]]).to_corner(UL)))
        v = Vector([1.5, 0], color=YELLOW)
        self.play(GrowArrow(v))
        self.play(Write(Text("Negative eigenvalue: flips direction, same line (λ=-1)").to_edge(UP)))
        self.play(ApplyMatrix(np.array([[-1, 0], [0, 1]]), v, run_time=2))
        self.play(v.animate.set_color(RED))
        self.wait()

        self.clear()

        # Scene 8: Summary
        summary = Text(
            "Summary:\n"
            "- Eigenvectors are non-zero vectors that only scale under a linear transform.\n"
            "- The scale factor is the eigenvalue.\n"
            "- They reveal intrinsic axes of the transformation."
        ).scale(0.7)
        self.play(Write(summary))
        self.wait(2)