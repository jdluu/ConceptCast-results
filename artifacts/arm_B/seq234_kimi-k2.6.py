from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Intro - What is a wave? (Wave fundamentals)
        title = Text("The Doppler Effect", font_size=48, color=BLUE)
        subtitle = Text("Understanding Wave Motion", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait(1)
        
        self.play(FadeOut(subtitle))
        
        # Create a simple wave representation
        wave_axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=3,
            axis_config={"color": GRAY},
            tips=False,
        ).shift(DOWN * 1.5)
        
        wave_label = MathTex("y = \\sin(x - vt)", font_size=28, color=YELLOW)
        wave_label.next_to(wave_axes, DOWN, buff=0.5)
        
        wave_graph = wave_axes.plot(lambda x: np.sin(x), color=YELLOW, x_range=[-5, 5])
        
        moving_dot = Dot(wave_axes.c2p(0, 0), color=RED, radius=0.08)
        
        self.play(Create(wave_axes), run_time=1.5)
        self.play(Create(wave_graph), run_time=2)
        self.play(FadeIn(wave_label))
        
        # Animate wave propagation
        for t in [0.5, 1.0, 1.5]:
            new_wave = wave_axes.plot(lambda x: np.sin(x - t), color=YELLOW, x_range=[-5, 5])
            self.play(Transform(wave_graph, new_wave), run_time=0.8)
            self.play(moving_dot.animate.move_to(wave_axes.c2p(t, np.sin(0))), run_time=0.5)
        
        self.play(FadeOut(moving_dot))
        
        # Introduce wavelength and frequency labels
        peak1 = wave_axes.c2p(np.pi/2, 1)
        peak2 = wave_axes.c2p(np.pi/2 + 2*np.pi, 1)
        
        wavelength_arrow = Arrow(
            wave_axes.c2p(np.pi/2, 1.8),
            wave_axes.c2p(np.pi/2 + 2*np.pi, 1.8),
            color=GREEN,
            buff=0
        )
        wavelength_label = MathTex("\\lambda", font_size=24, color=GREEN)
        wavelength_label.next_to(wavelength_arrow, UP, buff=0.1)
        
        self.play(Create(wavelength_arrow), Write(wavelength_label))
        
        freq_formula = MathTex("f = \\frac{v}{\\lambda}", font_size=32, color=WHITE)
        freq_formula.to_corner(UR, buff=0.5)
        
        self.play(Write(freq_formula))
        self.wait(1)
        
        self.clear()

        # Scene 2: Stationary source and observer (The baseline case)
        title2 = Text("Scene 2: Stationary Source & Observer", font_size=36, color=BLUE)
        title2.to_edge(UP)
        self.play(Write(title2))
        
        # Source and observer
        source = Dot(ORIGIN, color=RED, radius=0.15)
        source_label = Text("Source", font_size=20, color=RED)
        source_label.next_to(source, DOWN, buff=0.3)
        
        observer = Dot(RIGHT * 4, color=GREEN, radius=0.15)
        observer_label = Text("Observer", font_size=20, color=GREEN)
        observer_label.next_to(observer, DOWN, buff=0.3)
        
        self.play(FadeIn(source), Write(source_label))
        self.play(FadeIn(observer), Write(observer_label))
        
        # Sound waves (concentric circles emanating from source)
        waves = VGroup()
        for i in range(5):
            wave = Circle(radius=0.5 + i * 0.8, color=BLUE, stroke_opacity=0.7 - i*0.1)
            wave.move_to(source.get_center())
            waves.add(wave)
        
        self.play(Create(waves), run_time=1.5)
        
        # Animate waves expanding
        wave_animations = []
        for i, wave in enumerate(waves):
            new_wave = Circle(radius=1.5 + i * 0.8, color=BLUE, stroke_opacity=max(0.1, 0.7 - i*0.1))
            new_wave.move_to(source.get_center())
            wave_animations.append(Transform(wave, new_wave))
        
        self.play(*wave_animations, run_time=2)
        
        # Show equal spacing of wavefronts
        spacing_dots = VGroup()
        for r in [1.5, 2.3, 3.1, 3.9]:
            dot = Dot(source.get_center() + RIGHT * r, color=YELLOW, radius=0.05)
            spacing_dots.add(dot)
        
        spacing_brace = Brace(
            Line(source.get_center() + RIGHT * 1.5, source.get_center() + RIGHT * 2.3),
            UP,
            color=YELLOW
        )
        lambda_label = MathTex("\\lambda", font_size=20, color=YELLOW)
        lambda_label.next_to(spacing_brace, UP, buff=0.1)
        
        self.play(FadeIn(spacing_dots), run_time=1)
        self.play(GrowFromCenter(spacing_brace), Write(lambda_label))
        
        # Frequency observed equals frequency emitted
        f_eq = MathTex("f_{observed} = f_{source}", font_size=28, color=WHITE)
        f_eq.next_to(title2, DOWN, buff=0.5)
        
        self.play(Write(f_eq))
        self.wait(1)
        
        # Clean up
        self.play(
            FadeOut(waves), FadeOut(spacing_dots), FadeOut(spacing_brace),
            FadeOut(lambda_label), FadeOut(f_eq)
        )
        self.clear()

        # Scene 3: Moving source - wavefront compression and rarefaction
        title3 = Text("Scene 3: Moving Source", font_size=36, color=BLUE)
        title3.to_edge(UP)
        self.play(Write(title3))
        
        # Create a timeline showing source positions
        source_positions = [LEFT * 3, LEFT * 1.5, ORIGIN, RIGHT * 1.5]
        source_dots = VGroup(*[Dot(pos, color=RED, radius=0.1) for pos in source_positions])
        source_trail = VGroup(*[Dot(pos, color=RED, radius=0.05) for pos in source_positions[:-1]])
        
        self.play(FadeIn(source_trail), run_time=0.5)
        self.play(FadeIn(source_dots[-1]), run_time=0.5)
        
        # Wavefronts emitted at each position (asymmetric!)
        wavefronts_group = VGroup()
        
        # Wavefront from earliest position (largest, left-biased)
        wf1 = Circle(radius=2.5, color=BLUE, stroke_opacity=0.4)
        wf1.move_to(source_positions[0])
        
        # Wavefront from second position
        wf2 = Circle(radius=1.8, color=BLUE, stroke_opacity=0.5)
        wf2.move_to(source_positions[1])
        
        # Wavefront from third position
        wf3 = Circle(radius=1.0, color=BLUE, stroke_opacity=0.6)
        wf3.move_to(source_positions[2])
        
        # Wavefront from current position (smallest)
        wf4 = Circle(radius=0.5, color=BLUE, stroke_opacity=0.8)
        wf4.move_to(source_positions[3])
        
        wavefronts_group.add(wf1, wf2, wf3, wf4)
        
        self.play(Create(wavefronts_group), run_time=2)
        
        # Show compression on right, rarefaction on left
        arrow_source = Arrow(LEFT * 2, RIGHT * 2, color=RED, buff=0.3)
        arrow_label = Text("Source velocity", font_size=18, color=RED)
        arrow_label.next_to(arrow_source, UP, buff=0.1)
        
        self.play(GrowArrow(arrow_source), Write(arrow_label))
        
        # Highlight compressed region
        compressed_brace = Brace(
            Line(RIGHT * 2.5, RIGHT * 3.5),
            UP,
            color=YELLOW
        )
        compressed_label = Text("Compressed", font_size=16, color=YELLOW)
        compressed_label.next_to(compressed_brace, UP, buff=0.1)
        
        rarefied_brace = Brace(
            Line(LEFT * 4, LEFT * 2.5),
            DOWN,
            color=ORANGE
        )
        rarefied_label = Text("Rarefied", font_size=16, color=ORANGE)
        rarefied_label.next_to(rarefied_brace, DOWN, buff=0.1)
        
        self.play(
            GrowFromCenter(compressed_brace), Write(compressed_label),
            GrowFromCenter(rarefied_brace), Write(rarefied_label)
        )
        
        # Add observer on each side to set up next scene
        obs_right = Dot(RIGHT * 4, color=GREEN, radius=0.15)
        obs_left = Dot(LEFT * 4.5, color=PURPLE, radius=0.15)
        obs_right_label = Text("Observer A", font_size=16, color=GREEN)
        obs_left_label = Text("Observer B", font_size=16, color=PURPLE)
        obs_right_label.next_to(obs_right, DOWN, buff=0.2)
        obs_left_label.next_to(obs_left, DOWN, buff=0.2)
        
        self.play(
            FadeIn(obs_right), FadeIn(obs_left),
            Write(obs_right_label), Write(obs_left_label)
        )
        
        self.wait(1)
        self.clear()

        # Scene 4: Approaching source - higher apparent frequency
        title4 = Text("Scene 4: Source Approaching Observer", font_size=36, color=BLUE)
        title4.to_edge(UP)
        self.play(Write(title4))
        
        # Observer on right, source moving toward them
        observer = Dot(RIGHT * 3.5, color=GREEN, radius=0.15)
        obs_label = Text("Observer", font_size=20, color=GREEN)
        obs_label.next_to(observer, DOWN, buff=0.3)
        
        source = Dot(LEFT * 2, color=RED, radius=0.15)
        source_label = Text("Source moving right", font_size=18, color=RED)
        source_label.next_to(source, UP, buff=0.2)
        
        self.play(FadeIn(observer), Write(obs_label))
        self.play(FadeIn(source), Write(source_label))
        
        # Animate source moving toward observer with emitting waves
        source_path = Line(LEFT * 2, RIGHT * 1.5)
        
        emitted_waves = VGroup()
        positions = [LEFT * 2, LEFT * 0.5, RIGHT * 1.5]
        
        for i, pos in enumerate(positions):
            # Source jumps to position
            if i > 0:
                self.play(source.animate.move_to(pos), run_time=1)
            
            # Emit wave that continues expanding
            new_wave = Circle(radius=0.3, color=BLUE, stroke_opacity=0.8 - i*0.2)
            new_wave.move_to(pos)
            emitted_waves.add(new_wave)
            self.play(Create(new_wave), run_time=0.5)
        
        # Expand all waves
        expanded_waves = VGroup()
        for i, (wave, pos) in enumerate(zip(emitted_waves, positions)):
            expanded = Circle(radius=2.5 - i * 0.7, color=BLUE, stroke_opacity=0.5 - i*0.1)
            expanded.move_to(pos)
            expanded_waves.add(expanded)
        
        self.play(*[Transform(emitted_waves[i], expanded_waves[i]) for i in range(3)], run_time=1.5)
        
        # Show compressed wavelength
        incoming_fronts = VGroup(
            Dot(RIGHT * 2.5, color=YELLOW, radius=0.08),
            Dot(RIGHT * 1.2, color=YELLOW, radius=0.08),
        )
        
        lambda_small = Brace(
            Line(RIGHT * 1.2, RIGHT * 2.5),
            UP,
            color=YELLOW
        )
        lambda_obs_label = MathTex("\\lambda_{obs} < \\lambda", font_size=22, color=YELLOW)
        lambda_obs_label.next_to(lambda_small, UP, buff=0.1)
        
        self.play(FadeIn(incoming_fronts))
        self.play(GrowFromCenter(lambda_small), Write(lambda_obs_label))
        
        # Higher frequency result
        freq_high = MathTex("f_{obs} > f_{source}", font_size=28, color=GREEN)
        freq_high.next_to(title4, DOWN, buff=0.5)
        
        self.play(Write(freq_high))
        
        # Sound effect analogy - higher pitch
        pitch_text = Text("Higher pitch!", font_size=24, color=GREEN)
        pitch_text.next_to(observer, RIGHT, buff=0.5)
        
        self.play(Write(pitch_text))
        self.wait(1)
        
        self.clear()

        # Scene 5: Receding source - lower apparent frequency
        title5 = Text("Scene 5: Source Moving Away", font_size=36, color=BLUE)
        title5.to_edge(UP)
        self.play(Write(title5))
        
        # Observer on left, source moving away from them
        observer = Dot(LEFT * 3.5, color=PURPLE, radius=0.15)
        obs_label = Text("Observer", font_size=20, color=PURPLE)
        obs_label.next_to(observer, DOWN, buff=0.3)
        
        source = Dot(RIGHT * 2, color=RED, radius=0.15)
        source_label = Text("Source moving right", font_size=18, color=RED)
        source_label.next_to(source, UP, buff=0.2)
        
        self.play(FadeIn(observer), Write(obs_label))
        self.play(FadeIn(source), Write(source_label))
        
        # Animate source moving away
        positions = [RIGHT * 2, RIGHT * 3.5, RIGHT * 5]
        emitted_waves = VGroup()
        
        for i, pos in enumerate(positions):
            if i > 0:
                self.play(source.animate.move_to(pos), run_time=1)
            
            new_wave = Circle(radius=0.3, color=ORANGE, stroke_opacity=0.8 - i*0.2)
            new_wave.move_to(pos)
            emitted_waves.add(new_wave)
            self.play(Create(new_wave), run_time=0.5)
        
        # Expand waves - now stretched on left side
        expanded_waves = VGroup()
        for i, (wave, pos) in enumerate(zip(emitted_waves, positions)):
            expanded = Circle(radius=2.0 + i * 0.5, color=ORANGE, stroke_opacity=0.5 - i*0.1)
            expanded.move_to(pos)
            expanded_waves.add(expanded)
        
        self.play(*[Transform(emitted_waves[i], expanded_waves[i]) for i in range(3)], run_time=1.5)
        
        # Show rarefied wavelength reaching observer
        outgoing_fronts = VGroup(
            Dot(LEFT * 1.5, color=YELLOW, radius=0.08),
            Dot(LEFT * 3.0, color=YELLOW, radius=0.08),
        )
        
        lambda_large = Brace(
            Line(LEFT * 3.0, LEFT * 1.5),
            DOWN,
            color=YELLOW
        )
        lambda_obs_label2 = MathTex("\\lambda_{obs} > \\lambda", font_size=22, color=YELLOW)
        lambda_obs_label2.next_to(lambda_large, DOWN, buff=0.1)
        
        self.play(FadeIn(outgoing_fronts))
        self.play(GrowFromCenter(lambda_large), Write(lambda_obs_label2))
        
        # Lower frequency result
        freq_low = MathTex("f_{obs} < f_{source}", font_size=28, color=ORANGE)
        freq_low.next_to(title5, DOWN, buff=0.5)
        
        self.play(Write(freq_low))
        
        pitch_low_text = Text("Lower pitch!", font_size=24, color=ORANGE)
        pitch_low_text.next_to(observer, LEFT, buff=0.5)
        
        self.play(Write(pitch_low_text))
        self.wait(1)
        
        self.clear()

        # Scene 6: The general Doppler formula derivation
        title6 = Text("Scene 6: The Doppler Formula", font_size=36, color=BLUE)
        title6.to_edge(UP)
        self.play(Write(title6))
        
        # Setup with variables
        v_wave = MathTex("v", font_size=28, color=BLUE)  # wave speed
        v_source = MathTex("v_s", font_size=28, color=RED)  # source speed
        v_obs = MathTex("v_o", font_size=28, color=GREEN)  # observer speed
        
        v_wave.to_edge(LEFT, buff=1)
        v_wave.shift(UP * 1.5)
        v_source.next_to(v_wave, DOWN, buff=0.8)
        v_obs.next_to(v_source, DOWN, buff=0.8)
        
        v_wave_explain = Text("= speed of wave in medium", font_size=18, color=BLUE)
        v_source_explain = Text("= speed of source", font_size=18, color=RED)
        v_obs_explain = Text("= speed of observer", font_size=18, color=GREEN)
        
        v_wave_explain.next_to(v_wave, RIGHT, buff=0.3)
        v_source_explain.next_to(v_source, RIGHT, buff=0.3)
        v_obs_explain.next_to(v_obs, RIGHT, buff=0.3)
        
        self.play(Write(v_wave), Write(v_wave_explain))
        self.play(Write(v_source), Write(v_source_explain))
        self.play(Write(v_obs), Write(v_obs_explain))
        
        # Key insight: wavelength is modified by moving source
        insight = Text("Key insight: Moving source changes wavelength in medium", font_size=20, color=YELLOW)
        insight.to_edge(DOWN, buff=1)
        
        self.play(Write(insight))
        self.wait(1)
        
        # Derive modified wavelength
        self.play(FadeOut(insight), FadeOut(v_wave), FadeOut(v_wave_explain),
                  FadeOut(v_source_explain), FadeOut(v_obs), FadeOut(v_obs_explain))
        
        # Show source approaching case
        source_case = Text("Source approaching stationary observer:", font_size=22, color=WHITE)
        source_case.move_to(UP * 1)
        
        lambda_modified = MathTex("\\lambda' = \\lambda - v_s T = \\frac{v - v_s}{f}", font_size=26, color=YELLOW)
        lambda_modified.next_to(source_case, DOWN, buff=0.5)
        
        self.play(Write(source_case))
        self.play(Write(lambda_modified))
        
        # Then observed frequency
        freq_derive = MathTex("f_{obs} = \\frac{v}{\\lambda'} = \\frac{v}{v - v_s} f", font_size=26, color=GREEN)
        freq_derive.next_to(lambda_modified, DOWN, buff=0.5)
        
        self.play(Write(freq_derive))
        self.wait(1)
        
        # Highlight the factor
        highlight_box = SurroundingRectangle(freq_derive, color=YELLOW, buff=0.2)
        
        self.play(Create(highlight_box))
        self.wait(1)
        
        self.play(FadeOut(highlight_box), FadeOut(source_case), FadeOut(lambda_modified), FadeOut(freq_derive))
        
        # General formula
        general_title = Text("General case (source and observer moving):", font_size=22, color=WHITE)
        general_title.move_to(UP * 1)
        
        general_formula = MathTex(
            "f_{obs} = f \\left( \\frac{v \\pm v_o}{v \\mp v_s} \\right)",
            font_size=32, color=GREEN
        )
        general_formula.next_to(general_title, DOWN, buff=0.5)
        
        sign_note = Text("+ toward, - away", font_size=18, color=GRAY)
        sign_note.next_to(general_formula, DOWN, buff=0.3)
        
        self.play(Write(general_title))
        self.play(Write(general_formula))
        self.play(Write(sign_note))
        self.wait(1)
        
        self.clear()

        # Scene 7: Visual summary - ambulance/scenario animation
        title7 = Text("Scene 7: Real-World Example - Passing Siren", font_size=36, color=BLUE)
        title7.to_edge(UP)
        self.play(Write(title7))
        
        # Road
        road = Rectangle(width=12, height=1.5, fill_color=GRAY, fill_opacity=0.3, stroke_color=GRAY)
        road.to_edge(DOWN, buff=1)
        
        road_line = DashedLine(LEFT * 6, RIGHT * 6, color=YELLOW, dash_length=0.3)
        road_line.move_to(road.get_center())
        
        self.play(Create(road), Create(road_line))
        
        # Ambulance/moving source
        ambulance_body = Rectangle(width=1.2, height=0.6, fill_color=RED, fill_opacity=0.8, stroke_color=RED)
        ambulance_top = Rectangle(width=0.6, height=0.3, fill_color=RED, fill_opacity=0.8, stroke_color=RED)
        ambulance_top.next_to(ambulance_body, UP, buff=0)
        ambulance = VGroup(ambulance_body, ambulance_top)
        ambulance.move_to(LEFT * 5)
        
        siren = Dot(ambulance.get_center() + UP * 0.5, color=YELLOW, radius=0.08)
        ambulance.add(siren)
        
        self.play(FadeIn(ambulance))
        
        # Stationary observers on both sides of road
        obs1 = Dot(DOWN * 2.5 + LEFT * 3, color=GREEN, radius=0.12)
        obs2 = Dot(DOWN * 2.5 + RIGHT * 3, color=GREEN, radius=0.12)
        obs1_label = Text("A", font_size=16, color=GREEN)
        obs2_label = Text("B", font_size=16, color=GREEN)
        obs1_label.next_to(obs1, DOWN, buff=0.1)
        obs2_label.next_to(obs2, DOWN, buff=0.1)
        
        self.play(FadeIn(obs1), FadeIn(obs2), Write(obs1_label), Write(obs2_label))
        
        # Animate ambulance passing by with dynamic waves
        positions = [LEFT * 5, LEFT * 2.5, ORIGIN, RIGHT * 2.5, RIGHT * 5]
        
        accumulated_waves = VGroup()
        
        for i, pos in enumerate(positions):
            # Move ambulance
            self.play(ambulance.animate.move_to(pos), run_time=1.2 if i > 0 else 0.5)
            
            # Emit wave at this position
            wave = Circle(radius=0.4, color=BLUE, stroke_opacity=0.9 - i * 0.15)
            wave.move_to(pos)
            wave.position_source = pos  # Store for expansion
            
            accumulated_waves.add(wave)
            self.play(Create(wave), run_time=0.3)
            
            # Expand previous waves
            if len(accumulated_waves) > 1:
                expand_anims = []
                for j, w in enumerate(list(accumulated_waves)[:-1]):
                    new_radius = w.radius + 0.6 if hasattr(w, 'radius') else 0.4 + 0.6 * (i - j)
                    new_w = Circle(radius=new_radius, color=BLUE, 
                                  stroke_opacity=max(0.1, 0.9 - j * 0.15 - 0.05 * (i-j)))
                    new_w.move_to(w.position_source)
                    new_w.position_source = w.position_source
                    new_w.radius = new_radius
                    expand_anims.append(Transform(w, new_w))
                if expand_anims:
                    self.play(*expand_anims, run_time=0.5)
        
        # Freeze and show effect on each observer
        # Waves closer together approaching A (already passed), more spread going to B
        
        # Add frequency indicators
        freq_A = MathTex("f_A: low \\to high", font_size=20, color=GREEN)
        freq_B = MathTex("f_B: high \\to low", font_size=20, color=GREEN)
        freq_A.next_to(obs1, DOWN, buff=0.4)
        freq_B.next_to(obs2, DOWN, buff=0.4)
        
        self.play(Write(freq_A), Write(freq_B))
        
        # Pitch change text
        pitch_curve = ParametricFunction(
            lambda t: np.array([t, np.sin(t * 2) * 0.5, 0]),
            t_range=[-2, 2],
            color=YELLOW
        )
        pitch_curve.scale(0.5)
        pitch_curve.to_edge(RIGHT, buff=0.5)
        pitch_curve.shift(UP * 2)
        
        pitch_label = Text("Pitch vs time", font_size=16, color=YELLOW)
        pitch_label.next_to(pitch_curve, UP, buff=0.2)
        
        self.play(Create(pitch_curve), Write(pitch_label))
        self.wait(1)
        
        self.clear()

        # Scene 8: Light and the relativistic Doppler effect
        title8 = Text("Scene 8: Doppler Effect for Light", font_size=36, color=BLUE)
        title8.to_edge(UP)
        self.play(Write(title8))
        
        # Electromagnetic waves don't need medium
        no_medium = Text("Light waves travel without a medium!", font_size=24, color=YELLOW)
        no_medium.next_to(title8, DOWN, buff=0.5)
        
        self.play(Write(no_medium))
        self.wait(1)
        
        # Only relative velocity matters
        rel_velocity = Text("Only relative velocity matters", font_size=22, color=WHITE)
        rel_velocity.next_to(no_medium, DOWN, buff=0.5)
        
        self.play(Write(rel_velocity))
        
        # Show redshift and blueshift
        self.play(FadeOut(no_medium), FadeOut(rel_velocity))
        
        # Star emitting light
        star = Circle(radius=0.3, fill_color=YELLOW, fill_opacity=1, stroke_color=ORANGE)
        star.move_to(LEFT * 3)
        star_label = Text("Star", font_size=18, color=YELLOW)
        star_label.next_to(star, DOWN, buff=0.2)
        
        self.play(FadeIn(star), Write(star_label))
        
        # Light waves as oscillating EM field
        light_wave = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 1, 0.5],
            x_length=6,
            y_length=2,
            axis_config={"color": GRAY, "stroke_opacity": 0.5},
            tips=False,
        ).shift(RIGHT * 1.5)
        
        sine_wave = light_wave.plot(lambda x: 0.7 * np.sin(x * 3), color=BLUE, x_range=[-1, 5])
        
        self.play(Create(light_wave), Create(sine_wave))
        
        # Redshift: moving away
        redshift_wave = light_wave.plot(lambda x: 0.7 * np.sin(x * 2), color=RED, x_range=[-1, 5])
        
        self.play(Transform(sine_wave, redshift_wave))
        
        redshift_text = MathTex("\\text{Redshift: } \\lambda_{obs} > \\lambda_{emit}", font_size=24, color=RED)
        redshift_text.to_edge(DOWN, buff=1)
        
        self.play(Write(redshift_text))
        self.wait(0.8)
        
        # Blueshift: moving toward
        blueshift_wave = light_wave.plot(lambda x: 0.7 * np.sin(x * 4.5), color=BLUE, x_range=[-1, 5])
        
        self.play(Transform(sine_wave, blueshift_wave))
        
        blueshift_text = MathTex("\\text{Blueshift: } \\lambda_{obs} < \\lambda_{emit}", font_size=24, color=BLUE)
        blueshift_text.next_to(redshift_text, UP, buff=0.3)
        
        self.play(Write(blueshift_text))
        self.wait(0.8)
        
        # Astronomy application
        self.play(FadeOut(sine_wave), FadeOut(light_wave), FadeOut(redshift_text), FadeOut(blueshift_text))
        
        galaxy = Circle(radius=0.4, fill_color=PURPLE, fill_opacity=0.8, stroke_color=PURPLE)
        galaxy.move_to(RIGHT * 3)
        galaxy_label = Text("Distant galaxy", font_size=18, color=PURPLE)
        galaxy_label.next_to(galaxy, DOWN, buff=0.2)
        
        arrow_away = Arrow(galaxy.get_center(), galaxy.get_center() + RIGHT * 1.5, color=RED, buff=0.3)
        
        self.play(FadeIn(galaxy), Write(galaxy_label))
        self.play(GrowArrow(arrow_away))
        
        # Hubble's discovery
        hubble_text = Text("Universe is expanding!", font_size=22, color=YELLOW)
        hubble_text.next_to(arrow_away, UP, buff=0.3)
        
        self.play(Write(hubble_text))
        self.wait(1)
        
        self.clear()

        # Scene 9: Summary and key takeaways
        title9 = Text("Scene 9: Summary", font_size=36, color=BLUE)
        title9.to_edge(UP)
        self.play(Write(title9))
        
        # Key points as numbered list
        points = VGroup(
            MathTex("1. \\text{ Wave frequency changes for moving observer or source}", font_size=24, color=WHITE),
            MathTex("2. \\text{ Approaching } \\rightarrow \\text{ higher frequency (blueshift)}", font_size=24, color=GREEN),
            MathTex("3. \\text{ Receding } \\rightarrow \\text{ lower frequency (redshift)}", font_size=24, color=RED),
            MathTex("4. \\text{ Effect depends on relative velocity to wave speed}", font_size=24, color=YELLOW),
            MathTex("5. \\text{ Applies to sound, light, and all waves}", font_size=24, color=BLUE),
        )
        
        points.arrange(DOWN, buff=0.6)
        points.next_to(title9, DOWN, buff=1)
        
        for point in points:
            self.play(Write(point), run_time=1.2)
        
        self.wait(1)
        
        # Final formula reminder
        self.play(FadeOut(points))
        
        final_formula = MathTex(
            "f_{obs} = f_{source} \\left( \\frac{v \\pm v_o}{v \\mp v_s} \\right)",
            font_size=40, color=GREEN
        )
        final_formula.move_to(ORIGIN)
        
        formula_box = SurroundingRectangle(final_formula, color=YELLOW, buff=0.3, corner_radius=0.1)
        
        self.play(Write(final_formula))
        self.play(Create(formula_box))
        
        # Final "Doppler Effect" with visual
        doppler_final = Text("The Doppler Effect", font_size=32, color=BLUE)
        doppler_final.to_edge(DOWN, buff=1)
        
        # Small animated wave icons
        wave_icon1 = Circle(radius=0.2, color=BLUE, stroke_opacity=0.6)
        wave_icon2 = Circle(radius=0.3, color=BLUE, stroke_opacity=0.5)
        wave_icon3 = Circle(radius=0.4, color=BLUE, stroke_opacity=0.4)
        icons = VGroup(wave_icon1, wave_icon2, wave_icon3)
        icons.arrange(RIGHT, buff=0.1)
        icons.next_to(doppler_final, UP, buff=0.3)
        
        self.play(Write(doppler_final), Create(icons))
        
        # Pulse the icons
        self.play(icons.animate.scale(1.2), run_time=0.5, rate_func=there_and_back)
        
        self.wait(2)
        self.clear()

        # Scene 10: Outro / credits
        thanks = Text("Thanks for watching!", font_size=44, color=BLUE)
        self.play(Write(thanks))
        
        learn_more = Text("Explore: Acoustics, Astronomy, Radar, Medical Imaging", font_size=22, color=GRAY)
        learn_more.next_to(thanks, DOWN, buff=0.8)
        
        self.play(FadeIn(learn_more))
        
        # Final animated waves going outward
        final_waves = VGroup()
        for i in range(4):
            wave = Circle(radius=0.5 + i * 0.8, color=BLUE, stroke_opacity=0.8 - i * 0.15)
            wave.move_to(ORIGIN)
            final_waves.add(wave)
        
        final_waves.shift(DOWN * 2)
        
        self.play(Create(final_waves), run_time=1.5)
        
        self.play(final_waves.animate.scale(1.3), rate_func=there_and_back, run_time=1)
        
        self.wait(2)
        self.play(FadeOut(thanks), FadeOut(learn_more), FadeOut(final_waves))
        self.wait(0.5)
