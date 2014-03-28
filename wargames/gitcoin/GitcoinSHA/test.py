
import os
import subprocess
import sys
msg = "commit 233Nwhat is up doc"
command = "./sha1 '%s' 001 5 a" % msg
res = os.popen(command).read()
print res
