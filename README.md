# phpMyAdmin Authentication Bruteforce

tested on `phpMyAdmin 5.1.1`

multithreaded bruteforce attack on phpMyAdmin authentication now with support for the https-specific cookie name

```
usage: main.py [-h] [-url URL] [-user USER] [-dict DICT] [-threads THREADS]

e.g. python3 main.py -url http://example.com/pma/ -user root -dict password.txt -threads 2

optional arguments:
  -h, --help        show this help message and exit
  -url URL          The URL of target website
  -user USER        The username of MySQL (default: root)
  -dict DICT        The file path of password dictionary (default: password.txt)
  -threads THREADS  How many threads to use (default: 1)
```
