from flask import *
import time
import datetime
import db
import json
import re
import pytz

import logger
from flag import checktoken, getflag

MAX_ANSWER_LEN = 80

def MIN_INTERVAL_S_AFTER(submitted_count):
    return 3600

def flags_based_on_correct_count(token, count):
    flags = []
    if count>=3:
        flags.append(getflag(token, 1))
    if count>=6:
        flags.append(getflag(token, 2))
    return flags

with open('db/problemset.json', encoding='utf-8') as f:
    _problemset = json.load(f)
    for p in _problemset:
        for ans in p['answer']:
            assert re.match(p['answer_validator'], ans)
        del ans

    problemset = [{**p, 'answer': 'you guess'} for p in _problemset]
    answers = {p['id']: p['answer'] for p in _problemset}

print('got', len(problemset), 'questions')

app = Flask(__name__)
app.secret_key = 'vbhfgh7os34tbnuiz04klgdty023nbgpdf268bnbubg52l4fdpa55'

@app.template_filter(name='time')
def filter_time(s):
    date = datetime.datetime.fromtimestamp(s, pytz.timezone('Asia/Shanghai'))
    return date.strftime('%Y-%m-%d %H:%M:%S')

@app.route('/token', methods=['GET', 'POST'])
def token():
    if request.method=='POST':
        req_token = request.form['token'].strip()
        uid = checktoken(req_token)
        if uid:
            logger.write(uid, ['login', 'manual'])
            session['token'] = req_token
            return redirect('/')
        else:
            flash('Token无效')
    
    return render_template('token.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'token' in request.args:
        req_token = request.args['token']
        assert isinstance(req_token, str)
        uid = checktoken(req_token)
        if uid:
            logger.write(uid, ['login', 'auto'])
            session['token'] = req_token
            return redirect('/')
        else:
            return redirect('/token')

    if 'token' not in session:
        return redirect('/token')

    token = session['token']
    uid = checktoken(token)
    if not uid:
        flash('Token无效')
        return redirect('/token')

    history_raw = db.query_history(uid)
    if history_raw:
        next_submit_ts = history_raw[-1][0] + MIN_INTERVAL_S_AFTER(len(history_raw))
        remaining_waiting_s = int(next_submit_ts - time.time())
        if remaining_waiting_s<0:
            remaining_waiting_s = None
    else:
        remaining_waiting_s = None

    if request.method=='POST':
        if remaining_waiting_s:
            logger.write(uid, ['submission_tooquick', remaining_waiting_s])
            flash('还需要冷却 %d 秒才能再次提交'%remaining_waiting_s)
        else:
            submission = {
                pid: request.form.get(pid, '')
                for pid in answers.keys()
            }
            for v in submission.values():
                if len(v)>MAX_ANSWER_LEN:
                    logger.write(uid, ['submission_toolong', len(v), v[:MAX_ANSWER_LEN*2]])
                    flash('答案太长')
                    return redirect('/')
            
            logger.write(uid, ['submission', submission])
            
            db.push_history(uid, submission)
            flash('提交成功')

        return redirect('/')

    history = [{
        'time_ts': time_ts,
        'correct_count': len([1 for pid, ans in submission.items() if ans in answers[pid]]),
        'questions': [{
            'pid': pid,
            'answer': ans,
            #'correct': ans in answers[pid],
        } for pid, ans in submission.items()],
    } for time_ts, submission in history_raw]

    correct_count = max([0] + [submission['correct_count'] for submission in history])
    flags = flags_based_on_correct_count(token, correct_count)
    
    logger.write(uid, ['get_page', correct_count])

    return render_template(
        'index.html',
        problemset=problemset,
        history=history,
        remaining_waiting_s=remaining_waiting_s,
        correct_count=correct_count,
        flags=flags,
        max_length=MAX_ANSWER_LEN,
    )
    
@app.route('/check_answer/<int:idx>', methods=['GET'])
def check_answer(idx):
    token = session['token']
    uid = checktoken(token)
    if not uid:
        return 'Token无效'

    req_ans = request.args['ans']
    assert isinstance(req_ans, str)
    
    if not 0<=idx<len(problemset):
        return '题号错误'
        
    logger.write(uid, ['check_answer', idx, req_ans[:MAX_ANSWER_LEN*2]])
        
    if not req_ans:
        return 'OK'
    if len(req_ans)>MAX_ANSWER_LEN:
        return '答案过长'
    
    p = problemset[idx]
    if not re.match(p['answer_validator'], req_ans):
        return '格式错误'
    else:
        return 'OK'
        
@app.route('/log/blur')
def log_blur():
    token = session['token']
    uid = checktoken(token)
    if not uid:
        return 'Token无效'
        
    logger.write(uid, ['log_blur'])
    return 'OK'
    
@app.route('/log/focus')
def log_focus():
    token = session['token']
    uid = checktoken(token)
    if not uid:
        return 'Token无效'
        
    logger.write(uid, ['log_focus'])
    return 'OK'
    
@app.route('/log/paste', methods=['POST'])
def log_paste():
    token = session['token']
    uid = checktoken(token)
    if not uid:
        return 'Token无效'
        
    target = request.args['target']
    payload = request.json
    
    logger.write(uid, ['log_paste', target, payload])
    return 'OK'
    
    
app.run('0.0.0.0', 5000)