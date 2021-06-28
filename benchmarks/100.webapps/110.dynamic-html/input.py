
size_generators = {
    'test' : 10,
    'small' : 1000,
    'large': 100000
}

def buckets_count():
    return (0, 0)

def generate_input(data_dir, size, input_buckets, output_buckets, upload_func):
    input_config = {'username': 'testname'} 
    input_config['random_len'] = size_generators[size]
    return input_config

# prototyping utility
if __name__ == '__main__':
    import sys, os
    from os import path
    SCRIPT_DIR = path.abspath(path.join(path.dirname(__file__)))
    sys.path.append(path.join(SCRIPT_DIR, 'python'))
    sys.path.append(path.abspath(path.join(SCRIPT_DIR, '..', '..', 'wrappers', 'local', 'python')))
    sys.path.append(path.abspath(path.join(SCRIPT_DIR, '..', '..', '..', '..', 'pin-NearMAP', 'stublib', 'pybuild')))
    from pinnearmap import pinnearmap_phase
    config = generate_input('', 'small', '', '', '')
    import function
    pinnearmap_phase('main-start')
    function.handler(config)
    pinnearmap_phase('main-end')
