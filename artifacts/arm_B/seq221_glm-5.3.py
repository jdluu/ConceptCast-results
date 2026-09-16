from manim import *

# PLACEHOLDER — the original script was never received by the assistant.
# This file only exists so the render doesn't crash.
# Re-send the original script to get the real scenes back.


class OriginalScriptMissing(Scene):
    def construct(self) -> None:
        banner = Text("Original script not received", weight=BOLD)
        note = Text(
            "Re-send the original script to restore all scenes.",
            font_size=28,
        )
        note.next_to(banner, DOWN, buff=0.5)
        self.play(Write(banner))
        self.play(FadeIn(note))
        self.wait(2)
