import glob
from pathlib import Path
from . import BotzHub
import sys
import importlib
from pathlib import Path
import logging

logging.info("Starting Deployment...")


def load_plugins(plugin_name):
    path = Path(f"VideoEncoder/plugins/{plugin_name}.py")
    name = "VideoEncoder.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["VideoEncoder.plugins." + plugin_name] = load
    logging.info("VideoEncoder has Imported " + plugin_name)


path = "VideoEncoder/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

logging.info("Successfully deployed VideoEncoder!")

if __name__ == "__main__":
    BotzHub.run_until_disconnected()
