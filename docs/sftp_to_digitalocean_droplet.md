# How to transfer files to Digitalocean droplet

sftp is enabled by default. You can download FileZilla
https://filezilla-project.org/download.php?platform=osx

Then in ```Settings>SFTP``` add your machine's private key.
Needless to say, you should add your public key to the droplet's
```known_hosts``` file. Since private key file is located under a hidden folder ```.ssh```
to make it show up in macOs you can use below shortcut, taken from https://setapp.com/how-to/show-hidden-files-on-mac#:~:text=See%20hidden%20files%20on%20Mac%20via%20Finder&text=In%20Finder%2C%20open%20up%20your,2%20to%20hide%20them%20again!

```python
Command+Shift+Dot
```

Then you can connect to ```sftp://<ip address>``` with your credentials.

For detailed instructions refer to https://www.digitalocean.com/docs/droplets/how-to/transfer-files/#:~:text=Right-click%20the%20file%20you,download%20to%20your%20local%20machine.
