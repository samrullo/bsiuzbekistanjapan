# Custom error handlers

```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500
```

<p>Error handlers return a response, like view functions,
but they also need to return the numeric status code 
that corresponds to the error, which Flask conveniently
accepts as a second return value</p>

<p>If we want to implement error handlers with blueprints, the need to use app_errorhandler decorator</p>

```python
@main_bp.app_errorhandler(400)
def page_not_found(e):
    return render_template("errors/400.html"),400

@main_bp.app_errorhandler(500)
def internal_server_eror(e):
    return render_template("errors/500.html"),500
```