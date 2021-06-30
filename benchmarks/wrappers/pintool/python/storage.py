import io
import os
import sys
import uuid
import shutil

try:
    from pinnearmap import pinnearmap_phase
except ImportError:
    # Do nothing when not running under the instrumentation tool
    def pinnearmap_phase(name):
        pass

class storage:
    instance = None
    buckets = None

    def __init__(self):
        self.buckets = dict()

    @staticmethod
    def ndp_phase(phase_name):
        pinnearmap_phase(phase_name)

    @staticmethod
    def unique_name(name):
        name, extension = name.split('.')
        return '{name}.{random}.{extension}'.format(
                    name=name,
                    extension=extension,
                    random=str(uuid.uuid4()).split('-')[0]
                )

    def ensure_bucket(self, bucket):
        if bucket not in self.buckets:
            self.buckets[bucket] = dict()

    def upload(self, bucket, file, filepath):
        key_name = storage.unique_name(file)
        self.ensure_bucket(bucket)
        self.buckets[bucket][key_name] = filepath
        return key_name

    def download(self, bucket, file, filepath):
        shutil.copyfile(self.buckets[bucket][file], filepath)

    def download_directory(self, bucket, prefix, path):
        for object_name, stored_file in self.buckets[bucket].items():
            if not object_name.startswith(prefix):
                continue
            shutil.copyfile(stored_file, os.path.join(path, object_name))

    def upload_stream(self, bucket, file, bytes_data):
        key_name = storage.unique_name(file)
        # no-op write
        return key_name

    def download_stream(self, bucket, file):
        data = b''
        filepath = self.buckets[bucket][file]
        with io.open(filepath, 'r') as fp:
            data = fp.read()
        return data

    def get_instance():
        if storage.instance is None:
            storage.instance = storage()
        return storage.instance

