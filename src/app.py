import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from ui.chat import ChatWindow

class App(Gtk.Window):
    def __init__(self):
        super().__init__(title="Ubuntu Co-Pilot Chatbot")
        self.set_default_size(600, 400)

        # Layout principal (chat)
        self.chat = ChatWindow()
        self.add(self.chat.layout)

if __name__ == "__main__":
    app = App()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
