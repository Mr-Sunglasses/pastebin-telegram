import os
import sys


def file_writer(text):
    with open("file.txt", "w") as text_file:
        text_file.write(text)


def file_remover():
    if os.path.exists("file.txt"):
        os.remove("file.txt")  # one file at a time
