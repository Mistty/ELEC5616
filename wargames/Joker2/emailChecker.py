#! /usr/bin/python3.2

import urllib.request

suffix = "freelancer.com"

myStr = "https://www.freelancer.com/ajax/check-email-exist.php?email=%s%%40"+suffix+"&json=true&validator=true"

possibleChars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
baseNo = len(possibleChars)

def nextUname(uname):
    ltrSum = 0
    strLen = len(uname) - 1
    for c in uname:
        ltrSum = ltrSum + (possibleChars.index(c)*(baseNo**strLen))
        strLen = strLen - 1
    ltrSum = ltrSum + 1
    newUname = ''
    while ltrSum > 0:
        ind = (ltrSum%baseNo);
        c = possibleChars[ind]
        newUname = c + newUname
        ltrSum = ltrSum - ind
        ltrSum = int(ltrSum/baseNo)
    return newUname

uname = 'vxg'
while True:
    try:
        #        print(uname)
        response = urllib.request.urlopen(myStr % uname, timeout = 3).read()
        if bytes('false',"ascii") in response:
            print('Got:' + uname)
        uname = nextUname(uname)
    except:
        pass
