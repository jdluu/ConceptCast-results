from manim import *

class SecantLineScene(Scene):
    def construct(self):
        # Scene setup
        title = Text("Understanding Secant Lines", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Axes setup
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_numbers": True},
        ).add_coordinates()
        
        graph = axes.plot(lambda x: 0.5 * x**2, x_range=[0, 4], color=BLUE)
        graph_label = axes.get_graph_label(graph, label="f(x) = 0.5x^2")

        self.play(Create(axes), Create(graph), Write(graph_label))

        # Points definition
        x1_val = 1
        x2_val = 3
        y1_val = 0.5 * x1_val**2
        y2_val = 0.5 * x2_val**2

        p1 = Dot(axes.c2p(x1_val, y1_val), color=YELLOW)
        p1_label = MathTex(f"A({x1_val}, {y1_val:.1f})", font_size=24).next_to(p1, DL)
        
        p2 = Dot(axes.c2p(x2_val, y2_val), color=YELLOW)
        p2_label = MathTex(f"B({x2_val}, {y2_val:.1f})", font_size=24).next_to(p2, UR)

        self.play(FadeIn(p1), Write(p1_label), FadeIn(p2), Write(p2_label))

        # Second part: Slope calculation
        title2 = Text("Calculating the Slope", font_size=40).to_edge(UP)
        step_text = Text("Slope = Rise / Run", font_size=30).next_to(title2, DOWN)

        # Create a line connecting the two points manually
        secant_line = Line(
            axes.c2p(x1_val, y1_val), 
            axes.c2p(x2_val, y2_val), 
            color=RED
        )
        
        # Calculate slope
        slope_val = (y2_val - y1_val) / (x2_val - x1_val)
        slope_text = MathTex(f"\\text{{Slope}} = \\frac{{\\Delta y}}{{\\Delta x}} = \\frac{{{y2_val:.1f} - {y1_val:.1f}}}{{{x2_val} - {x1_val}}} = {slope_val:.1f}", font_size=32, color=RED).to_edge(DOWN)
        
        # Add visual triangle for rise/run (optional but helpful)
        run_line = Line(
            axes.c2p(x1_val, y1_val),
            axes.c2p(x2_val, y1_val),
            color=YELLOW,
            stroke_width=3
        )
        rise_line = Line(
            axes.c2p(x2_val, y1_val),
            axes.c2p(x2_val, y2_val),
            color=GREEN,
            stroke_width=3
        )
        triangle = VGroup(run_line, rise_line)
        
        self.play(Write(title2), FadeIn(step_text))
        self.play(Create(axes), Create(graph)) # Replaying axes creation for scene transition if needed, or remove if static
        self.play(FadeIn(p1), Write(p1_label), FadeIn(p2), Write(p2_label))
        self.play(Create(secant_line), Create(triangle), Write(slope_text))
        
        self.wait(3)
