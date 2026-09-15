import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Forward Pass: Making a Prediction ---
        self.camera.background_color = "#181825"

        # --- Create layers ---
        l1_nodes = VGroup(
            *[
                Circle(radius=0.35, color="#7AA2F7", fill_opacity=0.15, stroke_width=2)
                for _ in range(3)
            ]
        )
        l1_nodes.arrange(DOWN, buff=0.6).shift(LEFT * 4)
        l1_label = Text("Input Layer", font_size=18, color="#C0CAF5").next_to(
            l1_nodes, DOWN, buff=0.35
        )

        l2_nodes = VGroup(
            *[
                Circle(radius=0.35, color="#BB9AF7", fill_opacity=0.15, stroke_width=2)
                for _ in range(3)
            ]
        )
        l2_nodes.arrange(DOWN, buff=0.6).shift(LEFT * 1)
        l2_label = Text("Hidden Layer", font_size=18, color="#C0CAF5").next_to(
            l2_nodes, DOWN, buff=0.35
        )

        l3_nodes = VGroup(
            *[Circle(radius=0.35, color="#9ECE6A", fill_opacity=0.15, stroke_width=2)]
        )
        l3_nodes.shift(RIGHT * 2)
        l3_label = Text("Output Layer", font_size=18, color="#C0CAF5").next_to(
            l3_nodes, DOWN, buff=0.35
        )

        pred_box = Rectangle(
            width=1.8, height=1.0, color="#E0AF68", stroke_width=2
        ).shift(RIGHT * 3.5)
        pred_label = Text("Prediction", font_size=18, color="#C0CAF5").next_to(
            pred_box, DOWN, buff=0.25
        )

        arrows_1_2 = VGroup()
        for n1 in l1_nodes:
            for n2 in l2_nodes:
                arrows_1_2.add(
                    Arrow(
                        start=n1.get_right(),
                        end=n2.get_left(),
                        buff=0.08,
                        color="#565F89",
                        stroke_width=1.2,
                        tip_length=0.12,
                    )
                )
        arrows_2_3 = VGroup()
        for n2 in l2_nodes:
            for n3 in l3_nodes:
                arrows_2_3.add(
                    Arrow(
                        start=n2.get_right(),
                        end=n3.get_left(),
                        buff=0.08,
                        color="#565F89",
                        stroke_width=1.2,
                        tip_length=0.12,
                    )
                )
        arrow_out = Arrow(
            start=l3_nodes[0].get_right(),
            end=pred_box.get_left(),
            buff=0.08,
            color="#E0AF68",
            stroke_width=1.5,
            tip_length=0.15,
        )

        # --- Entrance: staggered reveal ---
        self.play(
            AnimationGroup(
                LaggedStart(*[Create(n) for n in l1_nodes], lag_ratio=0.15),
                LaggedStart(*[Create(n) for n in l2_nodes], lag_ratio=0.15),
                Create(l3_nodes[0]),
                lag_ratio=0.1,
                run_time=2.0,
            )
        )
        self.play(
            AnimationGroup(
                FadeIn(l1_label, shift=DOWN * 0.2),
                FadeIn(l2_label, shift=DOWN * 0.2),
                FadeIn(l3_label, shift=DOWN * 0.2),
                lag_ratio=0.2,
                run_time=1.0,
            )
        )
        self.play(
            AnimationGroup(
                LaggedStart(*[Create(a) for a in arrows_1_2], lag_ratio=0.03),
                LaggedStart(*[Create(a) for a in arrows_2_3], lag_ratio=0.08),
                Create(arrow_out),
                lag_ratio=0.05,
                run_time=2.0,
            )
        )
        self.play(
            FadeIn(pred_box, scale=0.9),
            FadeIn(pred_label, shift=DOWN * 0.2),
            run_time=1.0,
        )

        # --- Helper to spawn 3 dots at input nodes ---
        def spawn_wave():
            wave = VGroup()
            for n1 in l1_nodes:
                wave.add(Dot(point=n1.get_center(), radius=0.08, color="#E0AF68"))
            return wave

        # --- Wave 1: detailed journey with pulsing highlights ---
        wave1 = spawn_wave()
        self.play(FadeIn(wave1), run_time=0.5)

        self.play(
            *[wave1[i].animate.move_to(l2_nodes[i].get_center()) for i in range(3)],
            run_time=2.0,
            rate_func=smooth,
        )
        self.play(
            *[wave1[i].animate.scale(1.5).set_color("#F38BA8") for i in range(3)],
            run_time=0.3,
        )
        self.play(
            *[wave1[i].animate.scale(1 / 1.5).set_color("#E0AF68") for i in range(3)],
            run_time=0.3,
        )

        self.play(
            *[wave1[i].animate.move_to(l3_nodes[0].get_center()) for i in range(3)],
            run_time=2.0,
            rate_func=smooth,
        )
        self.play(
            *[wave1[i].animate.scale(1.5).set_color("#F38BA8") for i in range(3)],
            run_time=0.3,
        )
        self.play(
            *[wave1[i].animate.scale(1 / 1.5).set_color("#E0AF68") for i in range(3)],
            run_time=0.3,
        )

        self.play(
            *[
                wave1[i].animate.move_to(
                    pred_box.get_center() + UP * 0.1 + LEFT * 0.15 + RIGHT * 0.15 * i
                )
                for i in range(3)
            ],
            run_time=1.5,
            rate_func=smooth,
        )
        self.wait(0.5)

        # --- Waves 2 & 3: faster conveyor-belt reinforcement ---
        for _ in range(2):
            wave = spawn_wave()
            self.add(wave)
            self.play(
                *[wave[i].animate.move_to(l2_nodes[i].get_center()) for i in range(3)],
                run_time=1.5,
                rate_func=smooth,
            )
            self.play(
                *[wave[i].animate.move_to(l3_nodes[0].get_center()) for i in range(3)],
                run_time=1.5,
                rate_func=smooth,
            )
            self.play(
                *[
                    wave[i].animate.move_to(
                        pred_box.get_center()
                        + UP * 0.1
                        + LEFT * 0.15
                        + RIGHT * 0.15 * i
                    )
                    for i in range(3)
                ],
                run_time=1.2,
                rate_func=smooth,
            )
            self.wait(0.3)

        # --- Gentle final pulse at prediction ---
        self.play(
            *[wave1[i].animate.scale(1.3).set_color("#F38BA8") for i in range(3)],
            run_time=0.6,
        )
        self.play(
            *[wave1[i].animate.scale(1 / 1.3).set_color("#E0AF68") for i in range(3)],
            run_time=0.6,
        )
        self.wait(2.0)
        # --- Scene 2: Loss Function: Measuring Error ---
        self.clear()
        self.camera.background_color = "#181825"

        # Color palette from style guide
        blue_cool = "#2AC3DE"
        amber_warm = "#E0AF68"
        pink_loss = "#F7768E"
        gray_stand = "#565F89"
        accent_fulcrum = "#7AA2F7"
        text_primary = "#C0CAF5"

        # --- Stage 1: Build the Balance Scale (0-6s) ---
        # Stand at bottom
        stand = Line(
            start=[-0.5, -1, 0], end=[0.5, -1, 0], color=gray_stand, stroke_width=6
        )

        # Fulcrum (triangle)
        fulcrum = Triangle(color=accent_fulcrum, fill_opacity=0.8)
        fulcrum.scale(0.4)
        fulcrum.move_to([0, -0.65, 0])

        # The beam
        beam = Line(start=[-3, 0, 0], end=[3, 0, 0], color="#A9B1D6", stroke_width=5)

        # Left pan (box) - cool blue
        left_box = Rectangle(width=1.4, height=0.7, color=blue_cool, stroke_width=3)
        left_box.set_fill(blue_cool, opacity=0.15)
        left_box.move_to([-2, 0.9, 0])

        # Left strings
        left_strings = VGroup(
            Line([-3, 0, 0], [-2.5, 0.55, 0], color="#A9B1D6", stroke_width=2),
            Line([-3, 0, 0], [-2, 0.55, 0], color="#A9B1D6", stroke_width=2),
            Line([-3, 0, 0], [-1.5, 0.55, 0], color="#A9B1D6", stroke_width=2),
        )

        # Right pan (box) - warm amber
        right_box = Rectangle(width=1.4, height=0.7, color=amber_warm, stroke_width=3)
        right_box.set_fill(amber_warm, opacity=0.15)
        right_box.move_to([2, 0.9, 0])

        # Right strings
        right_strings = VGroup(
            Line([3, 0, 0], [1.5, 0.55, 0], color="#A9B1D6", stroke_width=2),
            Line([3, 0, 0], [2, 0.55, 0], color="#A9B1D6", stroke_width=2),
            Line([3, 0, 0], [2.5, 0.55, 0], color="#A9B1D6", stroke_width=2),
        )

        # Labels
        pred_label = Text("Prediction", font_size=28, color=blue_cool)
        pred_label.move_to(left_box.get_center())

        target_label = Text("Target", font_size=28, color=amber_warm)
        target_label.move_to(right_box.get_center())

        # Loss counter with ValueTracker
        loss_tracker = ValueTracker(0.0)
        loss_display = DecimalNumber(
            0.0, num_decimal_places=2, color=pink_loss, font_size=40
        )
        loss_text = Text("Loss:", font_size=32, color=text_primary)
        loss_group = VGroup(loss_text, loss_display).arrange(RIGHT, buff=0.2)
        loss_group.move_to([0, -2.2, 0])

        loss_display.add_updater(lambda m: m.set_value(loss_tracker.get_value()))

        # Fulcrum dot
        fulcrum_dot = Dot(point=[0, -0.3, 0], radius=0.06, color="#A9B1D6")

        # Scene title
        title = Text("Loss Function: Measuring Error", font_size=36, color=text_primary)
        title.to_edge(UP, buff=0.4)

        # === ENTRY (0-4.5s) ===
        self.play(
            AnimationGroup(
                FadeIn(stand),
                FadeIn(fulcrum),
                FadeIn(fulcrum_dot),
                FadeIn(beam),
                FadeIn(left_strings),
                FadeIn(right_strings),
                FadeIn(left_box),
                FadeIn(right_box),
                FadeIn(pred_label),
                FadeIn(target_label),
                FadeIn(loss_group),
                lag_ratio=0.1,
            ),
            run_time=3.5,
        )
        self.play(FadeIn(title), run_time=0.5)
        self.wait(0.5)

        # === NARRATION SETUP (4.5-7.5s) ===
        self.wait(3.0)

        # === Stage 2: First tip - small mismatch (7.5-14s) ===
        scale_mech = VGroup(
            beam,
            left_strings,
            right_strings,
            left_box,
            right_box,
            pred_label,
            target_label,
        )
        self.play(
            scale_mech.animate.rotate(-PI / 18, about_point=[0, -0.3, 0]),
            loss_tracker.animate.set_value(0.32),
            run_time=4.5,
            rate_func=smooth,
        )
        self.wait(2.0)

        # === Stage 3: Second tip - growing mismatch (14-21s) ===
        self.play(
            scale_mech.animate.rotate(-PI / 16, about_point=[0, -0.3, 0]),
            loss_tracker.animate.set_value(0.78),
            run_time=4.5,
            rate_func=smooth,
        )
        self.wait(2.0)

        # === Stage 4: Third tip - large mismatch (21-28s) ===
        # Custom exponential ease-out since ease_out_expo may not be available
        def ease_out_expo_custom(t):
            return 1 - pow(2, -10 * t)

        self.play(
            scale_mech.animate.rotate(-PI / 14, about_point=[0, -0.3, 0]),
            loss_tracker.animate.set_value(1.42),
            run_time=4.5,
            rate_func=ease_out_expo_custom,
        )
        self.wait(2.5)
        # --- Scene 3: Chain Rule: The Core Mechanism ---
        self.clear()
        # --- Scene 3: Chain Rule: The Core Mechanism ---
        # Color palette from style guidelines
        DOMINO_COLOR = "#C0CAF5"
        HAND_COLOR = "#E0AF68"
        GLOW_COLOR = "#F7768E"
        WEIGHT_COLOR = "#9ECE6A"
        AMBER = "#fab387"
        BLUE = "#89b4fa"
        BG_COLOR = "#181825"

        self.camera.background_color = BG_COLOR

        # ---- 1. OBJECTS ----

        # Domino line: 8 upright rectangles
        dominoes = VGroup()
        for i in range(8):
            dom = Rectangle(
                width=0.4,
                height=1.0,
                color=DOMINO_COLOR,
                fill_opacity=0.2,
                stroke_width=2,
            )
            dominoes.add(dom)
        dominoes.arrange(RIGHT, buff=0.9)
        dominoes.move_to(ORIGIN)

        # Push hand (arrow tapping from right)
        push_hand = Arrow(
            start=[4.2, 0.2, 0], end=[3.3, 0, 0], color=HAND_COLOR, stroke_width=3
        )

        # Glow effect behind rightmost domino
        glow = Circle(radius=0.5, color=GLOW_COLOR, fill_opacity=0.2, stroke_width=1)
        glow.move_to([3, 0, 0])

        # Labels
        label_final = Text("Final Prediction", color=HAND_COLOR, font_size=36)
        label_final.move_to([4, -1.5, 0])

        label_end = Text("Weight", color=WEIGHT_COLOR, font_size=36)
        label_end.move_to([-4, -1.5, 0])

        title = Text("Chain Rule: The Core Mechanism", color=BLUE, font_size=44)
        title.move_to([0, 2.5, 0])

        # ---- 2. ANIMATIONS ----
        # Total duration must be exactly 33.0 seconds

        # Act 1: Intro & Setup (0-4s)
        self.play(FadeIn(title), run_time=1.5)
        self.play(
            AnimationGroup(
                FadeIn(dominoes, shift=UP * 0.2),
                FadeIn(label_final),
                FadeIn(label_end),
                lag_ratio=0.2,
            ),
            run_time=2.5,
        )
        self.wait(1)  # cum to ~5.0s

        # Act 2: The Push (5-9.5s)
        self.play(FadeIn(push_hand, shift=RIGHT), run_time=1)  # 6.0
        self.wait(0.5)  # 6.5
        self.play(  # 6.8
            push_hand.animate.shift(LEFT * 0.3),
            run_time=0.3,
            rate_func=there_and_back,
        )
        self.wait(0.5)  # 7.3
        self.play(FadeOut(push_hand, shift=RIGHT), run_time=0.5)  # 7.8
        self.wait(0.2)  # 8.0
        self.play(FadeIn(glow, scale=0.5), run_time=0.5)  # 8.5
        self.wait(0.5)  # 9.0
        # End of act 2 at ~9.0s

        # Act 3: Chain Reaction (9s to ~26.5s)
        for i, dom in enumerate(dominoes):
            next_wait = 0.4 if i < len(dominoes) - 1 else 0.0
            self.play(
                dom.animate.rotate(-PI / 2.2, about_point=dom.get_bottom()).set_fill(
                    AMBER, opacity=0.55
                ),
                run_time=1.4,
                rate_func=rate_functions.ease_in_cubic,
            )
            self.play(
                dom.animate.set_fill(DOMINO_COLOR, opacity=0.2),
                run_time=0.3,
            )
            if next_wait > 0:
                self.wait(next_wait)

        # Act 4: Hold / Outro (to 33.0s)
        self.wait(6.0)
        # --- Scene 4: Gradient Computation: Error Signal Backward ---
        self.clear()
        # --- Scene 4: Gradient Computation: Error Signal Backward ---

        output_node = Circle(radius=0.5, color="#F7768E", fill_opacity=0).move_to(
            [3, 0, 0]
        )
        output_label = Text("Output", font_size=36).next_to(output_node, UP)

        hidden_node_a = Circle(radius=0.4, color="#BB9AF7", fill_opacity=0).move_to(
            [0, 2, 0]
        )
        hidden_label_a = Text("Hidden A", font_size=36).next_to(hidden_node_a, UP)

        hidden_node_b = Circle(radius=0.4, color="#BB9AF7", fill_opacity=0).move_to(
            [0, -2, 0]
        )
        hidden_label_b = Text("Hidden B", font_size=36).next_to(hidden_node_b, DOWN)

        input_nodes = VGroup(
            *[Circle(radius=0.35, color="#7AA2F7", fill_opacity=0) for _ in range(3)]
        )
        input_nodes.arrange(DOWN, buff=1.5).move_to([-4, 0, 0])

        # Reverse arrows for backpropagation
        arrow1a = Arrow(
            start=[3, 0, 0], end=[0, 2, 0], color="#565F89", stroke_width=4, buff=0.4
        )
        arrow1b = Arrow(
            start=[3, 0, 0], end=[0, -2, 0], color="#565F89", stroke_width=4, buff=0.4
        )
        arrow2a = Arrow(
            start=[0, 2, 0],
            end=[-4, 1.5, 0],
            color="#565F89",
            stroke_width=3,
            buff=0.35,
        )
        arrow2b = Arrow(
            start=[0, 2, 0], end=[-4, 0, 0], color="#565F89", stroke_width=3, buff=0.35
        )
        arrow2c = Arrow(
            start=[0, 2, 0],
            end=[-4, -1.5, 0],
            color="#565F89",
            stroke_width=3,
            buff=0.35,
        )
        arrow3a = Arrow(
            start=[0, -2, 0],
            end=[-4, 1.5, 0],
            color="#565F89",
            stroke_width=3,
            buff=0.35,
        )
        arrow3b = Arrow(
            start=[0, -2, 0], end=[-4, 0, 0], color="#565F89", stroke_width=3, buff=0.35
        )
        arrow3c = Arrow(
            start=[0, -2, 0],
            end=[-4, -1.5, 0],
            color="#565F89",
            stroke_width=3,
            buff=0.35,
        )

        reverse_arrows = VGroup(
            arrow1a, arrow1b, arrow2a, arrow2b, arrow2c, arrow3a, arrow3b, arrow3c
        )

        # Title
        title = Text(
            "Gradient Computation: Error Signal Backward", font_size=48
        ).to_edge(UP)

        # Setup static network
        self.add(
            title,
            output_node,
            output_label,
            hidden_node_a,
            hidden_label_a,
            hidden_node_b,
            hidden_label_b,
            input_nodes,
        )
        self.play(Create(reverse_arrows), run_time=1.5)
        self.wait(0.5)

        # Error dye blob at output
        error_dye = Circle(
            radius=0.15, fill_color="#F7768E", fill_opacity=0.8, stroke_width=0
        ).move_to([3, 0, 0])
        self.play(FadeIn(error_dye), run_time=0.5)

        # Animate backward signal flowing
        # Step 1: Output to Hidden
        dye_a = error_dye.copy().move_to([3, 0, 0])
        dye_b = error_dye.copy().move_to([3, 0, 0])

        self.play(
            dye_a.animate.move_to([0, 2, 0]).set_fill("#BB9AF7", opacity=0.7),
            dye_b.animate.move_to([0, -2, 0]).set_fill("#BB9AF7", opacity=0.7),
            hidden_node_a.animate.set_fill("#BB9AF7", opacity=0.4),
            hidden_node_b.animate.set_fill("#BB9AF7", opacity=0.4),
            run_time=2,
            rate_func=exponential_decay,
        )

        # Step 2: Hidden to Input (splitting and thinning)
        dye_a1 = dye_a.copy().move_to([0, 2, 0])
        dye_a2 = dye_a.copy().move_to([0, 2, 0])
        dye_a3 = dye_a.copy().move_to([0, 2, 0])
        dye_b1 = dye_b.copy().move_to([0, -2, 0])
        dye_b2 = dye_b.copy().move_to([0, -2, 0])
        dye_b3 = dye_b.copy().move_to([0, -2, 0])

        dye_a_list = [dye_a1, dye_a2, dye_a3]
        dye_b_list = [dye_b1, dye_b2, dye_b3]
        targets = [
            ([-4, 1.5, 0], 0.3),
            ([-4, 0, 0], 0.3),
            ([-4, -1.5, 0], 0.2),
        ]

        animations = []
        for i, (target, scale) in enumerate(targets):
            animations.append(dye_a_list[i].animate.move_to(target).scale(scale))
            animations.append(dye_b_list[i].animate.move_to(target).scale(scale))
        for i in range(3):
            animations.append(input_nodes[i].animate.set_fill("#7AA2F7", opacity=0.4))

        self.play(*animations, run_time=2.5, rate_func=exponential_decay)

        # Final labels
        chain_label = Text("Chain Rule Applied", font_size=40).to_edge(DOWN)
        self.play(Write(chain_label), run_time=1)

        self.wait(2)
        # --- Scene 5: Weight Update: Adjusting Connections ---
        config.background_color = "#181825"
        self.camera.background_color = config.background_color

        # 1. CREATE OBJECTS

        # Control panel (optimizer)
        control_panel = RoundedRectangle(
            corner_radius=0.2,
            width=6.0,
            height=2.5,
            color="#565F89",
            stroke_width=2,
            fill_color="#1e1e2e",
            fill_opacity=0.8,
        )
        control_panel.move_to([0, -1.5, 0])

        panel_label = Text("Optimizer", font_size=30, color="#C0CAF5")
        panel_label.next_to(control_panel, DOWN, buff=0.3)

        # Central weight knob
        weight_knob = Circle(radius=0.8, color="#E0AF68", stroke_width=3)
        weight_knob.move_to(ORIGIN)

        # Visible marker so rotation is seen
        knob_mark = Line(ORIGIN, RIGHT * 0.65, stroke_width=4, color="#E0AF68")
        knob_group = VGroup(weight_knob, knob_mark)
        knob_group.move_to(ORIGIN)

        # Gradient arrow (horizontal)
        gradient_arrow = Arrow(
            start=[-0.8, 1.5, 0],
            end=[0.8, 1.5, 0],
            color="#2AC3DE",
            stroke_width=3,
            buff=0.1,
            tip_length=0.25,
        )
        gradient_label = Text("Gradient", font_size=28, color="#2AC3DE")
        gradient_label.next_to(gradient_arrow, UP, buff=0.2)

        # Learning Rate arrow (vertical)
        lr_arrow = Arrow(
            start=[2.5, 0.8, 0],
            end=[2.5, -0.8, 0],
            color="#9ECE6A",
            stroke_width=3,
            buff=0.1,
            tip_length=0.25,
        )
        lr_label = Text("Learning Rate", font_size=28, color="#9ECE6A")
        lr_label.next_to(lr_arrow, RIGHT, buff=0.2)

        # Indicator light
        indicator_light = Dot(point=[-2.5, -1.5, 0], radius=0.15, color="#F7768E")

        # Weight readout
        weight_readout = Text("w:  0.50", font_size=22, color="#C0CAF5")
        weight_readout.move_to([0, -1.5, 0])

        # Mini network diagram
        mini_nodes = VGroup()
        positions = [
            [-2.2, 2.4, 0],
            [-0.8, 2.4, 0],
            [0.8, 2.4, 0],
            [2.2, 2.4, 0],
            [-1.5, 3.3, 0],
            [0.0, 3.3, 0],
            [1.5, 3.3, 0],
            [0.0, 4.2, 0],
        ]
        for pos in positions:
            mini_nodes.add(Dot(point=pos, radius=0.1, color="#7AA2F7"))

        mini_edges = VGroup()
        connections = [
            (0, 4),
            (1, 4),
            (1, 5),
            (2, 5),
            (2, 6),
            (3, 6),
            (4, 7),
            (5, 7),
            (6, 7),
        ]
        for a, b in connections:
            mini_edges.add(
                Line(
                    mini_nodes[a].get_center(),
                    mini_nodes[b].get_center(),
                    stroke_width=1.5,
                    color="#7AA2F7",
                ).set_opacity(0.6)
            )

        network_mini = VGroup(mini_nodes, mini_edges)
        network_mini.move_to([0, 0.3, 0])

        # 2. ADD / INTRO
        self.play(FadeIn(control_panel), FadeIn(panel_label), run_time=1)
        self.play(FadeIn(weight_knob), FadeIn(knob_mark), run_time=1)
        self.play(
            FadeIn(gradient_arrow),
            Write(gradient_label),
            FadeIn(lr_arrow),
            Write(lr_label),
            run_time=1,
        )
        self.play(
            FadeIn(network_mini),
            FadeIn(indicator_light),
            FadeIn(weight_readout),
            run_time=1,
        )
        self.wait(1)

        # 3. MAIN ANIMATIONS

        # Gradient arrow pulse
        self.play(
            gradient_arrow.animate.scale(1.2), rate_func=there_and_back, run_time=1
        )
        self.wait(0.5)

        # LR arrow pulse
        self.play(lr_arrow.animate.scale(1.2), rate_func=there_and_back, run_time=1)
        self.wait(0.5)

        # First knob rotation
        self.play(knob_group.animate.rotate(PI / 3), rate_func=smooth, run_time=2)
        wr1 = Text("w:  0.43", font_size=22, color="#C0CAF5")
        wr1.move_to(weight_readout.get_center())
        self.play(ReplacementTransform(weight_readout, wr1), run_time=0.5)
        weight_readout = wr1
        self.wait(0.5)

        # Second knob rotation
        self.play(knob_group.animate.rotate(-PI / 4), rate_func=smooth, run_time=2)
        wr2 = Text("w:  0.47", font_size=22, color="#C0CAF5")
        wr2.move_to(weight_readout.get_center())
        self.play(ReplacementTransform(weight_readout, wr2), run_time=0.5)
        weight_readout = wr2
        self.wait(0.5)

        # Third knob rotation
        self.play(knob_group.animate.rotate(PI / 6), rate_func=smooth, run_time=2)
        wr3 = Text("w:  0.44", font_size=22, color="#C0CAF5")
        wr3.move_to(weight_readout.get_center())
        self.play(ReplacementTransform(weight_readout, wr3), run_time=0.5)
        weight_readout = wr3
        self.wait(1)

        # Network morph (improvement)
        self.play(
            *[
                edge.animate.set_opacity(0.9).set_stroke(width=2.5, color="#a6e3a1")
                for edge in mini_edges
            ],
            *[node.animate.set_color("#a6e3a1") for node in mini_nodes],
            indicator_light.animate.set_color("#a6e3a1"),
            run_time=2.5,
        )
        self.wait(1)

        # Indicator pulse
        self.play(
            indicator_light.animate.scale(1.8), rate_func=there_and_back, run_time=1
        )
        self.wait(0.5)

        # Arrows dim (smaller gradients near optimum)
        self.play(
            gradient_arrow.animate.set_opacity(0.4),
            gradient_label.animate.set_opacity(0.4),
            lr_arrow.animate.set_opacity(0.6),
            lr_label.animate.set_opacity(0.6),
            run_time=2,
        )
        self.wait(1)

        # Fine-tuning rotation
        self.play(knob_group.animate.rotate(PI / 8), rate_func=smooth, run_time=2)
        self.wait(1)

        # Final network glow
        self.play(
            *[edge.animate.set_stroke(color="#94e2d5", width=3) for edge in mini_edges],
            *[node.animate.set_color("#94e2d5") for node in mini_nodes],
            indicator_light.animate.set_color("#94e2d5").scale(1.3),
            run_time=2,
        )
        wr_final = Text("w:  0.445", font_size=22, color="#C0CAF5")
        wr_final.move_to(weight_readout.get_center())
        self.play(ReplacementTransform(weight_readout, wr_final), run_time=0.5)
        self.wait(0.5)

        # Total = 31.0 seconds
        # --- Scene 6: Iteration and Convergence ---
        self.camera.background_color = "#181825"

        # ============================================================
        # 1. LOSS LANDSCAPE (2D contour rings representing 3D bowl)
        # ============================================================
        contour_rings = VGroup()
        colors = ["#1A1B2E", "#24283B", "#2E3A5F", "#3B4D7A", "#4A6395", "#5A7AB0"]
        for i, color in enumerate(colors):
            width = 7.0 - i * 1.0
            height = 4.5 - i * 0.65
            ellipse = Ellipse(
                width=width,
                height=height,
                color=color,
                fill_opacity=0.6,
                stroke_width=1.5,
                stroke_color="#565F89",
            )
            contour_rings.add(ellipse)

        center_glow = Ellipse(
            width=1.2,
            height=0.8,
            color="#9ECE6A",
            fill_opacity=0.35,
            stroke_width=2,
            stroke_color="#9ECE6A",
        )

        landscape = VGroup(contour_rings, center_glow)
        landscape.shift(DOWN * 0.3)

        # ============================================================
        # 2. BALL & 3D-LOOK HALO
        # ============================================================
        ball = Dot(point=UP * 2.5 + LEFT * 3.2, radius=0.18, color="#E0AF68")
        ball_halo = Circle(
            radius=0.28, color="#E0AF68", stroke_width=2, stroke_opacity=0.4
        )
        ball_halo.move_to(ball.get_center())
        ball_group = VGroup(ball, ball_halo)

        # ============================================================
        # 3. DESCENT TRAIL (pre-defined smooth path)
        # ============================================================
        path_points = [
            ball.get_center(),
            UP * 1.8 + LEFT * 2.0,
            UP * 0.9 + LEFT * 0.8,
            RIGHT * 0.5 + DOWN * 0.3,
            RIGHT * 1.5 + DOWN * 1.0,
            RIGHT * 2.1 + DOWN * 1.5,
        ]
        trail_path = VMobject()
        trail_path.set_points_as_corners(path_points)
        trail_path_smooth = trail_path.make_smooth()
        trail_path_smooth.set_stroke(color="#BB9AF7", width=3)

        # ============================================================
        # 4. LABELS
        # ============================================================
        global_min_label = Text("Global Minimum", font_size=28, color="#9ECE6A")
        global_min_label.move_to(DOWN * 1.8 + RIGHT * 2.5)

        title = Text("Iteration & Convergence", font_size=40, color="#C0CAF5")
        title.to_edge(UP, buff=0.5)

        subtitle = Text(
            "Each step rolls the ball closer to the lowest valley",
            font_size=22,
            color="#565F89",
        )
        subtitle.next_to(title, DOWN, buff=0.2)

        # ============================================================
        # 5. ANIMATION SEQUENCE (target duration: 27 s)
        # ============================================================

        # --- Phase 1: Reveal landscape & labels (0 s → 5 s) ---
        self.play(
            FadeIn(contour_rings, lag_ratio=0.1),
            FadeIn(center_glow),
            FadeIn(title),
            FadeIn(subtitle),
            run_time=3,
        )
        self.play(FadeIn(global_min_label), run_time=2)

        # --- Phase 2: Introduce ball (5 s → 7 s) ---
        self.play(FadeIn(ball_group), run_time=1.5)
        self.wait(0.5)

        # --- Phase 3: Ball descends leaving glowing trail (7 s → 22 s) ---
        self.play(
            MoveAlongPath(ball_group, trail_path_smooth),
            Create(trail_path_smooth),
            run_time=14,
            rate_func=smooth,
        )

        # --- Phase 4: Ball settles at bottom (22 s → 25 s) ---
        self.play(
            ball_group.animate.scale(1.3).set_color("#FFE4B5"),
            run_time=0.8,
            rate_func=there_and_back,
        )
        self.play(ball_group.animate.scale(1.0), run_time=0.7, rate_func=smooth)
        self.wait(1.5)

        # --- Phase 5: Final pause to pad to exactly 27 s (25 s → 27 s) ---
        self.wait(2)
        # --- Scene 7: Local Minima and Advanced Optimizers ---
        self.clear()
        # --- Scene 7: Local Minima and Advanced Optimizers ---
        # Color palette from style guidelines
        BG_COLOR = "#181825"
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"
        TOKYO_BLUE = "#7AA2F7"
        TOKYO_PURPLE = "#BB9AF7"
        TOKYO_GREEN = "#9ECE6A"
        TOKYO_GOLD = "#E0AF68"
        TOKYO_RED = "#F7768E"

        self.camera.background_color = BG_COLOR

        # ============================================================
        # 1. LOSS LANDSCAPE (2D wavy terrain)
        #    - Shallow local minimum near x=-1.5
        #    - Hill around x=0
        #    - Deep global minimum near x=2.5
        # ============================================================

        landscape_points = [
            np.array([-3.5, 1.5, 0]),
            np.array([-2.5, 0.8, 0]),
            np.array([-1.5, 0.2, 0]),  # shallow local minimum
            np.array([-0.8, 0.7, 0]),
            np.array([0.0, 1.4, 0]),  # hill peak
            np.array([0.6, 1.0, 0]),
            np.array([1.2, 0.4, 0]),
            np.array([1.8, -0.1, 0]),
            np.array([2.5, -0.5, 0]),  # deep global minimum
            np.array([3.2, -0.1, 0]),
            np.array([3.8, 0.6, 0]),
        ]

        loss_curve = VMobject()
        loss_curve.set_points_smoothly(landscape_points)
        loss_curve.set_stroke(TOKYO_BLUE, width=3, opacity=0.9)

        # Filled area under curve
        baseline = [np.array([p[0], -2.5, 0]) for p in landscape_points]
        fill_points = landscape_points + baseline[::-1]
        loss_fill = Polygon(*fill_points)
        loss_fill.set_fill(TOKYO_BLUE, opacity=0.12)
        loss_fill.set_stroke(width=0)

        # Terrain labels
        local_min_label = Text("Shallow Dip", font_size=18, color=PEACH)
        local_min_label.next_to(np.array([-1.5, 0.2, 0]), UP, buff=0.25)

        hill_label = Text("Local Hill", font_size=18, color=PINK)
        hill_label.next_to(np.array([0.0, 1.4, 0]), UP, buff=0.25)

        better_min_label = Text("Better Minimum", font_size=26, color=TOKYO_GREEN)
        better_min_label.move_to(np.array([2.5, -1.6, 0]))

        # ============================================================
        # 2. MARBLE (2D circle with glow)
        # ============================================================
        marble = Circle(radius=0.18, color=TOKYO_GOLD, fill_opacity=1.0)
        marble.set_fill(TOKYO_GOLD, opacity=0.95)
        marble.move_to(np.array([-1.5, 0.42, 0]))

        marble_glow = Circle(radius=0.32, color=TOKYO_GOLD, fill_opacity=0.15)
        marble_glow.set_fill(TOKYO_GOLD, opacity=0.15)
        marble_glow.move_to(np.array([-1.5, 0.42, 0]))

        # ============================================================
        # 3. ROCKET THRUSTERS (arrows with flame effects)
        # ============================================================
        # Positioned at the sides of the marble, pointing to propel forward
        thruster_left = Arrow(
            start=np.array([-1.65, 0.25, 0]),
            end=np.array([-1.35, 0.55, 0]),
            color=TOKYO_RED,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.35,
        )

        thruster_right = Arrow(
            start=np.array([-1.35, 0.25, 0]),
            end=np.array([-1.05, 0.55, 0]),
            color=TOKYO_RED,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.35,
        )

        # Flame glow circles at thruster tips
        flame_left = Dot(point=np.array([-1.35, 0.55, 0]), radius=0.1, color=PEACH)
        flame_left.set_fill(PEACH, opacity=0.8)
        flame_right = Dot(point=np.array([-1.05, 0.55, 0]), radius=0.1, color=PEACH)
        flame_right.set_fill(PEACH, opacity=0.8)

        # ============================================================
        # 4. BRAKE LIGHT (adaptive - glows on steep slopes)
        # ============================================================
        brake_light = Circle(radius=0.08, color=TOKYO_PURPLE, fill_opacity=0.5)
        brake_light.set_fill(TOKYO_PURPLE, opacity=0.5)
        brake_light.move_to(np.array([-1.5, 0.18, 0]))

        # ============================================================
        # 5. TITLE AND EXPLANATION
        # ============================================================
        title = Text("Escaping Local Minima", font_size=30, color=BLUE)
        title.to_edge(UP, buff=0.5)

        subtitle = Text("Momentum & Adaptive Learning Rates", font_size=20, color=TEAL)
        subtitle.next_to(title, DOWN, buff=0.15)

        # Group marble and its components for coordinated movement
        # Note: thrusters and flames need to stay relative to marble
        marble_core = VGroup(marble_glow, marble, brake_light)

        # ============================================================
        # ANIMATION SEQUENCE (28 seconds total)
        # ============================================================

        # --- Segment 1: Scene Setup (0s - 4s) ---
        self.play(
            FadeIn(loss_fill, run_time=1.5),
            Create(loss_curve, run_time=2),
            FadeIn(local_min_label, run_time=1),
            FadeIn(hill_label, run_time=1),
            run_time=3,
        )
        self.play(
            FadeIn(better_min_label, run_time=0.8),
            Write(title, run_time=1.2),
            Write(subtitle, run_time=1.2),
            run_time=1.2,
        )
        self.wait(0.8)

        # --- Segment 2: Marble Arrives (4s - 6s) ---
        self.play(
            FadeIn(marble, run_time=0.6),
            FadeIn(marble_glow, run_time=0.6),
            FadeIn(brake_light, run_time=0.6),
            run_time=0.8,
        )
        self.wait(1.2)

        # --- Segment 3: Thrusters Ignite (6s - 9s) ---
        self.play(
            GrowFromCenter(thruster_left, run_time=0.4),
            GrowFromCenter(thruster_right, run_time=0.4),
            FadeIn(flame_left, run_time=0.3),
            FadeIn(flame_right, run_time=0.3),
            run_time=0.5,
        )

        # Flame pulse - engines firing
        self.play(
            flame_left.animate.scale(1.4).set_opacity(1.0),
            flame_right.animate.scale(1.4).set_opacity(1.0),
            rate_func=there_and_back,
            run_time=0.6,
        )
        self.wait(0.5)

        # Second flame pulse
        self.play(
            flame_left.animate.scale(1.3),
            flame_right.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=0.5,
        )
        self.wait(0.9)

        # --- Segment 4: Climbing the Hill (9s - 14s) ---
        # Move from shallow min toward hill peak
        # We move the marble core and animate thrusters following

        # Position 1: Start climbing
        self.play(
            marble_core.animate.move_to(np.array([-0.6, 0.65, 0])),
            thruster_left.animate.put_start_and_end_on(
                np.array([-0.75, 0.48, 0]), np.array([-0.45, 0.78, 0])
            ),
            thruster_right.animate.put_start_and_end_on(
                np.array([-0.45, 0.48, 0]), np.array([-0.15, 0.78, 0])
            ),
            flame_left.animate.move_to(np.array([-0.45, 0.78, 0])),
            flame_right.animate.move_to(np.array([-0.15, 0.78, 0])),
            run_time=2,
            rate_func=smooth,
        )

        # Brake light flashes - adaptive control on slope
        self.play(
            brake_light.animate.scale(2.0).set_fill(TOKYO_PURPLE, opacity=1.0),
            run_time=0.4,
            rate_func=there_and_back,
        )
        self.wait(0.3)

        # Position 2: At hill peak
        self.play(
            marble_core.animate.move_to(np.array([0.2, 1.25, 0])),
            thruster_left.animate.put_start_and_end_on(
                np.array([0.05, 1.08, 0]), np.array([0.35, 1.38, 0])
            ),
            thruster_right.animate.put_start_and_end_on(
                np.array([0.35, 1.08, 0]), np.array([0.65, 1.38, 0])
            ),
            flame_left.animate.move_to(np.array([0.35, 1.38, 0])),
            flame_right.animate.move_to(np.array([0.65, 1.38, 0])),
            run_time=1.5,
            rate_func=smooth,
        )
        self.wait(0.8)

        # --- Segment 5: Descending to Better Minimum (14s - 20s) ---
        # Thrusters aid controlled descent
        self.play(
            thruster_left.animate.scale(0.7),
            thruster_right.animate.scale(0.7),
            run_time=0.5,
        )

        # Move down the slope - brake light active for control
        self.play(
            marble_core.animate.move_to(np.array([1.3, 0.35, 0])),
            thruster_left.animate.put_start_and_end_on(
                np.array([1.15, 0.18, 0]), np.array([1.45, 0.48, 0])
            ),
            thruster_right.animate.put_start_and_end_on(
                np.array([1.45, 0.18, 0]), np.array([1.75, 0.48, 0])
            ),
            flame_left.animate.move_to(np.array([1.45, 0.48, 0])),
            flame_right.animate.move_to(np.array([1.75, 0.48, 0])),
            brake_light.animate.scale(1.8).set_fill(TOKYO_PURPLE, opacity=0.9),
            run_time=2,
            rate_func=smooth,
        )

        # Brake pulses - controlling speed on steep descent
        self.play(
            brake_light.animate.scale(1.5).set_fill(TOKYO_PURPLE, opacity=1.0),
            run_time=0.3,
            rate_func=there_and_back,
        )
        self.wait(0.3)

        # Final approach to deep minimum
        self.play(
            marble_core.animate.move_to(np.array([2.5, -0.3, 0])),
            thruster_left.animate.put_start_and_end_on(
                np.array([2.35, -0.47, 0]), np.array([2.65, -0.17, 0])
            ),
            thruster_right.animate.put_start_and_end_on(
                np.array([2.65, -0.47, 0]), np.array([2.95, -0.17, 0])
            ),
            flame_left.animate.move_to(np.array([2.65, -0.17, 0])),
            flame_right.animate.move_to(np.array([2.95, -0.17, 0])),
            run_time=2,
            rate_func=smooth,
        )

        # Highlight the better minimum
        self.play(
            Indicate(better_min_label, color=GREEN, scale_factor=1.4),
            run_time=1.0,
        )
        self.wait(0.5)

        # --- Segment 6: Settling and Success (20s - 24s) ---
        # Retract thrusters
        self.play(
            FadeOut(thruster_left, run_time=0.5),
            FadeOut(thruster_right, run_time=0.5),
            FadeOut(flame_left, run_time=0.5),
            FadeOut(flame_right, run_time=0.5),
            brake_light.animate.scale(0.6).set_fill(TOKYO_PURPLE, opacity=0.2),
            run_time=0.8,
        )

        # Settle animation
        self.play(
            marble.animate.scale(1.15),
            rate_func=there_and_back,
            run_time=0.5,
        )
        self.play(
            marble_glow.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=0.5,
        )
        self.wait(2.2)

        # --- Segment 7: Final Emphasis (24s - 28s) ---
        success_box = SurroundingRectangle(better_min_label, color=GREEN, buff=0.2)
        self.play(
            Create(success_box, run_time=0.8),
            run_time=0.8,
        )

        # Subtle pulse on the success highlight
        self.play(
            success_box.animate.scale(1.05),
            rate_func=there_and_back,
            run_time=1.0,
        )

        # Hold final shot
        self.wait(2.2)
