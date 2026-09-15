from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Introduction to Doppler effect ---
        # -------------------------------------------------
        # 0️⃣ Scene styling
        # -------------------------------------------------
        # Background colour from the style guide
        self.camera.background_color = "#181825"

        # -------------------------------------------------
        # 1️⃣  Objects (positions, colours, sizes)
        # -------------------------------------------------
        # – Title (placed high, white)
        title_1 = Text(
            "Introduction to Doppler effect",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # – Main statement (centre, brand colour)
        main_1 = Text(
            "Today we are exploring Doppler effect.",
            font_size=48,
            color="#89b4fa",
        ).move_to(ORIGIN)

        # – A decorative “wave” that will grow from the centre
        wave_circle = Circle(
            radius=1.5,
            color="#fab387",  # second colour of the palette
            stroke_width=4,
        ).move_to(ORIGIN)

        # -------------------------------------------------
        # 2️⃣  Animations (use Write, FadeIn, GrowFromCenter)
        # -------------------------------------------------
        # Title appears with a hand‑write effect
        self.play(Write(title_1), run_time=2.0)

        # Main sentence fades in gently
        self.play(FadeIn(main_1, shift=UP * 0.5), run_time=1.5)

        # The “wave” grows from the centre, hinting at the Doppler idea
        self.play(GrowFromCenter(wave_circle), run_time=1.0)

        # -------------------------------------------------
        # 3️⃣  Wait – total scene duration must be 6 s
        #    (2 + 1.5 + 1 = 4.5 s → wait 1.5 s)
        # -------------------------------------------------
        self.wait(1.5)
        # --- Scene 2: Step 2: Why Doppler effect matters ---
        # -------------------------------------------------
        # 0. Global style
        # -------------------------------------------------
        self.camera.background_color = "#181825"  # dark background from style guide

        # -------------------------------------------------
        # 1. Objects
        # -------------------------------------------------
        # Title (appears at the top)
        title_2 = Text(
            "Why Doppler effect matters",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # Main axes (centered)
        main_2 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": "#fab387", "stroke_width": 2.0},
        )
        # Axes colour (overrides any default for the whole VGroup)
        main_2.set_color("#fab387")

        # A small dot that will “grow from center” to hint at a source
        source_dot = Dot(ORIGIN, radius=0.12, color="#a6e3a1")
        # Start invisible – GrowFromCenter will handle the reveal
        source_dot.scale(0)

        # -------------------------------------------------
        # 2. Animations (total run‑time = 6 seconds)
        # -------------------------------------------------
        # 0.0 s – 1.5 s : write the title
        self.play(Write(title_2, run_time=1.5))

        # 1.5 s – 3.0 s : fade in the axes
        self.play(FadeIn(main_2, run_time=1.5))

        # 3.0 s – 4.0 s : make the source dot appear from its centre
        self.play(GrowFromCenter(source_dot, run_time=1.0))

        # 4.0 s – 6.0 s : hold the scene for the narrator
        self.wait(2.0)
        # --- Scene 3: Step 3: Core mechanics of Doppler effect ---
        # -------------------------------------------------
        # Style settings (from the workflow context)
        # -------------------------------------------------
        # background
        self.camera.background_color = "#181825"

        # colour palette (same order as supplied)
        palette = [
            "#89b4fa",  # 0 – a soft blue
            "#fab387",  # 1 – a warm orange
            "#f38ba8",  # 2 – the pink used for the NumberLine
            "#a6e3a1",  # 3 – a fresh green
            "#94e2d5",  # 4 – a teal accent
        ]

        # -------------------------------------------------
        # 1️⃣ Objects
        # -------------------------------------------------
        # Title – placed high up
        title_3 = Text(
            "Core mechanics of Doppler effect",
            font_size=36,
            color=WHITE,
        ).to_edge(UP, buff=0.6)

        # NumberLine – centred and then shifted down
        main_3 = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
            color=palette[2],  # pink from the palette
            label_direction=DOWN,
        ).shift(DOWN * 2)

        # Dots representing the source (S) and observer (O)
        source = Dot(
            point=main_3.n2p(-3),
            radius=0.12,
            color=palette[3],
        )
        observer = Dot(
            point=main_3.n2p(3),
            radius=0.12,
            color=palette[0],
        )

        # Labels for the dots
        source_label = MathTex("S", font_size=24).next_to(source, UP)
        observer_label = MathTex("O", font_size=24).next_to(observer, UP)

        # Arrow showing the line‑of‑sight / wave travel direction
        arrow = Arrow(
            start=source.get_center(),
            end=observer.get_center(),
            buff=0.15,
            color=palette[4],
            max_tip_length_to_length_ratio=0.15,
        )

        # -------------------------------------------------
        # 2️⃣ Animations (total runtime = 6 seconds)
        # -------------------------------------------------
        # 0.0 s – title appears
        self.play(Write(title_3), run_time=1.5)  # 1.5 s

        # 1.5 s – number line slides in
        self.play(Create(main_3), run_time=1.0)  # 2.5 s

        # 2.5 s – source dot + label pop in
        self.play(
            FadeIn(source, scale=0.5),
            FadeIn(source_label, shift=UP * 0.3),
            run_time=0.75,
        )  # 3.25 s

        # 3.25 s – observer dot + label pop in
        self.play(
            FadeIn(observer, scale=0.5),
            FadeIn(observer_label, shift=UP * 0.3),
            run_time=0.75,
        )  # 4.0 s

        # 4.0 s – arrow appears to illustrate the “signal” direction
        self.play(Create(arrow), run_time=0.75)  # 4.75 s

        # 4.75 s – hold the final picture for the remaining time
        self.wait(1.25)  # 6.0 s total
        # --- Scene 4: Step 4: Common pitfalls in Doppler effect ---
        # -------------------------------------------------
        # 0️⃣ Global style (from workflow_context)
        # -------------------------------------------------
        self.camera.background_color = "#181825"  # background_color

        # -------------------------------------------------
        # 1️⃣ Title (placed 3 units up)
        # -------------------------------------------------
        title_4 = Text(
            "Common pitfalls in Doppler effect",
            font="Sans",  # primary_font from style_guidelines
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # -------------------------------------------------
        # 2️⃣ Pitfall icons + explanatory labels → main_4
        # -------------------------------------------------
        # colour palette from style_guidelines
        palette = ["#89b4fa", "#fab387", "#f38ba8"]  # three distinct hues

        labels = [
            "Assuming the source is stationary",
            "Ignoring the propagation medium",
            "Confusing frequency with pitch",
        ]

        pitfalls = []  # will hold three VGroups (icon + label)

        for col, txt in zip(palette, labels):
            # circular “warning” icon
            circ = Circle(
                radius=0.7,
                color=col,
                fill_opacity=0.4,
                stroke_width=2.0,  # default_stroke_width from style_guidelines
            )
            # exclamation mark centred inside the circle
            excl = Text("!", font="Sans", font_size=48, color=col).move_to(
                circ.get_center()
            )
            circ.add(excl)

            # label placed to the right of the icon
            lbl = Text(txt, font="Sans", font_size=28, color=WHITE)
            lbl.next_to(circ, RIGHT, buff=0.5)

            # group the icon and its label
            pit = VGroup(circ, lbl)
            pitfalls.append(pit)

        # combine all three pitfalls into a single VGroup
        main_4 = VGroup(*pitfalls).arrange(DOWN, buff=0.8)
        main_4.set_color("#a6e3a1")  # overall tint from style_guidelines
        main_4.move_to(ORIGIN)  # required position

        # -------------------------------------------------
        # 3️⃣ Animations (total ≈ 6 s)
        # -------------------------------------------------
        # 1️⃣ Title writes in (1.5 s)
        self.play(Write(title_4, run_time=1.5))

        # 2️⃣ Pitfalls appear one after another (≈ 2 s total)
        grow_anims = [GrowFromCenter(pit, run_time=1.0) for pit in pitfalls]
        self.play(LaggedStart(*grow_anims, lag_ratio=0.5))

        # 3️⃣ Brief pause for narration (1 s)
        self.wait(1.0)

        # 4️⃣ Fade everything out together (1 s)
        self.play(FadeOut(VGroup(title_4, main_4), run_time=1.0))

        # 5️⃣ Pad to hit exactly 6 s total (0.5 s)
        self.wait(0.5)  # 1.5 + 2.0 + 1.0 + 1.0 + 0.5 = 6.0 s
        # --- Scene 5: Step 5: Practical application of Doppler effect ---
        # ----- Scene setup ----------------------------------------------------
        # Dark background according to the style guide
        self.camera.background_color = "#181825"

        # ----- 1. Objects ------------------------------------------------------
        # Title at the top
        title_5 = Text(
            "Practical application of Doppler effect",
            font_size=36,
            color=WHITE,
        ).shift(UP * 3)

        # Simple illustrative table (feel free to adjust the contents)
        table_data = [
            ["Source", "Observer"],
            ["Train", "Stationary"],
            ["Frequency ↑", "Frequency ↓"],
        ]
        main_5 = (
            Table(
                table_data,
                include_outer_lines=True,
                line_config={"stroke_width": 2},
            )
            .scale(0.7)
            .set_color("#94e2d5")
        )  # palette colour
        main_5.move_to(ORIGIN)

        # ----- 2. Animations ---------------------------------------------------
        # Title appears with a handwritten effect
        self.play(Write(title_5), run_time=1.5)

        # Short pause before the main visual
        self.wait(0.2)

        # Table fades in gently
        self.play(FadeIn(main_5), run_time=2.0)

        # Brief pause
        self.wait(0.3)

        # Table grows from its centre, emphasizing the “building‑up” of data
        self.play(GrowFromCenter(main_5), run_time=1.5)

        # ----- 3. Final pause to match the required duration -------------------
        self.wait(0.5)  # total run‑time = 6.0 seconds
