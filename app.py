import os
import json
import secrets
import string
import time
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
# 🛑 صفحة "سنقر لا تسرق" الاحترافية المجهزة
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
            background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            text-align: center;
            padding: 1.5rem;
        }
        .card-custom {
            background: #1e293b;
            padding: 3rem 2rem;
            border-radius: 1.5rem;
            box-shadow: 0 25px 50px -12px rgba(239, 68, 68, 0.25);
            border: 2px solid #ef4444;
            max-width: 520px;
            width: 100%;
            backdrop-filter: blur(10px);
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
            font-weight: 700;
            font-size: 0.95rem;
            color: #fff !important;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        .btn-discord { background: linear-gradient(135deg, #5865F2, #4752C4); }
        .btn-youtube { background: linear-gradient(135deg, #FF0000, #CC0000); }
        .btn-tiktok { background: #000000; border: 1px solid #334155; }
        .social-btn:hover {
            transform: translateY(-4px) scale(1.03);
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
        }
        .warning-icon {
            font-size: 4.5rem;
            color: #ef4444;
            margin-bottom: 1rem;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.08); }
            100% { transform: scale(1); }
        }
        h1 { color: #ef4444; font-size: 2.5rem; margin-bottom: 1rem; font-weight: 900; }
        p { color: #94a3b8; font-size: 1.15rem; line-height: 1.7; margin-bottom: 0; }
    </style>
</head>
<body>
    <div class="card-custom">
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

        <div class="warning-icon">
            <i class="fas fa-user-shield"></i>
        </div>

        <h1>🦊🛑 سنقر لا تسرق!</h1>
        <p>عذراً، هذا الرابط محمي بواسطة منصة مهدي. مخصص لتشغيله داخل اللعبة عبر Delta/Executors ولا يمكنك عرض الكود المصدر من المتصفح.</p>
    </div>
</body>
</html>
'''

# ==========================================================
# 🛡️ الواجهة الرئيسية الشاملة لجميع الخدمات والمميزات
# ==========================================================
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة مهدي - استضافة وحماية سكربتات Lua</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-main: #0b0f19;
            --card-bg: #1e293b;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
            --accent-purple: #8b5cf6;
        }
        body { 
            background-color: var(--bg-main); 
            color: #f8fafc; 
            font-family: system-ui, -apple-system, sans-serif; 
        }
        .card { 
            background-color: var(--card-bg); 
            border: 1px solid #334155; 
            border-radius: 1.25rem; 
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
        }
        .nav-pills .nav-link {
            color: #94a3b8;
            font-weight: 600;
            border-radius: 0.75rem;
            padding: 0.75rem 1.25rem;
        }
        .nav-pills .nav-link.active {
            background-color: var(--accent-blue);
            color: #fff;
        }
        label { color: #e2e8f0 !important; font-weight: 600; margin-bottom: 0.5rem; }
        .form-control, .form-select { 
            background-color: #0f172a !important; 
            border: 1px solid #475569 !important; 
            color: #ffffff !important; 
            font-family: monospace;
        }
        .form-control:focus, .form-select:focus { 
            border-color: var(--accent-blue) !important; 
            box-shadow: 0 0 0 0.25rem rgba(59, 130, 246, 0.25) !important; 
        }
        .social-buttons { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
        .social-btn {
            display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px;
            border-radius: 50px; font-weight: 700; font-size: 0.95rem; color: #fff !important;
            text-decoration: none; transition: all 0.3s ease;
        }
        .btn-discord { background: #5865F2; }
        .btn-youtube { background: #FF0000; }
        .btn-tiktok { background: #000000; border: 1px solid #334155; }
        .social-btn:hover { transform: translateY(-3px); opacity: 0.95; }
        .result-box {
            background-color: #0f172a; border: 1px solid #334155;
            border-radius: 0.75rem; padding: 1.25rem; margin-top: 1rem;
        }
        code { color: #38bdf8; word-break: break-all; }
        .badge-guest { background: #0284c7; color: #fff; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; }
    </style>
</head>
<body class="py-4">
    <div class="container" style="max-width: 900px;">
        
        <!-- Header Section -->
        <div class="text-center mb-4">
            <h1 class="fw-bold text-primary mb-2">🛡️ منصة حماية واستضافة السكربتات</h1>
            <p class="text-light fs-5 mb-3">النظام الشامل لحماية أكواد Lua ودعم المشغلات (Delta, Solara, Hydrogen)</p>
            
            <div class="social-buttons mb-4">
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

            <!-- Navigation Tabs -->
            <ul class="nav nav-pills nav-justified bg-dark p-2 border border-secondary rounded-4 mb-4" id="mainTab">
                <li class="nav-item">
                    <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tab-create"><i class="fas fa-plus-circle me-1"></i> إنشاء رابط</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-guest"><i class="fas fa-user-astronaut me-1"></i> ميزات الضيف</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-templates"><li class="fas fa-code me-1"></i> أكواد جاهزة</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-edit"><i class="fas fa-edit me-1"></i> تعديل سكربت</button>
                </li>
            </ul>
        </div>

        <div class="tab-content">
            <!-- TAB 1: CREATE SCRIPT -->
            <div class="tab-pane fade show active" id="tab-create">
                <div class="card p-4">
                    <h4 class="text-white mb-3"><i class="fas fa-lock text-primary me-2"></i>إنشاء رابط Loadstring محمي</h4>
                    <div class="mb-3">
                        <label>كود اللوا الأصلي (Lua Script):</label>
                        <textarea id="newScript" class="form-control" rows="8" placeholder='print("Hello Mahdi!")'></textarea>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label>مفتاح التعديل (Password/Key):</label>
                            <input type="text" id="newKey" class="form-control" placeholder="أدخل كلمة سر لتعديل السكربت لاحقاً">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label>نوع التشفير المضاف (اختياري):</label>
                            <select id="obfuscateOpt" class="form-select">
                                <option value="none">بدون تشفير إضافي (Raw Protect)</option>
                                <option value="hex">تشفير Hex Strings</option>
                                <option value="base64">تشفير Base64 Loader</option>
                            </select>
                        </div>
                    </div>
                    <button onclick="createScript()" class="btn btn-primary btn-lg w-100 mt-2"><i class="fas fa-shield-alt me-2"></i>توليد الـ Loadstring المحمي</button>
                    <div id="createResult"></div>
                </div>
            </div>

            <!-- TAB 2: GUEST FEATURES -->
            <div class="tab-pane fade" id="tab-guest">
                <div class="card p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="text-white mb-0"><i class="fas fa-gift text-info me-2"></i>خدمات ومميزات الضيف</h4>
                        <span class="badge-guest">Guest Perks</span>
                    </div>
                    <p class="text-light">يمكنك كزائر تجربة السيرفر واختبار استجابته وقوة حمايته دون الحاجة لتسجيل أو إدخال كود خاص بك!</p>
                    
                    <div class="row g-3">
                        <div class="col-md-6">
                            <div class="p-3 border border-secondary rounded-3 bg-dark">
                                <h5>⚡ تجربة سريعة بضغطة زر</h5>
                                <p class="small text-secondary">يتم توليد سكربت لوا تجريبي يحتوي على إشعارات وشاشة نوتيفيكيشن فورية.</p>
                                <button onclick="generateGuestScript()" class="btn btn-info w-100">توليد سكربت تجريبي</button>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="p-3 border border-secondary rounded-3 bg-dark">
                                <h5>🔍 محاكي فحص الحماية</h5>
                                <p class="small text-secondary">جرب فتح رابط تجريبي كمتصفح لتشاهد رسالة (سنقر لا تسرق) مباشرة.</p>
                                <button onclick="testProtectionModal()" class="btn btn-outline-danger w-100">معاينة صفحة الحظر</button>
                            </div>
                        </div>
                    </div>
                    <div id="guestResult"></div>
                </div>
            </div>

            <!-- TAB 3: TEMPLATES -->
            <div class="tab-pane fade" id="tab-templates">
                <div class="card p-4">
                    <h4 class="text-white mb-3"><i class="fas fa-layer-group text-warning me-2"></i>أكواد وسكربتات لوا جاهزة</h4>
                    <p class="text-secondary mb-3">اختر أحد الأكواد الجاهزة أدناه واستضفه مباشرة بضغطة زر:</p>
                    
                    <div class="list-group">
                        <button onclick="loadTemplate(1)" class="list-group-item list-group-item-action bg-dark text-white border-secondary mb-2 rounded">
                            <div class="d-flex w-100 justify-content-between">
                                <h5 class="mb-1 text-primary">1. Notification GUI Script</h5>
                                <small class="text-muted">Lua UI</small>
                            </div>
                            <p class="mb-1 small text-secondary">سكربت يعرض إشعار ترحيبي مع صوت هادئ داخل رابلوكس.</p>
                        </button>
                        
                        <button onclick="loadTemplate(2)" class="list-group-item list-group-item-action bg-dark text-white border-secondary mb-2 rounded">
                            <div class="d-flex w-100 justify-content-between">
                                <h5 class="mb-1 text-success">2. Speed & Jump Power GUI</h5>
                                <small class="text-muted">Character Helper</small>
                            </div>
                            <p class="mb-1 small text-secondary">واجهة بسيطة لزيادة السرعة والقفز داخل أي لعبة.</p>
                        </button>
                    </div>
                </div>
            </div>

            <!-- TAB 4: EDIT SCRIPT -->
            <div class="tab-pane fade" id="tab-edit">
                <div class="card p-4">
                    <h4 class="text-white mb-3"><i class="fas fa-edit text-warning me-2"></i>تعديل سكربت موجود</h4>
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
                        <textarea id="editScript" class="form-control" rows="8" placeholder="ضع الكود الجديد هنا"></textarea>
                    </div>
                    <button onclick="updateScript()" class="btn btn-warning btn-lg w-100"><i class="fas fa-sync me-2"></i>تحديث الكود فوراً</button>
                    <div id="updateResult"></div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        async function createScript() {
            const script = document.getElementById('newScript').value;
            const key = document.getElementById('newKey').value;
            const obfuscate = document.getElementById('obfuscateOpt').value;
            const resDiv = document.getElementById('createResult');

            if (!script || !key) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3">يرجى إدخال الكود ومفتاح التعديل!</div>';
                return;
            }

            try {
                const res = await fetch('/api/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ script, key, obfuscate })
                });
                const data = await res.json();

                if (data.success) {
                    const loadstringCode = `loadstring(game:HttpGet("${data.raw_url}"))()`;
                    resDiv.innerHTML = `
                        <div class="result-box mt-3">
                            <h5 class="text-success mb-2">✅ تم الإنشاء والحماية بنجاح!</h5>
                            <p class="mb-2"><b>Script ID:</b> <code>${data.id}</code></p>
                            <label class="d-block mb-1">كود الـ Loadstring المباشر:</label>
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
                resDiv.innerHTML = '<div class="alert alert-danger mt-3">حدث خطأ أثناء الاتصال بالفيرسيل!</div>';
            }
        }

        async function generateGuestScript() {
            const guestScript = '-- Demo Script By Mahdi\\nprint("Hello from Guest Demo!")\\ngame:GetService("StarterGui"):SetCore("SendNotification", {Title="نجحت التجربة!", Text="السكربت التجريبي شغال مع Delta بنجاح 🚀", Duration=5})';
            const guestKey = "guest123";
            const resDiv = document.getElementById('guestResult');

            try {
                const res = await fetch('/api/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ script: guestScript, key: guestKey, obfuscate: "none" })
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
                        </div>
                    `;
                }
            } catch (err) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-2">حدث خطأ أثناء توليد التجربة!</div>';
            }
        }

        function loadTemplate(type) {
            const tabBtn = document.querySelector('#mainTab button[data-bs-target="#tab-create"]');
            const bsTab = new bootstrap.Tab(tabBtn);
            bsTab.show();

            if (type === 1) {
                document.getElementById('newScript').value = '-- Notification Script\\ngame:GetService("StarterGui"):SetCore("SendNotification", {\\n    Title = "أهلاً بك!";\\n    Text = "تم تشغيل السكربت بنجاح بواسطة منصة مهدي 🚀";\\n    Duration = 5;\\n})';
            } else if (type === 2) {
                document.getElementById('newScript').value = '-- Speed Boost\\nlocal player = game.Players.LocalPlayer\\nif player.Character and player.Character:FindFirstChild("Humanoid") then\\n    player.Character.Humanoid.WalkSpeed = 50\\n    print("Speed Set to 50")\\nend';
            }
            document.getElementById('newKey').value = '123456';
        }

        function testProtectionModal() {
            window.open('/raw/demo_test', '_blank');
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
        'key': key,
        'created_at': time.time()
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
        return jsonify({'success': False, 'error': 'مفتاح التعديل غير صحيح!'}), 403

    store[script_id]['script'] = new_script
    save_data(store)

    return jsonify({'success': True})

@app.route('/raw/<script_id>')
def get_raw_script(script_id):
    user_agent = request.headers.get('User-Agent', '').lower()
    
    browsers = ['mozilla', 'chrome', 'safari', 'edge', 'opera', 'firefox', 'msie']
    executors = ['roblox', 'delta', 'synapse', 'fluxus', 'krnl', 'hydrogen', 'electron', 'swagmode', 'solara']
    
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
