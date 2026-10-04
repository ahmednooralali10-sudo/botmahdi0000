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
# 🛑 صفحة "سنقر لا تسرق" المخصصة للمتصفح
# ==========================================================
WARNING_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سنقر لا تسرق!</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        body {
            background: #030712;
            color: #ffffff;
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            text-align: center;
            padding: 1.5rem;
            overflow: hidden;
        }
        .card-custom {
            background: rgba(17, 24, 39, 0.85);
            padding: 3rem 2rem;
            border-radius: 1.5rem;
            box-shadow: 0 0 50px rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.4);
            backdrop-filter: blur(12px);
            max-width: 680px;
            width: 100%;
            position: relative;
            z-index: 10;
        }
        .social-buttons {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        .social-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 18px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 0.88rem;
            color: #fff !important;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        .btn-discord { background: linear-gradient(135deg, #5865F2, #4752C4); }
        .btn-youtube { background: linear-gradient(135deg, #FF0000, #CC0000); }
        .btn-tiktok { background: #000000; border: 1px solid #334155; }
        .btn-protect { background: linear-gradient(135deg, #2563eb, #1d4ed8); }
        .btn-android { background: linear-gradient(135deg, #3DDC84, #10b981); color: #000 !important; }
        .btn-ios { background: linear-gradient(135deg, #000000, #334155); border: 1px solid #475569; }
        
        .social-btn:hover {
            transform: translateY(-3px) scale(1.03);
            box-shadow: 0 8px 25px rgba(0,0,0,0.6);
        }
        .warning-icon {
            font-size: 4.5rem;
            color: #ef4444;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        h1 { color: #ef4444; font-size: 2.4rem; margin-bottom: 1rem; font-weight: 900; }
        p { color: #9ca3af; font-size: 1.1rem; line-height: 1.7; margin: 0; }
    </style>
</head>
<body>
    <div class="card-custom">
        <div class="social-buttons">
            <a href="https://discord.gg/j8daZqG9V" target="_blank" class="social-btn btn-discord">
                <i class="fa-brands fa-discord fs-5"></i> Discord
            </a>
            <a href="https://youtube.com/@xoreyt0?si=swNpSO2vzquGFE4i" target="_blank" class="social-btn btn-youtube">
                <i class="fa-brands fa-youtube fs-5"></i> YouTube
            </a>
            <a href="https://www.tiktok.com/@lklkl7777" target="_blank" class="social-btn btn-tiktok">
                <i class="fa-brands fa-tiktok fs-5"></i> TikTok
            </a>
            <a href="https://lua-raw-xoremahdi-3mk.vercel.app/" target="_blank" class="social-btn btn-protect">
                <i class="fa-solid fa-shield-halved fs-5"></i> موقع الحماية
            </a>
            <a href="https://appwepsitemahdi.vercel.app/download?name=Delta+anroid&url=https%3A%2F%2Fdelta.filenetwork.vip%2Ffile%2FDelta-2.740.931.apk&icon=https%3A%2F%2Fcdn.discordapp.com%2Fattachments%2F1556178048284622978%2F1556199810103644250%2FIMG_9733.png%3Fbackend%3Db2%26ex%3D6ac34b83%26is%3D6ac1fa03%26hm%3D38f3ad341576a10dc842180678aa08ca97911c446b830e7ab16a2c3a4bde52a4%26&status=safe&timer=5" target="_blank" class="social-btn btn-android">
                <i class="fa-brands fa-android fs-5"></i> Delta Android
            </a>
            <a href="https://appwepsitemahdi.vercel.app/download?name=Delta+ios+&url=itms-services%3A%2F%2F%3Faction%3Ddownload-manifest%26url%3Dhttps%3A%2F%2Fdelta.bz%2Fmanifest.plist&icon=https%3A%2F%2Fcdn.discordapp.com%2Fattachments%2F1556178048284622978%2F1556199810103644250%2FIMG_9733.png%3Fbackend%3Db2%26ex%3D6ac34b83%26is%3D6ac1fa03%26hm%3D38f3ad341576a10dc842180678aa08ca97911c446b830e7ab16a2c3a4bde52a4%26&status=safe&timer=5" target="_blank" class="social-btn btn-ios">
                <i class="fa-brands fa-apple fs-5"></i> Delta iOS
            </a>
        </div>

        <div class="warning-icon">
            <i class="fa-solid fa-user-slash"></i>
        </div>

        <h1>سنقر لا تسرق!</h1>
        <p>عذراً، هذا الرابط محمي بواسطة منصة مهدي. مخصص لتشغيله داخل اللعبة عبر المشغلات المعتمدة ولا يمكنك عرض الكود المصدر من المتصفح.</p>
    </div>
</body>
</html>
'''

# ==========================================================
# 🛡️ الواجهة الرئيسية التفاعلية والمزينة بالكامل
# ==========================================================
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة مهدي - استضافة وحماية أكواد Lua</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        :root {
            --bg-main: #030712;
            --card-bg: rgba(17, 24, 39, 0.75);
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
        }
        body { 
            background-color: var(--bg-main); 
            color: #f3f4f6; 
            font-family: system-ui, -apple-system, sans-serif; 
            position: relative;
            min-height: 100vh;
            overflow-x: hidden;
        }
        #bgCanvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
        }
        .card { 
            background: var(--card-bg); 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            border-radius: 1.25rem; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            backdrop-filter: blur(16px);
        }
        .stat-card {
            background: rgba(31, 41, 55, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 1rem;
            padding: 1rem;
            text-align: center;
            transition: transform 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .nav-pills .nav-link {
            color: #9ca3af;
            font-weight: 700;
            border-radius: 0.75rem;
            padding: 0.75rem 1.25rem;
            transition: all 0.3s ease;
        }
        .nav-pills .nav-link.active {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: #fff;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        }
        label { color: #e5e7eb !important; font-weight: 600; margin-bottom: 0.5rem; }
        .form-control, .form-select { 
            background-color: rgba(3, 7, 18, 0.8) !important; 
            border: 1px solid rgba(255, 255, 255, 0.15) !important; 
            color: #ffffff !important; 
            font-family: monospace;
            border-radius: 0.75rem;
        }
        .form-control:focus, .form-select:focus { 
            border-color: var(--accent-blue) !important; 
            box-shadow: 0 0 0 0.25rem rgba(59, 130, 246, 0.25) !important; 
        }
        .social-buttons { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
        .social-btn {
            display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px;
            border-radius: 50px; font-weight: 700; font-size: 0.88rem; color: #fff !important;
            text-decoration: none; transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .btn-discord { background: #5865F2; }
        .btn-youtube { background: #FF0000; }
        .btn-tiktok { background: #000000; border: 1px solid #334155; }
        .btn-android { background: linear-gradient(135deg, #3DDC84, #10b981); color: #000 !important; }
        .btn-ios { background: linear-gradient(135deg, #000000, #334155); border: 1px solid #475569; }
        
        .social-btn:hover { transform: translateY(-3px); opacity: 0.95; }
        .result-box {
            background-color: rgba(3, 7, 18, 0.9); border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 0.75rem; padding: 1.25rem; margin-top: 1rem;
        }
        code { color: #38bdf8; word-break: break-all; }
        .badge-guest { background: #0284c7; color: #fff; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; }
        
        /* Toast Notification Styling */
        .toast-container {
            position: fixed;
            bottom: 20px;
            left: 20px;
            z-index: 9999;
        }
        .custom-toast {
            background: rgba(17, 24, 39, 0.95);
            border: 1px solid var(--accent-blue);
            color: #fff;
            padding: 12px 20px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            gap: 10px;
            backdrop-filter: blur(8px);
        }
    </style>
</head>
<body class="py-4">

    <!-- Canvas Background for Particles Effect -->
    <canvas id="bgCanvas"></canvas>

    <div class="container" style="max-width: 950px;">
        
        <!-- Header Section -->
        <div class="text-center mb-4">
            <h1 class="fw-bold text-primary mb-2"><i class="fa-solid fa-shield-halved"></i> منصة مهدي لاستضافة وحماية السكربتات</h1>
            <p class="text-secondary fs-5 mb-3">حماية متطورة ودعم كامل لجميع المشغلات (Delta, Solara, Hydrogen)</p>
            
            <div class="social-buttons mb-4">
                <a href="https://discord.gg/j8daZqG9V" target="_blank" class="social-btn btn-discord">
                    <i class="fa-brands fa-discord fs-5"></i> Discord
                </a>
                <a href="https://youtube.com/@xoreyt0?si=swNpSO2vzquGFE4i" target="_blank" class="social-btn btn-youtube">
                    <i class="fa-brands fa-youtube fs-5"></i> YouTube
                </a>
                <a href="https://www.tiktok.com/@lklkl7777" target="_blank" class="social-btn btn-tiktok">
                    <i class="fa-brands fa-tiktok fs-5"></i> TikTok
                </a>
                <a href="https://appwepsitemahdi.vercel.app/download?name=Delta+anroid&url=https%3A%2F%2Fdelta.filenetwork.vip%2Ffile%2FDelta-2.740.931.apk&icon=https%3A%2F%2Fcdn.discordapp.com%2Fattachments%2F1556178048284622978%2F1556199810103644250%2FIMG_9733.png%3Fbackend%3Db2%26ex%3D6ac34b83%26is%3D6ac1fa03%26hm%3D38f3ad341576a10dc842180678aa08ca97911c446b830e7ab16a2c3a4bde52a4%26&status=safe&timer=5" target="_blank" class="social-btn btn-android">
                    <i class="fa-brands fa-android fs-5"></i> Delta Android
                </a>
                <a href="https://appwepsitemahdi.vercel.app/download?name=Delta+ios+&url=itms-services%3A%2F%2F%3Faction%3Ddownload-manifest%26url%3Dhttps%3A%2F%2Fdelta.bz%2Fmanifest.plist&icon=https%3A%2F%2Fcdn.discordapp.com%2Fattachments%2F1556178048284622978%2F1556199810103644250%2FIMG_9733.png%3Fbackend%3Db2%26ex%3D6ac34b83%26is%3D6ac1fa03%26hm%3D38f3ad341576a10dc842180678aa08ca97911c446b830e7ab16a2c3a4bde52a4%26&status=safe&timer=5" target="_blank" class="social-btn btn-ios">
                    <i class="fa-brands fa-apple fs-5"></i> Delta iOS
                </a>
            </div>

            <!-- Statistics Dashboard Bar -->
            <div class="row g-3 mb-4">
                <div class="col-md-4">
                    <div class="stat-card">
                        <i class="fa-solid fa-server text-primary fs-4 mb-2"></i>
                        <h6 class="text-secondary mb-1">حالة السيرفر</h6>
                        <span class="badge bg-success">متصل (Online 99.9%)</span>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="stat-card">
                        <i class="fa-solid fa-shield-virus text-info fs-4 mb-2"></i>
                        <h6 class="text-secondary mb-1">نظام الحماية</h6>
                        <span class="badge bg-info">Anti-Browser Active</span>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="stat-card">
                        <i class="fa-solid fa-bolt text-warning fs-4 mb-2"></i>
                        <h6 class="text-secondary mb-1">سرعة الاستجابة</h6>
                        <span class="badge bg-warning text-dark">< 50ms Ultra Fast</span>
                    </div>
                </div>
            </div>

            <!-- Navigation Tabs -->
            <ul class="nav nav-pills nav-justified bg-dark p-2 border border-secondary rounded-4 mb-4" id="mainTab">
                <li class="nav-item">
                    <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tab-create"><i class="fa-solid fa-plus-circle me-1"></i> إنشاء رابط</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-guest"><i class="fa-solid fa-user-astronaut me-1"></i> ميزات الضيف</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-templates"><i class="fa-solid fa-code me-1"></i> أكواد جاهزة</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-edit"><i class="fa-solid fa-pen-to-square me-1"></i> تعديل سكربت</button>
                </li>
            </ul>
        </div>

        <div class="tab-content">
            <!-- TAB 1: CREATE SCRIPT -->
            <div class="tab-pane fade show active" id="tab-create">
                <div class="card p-4">
                    <h4 class="text-white mb-3"><i class="fa-solid fa-lock text-primary me-2"></i>إنشاء رابط Loadstring محمي</h4>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <label class="mb-0">كود اللوا الأصلي (Lua Script):</label>
                            <button class="btn btn-sm btn-outline-secondary" onclick="clearText('newScript')"><i class="fa-solid fa-trash me-1"></i>مسح الكود</button>
                        </div>
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
                    <button onclick="createScript()" class="btn btn-primary btn-lg w-100 mt-2"><i class="fa-solid fa-shield-cat me-2"></i>توليد الـ Loadstring المحمي</button>
                    <div id="createResult"></div>
                </div>
            </div>

            <!-- TAB 2: GUEST FEATURES -->
            <div class="tab-pane fade" id="tab-guest">
                <div class="card p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="text-white mb-0"><i class="fa-solid fa-gift text-info me-2"></i>خدمات ومميزات الضيف</h4>
                        <span class="badge-guest">Guest Perks</span>
                    </div>
                    <p class="text-light">يمكنك كزائر تجربة السيرفر واختبار استجابته وقوة حمايته دون الحاجة لتسجيل أو إدخال كود خاص بك!</p>
                    
                    <div class="row g-3">
                        <div class="col-md-6">
                            <div class="p-3 border border-secondary rounded-3 bg-dark">
                                <h5><i class="fa-solid fa-bolt text-warning me-2"></i>تجربة سريعة بضغطة زر</h5>
                                <p class="small text-secondary">يتم توليد سكربت لوا تجريبي يحتوي على إشعارات وشاشة نوتيفيكيشن فورية.</p>
                                <button onclick="generateGuestScript()" class="btn btn-info w-100"><i class="fa-solid fa-play me-1"></i> توليد سكربت تجريبي</button>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="p-3 border border-secondary rounded-3 bg-dark">
                                <h5><i class="fa-solid fa-magnifying-glass text-info me-2"></i>محاكي فحص الحماية</h5>
                                <p class="small text-secondary">جرب فتح رابط تجريبي كمتصفح لتشاهد رسالة (سنقر لا تسرق) مباشرة.</p>
                                <button onclick="testProtectionModal()" class="btn btn-outline-danger w-100"><i class="fa-solid fa-eye me-1"></i> معاينة صفحة الحظر</button>
                            </div>
                        </div>
                    </div>
                    <div id="guestResult"></div>
                </div>
            </div>

            <!-- TAB 3: TEMPLATES -->
            <div class="tab-pane fade" id="tab-templates">
                <div class="card p-4">
                    <h4 class="text-white mb-3"><i class="fa-solid fa-layer-group text-warning me-2"></i>أكواد وسكربتات لوا جاهزة</h4>
                    <p class="text-secondary mb-3">اختر أحد الأكواد الجاهزة أدناه واستضفه مباشرة بضغطة زر:</p>
                    
                    <div class="list-group">
                        <button onclick="loadTemplate(1)" class="list-group-item list-group-item-action bg-dark text-white border-secondary mb-2 rounded">
                            <div class="d-flex w-100 justify-content-between">
                                <h5 class="mb-1 text-primary"><i class="fa-solid fa-bell me-2"></i>1. Notification GUI Script</h5>
                                <small class="text-muted">Lua UI</small>
                            </div>
                            <p class="mb-1 small text-secondary">سكربت يعرض إشعار ترحيبي مع صوت هادئ داخل رابلوكس.</p>
                        </button>
                        
                        <button onclick="loadTemplate(2)" class="list-group-item list-group-item-action bg-dark text-white border-secondary mb-2 rounded">
                            <div class="d-flex w-100 justify-content-between">
                                <h5 class="mb-1 text-success"><i class="fa-solid fa-gauge-high me-2"></i>2. Speed & Jump Power GUI</h5>
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
                    <h4 class="text-white mb-3"><i class="fa-solid fa-pen-to-square text-warning me-2"></i>تعديل سكربت موجود</h4>
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
                    <button onclick="updateScript()" class="btn btn-warning btn-lg w-100"><i class="fa-solid fa-rotate me-2"></i>تحديث الكود فوراً</button>
                    <div id="updateResult"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Container for Toast Messages -->
    <div class="toast-container" id="toastBox"></div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Particles Background Animation Effect
        const canvas = document.getElementById('bgCanvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 1;
                this.speedX = Math.random() * 1 - 0.5;
                this.speedY = Math.random() * 1 - 0.5;
            }
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                if (this.x > canvas.width) this.x = 0;
                if (this.x < 0) this.x = canvas.width;
                if (this.y > canvas.height) this.y = 0;
                if (this.y < 0) this.y = canvas.height;
            }
            draw() {
                ctx.fillStyle = 'rgba(59, 130, 246, 0.4)';
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        for (let i = 0; i < 50; i++) particles.push(new Particle());

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {
                p.update();
                p.draw();
            });
            requestAnimationFrame(animateParticles);
        }
        animateParticles();

        // Toast Notification Helper
        function showToast(message) {
            const toastBox = document.getElementById('toastBox');
            const toast = document.createElement('div');
            toast.className = 'custom-toast';
            toast.innerHTML = `<i class="fa-solid fa-circle-check text-success"></i> <span>${message}</span>`;
            toastBox.appendChild(toast);
            setTimeout(() => { toast.remove(); }, 3500);
        }

        function clearText(elementId) {
            document.getElementById(elementId).value = '';
            showToast("تم مسح الكود!");
        }

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
                            <h5 class="text-success mb-2"><i class="fa-solid fa-circle-check me-1"></i> تم الإنشاء والحماية بنجاح!</h5>
                            <p class="mb-2"><b>Script ID:</b> <code>${data.id}</code></p>
                            <label class="d-block mb-1">كود الـ Loadstring المباشر:</label>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="loadstringInput" value='${loadstringCode}' readonly>
                                <button class="btn btn-outline-light" type="button" onclick="copyToClipboard('loadstringInput')"><i class="fa-regular fa-copy me-1"></i> نسخ الكود</button>
                            </div>
                        </div>
                    `;
                    showToast("تم إنشاء الرابط بنجاح!");
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
                            <h6 class="text-info mb-2"><i class="fa-solid fa-wand-magic-sparkles me-1"></i> تم توليد السكربت التجريبي للضيف بنجاح!</h6>
                            <p class="mb-1 text-light small"><b>Script ID:</b> <code>${data.id}</code> | <b>مفتاح التعديل:</b> <code>guest123</code></p>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="guestInput" value='${loadstringCode}' readonly>
                                <button class="btn btn-outline-light" type="button" onclick="copyToClipboard('guestInput')"><i class="fa-regular fa-copy me-1"></i> نسخ الـ Loadstring</button>
                            </div>
                        </div>
                    `;
                    showToast("تم توليد السكربت التجريبي للضيف!");
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
                document.getElementById('newScript').value = '-- Notification Script\\ngame:GetService("StarterGui"):SetCore("SendNotification", {\\n    Title = "أهلاً بك!";\\n    Text = "تم تشغيل السكربت بنجاح بواسطة منصة مهدي";\\n    Duration = 5;\\n})';
            } else if (type === 2) {
                document.getElementById('newScript').value = '-- Speed Boost\\nlocal player = game.Players.LocalPlayer\\nif player.Character and player.Character:FindFirstChild("Humanoid") then\\n    player.Character.Humanoid.WalkSpeed = 50\\n    print("Speed Set to 50")\\nend';
            }
            document.getElementById('newKey').value = '123456';
            showToast("تم تحميل النموذج الجاهز!");
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
                    resDiv.innerHTML = '<div class="alert alert-success mt-3"><i class="fa-solid fa-circle-check me-1"></i> تم تحديث السكربت بنجاح! سيعمل الكود الجديد فوراً بدون تغيير الرابط.</div>';
                    showToast("تم التحديث بنجاح!");
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
            showToast("تم نسخ الكود بنجاح!");
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
