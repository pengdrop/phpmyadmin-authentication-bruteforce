# phpMyAdmin Authentication Bruteforce

tested on `phpMyAdmin 4.9.0.1`

`password.txt` file's source is: <https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt>


Usage:
```
python3 main.py -url http://example.com/pma/ -user root -pdict password.txt
```
OR
```
python3 main.py -url http://example.com/pma/ -udict users.txt -pdict password.txt
```
