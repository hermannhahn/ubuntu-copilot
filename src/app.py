import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class App(Gtk.Window):
    def __init__(self):
        super().__init__(title="Linux Co-Pilot Chatbot")
        self.set_default_size(600, 400)

        # Layout principal (chat)


if __name__ == "__main__":
    app = App()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
