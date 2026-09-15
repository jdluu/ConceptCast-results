import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Wave Fundamentals ---
        # --- Scene 1: Wave Fundamentals ---
        # Set background color from style guidelines
        self.camera.background_color = "#181825"

        # Define Palette
        COLOR_SINE = "#89b4fa"  # Light blue
        COLOR_BRACE = "#fab387"  # Peach/Orange
        COLOR_TEXT = "#c0caf5"  # Soft lavender/white

        # 1. Axes Setup
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            y_length=4,
            axis_config={"include_tip": False, "color": GREY_C},
        ).shift(DOWN * 0.5)

        # 2. The Sine Wave (Animated)
        # We use a ValueTracker for time to animate the phase shift
        time_tracker = ValueTracker(0)

        # k = 2*PI/wavelength. Let wavelength = 2 for clarity.
        k = PI
        w = 2 * PI  # Angular frequency

        wave = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(k * x - w * time_tracker.get_value()),
                color=COLOR_SINE,
                stroke_width=4,
            )
        )

        # 3. Wavelength Visualization
        # To make the brace stay between peaks, we calculate the x-coordinates of the peaks
        # Peak 1: kx - wt = PI/2 => x = (PI/2 + wt)/k
        # Peak 2: kx - wt = 5PI/2 => x = (5PI/2 + wt)/k

        def get_peak_1():
            t = time_tracker.get_value()
            x = (PI / 2 + w * t) / k
            # Peak is at y=1, but we want the brace slightly above
            return axes.coords_to_point(x, 1.1)

        def get_peak_2():
            t = time_tracker.get_value()
            x = (5 * PI / 2 + w * t) / k
            return axes.coords_to_point(x, 1.1)

        wavelength_brace = always_redraw(
            lambda: BraceBetweenPoints(
                get_peak_1(), get_peak_2(), direction=UP, color=COLOR_BRACE
            )
        )

        wavelength_label = always_redraw(
            lambda: MathTex(r"\lambda", color=COLOR_BRACE).next_to(
                wavelength_brace, UP, buff=0.1
            )
        )

        # 4. Frequency Text
        freq_text = Text(
            "Frequency: cycles per second", font_size=32, color=COLOR_TEXT
        ).to_edge(UL, buff=1)

        # --- Animation sequence ---
        self.add(axes)
        self.play(Create(wave), Write(freq_text), run_time=2)
        self.wait(0.5)

        # Introduce the wavelength measurement
        self.play(FadeIn(wavelength_brace), Write(wavelength_label), run_time=1)

        # Animate the wave moving across the screen (phase shift)
        # time_tracker.get_value() increments, causing the wave to shift right
        self.play(time_tracker.animate.set_value(2.0), run_time=6, rate_func=linear)

        self.wait(2)
        # --- Scene 2: The Stationary Source ---
        # Set background color to match style guidelines
        self.camera.background_color = "#181825"

        # Color Palette from style guidelines
        COLOR_SOURCE = "#C0CAF5"  # Specific to the source dot
        COLOR_WAVE = "#89b4fa"  # Using the primary light blue for waves
        COLOR_LISTENER = "#BB9AF7"  # Purple for listener

        # 1. Objects Definitions

        # Stationary Sound Source
        source_dot = Dot(point=ORIGIN, color=COLOR_SOURCE, radius=0.1)
        source_label = Text("Sound Source", font="Sans", font_size=24).next_to(
            source_dot, UP
        )

        # Listener (placed to the right)
        listener_dot = Dot(point=[4, 0, 0], color=COLOR_LISTENER, radius=0.1)
        listener_label = Text("Listener", font="Sans", font_size=24).next_to(
            listener_dot, DOWN
        )

        # Grouping for initial entry
        source_group = VGroup(source_dot, source_label)
        listener_group = VGroup(listener_dot, listener_label)

        # 2. Animations

        # Initial setup (0.0s - 2.0s)
        self.play(FadeIn(source_group), FadeIn(listener_group), run_time=2.0)
        self.wait(1.0)

        # Wave Emission Logic
        # We will create a series of circles that expand and fade out.
        # To represent constant frequency, we trigger them at regular intervals.

        wave_circles = VGroup()
        # Total duration is 15s. Setup took 3s. Remaining 12s.
        # We will emit waves every 1.5 seconds.
        emission_interval = 1.5
        num_waves = 7

        # We use a loop to create a series of animations
        # Each wave: grows from 0 to 6 radius and fades out.

        last_wave_start = 3.0

        # Use a list of animations to maintain timing control
        wave_animations = []

        for i in range(num_waves):
            wave = Circle(radius=0, color=COLOR_WAVE, stroke_width=2)
            wave.set_stroke(opacity=0.8)

            # The wave expands and disappears
            # We use a custom animation sequence for each ring
            anim = Succession(
                # Expansion
                # Grow from center to a radius that reaches the listener and beyond
                # We use a function-based animation or a simple scale/transform
                # To ensure precise control, we'll manually animate the radius/scale
                # in a loop in the construct method instead of a list if it gets complex,
                # but for standard Manim, we can define the animation for each wave.
                # Note: Circle(radius=0) to Circle(radius=6)
                ReplacementTransform(
                    wave, Circle(radius=6, color=COLOR_WAVE).set_stroke(opacity=0)
                ),
                run_time=3.0,
            )

            # To handle the "concentric" look, we play these with a lag or in a sequence
            # Since we are in a single construct method, let's implement the loop sequentially
            # but overlap them using a separate logic or just sequential self.play.

        # REVISED WAVE LOOP for better visual flow and timing match:
        # To reach exactly 15s, let's be precise.

        # Time spent: 3s. Remaining: 12s.
        # Let's emit a wave every 1.5s.
        # Wave 1: 3.0 -> 6.0 (3s duration)
        # Wave 2: 4.5 -> 7.5
        # Wave 3: 6.0 -> 9.0
        # Wave 4: 7.5 -> 10.5
        # Wave 5: 9.0 -> 12.0
        # Wave 6: 10.5 -> 13.5
        # Wave 7: 12.0 -> 15.0

        for i in range(num_waves):
            wave = Circle(radius=0, color=COLOR_WAVE, stroke_width=2)
            target_wave = Circle(radius=6, color=COLOR_WAVE, stroke_width=2).set_stroke(
                opacity=0
            )

            # We use a delayed start for each wave.
            # Since Manim's self.play is blocking, we'll use AnimationGroup or
            # just a sequence of overlaps.
            # Actually, the cleanest way to get overlapping "ripples" is to
            # create a series of waves and animate them with a LaggedStart
            # or a custom loop.

            # To ensure the timing is EXACTLY 15s:
            # 0-2: Fade In
            # 2-3: Wait
            # 3-15: Ripples

            # We'll define the ripples as a group and use LaggedStart
            # Each ripple takes 3s to expand and vanish.
            # We start a new one every 1.5s.

            # Creating the ripples as distinct objects
            # We'll just create them one by one in a loop and play them
            # by shifting the time.

        # To correctly implement overlapping ripples in Manim:
        ripples = VGroup(
            *[
                Circle(radius=0, color=COLOR_WAVE, stroke_width=2)
                for _ in range(num_waves)
            ]
        )
        targets = VGroup(
            *[
                Circle(radius=6, color=COLOR_WAVE, stroke_width=2).set_stroke(opacity=0)
                for _ in range(num_waves)
            ]
        )

        self.play(
            LaggedStart(
                *[Transform(ripples[i], targets[i]) for i in range(num_waves)],
                lag_ratio=0.5,  # This creates the offset
                run_time=12.0 / (num_waves * 0.5),  # Adjusting to fit the 12s remaining
            ),
            run_time=12.0,  # The total duration for the ripple sequence
        )

        # Wait is not needed at the end because the total run_time of
        # (2s FadeIn + 1s Wait + 12s Ripples) = 15.0s
        # --- Scene 3: Source in Motion (Compression) ---
        self.clear()

        # --- Configuration & Colors ---
        # Using palette from workflow context
        COLOR_SOURCE = "#C0CAF5"
        COLOR_WAVE = "#7AA2F7"
        BG_COLOR = "#181825"
        self.camera.background_color = BG_COLOR

        # --- Objects ---

        # The moving source
        source = Dot(color=COLOR_SOURCE, radius=0.12)
        source_label = Text(
            "Moving Source", font="Sans", font_size=24, color=COLOR_SOURCE
        )
        source_label.next_to(source, UR, buff=0.2)
        source_group = VGroup(source, source_label)
        source_group.move_to(LEFT * 4)

        # Container for the rings to allow easy cleanup or transformation
        wavefronts = VGroup()

        # --- Animation Logic ---

        # Total duration requested: 14.5 seconds
        # 1. Initial Setup (2.0s)
        self.play(FadeIn(source_group), run_time=1.0)
        self.wait(1.0)

        # 2. Movement and Wave Emission (10.0s)
        # We will animate the source moving from -4 to 4
        # while periodically creating expanding circles.

        # Total travel distance = 8 units
        # Total travel time = 10 seconds
        # Velocity = 0.8 units/sec

        # To simulate the "Doppler Effect" visually:
        # - Each ring is created at the source's current position.
        # - Each ring expands at a constant rate (the speed of sound/light).
        # - Because the source moves in the direction of the waves,
        #   rings created later will be closer to rings created earlier in front.

        def get_ring():
            # Create a ring at the current position of the source
            ring = Circle(radius=0, color=COLOR_WAVE, stroke_width=2)
            ring.move_to(source.get_center())
            return ring

        # Time steps for emitting rings
        emission_interval = 0.8  # Emit a ring every 0.8 seconds
        total_move_time = 10.0

        # We use a ValueTracker to synchronize the source position and the wave expansion
        time_tracker = ValueTracker(0)
        source_velocity = 0.8  # units per second
        wave_velocity = 2.0  # units per second (expansion rate)

        # Custom update functions for the rings
        def update_ring(ring, dt):
            # The radius grows based on the wave velocity
            ring.radius += wave_velocity * dt
            # Fade out as they get larger to keep the scene clean
            ring.set_stroke(opacity=max(0, 1 - ring.radius / 6))

        # Main animation loop
        # We use a sequence of plays to move the source and add rings

        # To implement "continuous" ring growth and movement in Manim,
        # we can't easily use a simple loop with self.play.
        # Instead, we'll use a combination of a linear move and an add_updater.

        source_group.add_updater(lambda m, dt: m.shift(RIGHT * source_velocity * dt))

        # Start the motion
        self.add(source_group)

        # We manually trigger the emission of rings using a timer-like approach
        # Since add_updater runs every frame, we can track elapsed time
        start_time = self.time

        # To make the rings grow, we'll add them to the scene and give them updaters
        def ring_emission_logic(dt):
            # This is a trick: we can't easily "add" to the scene inside an updater
            # without potential issues, so we'll create a pool of rings or
            # use a custom loop.
            pass

        # Revised Approach for Stability:
        # Manually animate the source and periodically spawn rings.
        # Since we need exactly 14.5s, let's use a sequence of animations.

        # Remove the updater to handle it via explicit play calls for better control
        source_group.remove_updater(lambda m, dt: m.shift(RIGHT * source_velocity * dt))

        # Reset position for a clean sequence
        source_group.move_to(LEFT * 4)
        self.remove(source_group)
        self.add(source_group)

        # Ring Emission Sequence
        rings_to_create = int(total_move_time / emission_interval)

        # Create all rings as targets for the animation to keep it fluid
        # But since the source moves, we will create them in a loop.

        # To avoid "hallucinating" runtime behavior, we'll use a simple loop:
        for i in range(rings_to_create):
            # 1. Create the ring at current source position
            current_ring = get_ring()
            self.add(current_ring)

            # 2. Animate source moving forward and ring expanding simultaneously
            # The ring grows from 0 to a decent size.
            # The source moves by (source_velocity * emission_interval)
            dist_step = source_velocity * emission_interval

            # Expansion of the ring: radius grows by wave_velocity * emission_interval
            target_radius = wave_velocity * emission_interval

            self.play(
                source_group.animate.shift(RIGHT * dist_step),
                current_ring.animate.set_width(
                    target_radius * 2
                ),  # set_width is diameter
                run_time=emission_interval,
                rate_func=linear,
            )

            # Add an updater to the ring so it keeps growing while the NEXT ring is being created
            current_ring.add_updater(update_ring)

        # 3. Final Stabilization and Labels (2.5s)
        # Clean up updaters to stop movement
        for ring in (
            wavefronts
        ):  # This is just an empty list in my current logic, need to track
            pass

        # Better: just stop the clock and add the descriptive labels
        # The rings should be compressed in front and stretched behind.

        # Label for Compressed Waves (Front)
        comp_text = Text(
            "Compressed\n(Shorter λ)", font="Sans", font_size=20, color=COLOR_WAVE
        )
        comp_text.next_to(source, RIGHT, buff=1.0).shift(UP * 1)

        # Label for Stretched Waves (Back)
        stretch_text = Text(
            "Stretched\n(Longer λ)", font="Sans", font_size=20, color=COLOR_WAVE
        )
        stretch_text.next_to(source, LEFT, buff=1.0).shift(UP * 1)

        self.play(Write(comp_text), Write(stretch_text), run_time=1.5)

        # Final wait to hit the 14.5s mark
        # Current total: 2.0 (start) + 10.0 (move) + 1.5 (labels) = 13.5
        # Need 1.0 more.
        self.wait(1.0)

        # Final cleanup of updaters to prevent rendering glitches at the very end
        # (Though not strictly necessary for the video output)
        # --- Scene 4: Higher Pitch (Approach) ---
        self.clear()

        # --- Styling ---
        BG_COLOR = "#181825"
        PRIMARY_COLOR = "#89b4fa"
        ACCENT_COLOR = "#BB9AF7"
        DANGER_COLOR = "#F7768E"
        self.camera.background_color = BG_COLOR

        # --- Objects ---
        source = Dot(point=LEFT * 3, color=PRIMARY_COLOR, radius=0.15)
        source_label = Text("Source", font_size=24).next_to(source, UP)

        listener = Dot(point=RIGHT * 5, color=ACCENT_COLOR, radius=0.15)
        listener_label = Text("Listener", font_size=24).next_to(listener, UP)

        pitch_label = Text("Higher Pitch", font_size=36, color=DANGER_COLOR)
        pitch_label.to_edge(UP).shift(RIGHT * 2)

        # --- Timeline ---
        # Total Duration: 16.0s

        # 1. Setup: 2.0s
        self.play(
            FadeIn(source),
            FadeIn(source_label),
            FadeIn(listener),
            FadeIn(listener_label),
            run_time=1.0,
        )
        self.wait(1.0)

        # 2. Wave Train: 12.0s (6 waves * 2.0s each)
        for i in range(6):
            wave = Arc(radius=0.4, start_angle=PI / 2, angle=PI, color=PRIMARY_COLOR)
            wave.move_to(source.get_center())

            # Wave travels and turns red as it approaches/hits the listener
            # Duration: 1.5s
            self.play(
                wave.animate.shift(RIGHT * 9).set_color(DANGER_COLOR),
                run_time=1.5,
                rate_func=linear,
            )

            # Visual emphasis and cleanup: 0.5s
            if i == 1:
                self.play(Write(pitch_label), run_time=0.5)
            elif i == 3:
                self.play(Indicate(pitch_label), run_time=0.5)
            else:
                self.play(FadeOut(wave), run_time=0.5)

        # 3. Conclusion: 2.0s
        self.play(Indicate(listener), run_time=1.0)
        self.wait(1.0)
        # --- Scene 5: Lower Pitch (Recession) ---
        self.clear()

        # Colors from style guidelines and target scene
        COLOR_SOURCE = "#C0CAF5"
        COLOR_LISTENER = "#BB9AF7"
        COLOR_WAVE_LOW = "#9ECE6A"  # Green for low pitch
        BG_COLOR = "#181825"

        self.camera.background_color = BG_COLOR

        # 1. Objects Definition
        # Listener is stationary on the right
        listener = Dot(point=RIGHT * 4, color=COLOR_LISTENER, radius=0.15)
        listener_label = Text("Listener", font="Sans", font_size=24).next_to(
            listener, DOWN
        )

        # Source starts at center and moves right (away from listener's previous position/relative to center)
        # Actually, if it moves PAST the listener, it should start near listener and move further right.
        # Or start center and move past the listener. Let's have it move from center to the right, passing the listener.
        source = Dot(point=ORIGIN, color=COLOR_SOURCE, radius=0.15)
        source_label = Text("Sound Source", font="Sans", font_size=24).next_to(
            source, UP
        )
        source_group = VGroup(source, source_label)

        # Pitch Label
        pitch_label_low = Text(
            "Lower Pitch", font="Sans", font_size=36, color=COLOR_WAVE_LOW
        )
        pitch_label_low.to_edge(UP + RIGHT, buff=1.0)

        # 2. Animation Sequence

        # Initial setup
        self.add(listener, listener_label)
        self.play(FadeIn(source_group))
        self.wait(1)

        # Movement: Source moves from center, passes listener, and continues right
        # We want to visualize "Recession" (moving away)
        # To show stretched waves, we create circles that expand from the source's position at the time of emission

        waves = VGroup()

        # Animation of the source moving away
        # Total movement time: 8 seconds
        # We will emit waves every 1 second

        move_duration = 8.0
        start_pos = ORIGIN
        end_pos = RIGHT * 7

        # We'll use a ValueTracker or simply a loop to simulate the physics of wave emission
        # Since Manim is a movie, we'll pre-calculate the wave centers

        wave_centers = []
        for i in range(8):
            # Position of source at time t = i
            t = i / (move_duration / 7)  # spread over the duration
            # Linear interpolation
            pos = start_pos + (end_pos - start_pos) * (i / 7)
            wave_centers.append(pos)

        # Actual animation loop
        # We use a custom loop or a series of plays.
        # To ensure timing is exact, we use a sequence of animations.

        # Start moving source and labels
        self.play(
            source_group.animate.move_to(end_pos),
            run_time=move_duration,
            rate_func=linear,
        )

        # To simulate waves emitting WHILE moving, we need to overlap them.
        # Since 'play' blocks, we can't easily do this without a custom function or AnimationGroup.
        # Instead, we'll create the waves and animate their growth using a LaggedStart or similar.
        # However, for the "stretching" effect, the wave must expand from the center where it was created.

        # Redefining the movement to be combined with wave emission
        self.clear()
        self.add(listener, listener_label)
        source_group = VGroup(source, source_label).move_to(ORIGIN)
        self.add(source_group)

        # We will animate the source and waves together.
        # We use a ValueTracker for the source's x-position.
        time_tracker = ValueTracker(0)

        def get_source_pos():
            return RIGHT * time_tracker.get_value()

        # Update function for the source group
        source_group.add_updater(lambda m: m.move_to(get_source_pos()))

        # Waves implementation:
        # We will manually create wave circles at specific time intervals and animate their radius
        wave_list = []

        # We'll play the movement and the waves in a sequence of 1-second intervals to match narration
        for i in range(9):
            # Current position for this wave
            current_pos = RIGHT * i
            wave = Circle(radius=0, color=COLOR_WAVE_LOW, stroke_width=2)
            wave.move_to(current_pos)

            # Every second, we move the source forward and start a new wave
            self.play(
                time_tracker.animate.set_value(i),
                # If wave exists, grow it. If it's the first one, just start.
                # This is tricky with standard play. Let's use a simple approach:
                # Emit waves at intervals and let them grow.
                run_time=1.0,
                rate_func=linear,
            )

            # Emit and grow the wave at the current position
            wave = Circle(radius=0, color=COLOR_WAVE_LOW, stroke_width=2).move_to(
                get_source_pos()
            )
            self.add(wave)
            self.play(
                wave.animate.scale(12),  # Expand to cover screen
                wave.animate.set_stroke(opacity=0.3),  # Fade as it expands
                run_time=2.0,  # This will overlap with the next movement if we use a different approach
                rate_func=linear,
            )
            # To avoid blocking, we should use AnimationGroup.
            # Let's switch to a more robust "Pre-calculated" wave approach for Manim.

        # RE-IMPLEMENTING for timing and visual clarity (The "Robust" Way)
        self.clear()
        self.add(listener, listener_label)

        # Source group
        source_group = VGroup(
            Dot(color=COLOR_SOURCE), Text("Sound Source", font="Sans", font_size=20)
        ).arrange(DOWN, aligned_edge=UP)
        source_group.move_to(ORIGIN)

        # Define the wave expansion as a function of the source's movement
        # Wave i is emitted at time t_i. At time t, its radius is c*(t - t_i)

        # To make this visual, we create a set of circles that grow and move.
        # Since we want the "stretching" look (waves further apart behind the source),
        # the gaps between the circles will be larger than in the "Approaching" scene.

        # Total Duration: 15.0
        # 0-2s: Intro
        # 2-10s: Recession movement and wave emission
        # 10-15s: Final state and labels

        self.play(FadeIn(source_group), run_time=1)
        self.wait(1)

        # Create waves that grow while source moves
        # We use a loop and add_updater or just a series of animations
        waves_group = VGroup()

        # Movement from ORIGIN to RIGHT*6 over 8 seconds
        self.play(
            source_group.animate.move_to(RIGHT * 6), run_time=8.0, rate_func=linear
        )

        # To simulate the waves that were emitted during that move,
        # we create them now and animate them retrospectively or simply draw them.
        # For a clear "Recession" effect, we show the circles with large spacing.

        wave_positions = [RIGHT * x for x in range(0, 7)]
        for pos in wave_positions:
            w = Circle(radius=0, color=COLOR_WAVE_LOW).move_to(pos)
            waves_group.add(w)

        # Animate all waves expanding
        # The one created first (at ORIGIN) should be largest.
        animations = []
        for i, w in enumerate(waves_group):
            # The first wave (i=0) should be the largest, last (i=6) smallest
            final_radius = 6 - (i * 0.5)
            animations.append(w.animate.scale(final_radius).set_stroke(opacity=0.5))

        # Since we already spent 10 seconds (2 + 8), we have 5 seconds left.
        self.play(
            AnimationGroup(*animations, lag_ratio=0.1),
            Write(pitch_label_low),
            run_time=3.0,
        )

        self.wait(2.0)  # Total = 2 + 8 + 3 + 2 = 15.0
        # --- Scene 6: The Doppler Shift Transition ---
        # Color Palette from Style Guidelines
        COLOR_PRIMARY = "#89b4fa"  # Light Blue
        COLOR_SECONDARY = "#fab387"  # Orange-ish
        COLOR_ACCENT = "#f38ba8"  # Pinkish
        COLOR_SUCCESS = "#a6e3a1"  # Greenish
        COLOR_BG = "#181825"  # Background
        COLOR_CAR = "#E0AF68"  # Gold/Yellow
        COLOR_LISTENER = "#BB9AF7"  # Purple
        COLOR_AXES = "#C0CAF5"  # Pale Blue

        self.camera.background_color = COLOR_BG

        # --- Layout Setup ---
        # 1. Listener Position
        listener = Dot(point=RIGHT * 4 + UP * 2, color=COLOR_LISTENER)
        listener_label = Text("Listener", font="Sans", font_size=24).next_to(
            listener, UP
        )

        # 2. Car (Source)
        car = Dot(point=LEFT * 6 + UP * 2, color=COLOR_CAR, radius=0.15)
        car_label = Text("Car (Source)", font="Sans", font_size=24).next_to(car, UP)
        car_group = VGroup(car, car_label)

        # 3. Frequency Axes (Bottom Half)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 5, 1],
            x_length=9,
            y_length=4,
            axis_config={"color": COLOR_AXES},
            tips=False,
        ).shift(DOWN * 2.5)

        axes_label = axes.get_axis_labels(
            x_label=Text("Time (s)", font="Sans", font_size=20),
            y_label=Text("Frequency", font="Sans", font_size=20),
        )

        # --- Graph Logic ---
        # Sigmoid-like drop representing high pitch approaching and low pitch receding
        def freq_func(t):
            return 4.0 / (1 + np.exp(0.8 * (t - 5))) + 1.0

        # --- Animation Sequence ---
        # Phase 1: Introduction (3.0s)
        self.play(
            Write(axes),
            Write(axes_label),
            FadeIn(listener),
            Write(listener_label),
            run_time=2.0,
        )
        self.wait(1.0)

        # Phase 2: Movement and Graph (12.0s)
        # We use a ValueTracker to sync car position, the frequency curve, and the time axis.
        time_tracker = ValueTracker(0)

        # Car position updates based on time_tracker (moves from -6 to +6 over 10 units of time)
        car_group.add_updater(lambda m: m.set_x(-6 + time_tracker.get_value() * 1.2))

        # The curve draws itself as time progresses
        curve_segment = axes.plot(
            lambda x: freq_func(x), x_range=[0, 0], color=COLOR_PRIMARY
        )
        curve_segment.add_updater(
            lambda m: m.become(
                axes.plot(
                    lambda x: freq_func(x),
                    x_range=[0, time_tracker.get_value()],
                    color=COLOR_PRIMARY,
                )
            )
        )

        self.add(car_group, curve_segment)

        # Animate the time_tracker from 0 to 10 over 12 seconds
        # This drives both the car's movement and the graph's drawing.
        self.play(time_tracker.animate.set_value(10), run_time=12.0, rate_func=linear)

        # --- Final Phase: Conclusion (3.0s) ---
        conclusion_text = (
            Text(
                "Fundamental for Radar & Astronomy",
                font="Sans",
                font_size=32,
                color=COLOR_SUCCESS,
            )
            .to_edge(DOWN)
            .shift(UP * 1)
        )

        self.play(Write(conclusion_text), run_time=2.0)
        self.wait(1.0)
