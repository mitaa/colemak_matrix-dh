#! /usr/bin/env python3

import sys
import os
import subprocess
import shutil
from distutils.dir_util import copy_tree
import itertools


XKB_SRC = os.path.join(os.path.split(os.path.abspath(__file__))[0], "xkb")
assert os.path.isdir(XKB_SRC)


def build_kbd_from_xkb(layout, variant, dpath_kbd="/lib/kbd/keymaps/xkb"):
	# compile the keymap
	kbd_map = subprocess.check_output(["ckbcomp", layout, variant])
	fname = "{}-{}.map".format(layout, variant)
	with open(os.path.join(dpath_kbd, fname), "wb") as fp:
		fp.write(kbd_map)


def install(dpath_xkb="/usr/share/X11/xkb", dpath_kbd="/lib/kbd/keymaps/xkb"):
	assert os.path.isdir(dpath_xkb)
	assert os.path.isdir(dpath_kbd)

	for i in itertools.count():
		fldr = "xkb_backup.{:>02}".format(i)
		backup_dpath = os.path.join(os.path.split(dpath_xkb)[0], fldr)
		if not os.path.isdir(backup_dpath):
			break
	# errors if the backup directory already exists
	shutil.copytree(dpath_xkb, backup_dpath)
	# overwrites the existing directory
	copy_tree(XKB_SRC, dpath_xkb)
	build_kbd_from_xkb("us", "colemak_matrix-dh", dpath_kbd=dpath_kbd)


def restore(src):
	try:
		i = int(src)
	except ValueError:
		i = None

	if i is not None:
		pass



def main(args):
	if args[0] == "install":
		install()
	elif args[0] == "restore":
		restore(args[1])


if __name__ == "__main__":
	main(sys.argv[1:])