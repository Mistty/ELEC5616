#!/usr/bin/env python
# coding=utf-8

import hashlib
import os
import subprocess
import sys
import time

usage = """Usage: ./miner.py <clone_url> <public_username>
Arguments:

<clone_url> is the string you’d pass to `git clone` (i.e.
  something of the form `username@hostname:path`)

<public_username> is the public username provided to you in
  the CTF web interface."""

def solve():
	with open('difficulty.txt', 'r') as f:
		difficulty = f.read().strip()

	tree = subprocess.check_output(['git', 'write-tree']).strip()
	with open('.git/refs/heads/master', 'r') as f:
		parent = f.read().strip()
	timestamp = int(time.time())
	print 'Mining…'
	base_hasher = hashlib.sha1()
	# The length of all such commit messages is 233, as long as the nonce is 16
	# digits long.
	header = "commit 233\x00"
	base_content = """tree %s
parent %s
author CTF user <me@example.com> 1333333337 +0000
committer CTF user <me@example.com> 1333333337 +0000

Go Bobby Tables!!

""" % (tree, parent)
	base_hasher.update(header + base_content)

	with open('commit.txt', 'w') as f:
		f.write(base_content)
	command = './sha1 commit.txt %s %i %s' % (difficulty, NUMTHREADS, SALT)
	os.system(command)
	
	
	hasher = hashlib.sha1();
	with open('minedcommit.txt') as f:
		hasher.update(header + f.read())

	sha1 = hasher.hexdigest()
	print 'Mined a Gitcoin! The SHA-1 is:'
	os.system('git hash-object -t commit minedcommit.txt -w')
	os.system('git reset --hard %s' % sha1)

def prepare_index():
	os.system('perl -i -pe \'s/(%s: )(\d+)/$1 . ($2+1)/e\' LEDGER.txt' % public_username)
	os.system('grep -q "%s" LEDGER.txt || echo "%s: 1" >> LEDGER.txt' % (public_username, public_username))
	os.system('git add LEDGER.txt')

def reset():
	os.system('git reset --hard HEAD')
	os.system('git fetch')
	os.system('git reset --hard origin/master')


if __name__=="__main__":
	if len(sys.argv) < 3:
		print usage
		sys.exit(1)

	clone_spec = sys.argv[1]
	public_username = sys.argv[2]
	try:
		NUMTHREADS = int(sys.argv[3])
	except:
		NUMTHREADS = 4
	try:
		SALT = sys.argv[4]
	except:
		SALT = 'a'

	while True:
		prepare_index()
		solve()
		if os.system('git push origin master') == 0:
			print 'Success :)'
			reset()
		else:
			print 'Starting over :('
			reset()
