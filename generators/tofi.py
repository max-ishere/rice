from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from pathlib import Path
from datetime import datetime


def maybe(m):
    try:
        return m()
    except AttributeError as e:
        if e.obj is None:
            return None
        else: raise e


@dataclass
class Header:
    text: str = ''

    @classmethod
    def default(_, c: type):
        return Header().generated_time().class_path(c)

    def custom(self, text: str, end=''):
        self.text += text
        return self

    def generated_time(self, dt: datetime=None):
        self.text += f'Generated at {datetime.utcnow()} UTC\n'
        return self

    def class_path(self, c: type):
        self.text += f'Using {c.__module__}.{c.__class__.__qualname__}\n'
        return self


@dataclass
class ConfigFile:
    config_filename: Path = None
    header: Header=None

    def default_header(self):
        self.header = Header.default(self)
        return self

    def compile(self) -> str:
        raise NotImplementedError()

    def deploy(self, filename: Path = None):
        with open(filename or self.config_filename, 'w') as file:
            file.write(self.compile())


@dataclass
class Font:
    family: str=None
    style: str=None

@dataclass
class CursorType(Enum):
    Bar = auto()
    Block = auto()
    Underscore = auto()


@dataclass
class Color:
    r: int
    g: int
    b: int
    a: int = None

    def __repr__(self) -> str:
        if self.a is None:
            return f'#{self.r:02X}{self.g:02X}{self.b:02X}'
        else:
            return f'#{self.r:02X}{self.g:02X}{self.b:02X}{self.a:02X}'


@dataclass
class FontTheme:
    color: Color=None
    background: Color=None
    padding: int=None
    corner_radius: int=None


@dataclass
class TextTheme:
    text: FontTheme
    prompt: FontTheme=None
    placeholder: FontTheme=None
    input: FontTheme=None
    default_result: FontTheme=None
    alternate_result: FontTheme=None
    selection: FontTheme=None
    selection_match: Color=None
    

@dataclass
class CursorTheme:
    style: CursorType
    color: Color=None
    background: Color=None
    corner_radius: int=None
    thickness: int=None
    hidden: bool=None


@dataclass
class PromptTheme:
    text: str = None
    padding: int = None
    placeholder: str = None
    results: int = None
    result_spacing: int = None
    horizontal: bool = None
    min_width: int = None


@dataclass
class Padding:
    top: int=None
    bottom: int=None
    left: int=None
    right: int=None


@dataclass
class Margin:
    top: int=None
    bottom: int=None
    left: int=None
    right: int=None


@dataclass
class WindowTheme:
    width: int=None
    height: int=None
    background: Color=None
    outline_width: int=None
    outline_color: Color=None
    border_width: int=None
    border_color: Color=None
    corner_radius: int=None
    padding: Padding=None
    clip_to_padding: bool=None
    scale: bool=None


@dataclass
class Anchor(Flag):
    Top = auto()
    Bottom = auto()
    Left = auto()
    Right = auto()
    Center = auto()


@dataclass
class Position:
    output: str=None
    anchor: Anchor=None
    exclusive_zone: int=None
    margin: Margin=None


@dataclass
class Behaviour:
    mouse_cursor: bool=None
    history: bool=None
    history_file: str=None
    fuzzy_match: str=None
    require_match: bool=None
    hide_input: str=False # Specify a character to hide with or True for default character
    drun_launch: bool=None
    terminal: str=None
    late_keyboard_init: bool=None
    multi_instance: bool=None
    ascii_input: bool=None
 

@dataclass
class Fonts:
    regular: Font = None
    italic: Font = None
    bold: Font = None
    bold_italic: Font = None


@dataclass
class FontSize:
    small: int = None
    normal: int = None
    large: int = None
    huge: int = None


@dataclass
class ColorPallete:
    red: Color=None
    orange: Color=None
    yellow: Color=None
    green: Color=None
    cyan: Color=None
    blue: Color=None
    purple: Color=None
    magenta: Color=None


@dataclass
class ColorTheme:
    text: Color=None
    foreground: Color=None
    background: Color=None

    primary: Color=None
    on_primary: Color=None

    primary_dark: Color=None
    on_primary_dark: Color=None

    secondary: Color=None
    on_secondary: Color=None

    secondary_dark: Color=None
    on_secondary_dark: Color=None

    accent: Color=None
    on_accent: Color=None

    bright: ColorPallete=None
    normal: ColorPallete=None
    dim: ColorPallete=None


@dataclass
class Theme:
    font: Fonts = None
    font_size: FontSize = None
    colors: ColorTheme = None
    

