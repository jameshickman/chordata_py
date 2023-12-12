CHUNK_SIZE = 1024 * 32


def file_buffer(f, chunk_size):
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        yield chunk
