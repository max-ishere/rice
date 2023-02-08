from rice.generators.tofi import *

title = """Mac-inspired Tofi theme"""
category = "Theme template"
author = "max_ishere"
description = "A run launcher (tofi) theme similar to Mac."


def AppleTofi(theme: Theme = None, prompt="Run:", **kwargs: dict) -> Tofi:
    prompt = kwargs.get("prompt", prompt)
    theme = kwargs.get("theme", theme)

    return Tofi(
        font=theme.font.regular,
        font_size=theme.font_size.normal,
        text=TextTheme(
            text=FontTheme(
                color=theme.colors.text,
            ),
            prompt=FontTheme(
                color=theme.colors.on_primary_dark,
                background=theme.colors.primary_dark,
                padding="8, 12",
                corner_radius=10,
            ),
            selection=FontTheme(
                color=theme.colors.text,
                background=theme.colors.secondary_dark,
                padding="8, 12",
                corner_radius=10,
            ),
            selection_match=FontTheme(
                color=theme.colors.secondary,
            ),
        ),
        prompt=PromptTheme(
            text=prompt,
            placeholder="Application",
            horizontal=True,
            padding=22,
            result_spacing=30,
            min_width=300,
        ),
        window=WindowTheme(
            width="70%",
            height="70",
            background=theme.colors.background,
            outline_width=0,
            border_color=theme.colors.foreground,
            border_width=5,
            corner_radius=30,
            padding=Padding(top=13, left=17),
            clip_to_padding=False,
        ),
        behaviour=Behaviour(require_match=False),
    )
