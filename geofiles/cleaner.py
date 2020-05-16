import os


for f in os.listdir():
    if not f.endswith("DSM.tif") and f != "cleaner.py":
        os.remove(f)
