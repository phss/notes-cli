import os
from subprocess import call

EDITOR = os.environ.get('EDITOR','vim')

def edit_file(full_path):
  preread = ""
  if os.path.isfile(full_path):
    preread = open(full_path, "r").read()
  with open(full_path, "w") as f:
    f.write(preread)
    f.flush()
    call([EDITOR, f.name])

def print_file(full_path):
  print open(full_path).read()

def delete_file(full_path):
  print "Are you sure you want to delete %s? (y/n)" % full_path
  choice = io.get_choice()
  if choice == "y":
    os.remove(full_path)

def get_user_choice(options):
  if len(options) == 0:
    return None
  elif len(options) == 1:
    option = options[0]
  else:
    print "Options:"
    for i, option in enumerate(options):
      print "%d) %s" % (i+1, option)
    print "Which one?"
    choice = int(get_choice()) - 1
    option = options[choice]
  return option

def get_choice():
  return raw_input()

