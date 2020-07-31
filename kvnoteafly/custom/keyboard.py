import os

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.instructions import RenderContext
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.effectwidget import EffectWidget
from kivy.utils import get_color_from_hex


from custom.effects import ShaderTemplateMixin


class KeyboardLabelSeparatorOuter(Widget):
    background_color = get_color_from_hex("#0e0e0e")


class KeyboardLabelSeparatorInner(Label):
    background_color = get_color_from_hex("#0e0e0e")
    FONT_COLOR = "#eeeeee"
    FONT_SIZE = 36

    def __init__(self, **kwargs):
        markup_text = f"[color={self.FONT_COLOR}] + [/color]"
        super().__init__(text=markup_text, markup=True, font_size=self.FONT_SIZE, **kwargs)


class KeyboardImage(Image, ShaderTemplateMixin):
    fs = StringProperty('''
    vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
    {
        return color;
    }
    ''')
    vs = StringProperty('''
    void main (void) {
      frag_color = color;
      tex_coord0 = vTexCoords0;
      gl_Position = projection_mat * modelview_mat * vec4(vPosition.xy, 0.0, 1.0);
    }
    ''')

    display_pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        text = kwargs.pop('text')
        src = os.path.join("static", "keys", text.lower()) + ".png"
        if 'time_hint' in kwargs:
            time_hint = kwargs.pop('time_hint')
        else:
            time_hint = 1
        self.canvas = RenderContext()
        super().__init__(source=src, **kwargs)

        Clock.schedule_interval(self.update_shader, 0)
        Clock.schedule_once(self.toggle_display, time_hint)


    def update_shader(self, *args):
        s = self.canvas
        s['projection_mat'] = Window.render_context['projection_mat']
        s['time'] = Clock.get_boottime()
        s['resolution'] = list(map(float, self.size))
        s.ask_update()

    def on_fs(self, instance, value):
        self.canvas.shader.fs = self.FS_HEADER + value + self.FS_FOOTER

    def on_vs(self, instance, value):
        self.canvas.shader.vs = self.VS_HEADER + value

    def toggle_display(self, *args, **kwargs):
        self.display_pressed = not self.display_pressed

    def on_display_pressed(self, val, *args, **kwargs):
        self.vs = '''
            void main (void) {
              frag_color = color;
              tex_coord0 = vTexCoords0;
              gl_Position = projection_mat * modelview_mat * vec4(vPosition.x * 1.1, vPosition.y, 0.0, 1.1);
            }
            '''

        self.fs = '''
            vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
            {
                vec3 dark_color = color.xyz - 0.1;
                return vec4(dark_color, 1);
                
            }
            '''


class KeyboardLabel(Label):
    background_color = get_color_from_hex("#eeeeee")
    FONT_COLOR = '#0e0e0e'
    FONT_SIZE = 36

    def __init__(self, **kwargs):
        markup_text = f"[color={self.FONT_COLOR}]{kwargs.pop('text')}[/color]"
        super(KeyboardLabel, self).__init__(text=markup_text, markup=True, font_size=self.FONT_SIZE,
                                            **kwargs)
