import os
import json
import secrets
import string
from flask import Flask, request, jsonify, Response, render_template_string, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)  # مفتاح سري للجلسات (Sessions)

# إعدادات قوقل OAuth (قم بوضع بياناتك الحقيقية التي استخرجتها من لوحة قوقل هنا)
app.config['GOOGLE_CLIENT_ID'] = 'ضع_هنا_Client_ID_الخاص_بـ_قوقل'
app.config['GOOGLE_CLIENT_SECRET'] = 'ضع_هنا_Client_Secret_الخاص_بـ_قوقل'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

DATA_FILE = '/tmp/scripts_store.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass

def generate_id(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# ==========================================================
# 🔐 صفحة تسجيل الدخول بحساب قوقل (إذا لم يكن المستخدم مسجلاً)
# ==========================================================
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول مطلوب</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
            color: #ffffff;
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            text-align: center;
            padding: 1rem;
        }
        .card {
            background: rgba(30, 41, 59, 0.85);
            backdrop-filter: blur(16px);
            padding: 3rem 2rem;
            border-radius: 1.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(59, 130, 246, 0.3);
            max-width: 440px;
            width: 100%;
        }
        .btn-google {
            background-color: #ffffff;
            color: #000000;
            font-weight: 700;
            border-radius: 50px;
            padding: 12px 24px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            text-decoration: none;
            width: 100%;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        .btn-google:hover {
            background-color: #f1f5f9;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255,255,255,0.2);
        }
        h1 { color: #38bdf8; font-size: 2rem; margin-bottom: 1rem; font-weight: 800; }
        p { color: #94a3b8; font-size: 1.05rem; line-height: 1.6; margin-bottom: 2rem; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🔒 تسجيل الدخول مطلوب</h1>
        <p>عذراً يا مهدي، لا يمكنك دخول الموقع أو استخدام لوحة التحكم إلا بعد تسجيل الدخول باستخدام حساب Google الخاص بك.</p>
        <a href="/login/google" class="btn btn-google">
            <i class="fab fa-google text-danger fs-5"></i> تسجيل الدخول بواسطة Google
        </a>
    </div>
</body>
</html>
'''

# ==========================================================
# 🛑 صفحة حماية المتصفح للسكربتات "سنقر لا تسرق!"
# ==========================================================
WARNING_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سنقر لا تسرق!</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: radial-gradient(circle at center, #0f172a 0%, #020617 100%); color: #ffffff; font-family: system-ui, -apple-system, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; text-align: center; padding: 1rem; }
        .card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); padding: 3rem 2rem; border-radius: 1.5rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7); border: 1px solid rgba(239, 68, 68, 0.4); max-width: 480px; width: 100%; }
        h1 { color: #ef4444; font-size: 2.3rem; margin: 0 0 1rem 0; font-weight: 800; }
        p { color: #94a3b8; font-size: 1.1rem; line-height: 1.7; margin: 0; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🦊🛑 سنقر لا تسرق!</h1>
        <p>هذا الرابط مخصص للتشغيل داخل اللعبة (Executor) مباشرة، ولا يمكن عرض الكود البرمجي من خلال المتصفح العادي.</p>
    </div>
</body>
</html>
'''

# ==========================================================
# 🛡️ الواجهة الرئيسية (محمية بتسجيل الدخول)
# ==========================================================
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة حماية واستضافة السكربتات</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --bg-main: #07090e; --bg-card: rgba(19, 27, 46, 0.85); --border-color: rgba(51, 65, 85, 0.6); --primary-glow: rgba(37, 99, 235, 0.4); }
        body { background: radial-gradient(circle at top, #0f172a 0%, var(--bg-main) 100%); color: #f1f5f9; font-family: system-ui, -apple-system, sans-serif; min-height: 100vh; }
        .navbar-brand { font-weight: 800; background: linear-gradient(45deg, #38bdf8, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .card { background: var(--bg-card); backdrop-filter: blur(16px); border: 1px solid var(--border-color); border-radius: 1.25rem; box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5); }
        label { color: #cbd5e1 !important; font-weight: 600; margin-bottom: 0.5rem; font-size: 0.95rem; }
        .form-control { background-color: #0b0f19 !important; border: 1px solid #334155 !important; color: #ffffff !important; font-family: monospace; border-radius: 0.75rem; padding: 0.75rem 1rem; }
        .form-control:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 4px var(--primary-glow) !important; }
        .btn-custom-primary { background: linear-gradient(135deg, #2563eb, #1d4ed8); border: none; font-weight: 700; border-radius: 0.75rem; padding: 0.75rem 1.5rem; color: #fff; }
        .btn-custom-info { background: linear-gradient(135deg, #0284c7, #0369a1); border: none; font-weight: 700; border-radius: 0.75rem; padding: 0.75rem 1.5rem; color: #fff; }
        .btn-custom-warning { background: linear-gradient(135deg, #d97706, #b45309); border: none; font-weight: 700; border-radius: 0.75rem; padding: 0.75rem 1.5rem; color: #fff; }
        .social-btn { display: inline-flex; align-items: center; gap: 8px; padding: 8px 18px; border-radius: 50px; font-weight: 600; font-size: 0.9rem; color: #fff !important; text-decoration: none; }
        .btn-discord { background-color: #5865F2; } .btn-youtube { background-color: #FF0000; } .btn-tiktok { background-color: #000000; border: 1px solid #334155; }
        .result-box { background-color: #0b0f19; border: 1px solid #334155; border-radius: 0.75rem; padding: 1.25rem; margin-top: 1rem; }
        code { color: #38bdf8; word-break: break-all; }
        .download-box { background: rgba(15, 23, 42, 0.9); border: 1px dashed #3b82f6; border-radius: 1rem; padding: 1.5rem; margin-bottom: 2rem; }
        .toast-msg { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%) translateY(100px); background: #10b981; color: white; padding: 10px 24px; border-radius: 50px; font-weight: bold; transition: transform 0.3s ease; z-index: 9999; }
        .toast-msg.show { transform: translateX(-50%) translateY(0); }
    </style>
</head>
<body class="py-4">
    <div class="container" style="max-width: 800px;">
        
        <!-- Header & User Info -->
        <div class="d-flex justify-content-between align-items-center mb-4 p-3 card">
            <div>
                <h3 class="navbar-brand mb-0">Lua Protect Hub</h3>
                <small class="text-secondary">مرحباً بك، {{ user.name }} ({{ user.email }})</small>
            </div>
            <a href="/logout" class="btn btn-outline-danger btn-sm rounded-pill px-3"><i class="fas fa-sign-out-alt"></i> تسجيل خروج</a>
        </div>

        <!-- 🚀 قسم تحميل المشغلات -->
        <div class="download-box text-center">
            <h4 class="text-primary mb-3"><i class="fas fa-download me-2"></i> تحميل مشغلات روبلوكس (Executors)</h4>
            <div class="row g-2 justify-content-center">
                <div class="col-md-4">
                    <a href="https://deltaexploits.gg/" target="_blank" class="btn btn-dark w-100 border border-primary py-2">
                        <i class="fab fa-android text-success me-1"></i> تحميل Delta (أندرويد)
                    </a>
                </div>
                <div class="col-md-4">
                    <a href="https://deltaexploits.gg/" target="_blank" class="btn btn-dark w-100 border border-info py-2">
                        <i class="fab fa-apple text-info me-1"></i> تحميل Delta (أيفون iOS)
                    </a>
                </div>
                <div class="col-md-4">
                    <a href="https://fluxteam.net/" target="_blank" class="btn btn-dark w-100 border border-warning py-2">
                        <i class="fas fa-bolt text-warning me-1"></i> تحميل Fluxus بديل
                    </a>
                </div>
            </div>
        </div>

        <!-- ➕ إنشاء سكربت جديد -->
        <div class="card p-4 mb-4">
            <h4 class="text-white mb-3"><i class="fas fa-lock text-primary me-2"></i> إنشاء رابط Loadstring محمي جديد</h4>
            <div class="mb-3">
                <label>كود اللوا (Lua Script):</label>
                <textarea id="newScript" class="form-control" rows="4" placeholder='print("Hello Mahdi!")'></textarea>
            </div>
            <div class="mb-3">
                <label>كلمة سر التعديل (Key):</label>
                <input type="text" id="newKey" class="form-control" placeholder="مفتاح لتعديل السكربت لاحقاً">
            </div>
            <button onclick="createScript()" class="btn btn-custom-primary w-100">🔒 توليد الحماية والرابط</button>
            <div id="createResult"></div>
        </div>

    </div>

    <div id="toast" class="toast-msg">تم النسخ بنجاح إلى الحافظة! 📋</div>

    <script>
        function showToast() {
            const t = document.getElementById('toast');
            t.classList.add('show');
            setTimeout(() => { t.classList.remove('show'); }, 2000);
        }

        async function createScript() {
            const script = document.getElementById('newScript').value;
            const key = document.getElementById('newKey').value;
            const resDiv = document.getElementById('createResult');
            if (!script || !key) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3 py-2">يرجى إدخال الكود ومفتاح التعديل!</div>';
                return;
            }
            try {
                const res = await fetch('/api/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ script, key })
                });
                const data = await res.json();
                if (data.success) {
                    const loadstringCode = `loadstring(game:HttpGet("${data.raw_url}"))()`;
                    resDiv.innerHTML = `
                        <div class="result-box">
                            <h5 class="text-success mb-2"><i class="fas fa-check-circle"></i> تم الإنشاء بنجاح!</h5>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="loadstringInput" value='${loadstringCode}' readonly>
                                <button class="btn btn-outline-success" type="button" onclick="copyText('loadstringInput')"><i class="fas fa-copy"></i> نسخ الكود</button>
                            </div>
                        </div>
                    `;
                }
            } catch (err) { resDiv.innerHTML = '<div class="alert alert-danger mt-3 py-2">خطأ في الاتصال!</div>'; }
        }

        function copyText(elementId) {
            const copyText = document.getElementById(elementId);
            copyText.select();
            navigator.clipboard.writeText(copyText.value);
            showToast();
        }
    </script>
</body>
</html>
'''

# ==========================================================
# 🌐 مسارات التوجيه وتسجيل الدخول
# ==========================================================
@app.route('/')
def home():
    # التحقق هل المستخدم مسجل دخول أم لا
    if 'user' not in session:
        return render_template_string(LOGIN_HTML)
    return render_template_string(INDEX_HTML, user=session['user'])

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def authorize_google():
    token = google.authorize_access_token()
    resp = google.get('oauth2/v2/userinfo')
    user_info = resp.json()
    
    # تخزين بيانات المستخدم في الجلسة (Session)
    session['user'] = {
        'name': user_info.get('name'),
        'email': user_info.get('email')
    }
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/api/create', methods=['POST'])
def create_script():
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'غيرحمص/غير مسجل دخول'}), 401
    
    data = request.get_json() or {}
    script = data.get('script')
    key = data.get('key')
    if not script or not key:
        return jsonify({'success': False, 'error': 'السكربت والمفتاح مطلوبان'}), 400
        
    script_id = generate_id()
    store = load_data()
    store[script_id] = {'script': script, 'key': key, 'owner': session['user']['email']}
    save_data(store)
    
    raw_url = request.host_url.rstrip('/') + '/raw/' + script_id
    return jsonify({'success': True, 'id': script_id, 'raw_url': raw_url})

@app.route('/raw/<script_id>')
def get_raw_script(script_id):
    user_agent = request.headers.get('User-Agent', '').lower()
    browsers = ['mozilla', 'chrome', 'safari', 'edge', 'opera', 'firefox', 'msie']
    executors = ['roblox', 'delta', 'synapse', 'fluxus', 'krnl', 'hydrogen', 'electron', 'swagmode']
    is_executor = any(e in user_agent for e in executors)
    is_browser = any(b in user_agent for b in browsers) and not is_executor

    if is_browser:
        return WARNING_HTML, 200, {'Content-Type': 'text/html; charset=utf-8'}

    store = load_data()
    item = store.get(script_id)
    if not item:
        return Response('-- Script Not Found', status=404, mimetype='text/plain')
    return Response(item['script'], status=200, mimetype='text/plain; charset=utf-8')

if __name__ == 'main':
    app.run(debug=True)
