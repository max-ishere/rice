from .generators.tofi import *


def main():
    fonts = Fonts(regular=Font("Comic Mono"))
    colors = ColorTheme(
        text=Color(0xFF, 0xFF, 0xFF),
        primary=Color(0x55, 0x33, 0xEE),
        on_primary=Color(0x33, 0x22, 0xEE),
        primary_dark=Color(0x11, 0x08, 0x55),
        on_primary_dark=Color(0xFF, 0xFF, 0xFF),
        secondary=Color(0xEE, 0x33, 0xEE),
        secondary_dark=Color(0x55, 0x33, 0x55),
        background=Color(0x11, 0x11, 0x11),
        foreground=Color(0x99, 0x99, 0x99),
    )

    theme = Theme(font=fonts, font_size=FontSize(normal=11), colors=colors)
    Tofi.apple(theme).default_header().deploy()


if __name__ == "__main__":
    main()
