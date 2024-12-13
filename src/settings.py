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

def save_endpoint_id(endpoint_id):
    """Salva o ID do endpoint no arquivo de configuração."""
    with open(CONFIG_FILE, "w") as config_file:
        json.dump({"endpoint_id": endpoint_id}, config_file)

def load_endpoint_id():
    """Carrega o ID do endpoint do arquivo de configuração, se existir."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file).get("endpoint_id", "")
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
        
        # Campo para inserir o Project ID
        project_id_entry = Gtk.Entry()
        project_id_entry.set_placeholder_text("Insira seu Google Cloud Project ID")
        project_id_entry.set_text(load_project_id())
        layout.pack_start(project_id_entry, False, False, 0)

        # Campo para inserir a Região
        region_entry = Gtk.Entry()
        region_entry.set_placeholder_text("Insira sua Google Cloud Região")
        region_entry.set_text(load_region())
        layout.pack_start(region_entry, False, False, 0)

        # Campo para inserir o Endpoint ID
        endpoint_id_entry = Gtk.Entry()
        endpoint_id_entry.set_placeholder_text("Insira seu Google Cloud Endpoint ID")
        endpoint_id_entry.set_text(load_endpoint_id())
        layout.pack_start(endpoint_id_entry, False, False, 0)

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
