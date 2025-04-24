import os

async def cleanup_files(*paths):
    for path in paths:
        if path and os.path.exists(path):
            os.remove(path)
