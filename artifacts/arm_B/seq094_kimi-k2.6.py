from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Opening/Title Scene
        title = Text("Mathematical Visualization", font_size=72)
        subtitle = Text("An Exploration of Concepts", font_size=36).next_to(title, DOWN)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)
        
        # Scene 2: Introducing a Mathematical Concept
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": BLUE},
        )
        
        func_label = MathTex("f(x) = \\sin(x)").to_corner(UL)
        
        # Sine curve
        sine_curve = axes.plot(lambda x: np.sin(x), color=RED)
        
        self.play(Create(axes))
        self.play(Write(func_label))
        self.play(Create(sine_curve), run_time=2)
        self.wait(2)
        
        # Add a point moving on the curve
        dot = Dot(color=YELLOW)
        dot_movement = MoveAlongPath(dot, sine_curve, rate_func=linear)
        
        self.play(dot_movement, run_time=3)
        self.wait(1)
        self.play(FadeOut(axes), FadeOut(func_label), FadeOut(sine_curve), FadeOut(dot))
        self.wait(0.5)
        
        # Scene 3: Geometric Transformation
        # Create a square
        square = Square(side_length=2, color=BLUE)
        square.set_fill(BLUE, opacity=0.3)
        
        # Create a circle
        circle = Circle(radius=1, color=GREEN)
        circle.set_fill(GREEN, opacity=0.3)
        
        # Create a triangle
        triangle = Triangle(color=RED)
        triangle.set_fill(RED, opacity=0.3)
        triangle.scale(1.2)
        
        # Position shapes
        shapes = VGroup(square, circle, triangle).arrange(RIGHT, buff=1.5)
        
        self.play(Create(square))
        self.play(Create(circle))
        self.play(Create(triangle))
        self.wait(1)
        
        # Transform square to circle
        self.play(Transform(square, circle.copy()), run_time=2)
        self.wait(0.5)
        
        # Rotate all shapes
        self.play(
            Rotate(shapes, angle=2*PI, about_point=ORIGIN),
            run_time=3
        )
        self.wait(1)
        
        # Scale and fade out
        self.play(shapes.animate.scale(0.1), run_time=2)
        self.play(FadeOut(shapes))
        self.wait(0.5)
        
        # Scene 4: Equations and Text
        # Euler's identity
        euler = MathTex("e^{i\\pi} + 1 = 0")
        euler.scale(2)
        
        self.play(Write(euler))
        self.wait(1)
        
        # Break it down
        e_part = MathTex("e^{i\\pi}").scale(1.5).shift(UP*2 + LEFT*3)
        equals = MathTex("=").scale(1.5).shift(UP*2)
        result = MathTex("-1").scale(1.5).shift(UP*2 + RIGHT*3)
        
        self.play(euler.animate.scale(0.7).shift(UP))
        self.wait(0.5)
        
        explanation = VGroup(
            MathTex("\\text{Where } i = \\sqrt{-1}").shift(DOWN*2),
            MathTex("\\text{and } e^{ix} = \\cos(x) + i\\sin(x)").shift(DOWN*3)
        )
        
        self.play(Write(explanation))
        self.wait(2)
        self.play(FadeOut(euler), FadeOut(explanation))
        self.wait(0.5)
        
        # Scene 5: 3D-like visualization using 2D (since we need to use Scene, not ThreeDScene)
        # Create a 2D representation of 3D objects
        circle_3d = Circle(radius=2, color=BLUE)
        circle_3d.set_fill(BLUE, opacity=0.6)
        
        # Axes
        axes_2d = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": WHITE},
        )
        
        self.play(Create(axes_2d))
        self.play(Create(circle_3d))
        self.wait(1)
        
        # Rotate the circle to simulate 3D rotation
        self.play(Rotate(circle_3d, angle=2*PI, run_time=3))
        self.wait(1)
        
        # Add a wave surface representation
        wave = axes_2d.plot(lambda x: 0.5 * np.sin(3*x), color=GREEN)
        wave.set_stroke(GREEN, opacity=0.8)
        
        self.play(Transform(circle_3d, wave), run_time=2)
        self.wait(1)
        self.play(FadeOut(circle_3d), FadeOut(axes_2d), FadeOut(wave))
        self.wait(0.5)
        
        # Scene 6: Final/Closing Scene
        thanks = Text("Thank You!", font_size=96, color=YELLOW)
        subtitle = Text("Questions Welcome", font_size=48).next_to(thanks, DOWN)
        
        self.play(Write(thanks))
        self.wait(0.5)
        self.play(FadeIn(subtitle))
        
        # Pulse animation
        self.play(thanks.animate.scale(1.2), run_time=0.5)
        self.play(thanks.animate.scale(1/1.2), run_time=0.5)
        
        self.wait(2)
        self.play(FadeOut(thanks), FadeOut(subtitle))
