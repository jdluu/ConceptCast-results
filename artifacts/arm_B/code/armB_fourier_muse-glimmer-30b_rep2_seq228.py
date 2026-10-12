from manim import *

class MainScene(Scene):
    def construct(self):
        formula = Text("Formula").scale(0.8)
        inv = Text("Inverse").scale(0.8)
        inv.next_to(formula, DOWN, buff=0.5)
        
        arrow = Arrow(start=formula.get_bottom(), end=inv.get_top(), color=WHITE)
        
        self.add(formula, inv, arrow)
