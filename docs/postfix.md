# postfix 

## smtp session
```python
samrullo@mail:~$ telnet mail.uzjapa.com 25
Trying 10.47.0.5...
Connected to mail.uzjapa.com.
Escape character is '^]'.
220 mail.uzjapa.com ESMTP Postfix (Ubuntu)
HELO samrullo@uzjapa.com
250 mail.uzjapa.com
MAIL FROM:<samrullo@uzjapa.com>
250 2.1.0 Ok
RCPT TO:<amrulloev.subhon@gmail.com>
554 5.7.1 <amrulloev.subhon@gmail.com>: Relay access denied
RCPT TO:<
```