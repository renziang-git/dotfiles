#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class ScratchInput(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="sioyek.translate")

    def do_activate(self):
        self.win = Gtk.ApplicationWindow(application=self, title="Tmptype")
        self.win.set_default_size(220, 20)
#        self.win.set_border_width(1)

        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.textview.grab_focus()

        scroller.add(self.textview)
        self.win.add(scroller)

        # ⭐ 关键：在 Window 上监听 Esc
        self.win.connect("key-press-event", self.on_key_press)

        self.win.show_all()

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.quit()
            return True
        return False

app = ScratchInput()
app.run()