@dataclass
class Tofi(ConfigFile):
    config_filename: Path = Path.home() / '.config/tofi/config'
    
    font: Font = None
    font_size: int = None
    text: TextTheme = None
    cursor: CursorTheme = None
    prompt: PromptTheme = None
    window: WindowTheme = None
    position: Position = None
    behaviour: Behaviour = None
    include: [str] = None

    @classmethod
    def apple(_, theme: Theme=None, prompt='Run:', **kwargs: dict):
        prompt = kwargs.get('prompt', prompt)
        theme = kwargs.get('theme', theme)

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
                    padding='8, 12',
                    corner_radius=10,
                ),

                selection_match=FontTheme(
                    color=theme.colors.secondary,
                ),
            ),

            prompt=PromptTheme(
                text=prompt,
                placeholder='Application',
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
    
    def compile(self) -> str:
        # Create a dictionary that can be later converted to the config
        conf = {}
        # Only if the user set the key try to insert values

        conf['font'] = maybe(lambda: self.font.family)
        conf['font-size'] = maybe(lambda: self.font_size)

        for (name, theme) in [
            ('text', maybe(lambda: self.text.text)),
            ('prompt', maybe(lambda: self.text.prompt)),
            ('placeholder', maybe(lambda: self.text.placeholder)),
            ('input', maybe(lambda: self.text.input)),
            ('default-result', maybe(lambda: self.text.default_result)),
            ('selection', maybe(lambda: self.text.selection)),
            ('selection-match', maybe(lambda: self.text.selection_match)),
        ]:
            if theme is not None:
                conf.update({
                    f'{name}-color': theme.color,
                    f'{name}-background': theme.background,
                    f'{name}-background-padding': theme.padding,
                    f'{name}-background-corner-radius': theme.corner_radius,
                })
        
        conf.update({
            'text-cursor-style': maybe(lambda: self.cursor.style),
            'text-cursor-color': maybe(lambda: self.cursor.color),
            'text-cursor-background': maybe(lambda: self.cursor.background),
            'text-cursor-corner-radius': maybe(lambda: self.cursor.corner_radius),
            'text-cursor-thickness': maybe(lambda: self.cursor.thickness),
            'text-cursor': maybe(lambda: self.cursor.hidden),

            'prompt-text': maybe(lambda: self.prompt.text),
            'prompt-padding': maybe(lambda: self.prompt.padding),
            'placeholder-text': maybe(lambda: self.prompt.placeholder),
            'num-results': maybe(lambda: self.prompt.results),
            'result-spacing': maybe(lambda: self.prompt.result_spacing),
            'horizontal': maybe(lambda: self.prompt.horizontal),
            'min-input-width': maybe(lambda: self.prompt.min_width),

            'width': maybe(lambda: self.window.width),
            'height': maybe(lambda: self.window.height),
            'background-color': maybe(lambda: self.window.background),
            'outline-width': maybe(lambda: self.window.outline_width),
            'outline-color': maybe(lambda: self.window.outline_color),
            'border-width': maybe(lambda: self.window.border_width),
            'border-color': maybe(lambda: self.window.border_color),
            'corner-radius': maybe(lambda: self.window.corner_radius),
            'clip-to-padding': maybe(lambda: self.window.clip_to_padding),
            'scale': maybe(lambda: self.window.scale),
 
            'padding-top': maybe(lambda: self.window.padding.top),
            'padding-bottom': maybe(lambda: self.window.padding.bottom),
            'padding-left': maybe(lambda: self.window.padding.left),
            'padding-right': maybe(lambda: self.window.padding.right),
             
            'output': maybe(lambda: self.position.output),
            'anchor': maybe(lambda: self.position.anchor),
            'exclusize-zone': maybe(lambda: self.position.exclusive_zone),
 
            'margin-top': maybe(lambda: self.position.padding.top),
            'margin-bottom': maybe(lambda: self.position.padding.bottom),
            'margin-left': maybe(lambda: self.position.padding.left),
            'margin-right': maybe(lambda: self.position.padding.right),
 
            'hide-cursor': maybe(lambda: self.behaviour.mouse_cursor),
            'fuzzy-match': maybe(lambda: self.behaviour.fuzzy_match),
            'require-match': maybe(lambda: self.behaviour.require_match),
            'hide-input': maybe(lambda: self.behaviour.hide_input) == True \
                or type(maybe(lambda: self.behaviour.hide_input)) == str,
            'hidden-character': c if type(c := maybe(lambda: self.behaviour.hide_input)) \
                is str else None,
            'drun-launch': maybe(lambda: self.behaviour.drun_launch),
            'terminal': maybe(lambda: self.behaviour.terminal),
            'late-keyboard-init': maybe(lambda: self.behaviour.late_keyboard_init),
            'multi-instance': maybe(lambda: self.behaviour.multi_instance),
            'ascii-input': maybe(lambda: self.behaviour.ascii_input),
            'history': maybe(lambda: self.behaviour.history) == True \
                or type(maybe(lambda: self.behaviour.history)) == str, 
            'history-file': h if type(h := maybe(lambda: self.behaviour.history)) == str \
                else None,
        })

        conf = '\n'.join([f'{key} = {value}' 
                          for (key, value) in conf.items() 
                          if value is not None])

        conf += '\n'.join([f'include = {path}' 
                           for path in self.include or []])

        return '\n'.join([
            '# ' + line 
            for line in self.header.text.splitlines()
        ]) + '\n\n' + conf
