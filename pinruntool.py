import sys, os
from os import path
import io
import argparse
import importlib

SCRIPT_DIR = path.abspath(path.join(path.dirname(__file__)))
BENCHMARKS_DIR = path.join(SCRIPT_DIR, 'benchmarks')
PIN_DIR = path.abspath(path.join(SCRIPT_DIR, '..', 'pin-NearMAP'))
PIN_PY_DIR = path.join(PIN_DIR, 'stublib', 'pybuild')
WRAPPER_PY_DIR = path.join(BENCHMARKS_DIR, 'wrappers', 'pintool', 'python')

def main():
    sys.path.append(PIN_PY_DIR)
    from pinnearmap import pinnearmap_phase
    pinnearmap_phase("premain-prepare")
    p = argparse.ArgumentParser(description='PIN-instrumented running utility')
    p.add_argument('--py-file', dest='pyfile', type=str, help='function.py file path')
    p.add_argument('--size', dest='size', type=str, help='test/small/large', default='small')
    args = p.parse_args()
    py_file = str(args.pyfile)
    if not path.isfile(py_file):
        raise ValueError(f"Python function at {py_file} doesn't exist")
    sys.path.append(WRAPPER_PY_DIR)
    sys.path.append(path.dirname(py_file))
    sys.path.append(path.join(path.dirname(py_file), '..'))
    inputmod = importlib.import_module('input')
    from storage import storage
    S = storage.get_instance()
    requested_buckets = inputmod.buckets_count()
    input_buckets = list()
    for i in range(0, requested_buckets[0]):
        input_buckets.append(f"benchmark-{i}-input")
    output_buckets = list()
    for i in range(0, requested_buckets[1]):
        output_buckets.append(f"benchmark-{i}-input")
    py_dir = path.normpath(path.abspath(path.join(path.dirname(py_file), '..')))
    py_dir = py_dir.split(os.sep)
    assert(py_dir[-3] == 'benchmarks')
    py_dir[-3] = 'benchmarks-data'
    data_path = os.sep.join(py_dir)
    def uploader_func(bucket_idx: int, file: str, filepath: str) -> None:
        storage.get_instance().upload(input_buckets[bucket_idx], file, filepath)
    input_config = inputmod.generate_input(data_path, args.size, input_buckets, output_buckets, uploader_func)
    function = importlib.import_module(path.basename(py_file)[:-3])
    pinnearmap_phase("function-invoke")
    function.handler(input_config)
    pinnearmap_phase("function-invoke-finish")

if __name__ == '__main__':
    main()
