from .generators.tofi import *


def main():
    fonts = Fonts(regular=Font('Comic Mono'))
    colors = ColorTheme(
        text=Color(0xff, 0xff, 0xff),
        primary=Color(0x55, 0x33, 0xee), 
        on_primary=Color(0x33, 0x22, 0xee),

        primary_dark=Color(0x11, 0x08, 0x55),
        on_primary_dark=Color(0xff, 0xff, 0xff),
        
        secondary=Color(0xee, 0x33, 0xee),
        secondary_dark=Color(0x55, 0x33, 0x55),

        background=Color(0x11, 0x11, 0x11),
        foreground=Color(0x99, 0x99, 0x99),
    )

    theme = Theme(font=fonts, font_size=FontSize(normal=11), colors=colors)
    Tofi.apple(theme).default_header().deploy()


if __name__ == '__main__':
    main()
