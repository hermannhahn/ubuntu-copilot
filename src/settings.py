import gi
import json
import os

gi.require_version("Gtk", "4.0")
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

def save_project_id(project_id):
    """Salva o ID do projeto no arquivo de configuração."""
    with open(CONFIG_FILE, "w") as config_file:
        json.dump({"project_id": project_id}, config_file)

def load_project_id():
    """Carrega o ID do projeto do arquivo de configuração, se existir."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file).get("project_id", "")
    return ""

def save_region(region):
    """Salva a região no arquivo de configuração."""
    with open(CONFIG_FILE, "w") as config_file:
        json.dump({"region": region}, config_file)

def load_region():
    """Carrega a região do arquivo de configuração, se existir."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file).get("region", "")
    return ""

class SettingsWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Configurações do Chatbot")
        self.set_default_size(400, 200)

        # Layout principal
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        layout.set_margin_top(10)
        layout.set_margin_bottom(10)
        layout.set_margin_start(10)
        layout.set_margin_end(10)
        self.set_child(layout)

        # Campo para inserir a API Key
        self.api_key_entry = Gtk.Entry()
        self.api_key_entry.set_placeholder_text("Insira sua OpenAI API Key")
        self.api_key_entry.set_text(load_api_key())  # Preenche com a chave existente, se houver
        layout.append(self.api_key_entry)
        
        # Campo para inserir o Project ID
        self.project_id_entry = Gtk.Entry()
        self.project_id_entry.set_placeholder_text("Insira seu Google Cloud Project ID")
        self.project_id_entry.set_text(load_project_id())
        layout.append(self.project_id_entry)

        # Campo para inserir a Região
        self.region_entry = Gtk.Entry()
        self.region_entry.set_placeholder_text("Insira sua Google Cloud Região")
        self.region_entry.set_text(load_region())
        layout.append(self.region_entry)

        # Botão de salvar
        save_button = Gtk.Button(label="Salvar")
        save_button.connect("clicked", self.on_save_clicked)
        layout.append(save_button)

    def on_save_clicked(self, widget):
        api_key = self.api_key_entry.get_text().strip()
        project_id = self.project_id_entry.get_text().strip()
        region = self.region_entry.get_text().strip()

        if api_key:
            save_api_key(api_key)
        if project_id:
            save_project_id(project_id)
        if region:
            save_region(region)

        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Configurações salvas com sucesso!",
        )
        dialog.show()
        dialog.connect("response", lambda d, r: self.close(d))

    def close(self, d):
        d.close()
        self.destroy()

if __name__ == "__main__":
    app = Gtk.Application()
    def on_activate(app):
        win = SettingsWindow()
        win.set_application(app)
        win.present()

    app.connect("activate", on_activate)
    app.run()
