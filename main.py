# -*- coding: utf-8 -*-
"""NoseGol Automate - a small starter macro manager built with Python/Kivy."""
import json, os, webbrowser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore

KV = '''
<RootUI>:
    orientation: 'vertical'
    padding: '14dp'
    spacing: '10dp'
    canvas.before:
        Color:
            rgba: .055, .09, .16, 1
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: '[b]نوسه‌گل اتومیت[/b]'
        markup: True
        font_size: '26sp'
        color: .35, .82, 1, 1
        size_hint_y: None
        height: '52dp'
    Label:
        text: 'نسخهٔ آزمایشی ساخت و اجرای فرمان‌های ساده'
        font_size: '14sp'
        color: .88, .92, 1, 1
        size_hint_y: None
        height: '28dp'
    Button:
        text: '＋  ساخت فرمان جدید'
        size_hint_y: None
        height: '48dp'
        background_normal: ''
        background_color: .12, .48, .72, 1
        on_release: root.add_macro()
    ScrollView:
        do_scroll_x: False
        GridLayout:
            id: macro_list
            cols: 1
            spacing: '8dp'
            size_hint_y: None
            height: self.minimum_height
    Label:
        text: 'فعلاً اجرای دستی و بازکردن لینک پشتیبانی می‌شود؛ اجرای خودکار در پس‌زمینه هنوز اضافه نشده.'
        font_size: '12sp'
        color: .75, .78, .83, 1
        size_hint_y: None
        height: '44dp'
'''

class RootUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore(os.path.join(App.get_running_app().user_data_dir, 'macros.json'))
        self.refresh()

    def refresh(self):
        box = self.ids.macro_list
        box.clear_widgets()
        if not self.store.keys():
            box.add_widget(Label(text='هنوز فرمانی نساخته‌ای.', size_hint_y=None, height='50dp', color=(1,1,1,1)))
        for key in self.store.keys():
            m = self.store.get(key)
            row = BoxLayout(orientation='vertical', size_hint_y=None, height='116dp', padding='8dp', spacing='5dp')
            from kivy.graphics import Color, RoundedRectangle
            with row.canvas.before:
                Color(.10, .15, .24, 1)
                row.bg = RoundedRectangle(pos=row.pos, size=row.size, radius=[10])
            row.bind(pos=lambda w, p: setattr(w.bg, 'pos', p), size=lambda w, s: setattr(w.bg, 'size', s))
            row.add_widget(Label(text=f"[b]{m.get('name','فرمان')}[/b]\nنوع: {m.get('action','message')}", markup=True, halign='right', valign='middle', color=(1,1,1,1)))
            buttons = BoxLayout(size_hint_y=None, height='38dp', spacing='6dp')
            run = Button(text='اجرا', background_normal='', background_color=(.1,.55,.35,1))
            run.bind(on_release=lambda _, k=key: self.run_macro(k))
            delete = Button(text='حذف', size_hint_x=.35, background_normal='', background_color=(.55,.2,.22,1))
            delete.bind(on_release=lambda _, k=key: self.delete_macro(k))
            buttons.add_widget(run); buttons.add_widget(delete); row.add_widget(buttons); box.add_widget(row)

    def add_macro(self):
        layout = BoxLayout(orientation='vertical', padding='10dp', spacing='8dp')
        name = TextInput(hint_text='نام فرمان (مثلاً بازکردن سایت)', multiline=False, size_hint_y=None, height='44dp')
        kind = TextInput(hint_text='نوع: link یا message', text='message', multiline=False, size_hint_y=None, height='44dp')
        value = TextInput(hint_text='برای link آدرس https://... یا برای message متن پیام', multiline=False, size_hint_y=None, height='70dp')
        layout.add_widget(name); layout.add_widget(kind); layout.add_widget(value)
        buttons = BoxLayout(size_hint_y=None, height='44dp', spacing='8dp')
        popup = Popup(title='فرمان جدید', content=layout, size_hint=(.92,.55))
        save = Button(text='ذخیره')
        cancel = Button(text='لغو')
        def save_it(*_):
            if not name.text.strip() or not value.text.strip():
                self.info('نام و مقدار فرمان را وارد کن.'); return
            key = str(max([int(k) for k in self.store.keys()] + [0]) + 1)
            action = 'link' if kind.text.strip().lower() == 'link' else 'message'
            self.store.put(key, name=name.text.strip(), action=action, value=value.text.strip())
            popup.dismiss(); self.refresh()
        save.bind(on_release=save_it); cancel.bind(on_release=popup.dismiss)
        buttons.add_widget(save); buttons.add_widget(cancel); layout.add_widget(buttons)
        popup.open()

    def run_macro(self, key):
        m = self.store.get(key)
        if m.get('action') == 'link':
            url = m.get('value','').strip()
            if not url.startswith(('http://','https://')):
                self.info('آدرس باید با http:// یا https:// شروع شود.'); return
            try: webbrowser.open(url)
            except Exception: self.info('بازکردن لینک در این نسخه روی این دستگاه پشتیبانی نمی‌شود.')
        else:
            self.info(m.get('value',''))

    def delete_macro(self, key):
        self.store.delete(key); self.refresh()

    def info(self, message):
        Popup(title='نوسه‌گل', content=Label(text=message), size_hint=(.85,.35)).open()

class NoseGolApp(App):
    def build(self):
        self.title = 'نوسه‌گل اتومیت'
        Builder.load_string(KV)
        return RootUI()

if __name__ == '__main__':
    NoseGolApp().run()
