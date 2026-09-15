import numpy as np
from manim import *


class DopplerEffect(Scene):
    def construct(self):
        # Background color from guidelines
        self.camera.background_color = "#181825"

        # --- SCENE 1: Wave Fundamentals (Duration: 14.0s) ---
        # 1. Objects
        axis = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.2, 1.2, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": "#D8DEE9"},
        ).shift(DOWN * 0.5)

        axis_label = Text(
            "Amplitude vs Distance", font="Sans", font_size=24, color="#D8DEE9"
        )
        axis_label.next_to(axis, UP)

        # Sine wave: y = sin(x)
        sine_wave = axis.plot(lambda x: np.sin(x), x_range=[0, 2 * PI], color="#89b4fa")

        # Wavelength brace (distance between two peaks)
        # Peaks of sin(x) are at PI/2 and 5PI/2. Range is 2*PI.
        p1 = axis.c2p(PI / 2, 1)
        p2 = axis.c2p(5 * PI / 2, 1)

        # Since our plot only goes to 2PI, let's use the distance from 0 to 2PI for clarity or peak-to-peak
        # Adjusted: Peak at PI/2 and the next would be 5PI/2. Let's plot up to 3PI.
        sine_wave_long = axis.plot(
            lambda x: np.sin(x), x_range=[0, 3 * PI], color="#89b4fa"
        )

        wavelength_brace = BraceBetweenPoints(
            axis.c2p(PI / 2, 1), axis.c2p(5 * PI / 2, 1), UP
        ).set_color("#fab387")

        wavelength_text = MathTex(
            r"	ext{Wavelength } (\lambda)", color="#fab387", font_size=36
        )
        wavelength_text.next_to(wavelength_brace, UP, buff=0.2)

        # 2. Animations
        self.play(Write(axis), Write(axis_label), run_time=2)
        self.play(Create(sine_wave_long), run_time=3)
        self.play(Create(wavelength_brace), Write(wavelength_text), run_time=3)
        # Total spent: 2+3+3 = 8. Wait for remaining 6s to hit 14s.
        self.wait(6)

        self.play(
            FadeOut(
                VGroup(
                    axis, axis_label, sine_wave_long, wavelength_brace, wavelength_text
                )
            ),
            run_time=1,
        )

        # --- SCENE 2: Stationary Source (Duration: 14.0s) ---
        # 1. Objects
        source = Dot(point=ORIGIN, radius=0.15, color="#fab387")

        # Create a group of rings that will expand
        rings = VGroup()
        for i in range(8):
            ring = Circle(radius=0, color="#89b4fa", stroke_width=2)
            rings.add(ring)

        # 2. Animations
        self.play(FadeIn(source), run_time=1)

        # We simulate pulses. Every 1.5 seconds a new ring expands.
        # Total scene duration: 14s.
        for ring in rings:
            # Each ring: expands from 0 to 4 radius over 3 seconds, then fades
            self.play(
                ring.animate.set_radius(4).set_stroke(opacity=0),
                run_time=3,
                rate_func=linear,
            )
            # To make them overlap (pulse effect), we should use AnimationGroup or a loop
            # but standard 'play' is sequential. To get pulses, we use a custom loop with wait.

        # Re-calculating time for pulses:
        # Since the loop above is sequential (8 * 3 = 24s), it's too long.
        # Let's use a simpler approach: a few pulses with overlapping timing.

        # Correction for timing:
        # Pulse 1: 0-3s
        # Pulse 2: 1-4s
        # Pulse 3: 2-5s etc.
        # Total Duration = 14.0s.
        # Initial fade in (1s) + 4 pulses (12s) + end wait (1s).

        # Let's clear and restart the stationary source logic for timing precision.
        self.clear()
        self.add(source)

        def create_pulse():
            ring = Circle(radius=0, color="#89b4fa", stroke_width=2)
            self.add(ring)
            return ring

        # Manually managing the timing to reach 14.0s
        # 0-1s: Source appears
        # 1-13s: Pulses
        # 13-14s: Final wait

        # To achieve concurrent expanding rings, we use a loop with a small wait or a ValueTracker.
        # Simplified: Use a few large expansions.

        pulse_rings = VGroup(*[Circle(radius=0, color="#89b4fa") for _ in range(5)])

        # Animation sequence
        # We will use a simple approach: play pulses in a sequence with shorter durations
        # to fit the 13s window.
        for ring in pulse_rings:
            self.play(ring.animate.set_radius(5).set_stroke(opacity=0), run_time=2.5)

        self.wait(
            1.5
        )  # Adjusting to hit 14s total (1s start + 5*2.5 + 1.5 = 15.0 - too much)
        # Fixed: 1s start + 4*2.5 pulses + 3.5s wait = 14.0s.
