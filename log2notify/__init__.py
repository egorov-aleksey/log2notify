import argparse
import logging
import os

import pyinotify as i
from plyer import notification


class Watcher(i.ProcessEvent):
    pointers = {}

    def __init__(self, path):
        if os.path.isfile(path):
            self.register_file(path)
        elif os.path.isdir(path):
            self.register_dir(path)

    def register_dir(self, dir):
        for item in os.listdir(dir):
            path = os.path.join(dir, item)

            if os.path.isfile(path):
                self.register_file(path)
            elif os.path.isdir(path):
                self.register_dir(path)

    def register_file(self, file):
        logging.info(file)
        self.pointers[file] = os.path.getsize(file)

    def register_new_file(self, file):
        logging.info(file)
        self.pointers[file] = 0

    def unregister_file(self, file):
        self.pointers.pop(file)

    def update_file_pointer(self, file):
        self.pointers[file] = os.path.getsize(file)

    def read_file(self, file):
        pointer = self.pointers[file]
        f = open(file)
        f.seek(pointer)
        res = f.read()
        f.close()

        self.update_file_pointer(file)

        return res

    def process_IN_MODIFY(self, event):
        logging.info(event)

        file_name = event.pathname

        if os.path.isfile(file_name):
            if file_name not in self.pointers:
                self.register_new_file(file_name)

            txt = self.read_file(file_name)

            if txt:
                try:
                    notification.notify(
                        title=file_name,
                        message=txt
                    )
                except Exception as e:
                    logging.exception(e)
                    notification.notify(
                        title="Exception when notify: %s" % str(file_name),
                        message=str(e)
                    )

    def process_IN_DELETE(self, event):
        logging.info(event)

        file_name = event.pathname

        if os.path.isfile(file_name):
            self.unregister_file(file_name)


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="file or directory for watching", nargs="*", default=[os.getcwd()])

    args = parser.parse_args()

    wm = i.WatchManager()
    for p in args.path:
        wm.add_watch(p, i.ALL_EVENTS, proc_fun=Watcher(p))

    notifier = i.Notifier(wm)
    notifier.loop()
