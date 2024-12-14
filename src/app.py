import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from chat import ChatWindow

class App(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Ubuntu Co-Pilot Chatbot")
        self.set_default_size(600, 400)

        # Layout principal (chat)
        self.chat = ChatWindow()
        self.set_child(self.chat.layout)

class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        win = App(self)
        win.present()

if __name__ == "__main__":
    app = MyApp()
    app.run()
