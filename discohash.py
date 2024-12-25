import os
import logging
import subprocess
from pwnagotchi import plugins


class DiscoHash(plugins.Plugin):
    __author__ = 'YourName'
    __version__ = '1.0.0'
    __description__ = 'This plugin processes handshakes using hcxpcapngtool.'

    def __init__(self):
        self.ready = False

    def on_loaded(self):
        self.ready = True
        logging.info("[DiscoHash] Plugin loaded and ready.")

    def on_epoch(self, agent, epoch_data):
        if not self.ready:
            return

        handshake_dir = "/home/pi/handshakes"
        try:
            handshake_files = [
                os.path.join(handshake_dir, f) for f in os.listdir(handshake_dir)
                if f.endswith('.pcapng')
            ]
            for file in handshake_files:
                self.process_handshake(file)
        except FileNotFoundError:
            logging.error("[DiscoHash] Handshake directory does not exist.")
        except Exception as e:
            logging.error(f"[DiscoHash] Error processing handshakes: {e}")

    def process_handshake(self, file_path):
        try:
            logging.info(f"[DiscoHash] Processing {file_path}...")
            subprocess.run(
                ["/usr/bin/hcxpcapngtool", "-o", f"{file_path}.hccapx", file_path],
                check=True
            )
            logging.info(f"[DiscoHash] Successfully processed {file_path}.")
        except subprocess.CalledProcessError as e:
            logging.error(f"[DiscoHash] Error running hcxpcapngtool: {e}")
        except Exception as e:
            logging.error(f"[DiscoHash] Unexpected error: {e}")
