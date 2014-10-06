#!/usr/bin/env python3

import argparse
import os
import sys

parser = argparse.ArgumentParser('Generate source files: A.cpp B.cpp C.cpp')
parser.add_argument('--dir', help='Output directory', required=True)
parser.add_argument(
    '--smart',
    action='store_true',
    help='Do not create file if already exists and content is the same'
)
parser.add_argument(
    '--check-changes',
    action='store_true',
    help='Check that some of the files really change'
)
args = parser.parse_args()

print('Generate (python script)')

outdir = args.dir
os.makedirs(outdir, exist_ok=True)

change = False

def create(filename, content):
  if os.path.exists(filename) and args.smart:
    old_content = open(filename, 'r').read()
    if old_content == content:
      return
  global change
  change = True
  open(filename, 'w').write(content)

# Create A.cpp
content = """
const char* A() {
  return "Hello from A";
}
"""

create(os.path.join(outdir, 'A.cpp'), content)

# Create B.cpp
content = """
const char* B() {
  return "Hello from B";
}
"""

create(os.path.join(outdir, 'B.cpp'), content)

# Create C.cpp
content = """
const char* C() {
  return "Hello from C";
}
"""

create(os.path.join(outdir, 'C.cpp'), content)

# Check changes
if (not change) and args.check_changes:
  sys.exit('No changes!')
