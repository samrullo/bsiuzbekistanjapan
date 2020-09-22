# to append to history
You probably want to tell bash to not overwrite the history each time, but rather to append to it. You can do this by modifying your .bashrc to run
```python
shopt -s histappend
```

You can also increase the size of your history file by 
exporting ```HISTSIZE``` to be a large-ish number (it's in bytes, so 100000 should be plenty).
