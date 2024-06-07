import os
from whitenoise.compress import Compressor

_compressor = Compressor()


def is_cache_newer(source_file, cache_file):
    # 获取源文件和缓存文件的修改时间
    source_ctime = os.path.getctime(source_file)
    source_mtime = os.path.getmtime(source_file)
    source_time = source_ctime if source_ctime > source_mtime else source_mtime
    cache_ctime = os.path.getctime(cache_file)
    cache_mtime = os.path.getmtime(cache_file)
    cache_time = cache_ctime if cache_ctime > cache_mtime else cache_mtime
    # 如果缓存文件的修改时间比源文件的修改时间晚，返回True
    return cache_time > source_time


def compress_statics(static_dir):
    for dirpath, _dirs, files in os.walk(static_dir):
        for filename in files:
            if _compressor.should_compress(filename):
                path = os.path.join(dirpath, filename)
                # 判断一下缓存文件的时间戳是否比源文件新，如果是则不需要再次压缩
                if (os.path.exists(path + ".br") and is_cache_newer(path, path + ".br")) and (
                    os.path.exists(path + ".gz") and is_cache_newer(path, path + ".gz")
                ):
                    print(f"压缩缓存比源文件新，跳过: {path}")
                    continue
                for _compressed in _compressor.compress(path):
                    pass
