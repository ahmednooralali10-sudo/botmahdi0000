import os
import secrets
import string
import requests
from flask import Flask, request, jsonify, Response, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(24))

# إعدادات قوقل OAuth (يمكنك وضعها هنا أو كمتغيرات بيئة Environment Variables في Vercel)
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'ضع_هنا_Client_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'ضع_هنا_Client_Secret')

# قاعدة بيانات مؤقتة في الذاكرة لضمان عدم حدوث خطأ 500 على Vercel
SCRIPTS_DB = {}

def generate_id(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# صفحة تسجيل الدخول الإجبارية
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
        body { background: radial-gradient(circle at center, #0f172a 0%, #020617 100%); color: #ffffff; font-family: system-ui, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; text-align: center; padding: 1rem; }
        .card { background: rgba(30, 41, 59, 0.85); backdrop-filter: blur(16px); padding: 3rem 2rem; border-radius: 1.5rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8); border: 1px solid rgba(59, 130, 246, 0.3); max-width: 440px; width: 100%; }
        .btn-google { background-color: #ffffff; color: #000000; font-weight: 700; border-radius: 50px; padding: 12px 24px; display: inline-flex; align-items: center; justify-content: center; gap: 12px; text-decoration: none; width: 100%; box-shadow: 0 4px 15px rgba(0,0,0,0.3); transition: 0.3s; }
        .btn-google:hover { background-color: #f1f5f9; transform: translateY(-2px); }
        h1 { color: #38bdf8; font-size: 2rem; margin-bottom: 1rem; font-weight: 800; }
        p { color: #94a3b8; font-size: 1.05rem; line-height: 1.6; margin-bottom: 2rem; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🔒 تسجيل الدخول مطلوب</h1>
        <p>عذراً يا مهدي، لا يمكنك دخول الموقع أو رؤية لوحة التحكم إلا بعد تسجيل الدخول بحساب Google.</p>
        <a href="/login/google" class="btn btn-google">
            <i class="fab fa-google text-danger fs-5"></i> تسجيل الدخول بواسطة Google
        </a>
    </div>
</body>
</html>
'''

WARNING_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>سنقر لا تسرق!</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <style>
        body { background: #020617; color: #fff; display: flex; align-items: center; justify-content: center; height: 100vh; text-align: center; font-family: sans-serif; }
        .card { background: rgba(30, 41, 59, 0.7); padding: 3rem; border-radius: 1rem; border: 1px solid #ef4444; max-width: 450px; }
        h1 { color: #ef4444; margin-bottom: 1rem; }
        p { color: #94a3b8; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🦊🛑 سنقر لا تسرق!</h1>
        <p>هذا الرابط مخصص للتشغيل داخل اللعبة (Executor) مباشرة، ولا يمكن عرضه من خلال المتصفح العادي.</p>
    </div>
</body>
</html>
'''

INDEX_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة الحماية والمشغلات</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: radial-gradient(circle at top, #0f172a 0%, #07090e 100%); color: #f1f5f9; font-family: system-ui, sans-serif; min-height: 100vh; }
        .card { background: rgba(19, 27, 46, 0.85); border: 1px solid rgba(51, 65, 85, 0.6); border-radius: 1.25rem; }
        .form-control { background-color: #0b0f19 !important; border: 1px solid #334155 !important; color: #fff !important; font-family: monospace; border-radius: 0.75rem; padding: 0.75rem; }
        .download-box { background: rgba(15, 23, 42, 0.9); border: 1px dashed #3b82f6; border-radius: 1rem; padding: 1.5rem; margin-bottom: 2rem; }
        .toast-msg { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%) translateY(100px); background: #10b981; color: white; padding: 10px 24px; border-radius: 50px; font-weight: bold; transition: 0.3s; z-index: 9999; }
        .toast-msg.show { transform: translateX(-50%) translateY(0); }
    </style>
</head>
<body class="py-4">
    <div class="container" style="max-width: 800px;">
        <div class="d-flex justify-content-between align-items-center mb-4 p-3 card">
            <div>
                <h4 class="text-info fw-bold mb-0">Lua Protect Hub</h4>
                <small class="text-secondary">المستخدم: {{ user.name }} ({{ user.email }})</small>
            </div>
            <a href="/logout" class="btn btn-outline-danger btn-sm rounded-pill px-3"><i class="fas fa-sign-out-alt"></i> خروج</a>
        </div>

        <div class="download-box text-center">
            <h4 class="text-primary mb-3"><i class="fas fa-download me-2"></i> تحميل مشغلات روبلوكس</h4>
            <div class="row g-2 justify-content-center">
                <div class="col-md-4">
                    <a href="https://deltaexploits.gg/" target="_blank" class="btn btn-dark w-100 border border-primary py-2"><i class="fab fa-android text-success me-1"></i> تحميل Delta (أندرويد)</a>
                </div>
                <div class="col-md-4">
                    <a href="https://deltaexploits.gg/" target="_blank" class="btn btn-dark w-100 border border-info py-2"><i class="fab fa-apple text-info me-1"></i> تحميل Delta (أيفون)</a>
                </div>
                <div class="col-md-4">
                    <a href="https://fluxteam.net/" target="_blank" class="btn btn-dark w-100 border border-warning py-2"><i class="fas fa-bolt text-warning me-1"></i> تحميل Fluxus</a>
                </div>
            </div>
        </div>

        <div class="card p-4 mb-4">
            <h4 class="text-white mb-3"><i class="fas fa-lock text-primary me-2"></i> إنشاء رابط Loadstring محمي</h4>
            <div class="mb-3">
                <label class="text-secondary mb-1">كود اللوا (Lua Script):</label>
                <textarea id="newScript" class="form-control" rows="4" placeholder='print("Hello Mahdi!")'></textarea>
            </div>
            <div class="mb-3">
                <label class="text-secondary mb-1">كلمة سر التعديل (Key):</label>
                <input type="text" id="newKey" class="form-control" placeholder="مفتاح التعديل">
            </div>
            <button onclick="createScript()" class="btn btn-primary w-100 fw-bold py-2 rounded-3">🔒 توليد الحماية والرابط</button>
            <div id="createResult"></div>
        </div>
    </div>

    <div id="toast" class="toast-msg">تم النسخ بنجاح! 📋</div>

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
            if (!script || !key) { resDiv.innerHTML = '<div class="alert alert-danger mt-3 py-2">أدخل الكود والمفتاح!</div>'; return; }
            try {
                const res = await fetch('/api/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ script, key })
                });
                const data = await res.json();
                if (data.success) {
                    const code = `loadstring(game:HttpGet("${data.raw_url}"))()`;
                    resDiv.innerHTML = `<div class="bg-dark p-3 rounded mt-3 border border-success">
                        <input type="text" class="form-control mb-2" id="resCode" value='${code}' readonly>
                        <button class="btn btn-success btn-sm w-100" onclick="navigator.clipboard.writeText(document.getElementById('resCode').value); showToast();">نسخ الكود</button>
                    </div>`;
                }
            } catch(e) { resDiv.innerHTML = '<div class="alert alert-danger mt-3">خطأ في الاتصال!</div>'; }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    if 'user' not in session:
        return render_template_string(LOGIN_HTML)
    return render_template_string(INDEX_HTML, user=session['user'])

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope=email%20profile"
    return redirect(google_auth_url)

@app.route('/authorize/google')
def authorize_google():
    code = request.args.get('code')
    if not code:
        return redirect('/')
    
    redirect_uri = url_for('authorize_google', _external=True)
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    try:
        res = requests.post(token_url, data=payload)
        if res.status_code != 200:
            return f"فشل المصادقة مع قوقل: {res.text}", 400
            
        token_data = res.json()
        access_token = token_data.get('access_token')
        
        user_info_res = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={'Authorization': f'Bearer {access_token}'})
        if user_info_res.status_code != 200:
            return "فشل جلب بيانات المستخدم", 400
            
        user_info = user_info_res.json()
        session['user'] = {
            'name': user_info.get('name'),
            'email': user_info.get('email')
        }
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بقوقل: {str(e)}", 500
        
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/api/create', methods=['POST'])
def create_script():
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'غير مسجل دخول'}), 401
    data = request.get_json() or {}
    script = data.get('script')
    key = data.get('key')
    if not script or not key:
        return jsonify({'success': False, 'error': 'مطلوب السكربت والمفتاح'}), 400
    script_id = generate_id()
    SCRIPTS_DB[script_id] = {'script': script, 'key': key, 'owner': session['user']['email']}
    raw_url = request.host_url.rstrip('/') + '/raw/' + script_id
    return jsonify({'success': True, 'id': script_id, 'raw_url': raw_url})

@app.route('/raw/<script_id>')
def get_raw_script(script_id):
    ua = request.headers.get('User-Agent', '').lower()
    browsers = ['mozilla', 'chrome', 'safari', 'edge', 'opera', 'firefox']
    executors = ['roblox', 'delta', 'synapse', 'fluxus', 'krnl', 'hydrogen']
    if any(b in ua for b in browsers) and not any(e in ua for e in executors):
        return WARNING_HTML, 200, {'Content-Type': 'text/html; charset=utf-8'}
    
    item = SCRIPTS_DB.get(script_id)
    if not item:
        return Response('-- Script Not Found', status=404, mimetype='text/plain')
    return Response(item['script'], status=200, mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    app.run(debug=True)
