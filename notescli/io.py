import os
from subprocess import call

EDITOR = os.environ.get('EDITOR','vim')

def get_choice():
  return raw_input()

def edit_file(full_path):
  preread = ""
  if os.path.isfile(full_path):
    preread = open(full_path, "r").read()
  with open(full_path, "w") as f:
    f.write(preread)
    f.flush()
    call([EDITOR, f.name])

