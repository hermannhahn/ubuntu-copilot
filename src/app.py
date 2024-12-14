import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from ui.chat import ChatWindow
from settings import SettingsWindow, load_api_key, load_project_id, load_region

class App(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Ubuntu Co-Pilot Chatbot")
        self.set_default_size(600, 400)

        self.settings_window = SettingsWindow()
        self.api_key = load_api_key()
        self.project_id = load_project_id()
        self.region = load_region()

        # Verifica se as credenciais estão configuradas
        if not self.api_key or not self.project_id or not self.region:
            # api key alert message
            api_alert = Gtk.MessageDialog(
                transient_for=None,
                title="Settings",
                modal=True,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Por favor, configure as credenciais antes de continuar.",
            )
            api_alert.connect("response", lambda d, r: self.close_alert(d))
            api_alert.show()
            return

        # Layout principal (chat)
        self.chat = ChatWindow()
        self.set_child(self.chat.layout)
        
    def close_alert(self, d):
        d.close()
        self.open_settings()

    def open_settings(self):
        self.chat = ChatWindow()
        self.set_child(self.chat.layout)
        self.settings_window.show()


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        win = App(self)
        win.present()

if __name__ == "__main__":
    app = MyApp()
    app.run()
