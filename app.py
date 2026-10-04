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
# 🛑 صفحة "سنقر لا تسرق" مع أزرار التواصل المضيئة
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
            background-color: #0b0f19;
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
            background: #1e293b;
            padding: 2.5rem 2rem;
            border-radius: 1.25rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
            border: 2px solid #ef4444;
            max-width: 480px;
            width: 100%;
        }
        .social-buttons {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }
        .social-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 18px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.95rem;
            color: #fff !important;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .btn-discord { background-color: #5865F2; }
        .btn-youtube { background-color: #FF0000; }
        .btn-tiktok { background-color: #000000; border: 1px solid #334155; }
        .social-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.5);
            opacity: 0.9;
        }
        h1 { color: #ef4444; font-size: 2.2rem; margin: 0 0 1rem 0; font-weight: 800; }
        p { color: #cbd5e1; font-size: 1.1rem; line-height: 1.6; margin: 0; }
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
        <p>عذراً، هذا الرابط مخصص لتشغيله داخل اللعبة مباشرة ولا يمكنك عرض الكود البرمجي من المتصفح.</p>
    </div>
</body>
</html>
'''

# ==========================================================
# 🛡️ الصفحة الرئيسية لحماية السكربتات وتوفير ميزات للضيف
# ==========================================================
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حماية سكربتات اللوا - Lua Protect</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { 
            background-color: #0b0f19; 
            color: #f1f5f9; 
            font-family: system-ui, -apple-system, sans-serif; 
        }
        .card { 
            background-color: #1e293b; 
            border: 1px solid #334155; 
            border-radius: 1rem; 
        }
        label {
            color: #e2e8f0 !important;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .form-control { 
            background-color: #0f172a !important; 
            border: 1px solid #475569 !important; 
            color: #ffffff !important; 
            font-family: monospace;
            font-size: 0.95rem;
        }
        .form-control::placeholder {
            color: #64748b !important;
        }
        .form-control:focus { 
            border-color: #3b82f6 !important; 
            box-shadow: 0 0 0 0.25rem rgba(59, 130, 246, 0.25) !important; 
        }
        .btn-primary { background-color: #2563eb; border: none; font-weight: 600; }
        .btn-primary:hover { background-color: #1d4ed8; }
        .btn-warning { background-color: #d97706; border: none; color: #ffffff; font-weight: 600; }
        .btn-warning:hover { background-color: #b45309; color: #ffffff; }
        .btn-info { background-color: #0284c7; border: none; color: #ffffff; font-weight: 600; }
        .btn-info:hover { background-color: #0369a1; color: #ffffff; }
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
            padding: 8px 16px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.9rem;
            color: #fff !important;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .btn-discord { background-color: #5865F2; }
        .btn-youtube { background-color: #FF0000; }
        .btn-tiktok { background-color: #000000; border: 1px solid #334155; }
        .social-btn:hover { transform: translateY(-2px); opacity: 0.9; }
        .result-box {
            background-color: #0f172a;
            border: 1px solid #334155;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-top: 1rem;
        }
        code { color: #38bdf8; word-break: break-all; }
        .guest-badge {
            background-color: #0369a1;
            color: #e0f2fe;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            display: inline-block;
        }
    </style>
</head>
<body class="py-4">
    <div class="container" style="max-width: 750px;">
        
        <!-- Header -->
        <div class="text-center mb-4">
            <h2 class="fw-bold text-primary">🛡️ منصة حماية واستضافة السكربتات</h2>
            <p class="text-light mb-2">أنشئ رابط Loadstring محمي يعمل على Delta وجميع المشغلات</p>
            
            <div class="social-buttons mb-3">
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

        <!-- 🎁 قسم مميزات الضيف والزائر -->
        <div class="card p-3 mb-4 border-info">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h5 class="text-info mb-0">🎁 وضع التجربة المباشرة (Guest Mode)</h5>
                <span class="guest-badge">متاح للجميع</span>
            </div>
            <p class="text-light small mb-3">يمكنك كضيف تجربة السيرفر فوراً عن طريق توليد كود تجريبي جاهز ومحمي بضغطة زر واحدة!</p>
            <button onclick="generateGuestScript()" class="btn btn-info w-100">⚡ توليد سكربت تجريبي جاهز (للزوار)</button>
            <div id="guestResult"></div>
        </div>

        <!-- إنشاء سكربت جديد -->
        <div class="card p-4 mb-4">
            <h4 class="text-white mb-3">➕ إنشاء رابط محمي جديد</h4>
            <div class="mb-3">
                <label>كود اللوا (Lua Script):</label>
                <textarea id="newScript" class="form-control" rows="6" placeholder='print("Hello Mahdi!")'></textarea>
            </div>
            <div class="mb-3">
                <label>مفتاح التعديل (Password/Key):</label>
                <input type="text" id="newKey" class="form-control" placeholder="أدخل كلمة سر لتعديل السكربت بها لاحقاً">
            </div>
            <button onclick="createScript()" class="btn btn-primary btn-lg w-100">🔒 إنشاء وتوليد الـ Loadstring</button>
            <div id="createResult"></div>
        </div>

        <!-- تعديل سكربت موجود -->
        <div class="card p-4">
            <h4 class="text-white mb-3">✏️ تعديل كود سكربت حالي</h4>
            <div class="mb-3">
                <label>معرف السكربت (Script ID):</label>
                <input type="text" id="editId" class="form-control" placeholder="مثال: aBc123Xy">
            </div>
            <div class="mb-3">
                <label>مفتاح التعديل (Key):</label>
                <input type="password" id="editKey" class="form-control" placeholder="كلمة السر الخاصة بالسكربت">
            </div>
            <div class="mb-3">
                <label>الكود الجديد (New Lua Code):</label>
                <textarea id="editScript" class="form-control" rows="6" placeholder="ضع الكود الجديد هنا"></textarea>
            </div>
            <button onclick="updateScript()" class="btn btn-warning btn-lg w-100">🔄 تحديث السكربت</button>
            <div id="updateResult"></div>
        </div>
    </div>

    <script>
        async function generateGuestScript() {
            const guestScript = '-- Demo Script By Mahdi\\nprint("Hello from Guest Demo!")\\ngame:GetService("StarterGui"):SetCore("SendNotification", {Title="نجحت التجربة!", Text="السكربت التجريبي شغال مع Delta بنجاح 🚀", Duration=5})';
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
                        <div class="result-box mt-3">
                            <h6 class="text-info mb-2">🎉 تم توليد السكربت التجريبي للضيف بنجاح!</h6>
                            <p class="mb-1 text-light small"><b>Script ID:</b> <code>${data.id}</code> | <b>مفتاح التعديل:</b> <code>guest123</code></p>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="guestInput" value='${loadstringCode}' readonly>
                                <button class="btn btn-outline-light" type="button" onclick="copyToClipboard('guestInput')">📋 نسخ الـ Loadstring</button>
                            </div>
                            <small class="text-secondary">جرب فتح الرابط المباشر في المتصفح لتشاهد رسالة (سنقر لا تسرق)، أو شغّله في روبلوكس مباشرة!</small>
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
                resDiv.innerHTML = '<div class="alert alert-danger mt-3">يرجى إدخال الكود ومفتاح التعديل!</div>';
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
                        <div class="result-box mt-3">
                            <h5 class="text-success mb-2">✅ تم الإنشاء بنجاح!</h5>
                            <p class="mb-2"><b>Script ID:</b> <code id="createdId">${data.id}</code></p>
                            <label class="d-block mb-1">كود الـ Loadstring:</label>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="loadstringInput" value='${loadstringCode}' readonly>
                                <button class="btn btn-outline-light" type="button" onclick="copyToClipboard('loadstringInput')">📋 نسخ الكود</button>
                            </div>
                        </div>
                    `;
                } else {
                    resDiv.innerHTML = `<div class="alert alert-danger mt-3">${data.error}</div>`;
                }
            } catch (err) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3">حدث خطأ في الاتصال بالفرسيل!</div>';
            }
        }

        async function updateScript() {
            const id = document.getElementById('editId').value;
            const key = document.getElementById('editKey').value;
            const script = document.getElementById('editScript').value;
            const resDiv = document.getElementById('updateResult');

            if (!id || !key || !script) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3">يرجى ملء جميع الحقول المطلوب تعديلها!</div>';
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
                    resDiv.innerHTML = '<div class="alert alert-success mt-3">✅ تم تحديث السكربت بنجاح! سيعمل الكود الجديد فوراً بدون تغيير الرابط.</div>';
                } else {
                    resDiv.innerHTML = `<div class="alert alert-danger mt-3">${data.error}</div>`;
                }
            } catch (err) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3">حدث خطأ أثناء التحديث!</div>';
            }
        }

        function copyToClipboard(elementId) {
            const copyText = document.getElementById(elementId);
            copyText.select();
            copyText.setSelectionRange(0, 99999);
            navigator.clipboard.writeText(copyText.value);
            alert("تم نسخ الكود بنجاح!");
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
