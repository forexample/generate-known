#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser('Generate source files: A.cpp')
parser.add_argument('--dir', help='Output directory', required=True)
parser.add_argument(
    '--smart',
    action='store_true',
    help='Do not create file if already exists and content is the same'
)
args = parser.parse_args()

print('Generate (python script)')

outdir = args.dir
os.makedirs(outdir, exist_ok=True)

def create(filename, content):
  if os.path.exists(filename) and args.smart:
    old_content = open(filename, 'r').read()
    if old_content == content:
      return
  open(filename, 'w').write(content)

# Create A.cpp
a_content = """
const char* A() {
  return "Hello from A";
}
"""

create(os.path.join(outdir, 'A.cpp'), a_content)
