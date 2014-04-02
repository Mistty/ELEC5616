#!/usr/bin/env python
# coding=utf-8

import hashlib
import os
import subprocess
import sys
import time

usage = """Usage: ./miner.py <clone_url> <public_username> [NUMTHREADS] [SALT]
Arguments:

<clone_url> is the string you’d pass to `git clone` (i.e.
  something of the form `username@hostname:path`)

<public_username> is the public username provided to you in
  the CTF web interface.

[NUMTHREADS]

[SALT]
"""

def solve(NUMTHREADS, SALT):
	with open('gitcoin/difficulty.txt', 'r') as f:
		difficulty = f.read().strip()

	tree = subprocess.check_output(['git', 'write-tree']).strip()
	with open('gitcoin/.git/refs/heads/master', 'r') as f:
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

	with open('GitcoinSHA/commit.txt', 'w') as f:
		f.write(base_content)
	command = 'GitcoinSHA/sha1 commit.txt %s %i %s' % (difficulty, NUMTHREADS, SALT)
	
	if os.system(command) != 0:
		print "Hash invalidated. Restarting"
		return False
	
	hasher = hashlib.sha1();
	with open('minedcommit.txt') as f:
		hasher.update(header + f.read())

	sha1 = hasher.hexdigest()
	print 'Mined a Gitcoin! The SHA-1 is:'
	os.system('cd gitcoin; git hash-object -t commit minedcommit.txt -w')
	os.system('cd gitcoin; git reset --hard %s' % sha1)
	
	return True

def prepare_index():
	os.system('perl -i -pe \'s/(%s: )(\d+)/$1 . ($2+1)/e\' gitcoin/LEDGER.txt' % public_username)
	os.system('grep -q "%s" gitcoin/LEDGER.txt || echo "%s: 1" >> gitcoin/LEDGER.txt' % (public_username, public_username))
	os.system('cd gitcoin; git add LEDGER.txt')

def reset():
	os.system('cd gitcoin; git reset --hard HEAD')
	os.system('cd gitcoin; git fetch')
	os.system('cd gitcoin; git reset --hard origin/master')

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

	if os.path.exists('gitcoin'):
		reset()
	else:
		os.system('git clone git@cryptologic.org:gitcoin.git')

	while True:
		prepare_index()
		if solve(NUMTHREADS, SALT):
			if os.system('git push origin master') == 0:
				print 'Success :)'
			else:
				print 'Starting over :('
		reset()
