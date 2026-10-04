import os
import sqlite3
import secrets
import string
from flask import Flask, request, jsonify, Response, render_template_string

app = Flask(__name__)

# مسار قاعدة البيانات في البيئة المؤقتة لـ Vercel Serverless
DB_PATH = '/tmp/scripts.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scripts (
            id TEXT PRIMARY KEY,
            script_code TEXT NOT NULL,
            edit_key TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_id(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# صفحة الحماية التي تظهر في المتصفح
WARNING_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سنقر لا تسرق!</title>
    <style>
        body {
            background-color: #0f172a;
            color: #ffffff;
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        .card {
            background: #1e293b;
            padding: 2.5rem 3rem;
            border-radius: 1rem;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5);
            border: 2px solid #ef4444;
            max-width: 400px;
        }
        h1 { color: #ef4444; font-size: 2.2rem; margin: 0 0 1rem 0; }
        p { color: #94a3b8; font-size: 1.1rem; line-height: 1.6; margin: 0; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🦊🛑 سنقر لا تسرق!</h1>
        <p>عذراً، هذا الرابط مخصص لتشغيله داخل اللعبة مباشرة ولا يمكنك عرض الكود البرمجي من المتصفح.</p>
    </div>
</body>
</html>
'''

# الواجهة الرئيسية للموقع (HTML + CSS + JS)
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حماية سكربتات اللوا - Lua Protect</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: system-ui, sans-serif; }
        .card { background-color: #1e293b; border: 1px solid #334155; border-radius: 1rem; }
        .btn-primary { background-color: #3b82f6; border: none; }
        .btn-primary:hover { background-color: #2563eb; }
        .btn-warning { background-color: #f59e0b; border: none; color: #fff; }
        .btn-warning:hover { background-color: #d97706; color: #fff; }
        .form-control { background-color: #0f172a; border: 1px solid #334155; color: #f8fafc; }
        .form-control:focus { background-color: #0f172a; color: #f8fafc; border-color: #3b82f6; box-shadow: none; }
        code { color: #38bdf8; }
    </style>
</head>
<body class="py-5">
    <div class="container" style="max-width: 800px;">
        <div class="text-center mb-5">
            <h1 class="fw-bold text-primary">🛡️ منصة حماية سكربتات Lua</h1>
            <p class="text-secondary">احمِ أكوادك من السرقة واستضفها برابط loadstring محمي مع إمكانية التعديل في أي وقت!</p>
        </div>

        <!-- إنشاء سكربت جديد -->
        <div class="card p-4 mb-4">
            <h4 class="mb-3">➕ إنشاء سكربت جديد</h4>
            <div class="mb-3">
                <label class="form-label">كود اللوا (Lua Code):</label>
                <textarea id="newScript" class="form-control" rows="6" placeholder='print("Hello World!")'></textarea>
            </div>
            <div class="mb-3">
                <label class="form-label">مفتاح التعديل (Password / Key):</label>
                <input type="text" id="newKey" class="form-control" placeholder="ضع كلمة سر لتدخل بها لاحقاً وتعدل السكربت">
            </div>
            <button onclick="createScript()" class="btn btn-primary btn-lg w-100">🔒 إنشاء واستضافة الرابط المحمي</button>
            <div id="createResult" class="mt-3"></div>
        </div>

        <!-- تعديل سكربت حالي -->
        <div class="card p-4">
            <h4 class="mb-3">✏️ تعديل سكربت حالي</h4>
            <div class="mb-3">
                <label class="form-label">معرف السكربت (Script ID):</label>
                <input type="text" id="editId" class="form-control" placeholder="مثال: aBc123Xy">
            </div>
            <div class="mb-3">
                <label class="form-label">مفتاح التعديل (Key):</label>
                <input type="password" id="editKey" class="form-control" placeholder="كلمة السر التي أنشأت بها السكربت">
            </div>
            <div class="mb-3">
                <label class="form-label">الكود الجديد:</label>
                <textarea id="editScript" class="form-control" rows="6" placeholder="ضع الكود الجديد هنا"></textarea>
            </div>
            <button onclick="updateScript()" class="btn btn-warning btn-lg w-100">🔄 تحديث الكود</button>
            <div id="updateResult" class="mt-3"></div>
        </div>
    </div>

    <script>
        async function createScript() {
            const script = document.getElementById('newScript').value;
            const key = document.getElementById('newKey').value;
            const resDiv = document.getElementById('createResult');

            if (!script || !key) {
                resDiv.innerHTML = '<div class="alert alert-danger">يرجى كتابة الكود ووضع مفتاح التعديل!</div>';
                return;
            }

            const res = await fetch('/api/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ script, key })
            });

            const data = await res.json();
            if (data.success) {
                const loadstringCode = `loadstring(game:HttpGet("${data.raw_url}"))()`;
                resDiv.innerHTML = `
                    <div class="alert alert-success">
                        <h5>✅ تم إنشاء الرابط بنجاح!</h5>
                        <p class="mb-1"><b>معرّف السكربت (Script ID):</b> <code>${data.id}</code> (احفظه لتعدل عليه لاحقاً)</p>
                        <p class="mb-2"><b>كود الـ Loadstring الخاص بك:</b></p>
                        <input type="text" class="form-control mb-2" value='${loadstringCode}' readonly id="loadstringInput">
                        <button class="btn btn-sm btn-outline-light" onclick="navigator.clipboard.writeText(\`${loadstringCode}\`)">📋 نسخ الـ Loadstring</button>
                    </div>
                `;
            } else {
                resDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            }
        }

        async function updateScript() {
            const id = document.getElementById('editId').value;
            const key = document.getElementById('editKey').value;
            const script = document.getElementById('editScript').value;
            const resDiv = document.getElementById('updateResult');

            if (!id || !key || !script) {
                resDiv.innerHTML = '<div class="alert alert-danger">يرجى ملء جميع الحقول!</div>';
                return;
            }

            const res = await fetch('/api/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ id, key, script })
            });

            const data = await res.json();
            if (data.success) {
                resDiv.innerHTML = '<div class="alert alert-success">✅ تم تحديث الكود بنجاح! سيتم تشغيل الكود الجديد فوراً من نفس الرابط.</div>';
            } else {
                resDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

# API لإنشاء سكربت جديد
@app.route('/api/create', methods=['POST'])
def create_script():
    init_db()
    data = request.get_json() or {}
    script = data.get('script')
    key = data.get('key')

    if not script or not key:
        return jsonify({'success': False, 'error': 'السكربت والمفتاح مطلوبان'}), 400

    script_id = generate_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO scripts (id, script_code, edit_key) VALUES (?, ?, ?)', (script_id, script, key))
    conn.commit()
    conn.close()

    raw_url = request.host_url.rstrip('/') + '/raw/' + script_id
    return jsonify({'success': True, 'id': script_id, 'raw_url': raw_url})

# API لتحديث كود موجود
@app.route('/api/update', methods=['POST'])
def update_script():
    init_db()
    data = request.get_json() or {}
    script_id = data.get('id')
    key = data.get('key')
    new_script = data.get('script')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT edit_key FROM scripts WHERE id = ?', (script_id,))
    row = c.fetchone()

    if not row:
        conn.close()
        return jsonify({'success': False, 'error': 'السكربت غير موجود'}), 444

    if row[0] != key:
        conn.close()
        return jsonify({'success': False, 'error': 'مفتاح التعديل غير صحيح!'}), 403

    c.execute('UPDATE scripts SET script_code = ? WHERE id = ?', (new_script, script_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

# رابط جلب الكود المحمي (Raw Endpoint)
@app.route('/raw/<script_id>')
def get_raw_script(script_id):
    user_agent = request.headers.get('User-Agent', '').lower()
    browsers = ['mozilla', 'chrome', 'safari', 'edge', 'opera', 'firefox', 'msie']
    is_browser = any(b in user_agent for b in browsers)

    # إذا كان الطلب من متصفح عادي -> إرجاع "سنقر لا تسرق"
    if is_browser:
        return WARNING_HTML, 200, {'Content-Type': 'text/html; charset=utf-8'}

    # إذا كان من Executor -> جلب الكود من قاعدة البيانات
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT script_code FROM scripts WHERE id = ?', (script_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        return Response('-- Script not found!', status=404, mimetype='text/plain')

    return Response(row[0], status=200, mimetype='text/plain')

if __name__ == '__main__':
    app.run()
