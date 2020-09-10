from flask import url_for as flask_url_for,g

url_for=lambda endpoint,**kwargs : flask_url_for(endpoint,lang=g.current_lang,**kwargs)