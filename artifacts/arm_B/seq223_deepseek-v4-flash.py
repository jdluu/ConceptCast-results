from manim import *
import numpy as np

class FourierSynth(Scene):
    def construct(self):
        # Title
        title = Text("Fourier Synthesis", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Axes for the individual sine waves
        axes1 = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=3,
            y_length=2
        ).shift(LEFT*5 + UP*2)
        axes2 = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=3,
            y_length=2
        ).shift(LEFT*5)
        axes3 = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=3,
            y_length=2
        ).shift(LEFT*5 + DOWN*2)
        axes4 = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=3,
            y_length=2
        ).shift(LEFT*5 + DOWN*4)
        
        # Axes for the combined signal
        axes5 = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=4
        ).shift(RIGHT*3 + UP*0.5)
        
        # Labels for individual waves
        label1 = MathTex("\\sin(2\\pi t)", color=BLUE).scale(0.5).next_to(axes1, DOWN*0.7)
        label2 = MathTex("\\frac{1}{3}\\sin(6\\pi t)", color=GREEN).scale(0.5).next_to(axes2, DOWN*0.7)
        label3 = MathTex("\\frac{1}{5}\\sin(10\\pi t)", color=RED).scale(0.5).next_to(axes3, DOWN*0.7)
        label4 = MathTex("\\frac{1}{7}\\sin(14\\pi t)", color=YELLOW).scale(0.5).next_to(axes4, DOWN*0.7)
        
        # Draw axes
        self.play(
            Create(axes1), Create(axes2), Create(axes3), Create(axes4), Create(axes5),
            Write(label1), Write(label2), Write(label3), Write(label4)
        )
        self.wait(0.5)
        
        # Create sine waves
        waves = []
        for ax, a, f, c in [(axes1, 1, 1, BLUE), (axes2, 1/3, 3, GREEN), (axes3, 1/5, 5, RED), (axes4, 1/7, 7, YELLOW)]:
            wave = ax.plot(lambda x: a * np.sin(2 * np.pi * f * x), x_range=[0, 1], color=c)
            waves.append(wave)
        
        # Animate sine waves
        for wave in waves:
            self.play(Create(wave), run_time=0.5)
        self.wait(0.5)
        
        # Combined wave
        combined_wave = axes5.plot(
            lambda x: np.sin(2*np.pi*x) + (1/3)*np.sin(6*np.pi*x) + (1/5)*np.sin(10*np.pi*x) + (1/7)*np.sin(14*np.pi*x),
            x_range=[0, 1],
            color=PURPLE
        )
        
        # Labels for combined wave
        combined_label = MathTex(
            "\\sin(2\\pi t) + \\frac{1}{3}\\sin(6\\pi t) + \\frac{1}{5}\\sin(10\\pi t) + \\frac{1}{7}\\sin(14\\pi t)",
            color=PURPLE
        ).scale(0.5).next_to(axes5, DOWN*0.7)
        
        self.play(Create(combined_wave), Write(combined_label), run_time=1.5)
        self.wait(1)
        
        # Update animation to show more terms
        for n in range(9, 20, 2):
            a_val = 1/n
            f_val = n
            # Show new wave being added with animation
            new_wave = axes5.plot(
                lambda x, n=n: np.sum([(1/(2*i+1))*np.sin(2*np.pi*(2*i+1)*x) for i in range((n+1)//2)]),
                x_range=[0, 1],
                color=PURPLE
            )
            self.play(Transform(combined_wave, new_wave), run_time=0.3)
            
            # Update label
            terms = []
            for k in range((n+1)//2):
                denominator = 2*k+1
                terms.append("\\frac{1}{" + str(denominator) + "}\\sin(" + str(denominator) + "\\cdot 2\\pi t)")
            new_label = MathTex(
                " + ".join(terms),
                color=PURPLE
            ).scale(0.3).next_to(axes5, DOWN*0.7)
            self.play(Transform(combined_label, new_label), run_time=0.3)
        
        self.wait(2)
