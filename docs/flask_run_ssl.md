# To run flask with *https*

```python
if __name__ == "__main__":
    app.run(ssl_context='adhoc')
```

```bash
$flask run --cert=adhoc
```
