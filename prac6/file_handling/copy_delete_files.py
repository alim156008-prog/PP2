import shutil
import os

shutil.copy("text.txt", "copy.txt")  
os.remove("copy.txt")   