from flask import *
import json
import re

registry = {
    'admin': ({'Content-Type': 'text/html'}, '<title>hello world!</title>'),
}
NAME_RE = re.compile(r'^[a-z0-9~_-]+$')

app = Flask(__name__)

@app.route('/<name>/')
@app.route('/<name>/<path:subpath>')
def view_homepage(name, subpath=None):
    content = registry.get(name, None)
    if not content:
        return '<title>ERROR</title>此个人主页不存在'
    
    headers, body = content
    return body, headers
    
def is_safe(s):
    return isinstance(s, str) and not any(c in s for c in '\r\n')
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
        
    name = request.form['name']
    header = request.form['header']
    body = request.form['body']
    
    try:
        header = json.loads(header)
    except Exception:
        return '响应头不合法'
    
    if not NAME_RE.match(name):
        return '名称不合法'
    if not isinstance(header, dict) or not all(is_safe(k) and is_safe(v) for k, v in header.items()):
        return '响应头不合法'
    if name in registry:
        return '已经注册过了'
        
    registry[name] = (header, body)
    return f'注册成功，点击 <a href="/{name}/">进入你的个人主页</a>'
    
if __name__=='__main__':
    app.run('127.0.0.1', 5000, debug=False)