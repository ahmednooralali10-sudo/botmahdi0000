import os
import json
import secrets
import string
from flask import Flask, request, jsonify, Response, render_template_string

app = Flask(__name__)

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
# 🛑 صفحة حماية المتصفح "سنقر لا تسرق!"
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
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            padding: 3rem 2rem;
            border-radius: 1.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            border: 1px solid rgba(239, 68, 68, 0.4);
            max-width: 480px;
            width: 100%;
        }
        .social-buttons {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        .social-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.95rem;
            color: #fff !important;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .btn-discord { background-color: #5865F2; }
        .btn-youtube { background-color: #FF0000; }
        .btn-tiktok { background-color: #000000; border: 1px solid #334155; }
        .social-btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
            opacity: 0.9;
        }
        h1 { color: #ef4444; font-size: 2.3rem; margin: 0 0 1rem 0; font-weight: 800; text-shadow: 0 0 20px rgba(239, 68, 68, 0.4); }
        p { color: #94a3b8; font-size: 1.1rem; line-height: 1.7; margin: 0; }
    </style>
</head>
<body>
    <div class="card">
        <div class="social-buttons">
            <a href="https://discord.gg/j8daZqG9V" target="_blank" class="social-btn btn-discord">
                <i class="fab fa-discord fs-5"></i> Discord
            </a>
            <a href="https://youtube.com/@xoreyt0?si=swNpSO2vzquGFE4i" target="_blank" class="social-btn btn-youtube">
                <i class="fab fa-youtube fs-5"></i> YouTube
            </a>
            <a href="https://www.tiktok.com/@lklkl7777" target="_blank" class="social-btn btn-tiktok">
                <i class="fab fa-tiktok fs-5"></i> TikTok
            </a>
        </div>

        <h1>🦊🛑 سنقر لا تسرق!</h1>
        <p>عذراً، هذا الرابط مخصص للتشغيل داخل اللعبة (Executor) مباشرة، ولا يمكن عرض الكود البرمجي من خلال المتصفح العادي.</p>
    </div>
</body>
</html>
'''

# ==========================================================
# 🛡️ الواجهة الرئيسية المطورة والفاخرة
# ==========================================================
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة حماية واستضافة السكربتات الاحترافية</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-main: #07090e;
            --bg-card: rgba(19, 27, 46, 0.85);
            --border-color: rgba(51, 65, 85, 0.6);
            --primary-glow: rgba(37, 99, 235, 0.4);
        }
        body { 
            background: radial-gradient(circle at top, #0f172a 0%, var(--bg-main) 100%);
            color: #f1f5f9; 
            font-family: system-ui, -apple-system, sans-serif; 
            min-height: 100vh;
        }
        .navbar-brand {
            font-weight: 800;
            background: linear-gradient(45deg, #38bdf8, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .card { 
            background: var(--bg-card); 
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color); 
            border-radius: 1.25rem; 
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease;
        }
        .card:hover {
            border-color: rgba(59, 130, 246, 0.3);
        }
        label {
            color: #cbd5e1 !important;
            font-weight: 600;
            margin-bottom: 0.5rem;
            font-size: 0.95rem;
        }
        .form-control { 
            background-color: #0b0f19 !important; 
            border: 1px solid #334155 !important; 
            color: #ffffff !important; 
            font-family: monospace;
            font-size: 0.95rem;
            border-radius: 0.75rem;
            padding: 0.75rem 1rem;
        }
        .form-control::placeholder { color: #475569 !important; }
        .form-control:focus { 
            border-color: #3b82f6 !important; 
            box-shadow: 0 0 0 4px var(--primary-glow) !important; 
        }
        .btn-custom-primary { 
            background: linear-gradient(135deg, #2563eb, #1d4ed8); 
            border: none; 
            font-weight: 700;
            border-radius: 0.75rem;
            padding: 0.75rem 1.5rem;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
            transition: all 0.3s ease;
            color: #fff;
        }
        .btn-custom-primary:hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
            background: linear-gradient(135deg, #1d4ed8, #1e40af);
        }
        .btn-custom-info { 
            background: linear-gradient(135deg, #0284c7, #0369a1); 
            border: none; 
            font-weight: 700;
            border-radius: 0.75rem;
            padding: 0.75rem 1.5rem;
            box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
            transition: all 0.3s ease;
            color: #fff;
        }
        .btn-custom-info:hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(2, 132, 199, 0.6);
            background: linear-gradient(135deg, #0369a1, #075985);
        }
        .btn-custom-warning { 
            background: linear-gradient(135deg, #d97706, #b45309); 
            border: none; 
            font-weight: 700;
            border-radius: 0.75rem;
            padding: 0.75rem 1.5rem;
            box-shadow: 0 4px 15px rgba(217, 119, 6, 0.4);
            transition: all 0.3s ease;
            color: #fff;
        }
        .btn-custom-warning:hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(217, 119, 6, 0.6);
            background: linear-gradient(135deg, #b45309, #92400e);
        }
        .social-buttons {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-top: 1rem;
            flex-wrap: wrap;
        }
        .social-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 18px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.9rem;
            color: #fff !important;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .btn-discord { background-color: #5865F2; }
        .btn-youtube { background-color: #FF0000; }
        .btn-tiktok { background-color: #000000; border: 1px solid #334155; }
        .social-btn:hover { transform: translateY(-3px) scale(1.03); opacity: 0.95; }
        .result-box {
            background-color: #0b0f19;
            border: 1px solid #334155;
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin-top: 1rem;
            animation: fadeIn 0.4s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        code { color: #38bdf8; word-break: break-all; }
        .stats-badge {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid #334155;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.85rem;
            color: #94a3b8;
        }
        /* Toast notification */
        .toast-msg {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: #10b981;
            color: white;
            padding: 10px 24px;
            border-radius: 50px;
            font-weight: bold;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transition: transform 0.3s ease;
            z-index: 9999;
        }
        .toast-msg.show {
            transform: translateX(-50%) translateY(0);
        }
    </style>
</head>
<body class="py-4">
    <div class="container" style="max-width: 800px;">
        
        <!-- Header -->
        <div class="text-center mb-5">
            <div class="mb-2">
                <span class="stats-badge"><i class="fas fa-shield-halved text-primary me-2"></i> منصة حماية سكربتات روبلوكس الاحترافية</span>
            </div>
            <h1 class="fw-bold navbar-brand display-6 mb-2">Lua Protect & Host</h1>
            <p class="text-secondary mb-3">احمِ كودك برابط Loadstring آمن يعمل بسلاسة على Delta وجميع المشغلات القوية</p>
            
            <div class="social-buttons mb-2">
                <a href="https://discord.gg/j8daZqG9V" target="_blank" class="social-btn btn-discord">
                    <i class="fab fa-discord fs-5"></i> سيرفر الديسكورد
                </a>
                <a href="https://youtube.com/@xoreyt0?si=swNpSO2vzquGFE4i" target="_blank" class="social-btn btn-youtube">
                    <i class="fab fa-youtube fs-5"></i> قناة اليوتيوب
                </a>
                <a href="https://www.tiktok.com/@lklkl7777" target="_blank" class="social-btn btn-tiktok">
                    <i class="fab fa-tiktok fs-5"></i> حساب التيك توك
                </a>
            </div>
        </div>

        <!-- 🎁 قسم تجربة الضيف السريعة -->
        <div class="card p-4 mb-4 border-info shadow-sm">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h5 class="text-info mb-0"><i class="fas fa-bolt me-2"></i> تجربة سريعة للزوار (Guest Demo)</h5>
                <span class="badge bg-info text-dark">فوري</span>
            </div>
            <p class="text-secondary small mb-3">اضغط الزر أدناه لتوليد سكربت تجريبي جاهز ومجرب على دلتا لترى كيف يعمل النظام:</p>
            <button onclick="generateGuestScript()" class="btn btn-custom-info w-100">⚡ توليد سكربت تجريبي الآن</button>
            <div id="guestResult"></div>
        </div>

        <!-- ➕ إنشاء سكربت جديد -->
        <div class="card p-4 mb-4">
            <h4 class="text-white mb-3"><i class="fas fa-lock text-primary me-2"></i> إنشاء رابط Loadstring محمي جديد</h4>
            <div class="mb-3">
                <label>كود اللوا (Lua Script):</label>
                <textarea id="newScript" class="form-control" rows="5" placeholder='print("Hello from Mahdi Server!")'></textarea>
            </div>
            <div class="mb-3">
                <label>كلمة سر التعديل (Key):</label>
                <input type="text" id="newKey" class="form-control" placeholder="مفتاح سري لتتمكن من تعديل الكود لاحقاً">
            </div>
            <button onclick="createScript()" class="btn btn-custom-primary w-100">🔒 توليد الحماية والرابط</button>
            <div id="createResult"></div>
        </div>

        <!-- ✏️ تعديل سكربت موجود -->
        <div class="card p-4">
            <h4 class="text-white mb-3"><i class="fas fa-pen-to-square text-warning me-2"></i> تعديل سكربت حالي</h4>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label>معرف السكربت (Script ID):</label>
                    <input type="text" id="editId" class="form-control" placeholder="مثال: aBc123Xy">
                </div>
                <div class="col-md-6 mb-3">
                    <label>كلمة السر (Key):</label>
                    <input type="password" id="editKey" class="form-control" placeholder="مفتاح السكربت السري">
                </div>
            </div>
            <div class="mb-3">
                <label>الكود الجديد (New Lua Code):</label>
                <textarea id="editScript" class="form-control" rows="5" placeholder="ضع الكود الجديد هنا وسيتحدث فوراً دون تغيير الرابط"></textarea>
            </div>
            <button onclick="updateScript()" class="btn btn-custom-warning w-100">🔄 حفظ التحديثات</button>
            <div id="updateResult"></div>
        </div>

    </div>

    <!-- Toast Notification -->
    <div id="toast" class="toast-msg">تم النسخ بنجاح إلى الحافظة! 📋</div>

    <script>
        function showToast() {
            const t = document.getElementById('toast');
            t.classList.add('show');
            setTimeout(() => {
                t.classList.remove('show');
            }, 2000);
        }

        async function generateGuestScript() {
            const guestScript = '-- Demo Script By Mahdi\\nprint("Hello from Guest Demo!")\\ngame:GetService("StarterGui"):SetCore("SendNotification", {Title="نجحت التجربة!", Text="السكربت شغال مع Delta بنجاح 🚀", Duration=5})';
            const guestKey = "guest123";
            const resDiv = document.getElementById('guestResult');

            try {
                const res = await fetch('/api/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ script: guestScript, key: guestKey })
                });
                const data = await res.json();

                if (data.success) {
                    const loadstringCode = `loadstring(game:HttpGet("${data.raw_url}"))()`;
                    resDiv.innerHTML = `
                        <div class="result-box">
                            <h6 class="text-info mb-2">🎉 تم توليد السكربت التجريبي بنجاح!</h6>
                            <p class="mb-1 text-secondary small"><b>Script ID:</b> <code>${data.id}</code> | <b>كلمة السر:</b> <code>guest123</code></p>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="guestInput" value='${loadstringCode}' readonly>
                                <button class="btn btn-outline-info" type="button" onclick="copyText('guestInput')"><i class="fas fa-copy"></i> نسخ</button>
                            </div>
                        </div>
                    `;
                }
            } catch (err) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-2">حدث خطأ أثناء توليد التجربة!</div>';
            }
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
                            <h5 class="text-success mb-2"><i class="fas fa-check-circle"></i> تم الحماية والإنشاء بنجاح!</h5>
                            <p class="mb-2 text-secondary"><b>Script ID:</b> <code>${data.id}</code></p>
                            <label class="d-block mb-1 text-light">كود الـ Loadstring الجاهز:</label>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="loadstringInput" value='${loadstringCode}' readonly>
                                <button class="btn btn-outline-success" type="button" onclick="copyText('loadstringInput')"><i class="fas fa-copy"></i> نسخ الكود</button>
                            </div>
                        </div>
                    `;
                } else {
                    resDiv.innerHTML = `<div class="alert alert-danger mt-3 py-2">${data.error}</div>`;
                }
            } catch (err) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3 py-2">حدث خطأ في الاتصال بالخادم!</div>';
            }
        }

        async function updateScript() {
            const id = document.getElementById('editId').value;
            const key = document.getElementById('editKey').value;
            const script = document.getElementById('editScript').value;
            const resDiv = document.getElementById('updateResult');

            if (!id || !key || !script) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3 py-2">يرجى ملء جميع الحقول المطلوبة للتعديل!</div>';
                return;
            }

            try {
                const res = await fetch('/api/update', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ id, key, script })
                });
                const data = await res.json();

                if (data.success) {
                    resDiv.innerHTML = '<div class="alert alert-success mt-3 py-2"><i class="fas fa-check-circle"></i> تم تحديث السكربت بنجاح! التغييرات سارية فوراً بدون تغيير الرابط.</div>';
                } else {
                    resDiv.innerHTML = `<div class="alert alert-danger mt-3 py-2">${data.error}</div>`;
                }
            } catch (err) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3 py-2">حدث خطأ أثناء الاتصال للتحديث!</div>';
            }
        }

        function copyText(elementId) {
            const copyText = document.getElementById(elementId);
            copyText.select();
            copyText.setSelectionRange(0, 99999);
            navigator.clipboard.writeText(copyText.value);
            showToast();
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

@app.route('/api/create', methods=['POST'])
def create_script():
    data = request.get_json() or {}
    script = data.get('script')
    key = data.get('key')

    if not script or not key:
        return jsonify({'success': False, 'error': 'السكربت والمفتاح مطلوبان'}), 400

    script_id = generate_id()
    store = load_data()
    store[script_id] = {
        'script': script,
        'key': key
    }
    save_data(store)

    raw_url = request.host_url.rstrip('/') + '/raw/' + script_id
    return jsonify({'success': True, 'id': script_id, 'raw_url': raw_url})

@app.route('/api/update', methods=['POST'])
def update_script():
    data = request.get_json() or {}
    script_id = data.get('id', '').strip()
    key = data.get('key', '').strip()
    new_script = data.get('script')

    store = load_data()

    if script_id not in store:
        return jsonify({'success': False, 'error': 'معرف السكربت غير موجود!'}), 404

    if store[script_id]['key'] != key:
        return jsonify({'success': False, 'error': 'مفتاح التعديل (كلمة السر) غير صحيح!'}), 403

    store[script_id]['script'] = new_script
    save_data(store)

    return jsonify({'success': True})

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
        return Response('-- Script Not Found or Expired', status=404, mimetype='text/plain')

    return Response(item['script'], status=200, mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    app.run()
