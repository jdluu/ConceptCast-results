import numpy as np
from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Intro
        title = Text("The Doppler Effect", font_size=48)
        subtitle = Text("Understanding Frequency Shift", font_size=32)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)
        
        # Scene 2: Wave basics
        source = Dot(color=YELLOW)
        source.move_to(LEFT * 4)
        
        circles = VGroup()
        for i in range(5):
            circle = Circle(radius=0.5 + i * 0.5, color=BLUE, stroke_opacity=0.5)
            circle.move_to(source.get_center())
            circles.add(circle)
        
        self.play(FadeIn(source))
        self.play(LaggedStart(*[Create(c) for c in circles], lag_ratio=0.3))
        self.wait(2)
        
        wavelength = DoubleArrow(
            source.get_center() + RIGHT * 0.5,
            source.get_center() + RIGHT * 1.5,
            buff=0
        )
        wavelength_label = MathTex(r"\lambda", color=GREEN)
        wavelength_label.scale(0.8)
        wavelength_label.next_to(wavelength, UP)
        
        self.play(GrowArrow(wavelength))
        self.play(Write(wavelength_label))
        self.wait(2)
        self.play(FadeOut(source), FadeOut(circles), FadeOut(wavelength), FadeOut(wavelength_label))
        self.wait(0.5)
        
        # Scene 3: Observer detection
        source = Dot(color=YELLOW)
        source.move_to(LEFT * 3)
        
        observer = Dot(color=RED)
        observer.move_to(RIGHT * 3)
        
        source_label = Text("Source", font_size=24)
        source_label.next_to(source, UP)
        
        observer_label = Text("Observer", font_size=24)
        observer_label.next_to(observer, UP)
        
        self.play(FadeIn(source), FadeIn(observer))
        self.play(Write(source_label), Write(observer_label))
        
        waves = VGroup()
        for i in range(3):
            wave = Circle(radius=0.3 + i * 0.8, color=BLUE, stroke_opacity=0.6)
            wave.move_to(source.get_center())
            waves.add(wave)
        
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.4))
        
        freq_value = MathTex("f_0 = f_{source}", color=GREEN)
        freq_value.scale(0.8)
        freq_value.next_to(observer, DOWN * 2)
        
        self.play(Write(freq_value))
        self.wait(2)
        self.play(FadeOut(source), FadeOut(observer), FadeOut(source_label), FadeOut(observer_label), FadeOut(waves), FadeOut(freq_value))
        self.wait(0.5)
        
        # Scene 4: Source moving
        source = Dot(color=YELLOW)
        source.move_to(LEFT * 4)
        
        observer = Dot(color=RED)
        observer.move_to(RIGHT * 3)
        
        self.add(source, observer)
        
        front_waves = VGroup()
        back_waves = VGroup()
        
        for i in range(3):
            front = Circle(radius=0.3 + i * 0.5, color=GREEN, stroke_opacity=0.6)
            front.move_to(source.get_center() + RIGHT * i * 0.3)
            front_waves.add(front)
            
            back = Circle(radius=0.5 + i * 0.7, color=RED, stroke_opacity=0.6)
            back.move_to(source.get_center() + LEFT * i * 0.3)
            back_waves.add(back)
        
        self.play(
            LaggedStart(*[Create(w) for w in front_waves], lag_ratio=0.3),
            LaggedStart(*[Create(w) for w in back_waves], lag_ratio=0.3),
            run_time=3
        )
        
        time_labels = VGroup()
        for i in range(3):
            t_label = MathTex(f"t={i+1}", color=WHITE)
            t_label.scale(0.7)
            t_label.move_to(source.get_center() + RIGHT * (1 + i * 1.8) + UP * 2.5)
            time_labels.add(t_label)
        
        self.play(Write(time_labels))
        self.wait(2)
        self.play(FadeOut(source), FadeOut(observer), FadeOut(front_waves), FadeOut(back_waves), FadeOut(time_labels))
        self.wait(0.5)
        
        # Scene 5: Blueshift
        observer = Dot(color=RED)
        observer.move_to(RIGHT * 3)
        
        self.add(observer)
        
        source = Dot(color=YELLOW)
        source.shift(LEFT * 5)
        
        waves = VGroup()
        positions = []
        
        for i in range(4):
            pos = LEFT * 5 + RIGHT * (2 + i * 0.8)
            positions.append(pos)
            wave = Circle(radius=0.4 + i * 0.4, color=GREEN, stroke_opacity=0.6)
            wave.move_to(pos)
            waves.add(wave)
        
        self.play(
            source.animate.move_to(RIGHT * 1),
            LaggedStart(*[Create(w) for w in waves], lag_ratio=0.2),
            run_time=3
        )
        
        blueshift = Text("BLUESHIFT", color=BLUE, font_size=36)
        blueshift.to_edge(UP)
        
        lambda_label = MathTex(r"\lambda", color=GREEN)
        lambda_label.scale(0.8)
        lambda_label.next_to(waves[-1], DOWN)
        
        self.play(Write(blueshift))
        self.play(Write(lambda_label))
        self.wait(2)
        self.play(FadeOut(observer), FadeOut(source), FadeOut(waves), FadeOut(blueshift), FadeOut(lambda_label))
        self.wait(0.5)
        
        # Scene 6: Redshift
        source = Dot(color=YELLOW)
        observer = Dot(color=RED)
        observer.move_to(LEFT * 3)
        
        self.add(observer)
        
        waves = VGroup()
        
        for i in range(4):
            pos = RIGHT * 2 + LEFT * i * 1.2
            wave = Circle(radius=0.6 + i * 0.6, color=RED, stroke_opacity=0.6)
            wave.move_to(pos)
            waves.add(wave)
        
        self.play(
            source.animate.move_to(RIGHT * 4),
            LaggedStart(*[Create(w) for w in waves], lag_ratio=0.2),
            run_time=3
        )
        
        redshift = Text("REDSHIFT", color=RED, font_size=36)
        redshift.to_edge(UP)
        
        self.play(Write(redshift))
        self.wait(2)
        self.play(FadeOut(source), FadeOut(observer), FadeOut(waves), FadeOut(redshift))
        self.wait(0.5)
        
        # Scene 7: Formulas
        formula_source = MathTex(
            r"f_{observed} = f_{source} \cdot \frac{v}{v \pm v_{source}}"
        )
        formula_source.scale(1.2)
        formula_source.to_edge(UP)
        
        self.play(Write(formula_source))
        
        case1 = VGroup()
        case1_text = Text("Approaching:", font_size=28, color=GREEN)
        case1_formula = MathTex(r"f_{obs} = f_0 \frac{v}{v - v_s} > f_0", color=WHITE)
        case1_formula.scale(0.8)
        case1.add(case1_text, case1_formula)
        case1.arrange(DOWN)
        case1.move_to(LEFT * 3 + DOWN)
        
        case2 = VGroup()
        case2_text = Text("Receding:", font_size=28, color=RED)
        case2_formula = MathTex(r"f_{obs} = f_0 \frac{v}{v + v_s} < f_0", color=WHITE)
        case2_formula.scale(0.8)
        case2.add(case2_text, case2_formula)
        case2.arrange(DOWN)
        case2.move_to(RIGHT * 3 + DOWN)
        
        self.play(
            FadeIn(case1_text),
            Write(case1_formula)
        )
        self.play(
            FadeIn(case2_text),
            Write(case2_formula)
        )
        self.wait(2)
        self.play(FadeOut(formula_source), FadeOut(case1), FadeOut(case2))
        self.wait(0.5)
        
        # Scene 8: Applications
        title = Text("Real World Applications", font_size=40)
        title.to_edge(UP)
        
        self.play(Write(title))
        
        apps = VGroup(
            Text("• Police radar (speed detection)", font_size=28),
            Text("• Astronomy (expanding universe)", font_size=28),
            Text("• Medical ultrasound (blood flow)", font_size=28),
            Text("• Weather radar (storm tracking)", font_size=28)
        )
        apps.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        apps.move_to(DOWN * 0.5)
        
        self.play(LaggedStart(*[Write(app) for app in apps], lag_ratio=0.3))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(apps))
        self.wait(0.5)
        
        # Scene 9: Siren demo
        road = Rectangle(width=10, height=0.5, color=GRAY)
        road.move_to(DOWN * 2)
        
        car = Rectangle(width=1.5, height=0.8, color=BLUE)
        car.move_to(LEFT * 4 + DOWN * 2)
        
        observer = Dot(color=RED)
        observer.move_to(RIGHT * 3 + DOWN * 2)
        
        self.add(road, observer)
        self.play(FadeIn(car))
        
        waves = VGroup()
        for i in range(5):
            wave = Circle(radius=0.2 + i * 0.3, color=YELLOW, stroke_opacity=0.5)
            wave.move_to(car.get_center())
            waves.add(wave)
        
        self.play(
            car.animate.move_to(RIGHT * 4),
            LaggedStart(*[Create(w) for w in waves], lag_ratio=0.15),
            run_time=4
        )
        
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 2, 0.5],
            axis_config={"color": WHITE}
        )
        axes.scale(0.6)
        axes.to_edge(DOWN)
        
        pitch_curve = axes.plot(
            lambda x: 1.5 / (abs(x) + 0.5) + 0.3,
            x_range=[-4, 4]
        )
        pitch_curve.set_color(YELLOW)
        
        y_label = MathTex(r"\text{Pitch } \propto f", color=WHITE)
        y_label.scale(0.8)
        y_label.next_to(axes.y_axis, UP)
        
        self.play(Create(axes), Write(y_label))
        self.play(Create(pitch_curve))
        self.wait(2)
        self.play(FadeOut(road), FadeOut(car), FadeOut(observer), FadeOut(waves), FadeOut(axes), FadeOut(y_label), FadeOut(pitch_curve))
        self.wait(0.5)
        
        # Scene 10: Conclusion
        summary = VGroup(
            Text("The Doppler Effect:", font_size=36),
            Text("Relative motion changes perceived frequency", font_size=28),
            MathTex(r"f_{obs} = f_0 \frac{v \pm v_o}{v \mp v_s}")
        )
        summary.arrange(DOWN, buff=0.5)
        
        self.play(Write(summary[0]))
        self.play(FadeIn(summary[1]))
        self.play(Write(summary[2]))
        self.wait(2)
        
        doppler_eq = MathTex(
            r"\frac{\Delta f}{f_0} = \frac{v_{source}}{v}",
            color=WHITE
        )
        doppler_eq.scale(1.2)
        doppler_eq.move_to(ORIGIN)
        
        self.play(
            FadeOut(summary),
            Write(doppler_eq)
        )
        self.wait(2)
