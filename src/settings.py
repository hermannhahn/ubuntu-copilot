import gi
import json
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

CONFIG_FILE = "config.json"

def save_api_key(api_key):
    """Salva a chave da API no arquivo de configuração."""
    with open(CONFIG_FILE, "w") as config_file:
        json.dump({"api_key": api_key}, config_file)

def load_api_key():
    """Carrega a chave da API do arquivo de configuração, se existir."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file).get("api_key", "")
    return ""

class SettingsWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Configurações do Chatbot")
        self.set_default_size(400, 200)

        # Layout principal
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=10)
        self.add(layout)

        # Campo para inserir a API Key
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Insira sua OpenAI API Key")
        self.entry.set_text(load_api_key())  # Preenche com a chave existente, se houver
        layout.pack_start(self.entry, False, False, 0)

        # Botão de salvar
        save_button = Gtk.Button(label="Salvar")
        save_button.connect("clicked", self.on_save_clicked)
        layout.pack_start(save_button, False, False, 0)

    def on_save_clicked(self, widget):
        api_key = self.entry.get_text().strip()
        if api_key:
            save_api_key(api_key)
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Chave API salva com sucesso!",
            )
            dialog.run()
            dialog.destroy()
        else:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="A chave API não pode estar vazia.",
            )
            dialog.run()
            dialog.destroy()

if __name__ == "__main__":
    win = SettingsWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
