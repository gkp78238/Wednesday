import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .json_to_tml import json_to_tml
from thoughtspot_tml import Table
import json
import tempfile
from app import create_app, socketio

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            process_file(event.src_path)

def process_file(file_path):
    file_name = os.path.basename(file_path)
    logger.info(f"New file detected: {file_name}")

    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        
        tml_content = json_to_tml(json_data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tml', delete=False) as temp_file:
            temp_file.write(tml_content)
            temp_file_path = temp_file.name
        Table.load(temp_file_path)

        base_name = os.path.splitext(file_name)[0]
        tml_file_path = os.path.join('processed_files', f"{base_name}.tml")
        with open(tml_file_path, 'w') as tml_file:
            tml_file.write(tml_content)

        os.remove(temp_file_path)
        
        socketio.emit('file_processed', {'message': f"File {file_name} processed and converted to TML"}, namespace='/')
        logger.info(f"File {file_name} processed and converted to TML")

    except Exception as e:
        logger.error(f"Error processing {file_name}: {str(e)}")
        socketio.emit('file_processed', {'message': f"Error processing {file_name}: {str(e)}"})

    new_path = os.path.join('processed_files', file_name)
    os.rename(file_path, new_path)

if __name__ == "__main__":
    app = create_app()
    app.app_context().push()

    path_to_watch = os.path.join(os.path.dirname(__file__), '..', 'incoming_json')
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
