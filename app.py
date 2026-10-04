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
# 🛑 صفحة الحظر للمتصفح (سنقر لا تسرق)
# ==========================================================
WARNING_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سنقر لا تسرق! 🛡️</title>
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
            padding: 1.5rem;
            overflow: hidden;
        }
        .card-custom {
            background: rgba(17, 24, 39, 0.9);
            padding: 3rem 2rem;
            border-radius: 1.5rem;
            box-shadow: 0 0 50px rgba(239, 68, 68, 0.25);
            border: 1px solid rgba(239, 68, 68, 0.4);
            backdrop-filter: blur(16px);
            max-width: 680px;
            width: 100%;
            text-align: center;
        }
        .social-buttons { display: flex; justify-content: center; gap: 10px; margin-bottom: 2rem; flex-wrap: wrap; }
        .social-btn {
            display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px;
            border-radius: 50px; font-weight: 700; font-size: 0.88rem; color: #fff !important;
            text-decoration: none; transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        .btn-discord { background: linear-gradient(135deg, #5865F2, #4752C4); }
        .btn-youtube { background: linear-gradient(135deg, #FF0000, #CC0000); }
        .btn-tiktok { background: #000000; border: 1px solid #334155; }
        .btn-protect { background: linear-gradient(135deg, #2563eb, #1d4ed8); }
        .btn-android { background: linear-gradient(135deg, #3DDC84, #10b981); color: #000 !important; }
        .btn-ios { background: linear-gradient(135deg, #000000, #334155); border: 1px solid #475569; }
        .social-btn:hover { transform: translateY(-3px) scale(1.03); }
        .warning-icon { font-size: 4.5rem; color: #ef4444; margin-bottom: 1rem; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
        h1 { color: #ef4444; font-size: 2.4rem; font-weight: 900; }
        p { color: #9ca3af; font-size: 1.1rem; line-height: 1.7; }
    </style>
</head>
<body>
    <div class="card-custom">
        <div class="social-buttons">
            <a href="https://discord.gg/j8daZqG9V" target="_blank" class="social-btn btn-discord"><i class="fa-brands fa-discord"></i> Discord</a>
            <a href="https://youtube.com/@xoreyt0?si=swNpSO2vzquGFE4i" target="_blank" class="social-btn btn-youtube"><i class="fa-brands fa-youtube"></i> YouTube</a>
            <a href="https://www.tiktok.com/@lklkl7777" target="_blank" class="social-btn btn-tiktok"><i class="fa-brands fa-tiktok"></i> TikTok</a>
            <a href="https://lua-raw-xoremahdi-3mk.vercel.app/" target="_blank" class="social-btn btn-protect"><i class="fa-solid fa-shield-halved"></i> موقع الحماية</a>
            <a href="https://appwepsitemahdi.vercel.app/download?name=Delta+anroid&url=https%3A%2F%2Fdelta.filenetwork.vip%2Ffile%2FDelta-2.740.931.apk&icon=https%3A%2F%2Fcdn.discordapp.com%2Fattachments%2F1556178048284622978%2F1556199810103644250%2FIMG_9733.png%3Fbackend%3Db2%26ex%3D6ac34b83%26is%3D6ac1fa03%26hm%3D38f3ad341576a10dc842180678aa08ca97911c446b830e7ab16a2c3a4bde52a4%26&status=safe&timer=5" target="_blank" class="social-btn btn-android"><i class="fa-brands fa-android"></i> Delta Android</a>
            <a href="https://appwepsitemahdi.vercel.app/download?name=Delta+ios+&url=itms-services%3A%2F%2F%3Faction%3Ddownload-manifest%26url%3Dhttps%3A%2F%2Fdelta.bz%2Fmanifest.plist&icon=https%3A%2F%2Fcdn.discordapp.com%2Fattachments%2F1556178048284622978%2F1556199810103644250%2FIMG_9733.png%3Fbackend%3Db2%26ex%3D6ac34b83%26is%3D6ac1fa03%26hm%3D38f3ad341576a10dc842180678aa08ca97911c446b830e7ab16a2c3a4bde52a4%26&status=safe&timer=5" target="_blank" class="social-btn btn-ios"><i class="fa-brands fa-apple"></i> Delta iOS</a>
        </div>
        <div class="warning-icon"><i class="fa-solid fa-user-shield"></i></div>
        <h1>سنقر لا تسرق!</h1>
        <p>هذا الرابط محمي بواسطة منصة <b>مهدي</b>. مخصص للتنفيد المباشر داخل المشغلات المعتمدة (Delta, Solara, etc) ولا يمكنك عرض السورس كود من المتصفح.</p>
    </div>
</body>
</html>
'''

# ==========================================================
# 🚀 الواجهة الرئيسية المتطورة والمزينة بالكامل
# ==========================================================
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MAHDI V2 - منصة استضافة وحماية السكربتات العالمية</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        :root {
            --bg-dark: #030712;
            --card-bg: rgba(17, 24, 39, 0.8);
            --primary-glow: #3b82f6;
            --purple-glow: #8b5cf6;
            --accent-cyan: #06b6d4;
        }
        body {
            background-color: var(--bg-dark);
            color: #f3f4f6;
            font-family: system-ui, -apple-system, sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }
        #bgCanvas {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: -1; pointer-events: none;
        }
        .cyber-card {
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 1.5rem;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(20px);
            transition: all 0.3s ease;
        }
        .cyber-card:hover { border-color: rgba(59, 130, 246, 0.4); }
        .stat-card {
            background: rgba(31, 41, 55, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 1rem;
            padding: 1.2rem;
            text-align: center;
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-5px); border-color: var(--primary-glow); }
        .nav-pills .nav-link {
            color: #9ca3af;
            font-weight: 700;
            border-radius: 0.85rem;
            padding: 0.8rem 1.4rem;
            transition: all 0.3s ease;
        }
        .nav-pills .nav-link.active {
            background: linear-gradient(135deg, var(--primary-glow), var(--purple-glow));
            color: #fff;
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.5);
        }
        .form-control, .form-select {
            background-color: rgba(3, 7, 18, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            color: #ffffff !important;
            font-family: monospace;
            border-radius: 0.85rem;
        }
        .form-control:focus, .form-select:focus {
            border-color: var(--primary-glow) !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
        }
        .social-buttons { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
        .social-btn {
            display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px;
            border-radius: 50px; font-weight: 700; font-size: 0.88rem; color: #fff !important;
            text-decoration: none; transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        .btn-discord { background: #5865F2; }
        .btn-youtube { background: #FF0000; }
        .btn-tiktok { background: #000000; border: 1px solid #334155; }
        .btn-android { background: linear-gradient(135deg, #3DDC84, #10b981); color: #000 !important; }
        .btn-ios { background: linear-gradient(135deg, #000000, #334155); border: 1px solid #475569; }
        .social-btn:hover { transform: translateY(-3px) scale(1.03); }
        .result-box {
            background-color: rgba(3, 7, 18, 0.95);
            border: 1px solid var(--primary-glow);
            border-radius: 1rem; padding: 1.5rem; margin-top: 1.2rem;
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.2);
        }
        code { color: #38bdf8; word-break: break-all; }
        
        /* Toast Notifications */
        .toast-container { position: fixed; bottom: 25px; left: 25px; z-index: 9999; }
        .custom-toast {
            background: rgba(17, 24, 39, 0.95);
            border: 1px solid var(--primary-glow);
            color: #fff; padding: 14px 22px; border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6); display: flex;
            align-items: center; gap: 12px; backdrop-filter: blur(12px);
            animation: slideIn 0.3s ease forwards;
        }
        @keyframes slideIn { from { transform: translateX(-100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    </style>
</head>
<body class="py-4">

    <!-- Interactive Canvas Particles Background -->
    <canvas id="bgCanvas"></canvas>

    <div class="container" style="max-width: 1000px;">
        
        <!-- Main Header -->
        <div class="text-center mb-4">
            <div class="d-inline-block px-3 py-1 rounded-pill bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 mb-2 fw-bold">
                <i class="fa-solid fa-sparkles me-1"></i> الإصدار الاحترافي 2.0 MAHDI PLATFORM
            </div>
            <h1 class="fw-black display-5 text-white mb-2"><i class="fa-solid fa-shield-halved text-primary"></i> منصة مهدي الاستثنائية</h1>
            <p class="text-secondary fs-5 mb-4">استضافة متطورة، حماية مضادة للسرقة، وأدوات برمجة متكاملة لجميع المشغلات</p>
            
            <!-- Social Buttons -->
            <div class="social-buttons mb-4">
                <a href="https://discord.gg/j8daZqG9V" target="_blank" class="social-btn btn-discord"><i class="fa-brands fa-discord fs-5"></i> Discord</a>
                <a href="https://youtube.com/@xoreyt0?si=swNpSO2vzquGFE4i" target="_blank" class="social-btn btn-youtube"><i class="fa-brands fa-youtube fs-5"></i> YouTube</a>
                <a href="https://www.tiktok.com/@lklkl7777" target="_blank" class="social-btn btn-tiktok"><i class="fa-brands fa-tiktok fs-5"></i> TikTok</a>
                <a href="https://appwepsitemahdi.vercel.app/download?name=Delta+anroid&url=https%3A%2F%2Fdelta.filenetwork.vip%2Ffile%2FDelta-2.740.931.apk&icon=https%3A%2F%2Fcdn.discordapp.com%2Fattachments%2F1556178048284622978%2F1556199810103644250%2FIMG_9733.png%3Fbackend%3Db2%26ex%3D6ac34b83%26is%3D6ac1fa03%26hm%3D38f3ad341576a10dc842180678aa08ca97911c446b830e7ab16a2c3a4bde52a4%26&status=safe&timer=5" target="_blank" class="social-btn btn-android"><i class="fa-brands fa-android fs-5"></i> Delta Android</a>
                <a href="https://appwepsitemahdi.vercel.app/download?name=Delta+ios+&url=itms-services%3A%2F%2F%3Faction%3Ddownload-manifest%26url%3Dhttps%3A%2F%2Fdelta.bz%2Fmanifest.plist&icon=https%3A%2F%2Fcdn.discordapp.com%2Fattachments%2F1556178048284622978%2F1556199810103644250%2FIMG_9733.png%3Fbackend%3Db2%26ex%3D6ac34b83%26is%3D6ac1fa03%26hm%3D38f3ad341576a10dc842180678aa08ca97911c446b830e7ab16a2c3a4bde52a4%26&status=safe&timer=5" target="_blank" class="social-btn btn-ios"><i class="fa-brands fa-apple fs-5"></i> Delta iOS</a>
            </div>

            <!-- Dashboard Analytics Bar -->
            <div class="row g-3 mb-4">
                <div class="col-md-3 col-6">
                    <div class="stat-card">
                        <i class="fa-solid fa-server text-primary fs-3 mb-2"></i>
                        <h6 class="text-secondary small mb-1">حالة السيرفر</h6>
                        <span class="badge bg-success">Online 100%</span>
                    </div>
                </div>
                <div class="col-md-3 col-6">
                    <div class="stat-card">
                        <i class="fa-solid fa-shield-cat text-info fs-3 mb-2"></i>
                        <h6 class="text-secondary small mb-1">نظام الحماية</h6>
                        <span class="badge bg-info">Anti-Browser</span>
                    </div>
                </div>
                <div class="col-md-3 col-6">
                    <div class="stat-card">
                        <i class="fa-solid fa-bolt text-warning fs-3 mb-2"></i>
                        <h6 class="text-secondary small mb-1">سرعة الاستجابة</h6>
                        <span class="badge bg-warning text-dark">< 30ms</span>
                    </div>
                </div>
                <div class="col-md-3 col-6">
                    <div class="stat-card">
                        <i class="fa-solid fa-code-commit text-purple fs-3 mb-2" style="color: #8b5cf6;"></i>
                        <h6 class="text-secondary small mb-1">المشغلات المعتمدة</h6>
                        <span class="badge bg-primary">All Executors</span>
                    </div>
                </div>
            </div>

            <!-- Navigation Bar -->
            <ul class="nav nav-pills nav-justified bg-dark p-2 border border-secondary rounded-4 mb-4" id="mainTab">
                <li class="nav-item">
                    <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tab-create"><i class="fa-solid fa-plus-circle me-1"></i> إنشاء رابط</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-builder"><i class="fa-solid fa-wand-magic-sparkles me-1"></i> صانع الأكواد</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-guest"><i class="fa-solid fa-user-astronaut me-1"></i> ميزات الضيف</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-edit"><i class="fa-solid fa-pen-to-square me-1"></i> تعديل سكربت</button>
                </li>
            </ul>
        </div>

        <div class="tab-content">
            
            <!-- TAB 1: CREATE SCRIPT -->
            <div class="tab-pane fade show active" id="tab-create">
                <div class="cyber-card p-4">
                    <h4 class="text-white mb-3 d-flex align-items-center"><i class="fa-solid fa-lock text-primary me-2"></i> استضافة وحماية كود Lua جديد</h4>
                    
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <label class="mb-0 fw-bold">كود اللوا الأصلي (Lua Script):</label>
                            <div>
                                <button class="btn btn-sm btn-outline-info me-1" onclick="formatLuaCode()"><i class="fa-solid fa-align-left me-1"></i>تنسيق الكود</button>
                                <button class="btn btn-sm btn-outline-secondary" onclick="clearText('newScript')"><i class="fa-solid fa-trash me-1"></i>مسح</button>
                            </div>
                        </div>
                        <textarea id="newScript" class="form-control" rows="9" placeholder='print("Hello Mahdi Platform!")'></textarea>
                    </div>

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="fw-bold">اسم السكربت (Script Title - اختياري):</label>
                            <input type="text" id="scriptTitle" class="form-control" placeholder="مثال: Mahdi Hub V1">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="fw-bold">مفتاح التعديل (Key / Password):</label>
                            <input type="text" id="newKey" class="form-control" placeholder="أدخل كلمة سر لتعديل السكربت لاحقاً">
                        </div>
                    </div>

                    <button onclick="createScript()" class="btn btn-primary btn-lg w-100 mt-2 fw-bold"><i class="fa-solid fa-shield-cat me-2"></i> توليد الـ Loadstring المحمي المباشر</button>
                    <div id="createResult"></div>
                </div>
            </div>

            <!-- TAB 2: SCRIPT BUILDER -->
            <div class="tab-pane fade" id="tab-builder">
                <div class="cyber-card p-4">
                    <h4 class="text-white mb-2"><i class="fa-solid fa-wand-magic-sparkles text-warning me-2"></i> صانع السكربتات السريع (No-Code Builder)</h4>
                    <p class="text-secondary mb-4">اختر المزايا التي تريدها وسيقوم الموقع بتوليد كود لوا كامل وجاهز للاستضافة بنقرة زر واحدة:</p>

                    <div class="row g-3 mb-3">
                        <div class="col-md-6">
                            <div class="form-check form-switch p-3 border border-secondary rounded-3 bg-dark">
                                <input class="form-check-input float-end" type="checkbox" id="featSpeed">
                                <label class="form-check-label text-white ms-3 fw-bold" for="featSpeed">تفعيل السرعة الخارقة (Speed Boost - 100)</label>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-check form-switch p-3 border border-secondary rounded-3 bg-dark">
                                <input class="form-check-input float-end" type="checkbox" id="featJump">
                                <label class="form-check-label text-white ms-3 fw-bold" for="featJump">تفعيل القفز العالي (High Jump - 120)</label>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-check form-switch p-3 border border-secondary rounded-3 bg-dark">
                                <input class="form-check-input float-end" type="checkbox" id="featNoclip">
                                <label class="form-check-label text-white ms-3 fw-bold" for="featNoclip">تفعيل الاختراق عبر الجدران (Noclip)</label>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-check form-switch p-3 border border-secondary rounded-3 bg-dark">
                                <input class="form-check-input float-end" type="checkbox" id="featNotify">
                                <label class="form-check-label text-white ms-3 fw-bold" for="featNotify">إضافة إشعار ترحيبي عند التشغيل</label>
                            </div>
                        </div>
                    </div>

                    <button onclick="buildCustomScript()" class="btn btn-warning btn-lg w-100 fw-bold"><i class="fa-solid fa-code me-2"></i> إنتاج السكربت ونقله للمستضيف</button>
                </div>
            </div>

            <!-- TAB 3: GUEST PERKS -->
            <div class="tab-pane fade" id="tab-guest">
                <div class="cyber-card p-4">
                    <h4 class="text-white mb-3"><i class="fa-solid fa-user-astronaut text-info me-2"></i> ميزات الضيف والسكربتات الجاهزة</h4>
                    <p class="text-secondary">يمكنك كزائر تجربة السيرفر واختبار سرعة الاستجابة أو استكشاف نموذج السكربتات بضغطة زر:</p>

                    <div class="row g-3">
                        <div class="col-md-6">
                            <div class="p-3 border border-secondary rounded-3 bg-dark h-100">
                                <h5><i class="fa-solid fa-bolt text-warning me-2"></i>توليد سكربت تجريبي تجريبي</h5>
                                <p class="small text-secondary">يتم إنشاء رابط Loadstring تجريبي فوري يحتوي على إشعارات واختبار سيرفر.</p>
                                <button onclick="generateGuestScript()" class="btn btn-info w-100 mt-2 fw-bold"><i class="fa-solid fa-play me-1"></i> تجربة فورية</button>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="p-3 border border-secondary rounded-3 bg-dark h-100">
                                <h5><i class="fa-solid fa-shield-virus text-danger me-2"></i>معاينة نظام الحظر (Anti-Browser)</h5>
                                <p class="small text-secondary">شاهد كيف يظهر الموقع صفحة (سنقر لا تسرق) عند محاولة فتح الرابط من المتصفح.</p>
                                <button onclick="testProtectionModal()" class="btn btn-outline-danger w-100 mt-2 fw-bold"><i class="fa-solid fa-eye me-1"></i> فتح صفحة الحماية</button>
                            </div>
                        </div>
                    </div>
                    <div id="guestResult"></div>
                </div>
            </div>

            <!-- TAB 4: EDIT SCRIPT -->
            <div class="tab-pane fade" id="tab-edit">
                <div class="cyber-card p-4">
                    <h4 class="text-white mb-3"><i class="fa-solid fa-pen-to-square text-warning me-2"></i> تعديل سكربت مستضاف</h4>
                    
                    <div class="mb-3">
                        <label class="fw-bold">معرف السكربت (Script ID):</label>
                        <input type="text" id="editId" class="form-control" placeholder="مثال: aBc123Xy">
                    </div>
                    <div class="mb-3">
                        <label class="fw-bold">مفتاح التعديل (Password/Key):</label>
                        <input type="password" id="editKey" class="form-control" placeholder="كلمة السر الخاصة بالسكربت">
                    </div>
                    <div class="mb-3">
                        <label class="fw-bold">الكود الجديد (New Lua Code):</label>
                        <textarea id="editScript" class="form-control" rows="8" placeholder="ضع الكود الجديد هنا"></textarea>
                    </div>
                    <button onclick="updateScript()" class="btn btn-warning btn-lg w-100 fw-bold"><i class="fa-solid fa-rotate me-2"></i> تحديث الكود فوراً</button>
                    <div id="updateResult"></div>
                </div>
            </div>

        </div>
    </div>

    <!-- Toast Notifications Box -->
    <div class="toast-container" id="toastBox"></div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Canvas Interactive Particles
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
                this.x += this.speedX; this.y += this.speedY;
                if (this.x > canvas.width) this.x = 0;
                if (this.x < 0) this.x = canvas.width;
                if (this.y > canvas.height) this.y = 0;
                if (this.y < 0) this.y = canvas.height;
            }
            draw() {
                ctx.fillStyle = 'rgba(59, 130, 246, 0.35)';
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        for (let i = 0; i < 60; i++) particles.push(new Particle());

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => { p.update(); p.draw(); });
            requestAnimationFrame(animate);
        }
        animate();

        // Toast Helper
        function showToast(msg) {
            const toastBox = document.getElementById('toastBox');
            const toast = document.createElement('div');
            toast.className = 'custom-toast';
            toast.innerHTML = `<i class="fa-solid fa-circle-check text-success fs-5"></i> <span>${msg}</span>`;
            toastBox.appendChild(toast);
            setTimeout(() => { toast.remove(); }, 3500);
        }

        function clearText(id) {
            document.getElementById(id).value = '';
            showToast("تم المسح!");
        }

        // Lua Code Formatter
        function formatLuaCode() {
            let code = document.getElementById('newScript').value;
            if (!code.trim()) return;
            let lines = code.split('\n').map(l => l.trim()).filter(l => l.length > 0);
            document.getElementById('newScript').value = lines.join('\n');
            showToast("تم تنظيف وتنسيق كود اللوا!");
        }

        // Auto Script Builder
        function buildCustomScript() {
            let scriptLines = ['-- Generated By Mahdi Hub Auto-Builder'];
            
            if (document.getElementById('featNotify').checked) {
                scriptLines.push('game:GetService("StarterGui"):SetCore("SendNotification", {Title="Mahdi Hub", Text="تم تفعيل السكربت بنجاح!", Duration=5})');
            }
            if (document.getElementById('featSpeed').checked) {
                scriptLines.push('game.Players.LocalPlayer.Character.Humanoid.WalkSpeed = 100');
            }
            if (document.getElementById('featJump').checked) {
                scriptLines.push('game.Players.LocalPlayer.Character.Humanoid.JumpPower = 120');
            }
            if (document.getElementById('featNoclip').checked) {
                scriptLines.push('game:GetService("RunService").Stepped:Connect(function()\n    for _, v in pairs(game.Players.LocalPlayer.Character:GetChildren()) do\n        if v:IsA("BasePart") then v.CanCollide = false end\n    end\nend)');
            }

            if (scriptLines.length === 1) {
                showToast("يرجى اختيار ميزة واحدة على الأقل!");
                return;
            }

            document.getElementById('newScript').value = scriptLines.join('\n\n');
            
            const tabBtn = document.querySelector('#mainTab button[data-bs-target="#tab-create"]');
            new bootstrap.Tab(tabBtn).show();
            showToast("تم إنشاء السكربت ونقله لصفحة الاستضافة!");
        }

        async function createScript() {
            const script = document.getElementById('newScript').value;
            const key = document.getElementById('newKey').value;
            const title = document.getElementById('scriptTitle').value || 'Mahdi Script';
            const resDiv = document.getElementById('createResult');

            if (!script || !key) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3">يرجى إدخال كود اللوا ومفتاح التعديل!</div>';
                return;
            }

            try {
                const res = await fetch('/api/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ script, key, title })
                });
                const data = await res.json();

                if (data.success) {
                    const loadstringCode = `loadstring(game:HttpGet("${data.raw_url}"))()`;
                    resDiv.innerHTML = `
                        <div class="result-box">
                            <h5 class="text-success mb-2"><i class="fa-solid fa-circle-check me-1"></i> تم إنشاء وحماية السكربت بنجاح!</h5>
                            <p class="mb-2"><b>Script ID:</b> <code>${data.id}</code></p>
                            <label class="d-block mb-1 fw-bold">كود الـ Loadstring المباشر:</label>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="loadstringInput" value='${loadstringCode}' readonly>
                                <button class="btn btn-outline-light" type="button" onclick="copyToClipboard('loadstringInput')"><i class="fa-regular fa-copy me-1"></i> نسخ الكود</button>
                            </div>
                        </div>
                    `;
                    showToast("تم توليد الـ Loadstring بنجاح!");
                } else {
                    resDiv.innerHTML = `<div class="alert alert-danger mt-3">${data.error}</div>`;
                }
            } catch (err) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3">حدث خطأ أثناء الاتصال بالخادم!</div>';
            }
        }

        async function generateGuestScript() {
            const guestScript = '-- Demo Script By Mahdi\\nprint("Hello Mahdi!")\\ngame:GetService("StarterGui"):SetCore("SendNotification", {Title="منصة مهدي", Text="السكربت التجريبي يعمل بنجاح 🚀", Duration=5})';
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
                            <h6 class="text-info mb-2"><i class="fa-solid fa-wand-magic-sparkles me-1"></i> تم توليد السكربت التجريبي!</h6>
                            <p class="mb-1 text-light small"><b>Script ID:</b> <code>${data.id}</code> | <b>كلمة السر:</b> <code>guest123</code></p>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="guestInput" value='${loadstringCode}' readonly>
                                <button class="btn btn-outline-light" type="button" onclick="copyToClipboard('guestInput')"><i class="fa-regular fa-copy me-1"></i> نسخ الرابط</button>
                            </div>
                        </div>
                    `;
                    showToast("تم التوليد بنجاح!");
                }
            } catch (err) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-2">حدث خطأ أثناء الاتصال!</div>';
            }
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
                resDiv.innerHTML = '<div class="alert alert-danger mt-3">يرجى ملء جميع الحقول المطلوبة!</div>';
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
                    resDiv.innerHTML = '<div class="alert alert-success mt-3"><i class="fa-solid fa-circle-check me-1"></i> تم تحديث السكربت بنجاح! سيعمل الكود الجديد فوراً دون الحاجة لتغيير الـ Loadstring.</div>';
                    showToast("تم التحديث بنجاح!");
                } else {
                    resDiv.innerHTML = `<div class="alert alert-danger mt-3">${data.error}</div>`;
                }
            } catch (err) {
                resDiv.innerHTML = '<div class="alert alert-danger mt-3">حدث خطأ أثناء التحديث!</div>';
            }
        }

        function copyToClipboard(id) {
            const input = document.getElementById(id);
            input.select();
            navigator.clipboard.writeText(input.value);
            showToast("تم النسخ إلى الحافظة!");
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
    title = data.get('title', 'Untitled Script')

    if not script or not key:
        return jsonify({'success': False, 'error': 'السكربت ومفتاح التعديل مطلوبان'}), 400

    script_id = generate_id()
    store = load_data()
    store[script_id] = {
        'script': script,
        'key': key,
        'title': title,
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
