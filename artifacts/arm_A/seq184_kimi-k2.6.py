from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction - Waves in a stationary medium
        title = Text("The Doppler Effect", font_size=48, color=BLUE)
        subtitle = Text("Understanding Wave Motion", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(1)
        
        # Create a stationary wave source and concentric circles
        source = Dot(LEFT * 4 + DOWN * 2, color=RED)
        source_label = Text("Source", font_size=20, color=RED)
        source_label.next_to(source, DOWN)
        
        self.play(FadeOut(subtitle), run_time=0.5)
        self.play(title.animate.scale(0.6).to_edge(UP))
        self.play(FadeIn(source), Write(source_label), run_time=1)
        
        # Animate expanding wavefronts
        wavefronts = VGroup()
        for i in range(5):
            circle = Circle(radius=0.5 + i * 0.8, color=BLUE, stroke_opacity=0.7 - i * 0.12).move_to(source.get_center())
            wavefronts.add(circle)
        
        self.play(*[Create(w) for w in wavefronts], run_time=2)
        self.wait(1)
        
        # Show wavefronts expanding
        expanded_waves = VGroup()
        for i in range(5):
            circle = Circle(radius=1.5 + i * 0.8, color=BLUE, stroke_opacity=0.6 - i * 0.1).move_to(source.get_center())
            expanded_waves.add(circle)
        
        self.play(*[Transform(wavefronts[i], expanded_waves[i]) for i in range(5)], run_time=2)
        
        # Add observer
        observer = Dot(RIGHT * 4 + DOWN * 2, color=GREEN)
        observer_label = Text("Observer", font_size=20, color=GREEN)
        observer_label.next_to(observer, DOWN)
        
        self.play(FadeIn(observer), Write(observer_label), run_time=1)
        self.wait(0.5)
        
        # Show equal spacing
        spacing_lines = VGroup()
        for i in range(4):
            line = DashedLine(
                start=source.get_center() + RIGHT * (1.2 + i * 1.5),
                end=observer.get_center() - RIGHT * (1.2 + (3-i) * 1.5),
                color=YELLOW,
                stroke_opacity=0.5
            )
            spacing_lines.add(line)
        
        equal_text = Text("Equal wavelength → Equal frequency", font_size=22, color=YELLOW)
        equal_text.next_to(title, DOWN)
        
        self.play(Create(spacing_lines), Write(equal_text), run_time=1.5)
        self.wait(2)
        
        self.play(
            FadeOut(wavefronts), FadeOut(spacing_lines), FadeOut(source), 
            FadeOut(source_label), FadeOut(observer), FadeOut(observer_label),
            FadeOut(equal_text), FadeOut(title), run_time=1
        )
        self.clear()
        
        # Scene 2: Understanding wavelength and frequency basics
        title2 = Text("Wave Basics: λ and f", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title2), run_time=1)
        
        # Draw a simple sine wave
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=3,
            axis_config={"color": WHITE}
        ).shift(DOWN * 0.5)
        
        x_label = Text("x (distance)", font_size=18).next_to(axes.x_axis, RIGHT)
        y_label = Text("amplitude", font_size=18).next_to(axes.y_axis, UP)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)
        
        sine_wave = axes.plot(lambda x: 1.5 * np.sin(x), color=BLUE, x_range=[0, 10])
        self.play(Create(sine_wave), run_time=2)
        
        # Mark one wavelength
        wavelength_brace = Brace(Line(axes.c2p(0, 0), axes.c2p(2*np.pi, 0)), DOWN, color=YELLOW)
        wavelength_label = Text("λ (wavelength)", font_size=20, color=YELLOW)
        wavelength_label.next_to(wavelength_brace, DOWN)
        
        self.play(Create(wavelength_brace), Write(wavelength_label), run_time=1)
        self.wait(0.5)
        
        # Add frequency annotation
        freq_arrow = Arrow(axes.c2p(0, 2.5), axes.c2p(2*np.pi, 2.5), buff=0, color=GREEN)
        freq_label = Text("f = waves/second", font_size=20, color=GREEN)
        freq_label.next_to(freq_arrow, UP)
        
        self.play(Create(freq_arrow), Write(freq_label), run_time=1)
        self.wait(1)
        
        # Show the wave equation
        equation = MathTex("v = \\lambda f", font_size=40, color=WHITE)
        equation.next_to(axes, DOWN, buff=0.8)
        
        self.play(Write(equation), run_time=1.5)
        self.wait(2)
        
        # Animate wave moving
        moving_wave = axes.plot(lambda x: 1.5 * np.sin(x - 0.5), color=BLUE, x_range=[0, 10])
        
        for _ in range(3):
            new_wave = axes.plot(lambda x, phase=_ * 0.5: 1.5 * np.sin(x - phase), color=BLUE, x_range=[0, 10])
            self.play(Transform(sine_wave, new_wave), run_time=0.5)
        
        self.wait(1)
        self.play(FadeOut(axes), FadeOut(x_label), FadeOut(y_label), 
                  FadeOut(sine_wave), FadeOut(wavelength_brace), 
                  FadeOut(wavelength_label), FadeOut(freq_arrow), 
                  FadeOut(freq_label), FadeOut(equation), FadeOut(title2), run_time=1)
        self.clear()
        
        # Scene 3: Moving source - wavefronts bunch up in front
        title3 = Text("Moving Source: Waves Compress Ahead", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title3), run_time=1)
        
        # Stationary source for comparison (faded)
        stationary_source = Dot(LEFT * 5 + DOWN * 1, color=GRAY, radius=0.15)
        stationary_label = Text("Stationary", font_size=16, color=GRAY).next_to(stationary_source, DOWN)
        
        # Moving source
        moving_source = Dot(LEFT * 3 + DOWN * 1, color=RED, radius=0.2)
        moving_label = Text("Moving →", font_size=18, color=RED).next_to(moving_source, UP)
        
        self.play(FadeIn(stationary_source), Write(stationary_label), run_time=0.8)
        self.play(FadeIn(moving_source), Write(moving_label), run_time=0.8)
        
        # Show stationary waves
        stat_waves = VGroup()
        for i in range(3):
            circle = Circle(radius=0.5 + i * 0.6, color=GRAY, stroke_opacity=0.3).move_to(stationary_source.get_center())
            stat_waves.add(circle)
        
        self.play(*[Create(w) for w in stat_waves], run_time=1)
        
        # Animate moving source emitting waves at different positions
        positions = [LEFT * 3 + DOWN * 1, LEFT * 2 + DOWN * 1, LEFT * 1 + DOWN * 1, LEFT * 0 + DOWN * 1]
        all_waves = VGroup()
        
        for i, pos in enumerate(positions):
            # Move source
            self.play(moving_source.animate.move_to(pos), run_time=0.8)
            
            # Emit wave
            wave = Circle(radius=0.3, color=BLUE, stroke_opacity=0.6).move_to(pos)
            self.play(Create(wave), run_time=0.3)
            all_waves.add(wave)
            
            # Expand previous waves
            expanded = VGroup()
            for j, w in enumerate(all_waves):
                new_radius = 0.3 + (len(positions) - j) * 0.5 + i * 0.2
                new_wave = Circle(radius=new_radius, color=BLUE, stroke_opacity=0.6 - j*0.1).move_to(positions[j])
                expanded.add(new_wave)
            
            if len(all_waves) > 1:
                self.play(*[Transform(all_waves[j], expanded[j]) for j in range(len(all_waves)-1)], run_time=0.3)
        
        self.wait(0.5)
        
        # Highlight compressed and expanded regions
        ahead_arrow = Arrow(RIGHT * 0.5 + DOWN * 1, RIGHT * 2.5 + DOWN * 1, color=YELLOW, buff=0.1)
        ahead_text = Text("Compressed\n(higher f)", font_size=18, color=YELLOW).next_to(ahead_arrow, UP)
        
        behind_arrow = Arrow(LEFT * 0.5 + DOWN * 1, LEFT * 2.5 + DOWN * 1, color=GREEN, buff=0.1)
        behind_text = Text("Stretched\n(lower f)", font_size=18, color=GREEN).next_to(behind_arrow, UP)
        
        self.play(Create(ahead_arrow), Write(ahead_text), run_time=0.8)
        self.play(Create(behind_arrow), Write(behind_text), run_time=0.8)
        self.wait(2)
        
        self.play(FadeOut(ahead_arrow), FadeOut(ahead_text), FadeOut(behind_arrow), 
                  FadeOut(behind_text), FadeOut(all_waves), FadeOut(moving_source),
                  FadeOut(moving_label), FadeOut(stat_waves), FadeOut(stationary_source),
                  FadeOut(stationary_label), FadeOut(title3), run_time=1)
        self.clear()
        
        # Scene 4: Mathematical derivation for moving source
        title4 = Text("Source Moving at Speed vs", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title4), run_time=1)
        
        # Setup with source and wavefronts
        source_pos = LEFT * 2 + DOWN * 0.5
        source_s = Dot(source_pos, color=RED, radius=0.2)
        source_text = MathTex("v_s", color=RED, font_size=30).next_to(source_s, UP)
        
        self.play(FadeIn(source_s), Write(source_text), run_time=1)
        
        # Wavefronts emitted at positions
        emit_positions = [LEFT * 4, LEFT * 2.5, LEFT * 1]
        wavefront_group = VGroup()
        
        for i, pos in enumerate(emit_positions):
            # Show source at emission point
            ghost = Dot(pos + DOWN * 0.5, color=RED, radius=0.1, fill_opacity=0.5)
            label = Text(f"t={i}", font_size=14, color=GRAY).next_to(ghost, DOWN)
            
            self.play(FadeIn(ghost), Write(label), run_time=0.5)
            
            # Wave expands
            wave = Circle(radius=0.5 + i * 0.7, color=BLUE).move_to(pos + DOWN * 0.5)
            wavefront_group.add(wave)
            self.play(Create(wave), run_time=0.5)
            
            ghost_group = VGroup(ghost, label)
            if i < 2:
                self.play(FadeOut(ghost_group), run_time=0.3)
            else:
                self.play(ghost_group.animate.set_opacity(0.3), run_time=0.3)
        
        # Show wavelength in front (compressed)
        front_line1 = always_redraw(lambda: DashedLine(
            emit_positions[0] + DOWN * 0.5 + RIGHT * (0.5 + 2 * 0.7),
            emit_positions[1] + DOWN * 0.5 + RIGHT * (0.5 + 1 * 0.7),
            color=YELLOW
        ))
        # Actually create static lines for clarity
        front_line = DashedLine(
            emit_positions[0] + DOWN * 0.5 + RIGHT * 1.9,
            emit_positions[1] + DOWN * 0.5 + RIGHT * 1.2,
            color=YELLOW
        )
        lambda_front = MathTex("\\lambda_{front} < \\lambda", color=YELLOW, font_size=24)
        lambda_front.next_to(front_line, UP, buff=0.3)
        
        back_line = DashedLine(
            emit_positions[1] + DOWN * 0.5 + LEFT * 1.2,
            emit_positions[2] + DOWN * 0.5 + LEFT * 0.5,
            color=GREEN
        )
        lambda_back = MathTex("\\lambda_{back} > \\lambda", color=GREEN, font_size=24)
        lambda_back.next_to(back_line, DOWN, buff=0.3)
        
        self.play(Create(front_line), Write(lambda_front), run_time=1)
        self.play(Create(back_line), Write(lambda_back), run_time=1)
        
        # Show formula
        formula = MathTex(
            "\\lambda' = \\lambda - v_s T = \\frac{v - v_s}{f}",
            font_size=32, color=WHITE
        ).next_to(source_s, DOWN, buff=1.5)
        
        self.play(Write(formula), run_time=2)
        self.wait(2)
        
        observed_freq = MathTex(
            "f' = \\frac{v}{\\lambda'} = \\frac{f}{1 - v_s/v}",
            font_size=32, color=ORANGE
        ).next_to(formula, DOWN, buff=0.5)
        
        self.play(Write(observed_freq), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(source_s), FadeOut(source_text), FadeOut(wavefront_group),
                  FadeOut(front_line), FadeOut(lambda_front), FadeOut(back_line),
                  FadeOut(lambda_back), FadeOut(formula), FadeOut(observed_freq),
                  FadeOut(title4), run_time=1)
        self.clear()
        
        # Scene 5: Moving observer scenario
        title5 = Text("Moving Observer: Different Perspective", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title5), run_time=1)
        
        # Stationary source with waves
        source_fix = Dot(LEFT * 3, color=RED, radius=0.2)
        source_fix_text = Text("Fixed Source", font_size=18, color=RED).next_to(source_fix, DOWN)
        
        self.play(FadeIn(source_fix), Write(source_fix_text), run_time=0.8)
        
        # Create evenly spaced wavefronts
        fixed_waves = VGroup()
        for i in range(6):
            circle = Circle(radius=0.8 + i * 0.9, color=BLUE, stroke_opacity=0.5).move_to(source_fix.get_center())
            fixed_waves.add(circle)
        
        self.play(*[Create(w) for w in fixed_waves], run_time=1.5)
        
        # Moving observer
        observer_start = RIGHT * 3
        observer_end = RIGHT * 1
        
        obs = Dot(observer_start, color=GREEN, radius=0.2)
        obs_text = MathTex("v_o", color=GREEN, font_size=28).next_to(obs, UP)
        
        self.play(FadeIn(obs), Write(obs_text), run_time=0.8)
        
        # Animate observer moving toward source
        self.play(obs.animate.move_to(observer_end), run_time=2)
        
        # Show encountering more wavefronts
        wave_arrows = VGroup()
        for i, wave in enumerate(fixed_waves):
            if i >= 3:
                arrow = Arrow(
                    wave.get_right(),
                    obs.get_center(),
                    color=YELLOW,
                    stroke_opacity=0.6,
                    buff=0.2
                )
                wave_arrows.add(arrow)
        
        encounter_text = Text("Meets more waves per second!", font_size=22, color=YELLOW)
        encounter_text.to_edge(DOWN)
        
        self.play(*[Create(a) for a in wave_arrows], Write(encounter_text), run_time=1.5)
        self.wait(1)
        
        # Show the math
        obs_math = MathTex(
            "f' = f(1 + \\frac{v_o}{v})",
            font_size=34, color=ORANGE
        ).next_to(encounter_text, UP, buff=0.5)
        
        self.play(Write(obs_math), run_time=1.5)
        
        # Show observer moving away
        self.play(
            obs.animate.move_to(RIGHT * 5),
            FadeOut(encounter_text),
            run_time=2
        )
        
        away_text = Text("Meets fewer waves per second", font_size=22, color=GRAY)
        away_text.to_edge(DOWN)
        
        obs_math_away = MathTex(
            "f' = f(1 - \\frac{v_o}{v})",
            font_size=34, color=GRAY
        ).next_to(away_text, UP, buff=0.5)
        
        self.play(Write(away_text), Transform(obs_math, obs_math_away), run_time=1.5)
        self.wait(2)
        
        self.play(FadeOut(source_fix), FadeOut(source_fix_text), FadeOut(fixed_waves),
                  FadeOut(obs), FadeOut(obs_text), FadeOut(wave_arrows),
                  FadeOut(away_text), FadeOut(obs_math), FadeOut(title5), run_time=1)
        self.clear()
        
        # Scene 6: Complete formula combining both effects
        title6 = Text("General Doppler Equation", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title6), run_time=1)
        
        # Build up the formula piece by piece
        v_symbol = MathTex("v", font_size=36, color=BLUE)
        v_symbol.shift(UP * 1.5)
        v_label = Text("speed of sound", font_size=18, color=BLUE).next_to(v_symbol, UP)
        
        self.play(Write(v_symbol), Write(v_label), run_time=1)
        
        # Source velocity
        vs_group = VGroup(
            MathTex("v_s > 0", font_size=28, color=RED),
            Text("source moving toward observer", font_size=16, color=RED)
        ).arrange(DOWN).shift(LEFT * 3)
        
        # Observer velocity  
        vo_group = VGroup(
            MathTex("v_o > 0", font_size=28, color=GREEN),
            Text("observer moving toward source", font_size=16, color=GREEN)
        ).arrange(DOWN).shift(RIGHT * 3)
        
        self.play(Write(vs_group), run_time=1)
        self.play(Write(vo_group), run_time=1)
        
        # The big formula
        big_formula = MathTex(
            "f' = f \\frac{v + v_o}{v - v_s}",
            font_size=44, color=YELLOW
        )
        big_formula.shift(DOWN * 0.5)
        
        self.play(FadeOut(v_symbol), FadeOut(v_label), 
                  vs_group.animate.set_opacity(0.3), vo_group.animate.set_opacity(0.3), run_time=0.5)
        self.play(Write(big_formula), run_time=2)
        
        # Annotate parts
        numerator_brace = Brace(big_formula[0][4:7], UP, color=GREEN)
        numerator_text = Text("observer toward", font_size=16, color=GREEN).next_to(numerator_brace, UP)
        
        denominator_brace = Brace(big_formula[0][8:11], DOWN, color=RED)
        denominator_text = Text("source toward", font_size=16, color=RED).next_to(denominator_brace, DOWN)
        
        self.play(Create(numerator_brace), Write(numerator_text), run_time=1)
        self.play(Create(denominator_brace), Write(denominator_text), run_time=1)
        
        # Special cases
        cases = VGroup(
            Text("vs=0: moving observer only", font_size=18, color=GREEN),
            Text("vo=0: moving source only", font_size=18, color=RED),
            Text("vs=vo=0: no shift", font_size=18, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT).shift(DOWN * 2.5 + LEFT * 2)
        
        self.play(Write(cases), run_time=1.5)
        self.wait(2)
        
        self.play(FadeOut(big_formula), FadeOut(numerator_brace), FadeOut(numerator_text),
                  FadeOut(denominator_brace), FadeOut(denominator_text), FadeOut(vs_group),
                  FadeOut(vo_group), FadeOut(cases), FadeOut(title6), run_time=1)
        self.clear()
        
        # Scene 7: Electromagnetic waves / light - relativistic Doppler
        title7 = Text("Light and Relativistic Effects", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title7), run_time=1)
        
        # Different for light - no medium needed
        light_note = Text("Light needs NO medium!", font_size=24, color=YELLOW)
        light_note.shift(UP * 2)
        
        self.play(Write(light_note), run_time=1)
        
        # Show light source
        star = Star(n=5, outer_radius=0.4, inner_radius=0.2, color=YELLOW, fill_opacity=1)
        star.shift(LEFT * 2)
        star_label = Text("Star", font_size=18, color=YELLOW).next_to(star, DOWN)
        
        self.play(FadeIn(star), Write(star_label), run_time=0.8)
        
        # Light wavefronts (not circles in 3D, but showing concept)
        light_waves = VGroup()
        for i in range(5):
            circle = Circle(radius=0.5 + i * 0.7, color=WHITE, stroke_opacity=0.6).move_to(star.get_center())
            light_waves.add(circle)
        
        self.play(*[Create(w) for w in light_waves], run_time=1.5)
        
        # Relativistic formula
        rel_formula = MathTex(
            "\\frac{f'}{f} = \\sqrt{\\frac{1 + \\beta}{1 - \\beta}}",
            font_size=36, color=ORANGE
        )
        rel_formula.shift(DOWN * 0.5)
        
        beta_def = MathTex(
            "\\beta = \\frac{v}{c}",
            font_size=28, color=GREEN
        ).next_to(rel_formula, DOWN, buff=0.5)
        
        c_label = Text("speed of light", font_size=16, color=GREEN).next_to(beta_def, DOWN)
        
        self.play(Write(rel_formula), run_time=1.5)
        self.play(Write(beta_def), Write(c_label), run_time=1)
        
        # Redshift and blueshift
        shift_examples = VGroup(
            Text("Moving away: REDSHIFT (lower f, longer λ)", font_size=20, color=RED),
            Text("Moving toward: BLUESHIFT (higher f, shorter λ)", font_size=20, color=BLUE)
        ).arrange(DOWN, buff=0.5).shift(DOWN * 2.5)
        
        self.play(Write(shift_examples), run_time=1.5)
        
        # Astronomical application
        astro_text = Text("Used to measure galaxy velocities!", font_size=20, color=YELLOW).to_edge(DOWN)
        self.play(FadeIn(astro_text), run_time=1)
        self.wait(2)
        
        self.play(FadeOut(star), FadeOut(star_label), FadeOut(light_waves),
                  FadeOut(rel_formula), FadeOut(beta_def), FadeOut(c_label),
                  FadeOut(shift_examples), FadeOut(astro_text), FadeOut(light_note),
                  FadeOut(title7), run_time=1)
        self.clear()
        
        # Scene 8: Real-world applications and demonstrations
        title8 = Text("Real-World Applications", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title8), run_time=1)
        
        # Police siren
        police_car = Square(side_length=0.8, color=BLUE, fill_opacity=0.8).shift(LEFT * 4 + UP * 1.5)
        police_text = Text("Police Siren", font_size=18, color=BLUE).next_to(police_car, DOWN)
        siren = Circle(radius=0.2, color=RED).move_to(police_car.get_top())
        
        self.play(FadeIn(police_car), Write(police_text), FadeIn(siren), run_time=0.8)
        
        # Sound waves
        siren_waves = VGroup()
        for i in range(3):
            arc = Arc(radius=0.5 + i * 0.5, start_angle=-PI/3, angle=2*PI/3, color=RED, stroke_opacity=0.6).move_to(siren.get_center())
            siren_waves.add(arc)
        
        self.play(*[Create(w) for w in siren_waves], run_time=1)
        
        # Moving car animation
        self.play(
            police_car.animate.shift(RIGHT * 6),
            siren.animate.shift(RIGHT * 6),
            *[w.animate.shift(RIGHT * 6) for w in siren_waves],
            run_time=2
        )
        
        # Radar / sonar
        radar = Circle(radius=0.4, color=GREEN, fill_opacity=0.5).shift(LEFT * 4 + DOWN * 1)
        radar_text = Text("Radar/Sonar", font_size=18, color=GREEN).next_to(radar, DOWN)
        
        self.play(FadeIn(radar), Write(radar_text), run_time=0.8)
        
        # Pulse out and back
        pulse = Dot(radar.get_center(), color=YELLOW)
        target = Dot(RIGHT * 2 + DOWN * 1, color=WHITE)
        target_text = Text("target", font_size=16, color=WHITE).next_to(target, DOWN)
        
        self.play(FadeIn(pulse), FadeIn(target), Write(target_text), run_time=0.5)
        self.play(pulse.animate.move_to(target.get_center()), run_time=1)
        self.play(pulse.animate.move_to(radar.get_center()), run_time=0.8)
        
        # Medical ultrasound
        us = RoundedRectangle(width=0.6, height=1.2, color=PURPLE).shift(RIGHT * 3 + DOWN * 1)
        us_text = Text("Ultrasound", font_size=18, color=PURPLE).next_to(us, DOWN)
        
        self.play(FadeIn(us), Write(us_text), run_time=0.8)
        
        # Blood flow measurement
        blood = Arrow(us.get_left(), us.get_left() + LEFT * 1.5, color=RED, buff=0.2)
        blood_text = Text("blood flow", font_size=14, color=RED).next_to(blood, DOWN)
        
        self.play(Create(blood), Write(blood_text), run_time=0.6)
        
        # All applications
        all_apps = VGroup(
            Text("• Police radar", font_size=18),
            Text("• Weather radar", font_size=18),
            Text("• Medical Doppler", font_size=18),
            Text("• Astronomy", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 4 + UP * 1)
        
        self.play(Write(all_apps), run_time=1.5)
        self.wait(2)
        
        self.play(FadeOut(police_car), FadeOut(police_text), FadeOut(siren),
                  FadeOut(siren_waves), FadeOut(radar), FadeOut(radar_text),
                  FadeOut(pulse), FadeOut(target), FadeOut(target_text),
                  FadeOut(us), FadeOut(us_text), FadeOut(blood), FadeOut(blood_text),
                  FadeOut(all_apps), FadeOut(title8), run_time=1)
        self.clear()
        
        # Scene 9: Summary and key takeaways
        title9 = Text("Summary", font_size=44, color=BLUE).to_edge(UP)
        self.play(Write(title9), run_time=1)
        
        # Key points
        points = VGroup(
            Text("• Waves compress when source & observer approach", font_size=22),
            Text("• Waves stretch when source & observer recede", font_size=22),
            Text("• Higher frequency = higher pitch (sound)", font_size=22),
            Text("• Lower frequency = lower pitch (sound)", font_size=22),
            Text("• Same effect for light: redshift/blueshift", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).shift(UP * 0.5)
        
        self.play(Write(points), run_time=2.5)
        
        # Final formula
        final_formula = MathTex(
            "f' = f \\frac{v \\pm v_o}{v \\mp v_s}",
            font_size=40, color=YELLOW
        ).shift(DOWN * 2)
        
        sign_note = Text("Top signs: approaching    Bottom signs: receding", font_size=18, color=GRAY)
        sign_note.next_to(final_formula, DOWN)
        
        self.play(Write(final_formula), run_time=1.5)
        self.play(Write(sign_note), run_time=1)
        self.wait(2)
        
        # Fade to thanks
        thanks = Text("Thanks for watching!", font_size=36, color=GREEN)
        
        self.play(
            FadeOut(points), FadeOut(final_formula), FadeOut(sign_note),
            Transform(title9, thanks), run_time=1.5
        )
        self.wait(2)
        
        self.play(FadeOut(title9), run_time=1)
        self.clear()
