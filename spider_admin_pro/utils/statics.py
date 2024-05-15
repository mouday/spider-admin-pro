import os
from whitenoise.compress import Compressor

_compressor = Compressor()


def compress_statics(static_dir):
    for dirpath, _dirs, files in os.walk(static_dir):
        for filename in files:
            if _compressor.should_compress(filename):
                path = os.path.join(dirpath, filename)
                for _compressed in _compressor.compress(path):
                    pass
