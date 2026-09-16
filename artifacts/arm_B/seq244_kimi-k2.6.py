from manim import *

class SceneGen(Scene):
    def construct(self):
        # IntroScene content
        title = Text("Welcome to the Animation")
        title.scale(1.5)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        
        # MainContent content
        # Create a circle
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        self.wait(1)
        
        # Transform to square
        square = Square(side_length=3.5, color=GREEN)
        self.play(Transform(circle, square))
        self.wait(1)
        
        # Add some text
        text = Text("Circle → Square")
        text.next_to(square, DOWN)
        self.play(Write(text))
        self.wait(2)
        
        # Clean up
        self.play(FadeOut(circle), FadeOut(text))
        
        # OutroScene content
        thanks = Text("Thanks for watching!")
        thanks.scale(1.5)
        thanks.set_color(YELLOW)
        self.play(Write(thanks))
        self.wait(2)
        
        # Add a simple animation
        dot = Dot(color=RED)
        dot.shift(LEFT * 3)
        self.play(dot.animate.move_to(RIGHT * 3), run_time=2)
        self.wait(1)
        self.play(FadeOut(thanks), FadeOut(dot))

# Configuration for rendering
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 8
config.frame_width = 14.222
