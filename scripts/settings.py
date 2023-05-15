from pathlib import Path

import gradio as gr
from modules import shared, scripts
from modules import script_callbacks

base_dir = Path(scripts.basedir())

def on_ui_settings():
    section = "image-upload", "Image Upload"
    shared.opts.add_option("iu_server_host", shared.OptionInfo("", "Server hostname", section=section))
    shared.opts.add_option("iu_server_port", shared.OptionInfo(22, "Server port", section=section))
    shared.opts.add_option("iu_server_user", shared.OptionInfo("", "Server username", section=section))
    shared.opts.add_option("iu_server_pass", shared.OptionInfo("", "Server password", section=section))
    shared.opts.add_option("iu_server_path", shared.OptionInfo("/", "Server path", section=section))

script_callbacks.on_ui_settings(on_ui_settings)
