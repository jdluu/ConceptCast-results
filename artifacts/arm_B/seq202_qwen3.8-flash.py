"""Placeholder corrected script returned when no previous scenes were provided."""

try:
    from manim import Scene, Text, Write
except ImportError:
    try:
        from manimlib import Scene, Text, Write
    except ImportError:
        Scene = object
        Text = None
        Write = None


class PlaceholderScene(Scene):
    def construct(self):
        if Write is None or Text is None:
            return
        text = Text("No original script was provided; placeholder scene preserved.")
        self.play(Write(text))