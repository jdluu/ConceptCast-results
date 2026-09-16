from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Stationary Source and Observer - Wavefronts
        self.play_write_title("Stationary Source")
        source = Dot(color=YELLOW).shift(LEFT * 3)
        source_label = Text("Source", font_size=24).next_to(source, DOWN)
        observer = Dot(color=BLUE).shift(RIGHT * 3)
        observer_label = Text("Observer", font_size=24).next_to(observer, DOWN)
        
        self.play(FadeIn(source), FadeIn(source_label), FadeIn(observer), FadeIn(observer_label))
        self.wait(0.5)

        emitted_circles = VGroup()
        emission_timer = ValueTracker(0)
        
        def update_wavefronts(mob, dt):
            # Update emission timer
            emission_timer.increment_value(dt)
            
            # Emit new wavefront every 0.5 seconds
            if emission_timer.get_value() >= 0.5:
                emission_timer.set_value(0)
                c = Circle(radius=0.1, color=WHITE, stroke_width=2).move_to(source.get_center())
                emitted_circles.add(c)
                self.add(c)
            
            # Expand existing wavefronts
            to_remove = []
            for c in emitted_circles:
                c.radius += dt * 1.5
                c.become(Circle(radius=c.radius, color=WHITE, stroke_width=2).move_to(source.get_center()))
                if c.radius > 7:
                    to_remove.append(c)
            
            for c in to_remove:
                emitted_circles.remove(c)
                self.remove(c)

        dummy = Mobject()
        dummy.add_updater(update_wavefronts)
        self.add(dummy)
        self.wait(3)
        dummy.remove_updater(update_wavefronts)
        self.clear()

        # Scene 2: Frequency Measurement at Rest
        self.play_write_title("Measuring Frequency at Rest")
        axes = Axes(
            x_range=[0, 10, 1], y_range=[-1.5, 1.5, 1],
            x_length=10, y_length=3, axis_config={"include_numbers": False}
        ).shift(DOWN)
        wave_graph = axes.plot(lambda x: np.sin(x), x_range=[0, 10], color=GREEN)
        freq_label = MathTex("f_0", font_size=36).next_to(axes, UP)
        period_brace = BraceBetweenPoints(axes.c2p(0,0), axes.c2p(2*PI, 0), direction=DOWN)
        period_text = MathTex("T_0", font_size=30).next_to(period_brace, DOWN)
        
        self.play(Create(axes), Create(wave_graph), Write(freq_label))
        self.play(GrowFromCenter(period_brace), Write(period_text))
        self.wait(2)
        self.clear()

        # Scene 3: Moving Source - Wavefront Compression/Expansion
        self.play_write_title("Moving Source: Wavefront Distortion")
        source_moving = Dot(color=YELLOW).shift(LEFT * 5)
        source_moving_label = Text("Source (Moving ->)", font_size=24).next_to(source_moving, UP)
        observer_static = Dot(color=BLUE).shift(RIGHT * 3)
        observer_static_label = Text("Observer", font_size=24).next_to(observer_static, DOWN)
        
        self.play(FadeIn(source_moving), FadeIn(source_moving_label), FadeIn(observer_static), FadeIn(observer_static_label))
        
        emitted_circles = VGroup()
        emission_timer = ValueTracker(0)
        
        def update_emission(mob, dt):
            # Update timer
            emission_timer.increment_value(dt)
            
            # Emit new wavefront every 0.5 seconds
            if emission_timer.get_value() >= 0.5:
                emission_timer.set_value(0)
                c = Circle(radius=0.1, color=WHITE, stroke_width=2).move_to(source_moving.get_center())
                emitted_circles.add(c)
                self.add(c)
            
            # Update existing circles: expand but stay at emission center
            to_remove = []
            for c in emitted_circles:
                c.radius += dt * 1.5
                c.become(Circle(radius=c.radius, color=WHITE, stroke_width=2).move_to(c.get_center()))
                if c.radius > 10:
                    to_remove.append(c)
            
            for c in to_remove:
                emitted_circles.remove(c)
                self.remove(c)
            
            # Move source
            source_moving.shift(RIGHT * 1.0 * dt)
            source_moving_label.next_to(source_moving, UP)

        dummy = Mobject()
        dummy.add_updater(update_emission)
        self.add(dummy)
        self.wait(5)
        dummy.remove_updater(update_emission)
        self.clear()

        # Scene 4: Visualizing Wavelength Shift
        self.play_write_title("Wavelength Compression & Expansion")
        axes_top = Axes(x_range=[0, 10], y_range=[-1,1], x_length=10, y_length=2).shift(UP*2)
        axes_bot = Axes(x_range=[0, 10], y_range=[-1,1], x_length=10, y_length=2).shift(DOWN*2)
        
        wave_compressed = axes_top.plot(lambda x: np.sin(2*x), color=RED)
        wave_stretched = axes_bot.plot(lambda x: np.sin(0.5*x), color=BLUE)
        
        label_comp = Text("Compressed Wavelength (Higher Pitch)", font_size=24, color=RED).next_to(axes_top, UP)
        label_stretch = Text("Stretched Wavelength (Lower Pitch)", font_size=24, color=BLUE).next_to(axes_bot, DOWN)
        
        lambda_comp = MathTex("\\lambda_{obs} < \\lambda_{src}", font_size=30).next_to(axes_top, RIGHT)
        lambda_stretch = MathTex("\\lambda_{obs} > \\lambda_{src}", font_size=30).next_to(axes_bot, RIGHT)

        self.play(Create(axes_top), Create(axes_bot))
        self.play(Create(wave_compressed), Write(label_comp), Write(lambda_comp))
        self.play(Create(wave_stretched), Write(label_stretch), Write(lambda_stretch))
        self.wait(2)
        self.clear()

        # Scene 5: Moving Observer Scenario
        self.play_write_title("Moving Observer")
        source_stat = Dot(color=YELLOW).shift(LEFT * 3)
        obs_moving = Dot(color=BLUE).shift(RIGHT * 3)
        obs_label = Text("Observer (Moving ->)", font_size=24).next_to(obs_moving, UP)
        src_label = Text("Source (Stationary)", font_size=24).next_to(source_stat, DOWN)
        
        # Static wavefield visualization
        static_waves = VGroup(*[Circle(radius=i*0.8, color=GREY, stroke_width=1).move_to(source_stat.get_center()) for i in range(1, 8)])
        
        self.play(FadeIn(source_stat), FadeIn(src_label), FadeIn(obs_moving), FadeIn(obs_label), Create(static_waves))
        
        # Observer moves through wavefronts
        self.play(obs_moving.animate.shift(LEFT * 6), obs_label.animate.shift(LEFT * 6), run_time=4, rate_func=linear)
        self.wait(1)
        self.clear()

        # Scene 6: Deriving the Formula
        self.play_write_title("The Doppler Formula")
        
        formula_general = MathTex(
            "f_{observed} = f_{source} \\left( \\frac{v \\pm v_{observer}}{v \\mp v_{source}} \\right)",
            font_size=48
        )
        
        case1 = MathTex("\\text{Source Moving Toward Observer: } f' = f \\left( \\frac{v}{v - v_s} \\right)", font_size=36, color=RED).shift(UP)
        case2 = MathTex("\\text{Observer Moving Toward Source: } f' = f \\left( \\frac{v + v_o}{v} \\right)", font_size=36, color=BLUE).shift(DOWN)
        
        self.play(Write(formula_general))
        self.wait(1)
        self.play(formula_general.animate.shift(UP*2))
        self.play(Write(case1), Write(case2))
        self.wait(2)
        self.clear()

        # Scene 7: Sonic Boom (Supersonic)
        self.play_write_title("Supersonic Speed: Shock Wave")
        plane = Triangle(color=GREY, fill_opacity=1).scale(0.3).rotate(-PI/2).shift(LEFT*6)
        shock_waves = VGroup()
        
        mach_cone_lines = VGroup(
            Line(plane.get_right(), plane.get_right() + RIGHT*10 + UP*5, color=RED, stroke_width=3),
            Line(plane.get_right(), plane.get_right() + RIGHT*10 + DOWN*5, color=RED, stroke_width=3)
        )
        mach_text = Text("Mach Cone", font_size=24, color=RED).next_to(mach_cone_lines, RIGHT)
        
        self.play(FadeIn(plane))
        self.play(Create(mach_cone_lines), Write(mach_text))
        
        # Animate plane moving faster than waves
        plane_anim = plane.animate.shift(RIGHT * 12)
        self.play(plane_anim, run_time=3, rate_func=linear)
        
        self.wait(1)
        self.clear()

        # Scene 8: Real World Applications
        self.play_write_title("Applications")
        apps = VGroup(
            Text("🚑 Ambulance Siren Pitch Change", font_size=32),
            Text("🌌 Redshift/Blueshift (Astronomy)", font_size=32),
            Text("🌡️ Doppler Radar (Weather)", font_size=32),
            Text("🩺 Ultrasound Blood Flow", font_size=32)
        ).arrange(DOWN, buff=0.5)
        
        self.play(LaggedStart(*[FadeIn(app, shift=UP) for app in apps], lag_ratio=0.3))
        self.wait(3)
        self.clear()
        
        # Final Scene
        end_text = Text("The Doppler Effect: Relative Motion Changes Frequency", font_size=36, color=YELLOW)
        self.play(Write(end_text))
        self.wait(2)

    def play_write_title(self, text):
        title = Text(text, font_size=48, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))
        self.wait(0.2)