"""Local SECOND LOOK prototype; no third-party packages required."""
import json
import sqlite3
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import ai

ROOT = Path(__file__).resolve().parent
DB = ROOT / 'second-look.db'
CRITERIA = ['문제 해결', '개인 기여', '협업']
TRANSCRIPT = [
    ('e1', '00:18', '면접관', '팀 프로젝트에서 의견 충돌을 어떻게 해결했나요?'),
    ('e2', '00:28', '지원자', '서로 다른 해결책이 나와서 각 방법을 직접 실험하고 결과를 비교한 뒤 결정했습니다.'),
    ('e3', '01:12', '면접관', '그 과정에서 본인이 맡은 역할을 구체적으로 말씀해 주세요.'),
    ('e4', '01:23', '지원자', '저는 비교 기준을 정하고 테스트 코드를 작성했습니다. 결과는 팀원들과 함께 해석했습니다.'),
    ('e5', '02:15', '면접관', '팀원과 협업하면서 어려웠던 점은 무엇이었나요?'),
    ('e6', '02:28', '지원자', '처음에는 서로 설명이 부족했지만 매일 짧게 진행 상황을 공유하며 조율했습니다.'),
]

@contextmanager
def connect():
    db = sqlite3.connect(DB, timeout=10)
    db.row_factory = sqlite3.Row
    try:
        with db:
            yield db
    finally:
        db.close()

def init():
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, person TEXT NOT NULL, evidence_id TEXT NOT NULL, criterion TEXT NOT NULL, polarity TEXT NOT NULL, text TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS locks (person TEXT PRIMARY KEY, locked INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS review (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        INSERT OR IGNORE INTO locks VALUES ('A',0),('B',0);
        ''')

def state(db):
    notes = [dict(r) for r in db.execute('SELECT * FROM notes ORDER BY id')]
    locks = {r['person']: bool(r['locked']) for r in db.execute('SELECT * FROM locks')}
    review = {r['key']: r['value'] for r in db.execute('SELECT * FROM review')}
    return {'transcript': [dict(zip(('id','time','speaker','text'), row)) for row in TRANSCRIPT],
            'criteria': CRITERIA, 'notes': notes, 'locks': locks, 'review': review}

class Handler(BaseHTTPRequestHandler):
    def reply(self, code, data, content_type='application/json; charset=utf-8'):
        body = json.dumps(data, ensure_ascii=False).encode() if content_type.startswith('application/json') else data
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/state':
            with connect() as db: self.reply(200, state(db))
            return
        files = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'), '/style.css': ('style.css', 'text/css')}
        if path not in files: return self.reply(404, {'error': 'Not found'})
        name, kind = files[path]
        self.reply(200, (ROOT / name).read_bytes(), kind + '; charset=utf-8')

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length > 100000: raise ValueError('요청이 너무 큽니다.')
            data = json.loads(self.rfile.read(length) or b'{}')
            path = urlparse(self.path).path
            with connect() as db:
                if path == '/api/note':
                    person, eid = data.get('person'), data.get('evidence_id')
                    criterion, polarity = data.get('criterion'), data.get('polarity')
                    note = str(data.get('text', '')).strip()
                    if person not in ('A','B') or eid not in [t[0] for t in TRANSCRIPT] or criterion not in CRITERIA or polarity not in ('긍정','부정','의문') or not note or len(note) > 500:
                        raise ValueError('기록 내용을 확인해 주세요.')
                    if db.execute('SELECT locked FROM locks WHERE person=?', (person,)).fetchone()[0]: raise ValueError('확정한 기록은 수정할 수 없습니다.')
                    db.execute('INSERT INTO notes(person,evidence_id,criterion,polarity,text) VALUES (?,?,?,?,?)', (person,eid,criterion,polarity,note))
                elif path == '/api/lock':
                    person = data.get('person')
                    if person not in ('A','B'): raise ValueError('평가자를 확인해 주세요.')
                    if not db.execute('SELECT 1 FROM notes WHERE person=?', (person,)).fetchone(): raise ValueError('기록을 하나 이상 남겨 주세요.')
                    db.execute('UPDATE locks SET locked=1 WHERE person=?', (person,))
                elif path == '/api/review':
                    if db.execute('SELECT SUM(locked) FROM locks').fetchone()[0] != 2: raise ValueError('두 평가자의 기록을 먼저 확정해 주세요.')
                    key, value = data.get('key'), str(data.get('value', ''))
                    if key not in ('facts','differences','questions','changes','handoff','hud') or len(value) > 10000: raise ValueError('검토 내용을 확인해 주세요.')
                    db.execute('INSERT OR REPLACE INTO review VALUES (?,?)', (key,value))
                elif path == '/api/ai-suggestions':
                    if db.execute('SELECT SUM(locked) FROM locks').fetchone()[0] != 2: raise ValueError('두 평가자의 기록을 먼저 확정해 주세요.')
                    current = state(db)
                    suggestions = ai.suggest(current['transcript'], current['notes'])
                    return self.reply(200, {'suggestions': suggestions})
                elif path == '/api/demo':
                    db.execute('DELETE FROM notes'); db.execute('DELETE FROM review'); db.execute('UPDATE locks SET locked=0')
                    db.executemany('INSERT INTO notes(person,evidence_id,criterion,polarity,text) VALUES (?,?,?,?,?)', [
                        ('A','e2','문제 해결','긍정','실험 결과를 비교해 결정한 과정이 구체적이다.'),
                        ('B','e2','개인 기여','의문','실험에서 지원자가 직접 맡은 역할은 아직 모르겠다.'),
                        ('A','e6','협업','긍정','짧은 진행 상황 공유로 팀원과 조율했다.'),
                    ])
                    db.execute('UPDATE locks SET locked=1')
                else: return self.reply(404, {'error':'Not found'})
                self.reply(200, {'ok':True})
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self.reply(400, {'error':str(exc)})

if __name__ == '__main__':
    init()
    server = ThreadingHTTPServer(('127.0.0.1', 8765), Handler)
    print('SECOND LOOK: http://127.0.0.1:8765', flush=True)
    server.serve_forever()
