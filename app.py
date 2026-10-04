import os
import json
import secrets
import string
import time
from flask import Flask, request, jsonify, Response, render_template_string

app = Flask(__name__)

# =========================================================
# SETTINGS
# =========================================================

DATA_FILE = "/tmp/scripts_store.json"

MAX_SCRIPT_SIZE = 500_000
MAX_TITLE_SIZE = 80
MAX_KEY_SIZE = 150


# =========================================================
# DATABASE
# =========================================================

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )
        return True
    except Exception:
        return False


def generate_id(length=10):
    alphabet = string.ascii_letters + string.digits
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


def now():
    return int(time.time())


def safe_text(value, maximum):
    if value is None:
        return ""

    value = str(value).strip()

    return value[:maximum]


# =========================================================
# WARNING PAGE
# =========================================================

WARNING_HTML = r'''
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>MAHDI SECURITY</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect"
      href="https://fonts.gstatic.com"
      crossorigin>

<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap"
      rel="stylesheet">

<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<style>

*{
    box-sizing:border-box;
}

html,body{
    margin:0;
    min-height:100%;
}

body{
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:22px;

    font-family:Cairo,system-ui,sans-serif;

    color:white;

    background:
        radial-gradient(circle at 20% 20%,rgba(239,68,68,.18),transparent 35%),
        radial-gradient(circle at 80% 80%,rgba(139,92,246,.15),transparent 35%),
        #020617;
}

.card{

    width:min(680px,100%);

    padding:32px 24px;

    text-align:center;

    border:1px solid rgba(255,255,255,.10);

    border-radius:28px;

    background:
        linear-gradient(
            145deg,
            rgba(15,23,42,.95),
            rgba(2,6,23,.92)
        );

    box-shadow:
        0 30px 100px rgba(0,0,0,.65),
        0 0 60px rgba(239,68,68,.12);

    backdrop-filter:blur(25px);

    animation:appear .5s ease;
}

@keyframes appear{
    from{
        opacity:0;
        transform:translateY(20px) scale(.97);
    }
    to{
        opacity:1;
        transform:none;
    }
}

.icon{

    width:105px;
    height:105px;

    margin:0 auto 20px;

    display:flex;
    align-items:center;
    justify-content:center;

    border-radius:50%;

    font-size:45px;

    color:#ef4444;

    background:rgba(239,68,68,.10);

    border:1px solid rgba(239,68,68,.25);

    box-shadow:
        0 0 50px rgba(239,68,68,.20);

    animation:pulse 2s infinite;
}

@keyframes pulse{
    50%{
        transform:scale(1.05);
    }
}

h1{
    margin:0 0 10px;

    font-size:clamp(28px,6vw,46px);

    font-weight:900;
}

h1 span{
    color:#ef4444;
}

p{
    color:#94a3b8;
    line-height:1.9;
    margin:0 auto 25px;
}

.badge{

    display:inline-flex;

    align-items:center;

    gap:8px;

    padding:9px 14px;

    border-radius:999px;

    color:#fca5a5;

    background:rgba(239,68,68,.08);

    border:1px solid rgba(239,68,68,.18);

    font-size:13px;

    font-weight:800;

    margin-bottom:20px;
}

.links{

    display:flex;

    justify-content:center;

    flex-wrap:wrap;

    gap:10px;
}

.links a{

    text-decoration:none;

    color:white;

    padding:10px 16px;

    border-radius:14px;

    background:rgba(255,255,255,.06);

    border:1px solid rgba(255,255,255,.08);

    transition:.2s;

    font-size:13px;

    font-weight:800;
}

.links a:hover{
    transform:translateY(-3px);
    background:rgba(255,255,255,.10);
}

.footer{
    margin-top:25px;
    color:#475569;
    font-size:12px;
}

</style>
</head>

<body>

<div class="card">

    <div class="icon">
        <i class="fa-solid fa-user-shield"></i>
    </div>

    <div class="badge">
        <i class="fa-solid fa-shield-halved"></i>
        MAHDI SECURITY
    </div>

    <h1>
        سنقر <span>لا تسرق!</span>
    </h1>

    <p>
        هذا الرابط مخصص للتنفيذ المباشر.
        لا يمكن عرض محتوى السكربت من المتصفح.
        استخدم الرابط من البيئة المدعومة.
    </p>

    <div class="links">

        <a href="https://discord.gg/j8daZqG9V"
           target="_blank">
            <i class="fa-brands fa-discord"></i>
            Discord
        </a>

        <a href="https://youtube.com/@xoreyt0"
           target="_blank">
            <i class="fa-brands fa-youtube"></i>
            YouTube
        </a>

        <a href="https://www.tiktok.com/@lklkl7777"
           target="_blank">
            <i class="fa-brands fa-tiktok"></i>
            TikTok
        </a>

    </div>

    <div class="footer">
        MAHDI PLATFORM • Protected Script
    </div>

</div>

</body>
</html>
'''


# =========================================================
# MAIN WEBSITE
# =========================================================

INDEX_HTML = r'''
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,initial-scale=1.0">

<title>MAHDI PLATFORM V3</title>

<link rel="preconnect"
      href="https://fonts.googleapis.com">

<link rel="preconnect"
      href="https://fonts.gstatic.com"
      crossorigin>

<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap"
      rel="stylesheet">

<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<style>

:root{

    --bg:#020617;

    --panel:rgba(15,23,42,.72);

    --panel2:rgba(15,23,42,.48);

    --border:rgba(255,255,255,.09);

    --text:#f8fafc;

    --muted:#94a3b8;

    --blue:#3b82f6;

    --purple:#8b5cf6;

    --cyan:#06b6d4;

    --green:#22c55e;

    --red:#ef4444;

    --orange:#f59e0b;

}

*{
    box-sizing:border-box;
}

html{
    scroll-behavior:smooth;
}

body{

    margin:0;

    min-height:100vh;

    color:var(--text);

    font-family:Cairo,system-ui,sans-serif;

    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(59,130,246,.14),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(139,92,246,.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(6,182,212,.08),
            transparent 35%
        ),
        var(--bg);

    overflow-x:hidden;
}

#particles{

    position:fixed;

    inset:0;

    z-index:-1;

    pointer-events:none;
}

.container-main{

    width:min(1100px,calc(100% - 24px));

    margin:auto;

    padding:22px 0 50px;
}


/* HEADER */

.header{

    text-align:center;

    padding:25px 10px 20px;
}

.brand{

    display:inline-flex;

    align-items:center;

    gap:8px;

    padding:8px 14px;

    border-radius:999px;

    color:#bfdbfe;

    background:rgba(59,130,246,.08);

    border:1px solid rgba(59,130,246,.18);

    font-size:12px;

    font-weight:900;
}

.header h1{

    margin:15px 0 5px;

    font-size:clamp(30px,6vw,52px);

    font-weight:900;

    letter-spacing:-1px;
}

.header h1 span{

    background:
        linear-gradient(
            90deg,
            var(--blue),
            var(--purple),
            var(--cyan)
        );

    -webkit-background-clip:text;

    color:transparent;
}

.header p{

    margin:0 auto 20px;

    max-width:700px;

    color:var(--muted);

    line-height:1.8;
}


/* SOCIAL */

.social{

    display:flex;

    justify-content:center;

    flex-wrap:wrap;

    gap:9px;

    margin:15px 0 25px;
}

.social a{

    display:inline-flex;

    align-items:center;

    gap:7px;

    padding:9px 14px;

    border-radius:13px;

    color:white;

    text-decoration:none;

    font-size:12px;

    font-weight:800;

    border:1px solid var(--border);

    background:rgba(255,255,255,.05);

    transition:.2s;
}

.social a:hover{

    transform:translateY(-3px);

    background:rgba(255,255,255,.10);
}


/* STATS */

.stats{

    display:grid;

    grid-template-columns:
        repeat(4,1fr);

    gap:12px;

    margin-bottom:18px;
}

.stat{

    padding:17px;

    text-align:center;

    border-radius:18px;

    border:1px solid var(--border);

    background:var(--panel2);

    backdrop-filter:blur(18px);

    transition:.25s;
}

.stat:hover{

    transform:translateY(-4px);

    border-color:rgba(59,130,246,.35);
}

.stat i{

    font-size:23px;

    margin-bottom:8px;

    color:#60a5fa;
}

.stat b{

    display:block;

    font-size:18px;
}

.stat small{

    color:var(--muted);

    font-size:11px;
}


/* TABS */

.tabs{

    display:flex;

    gap:7px;

    overflow-x:auto;

    padding:6px;

    margin-bottom:15px;

    border-radius:18px;

    background:rgba(15,23,42,.72);

    border:1px solid var(--border);

    scrollbar-width:none;
}

.tabs::-webkit-scrollbar{
    display:none;
}

.tab{

    flex:1;

    min-width:140px;

    padding:12px;

    border:0;

    border-radius:13px;

    color:var(--muted);

    background:transparent;

    font-family:inherit;

    font-weight:800;

    cursor:pointer;

    transition:.2s;
}

.tab.active{

    color:white;

    background:
        linear-gradient(
            135deg,
            var(--blue),
            var(--purple)
        );

    box-shadow:
        0 8px 25px rgba(59,130,246,.22);
}


/* CARDS */

.card{

    padding:22px;

    border-radius:24px;

    border:1px solid var(--border);

    background:var(--panel);

    backdrop-filter:blur(25px);

    box-shadow:
        0 20px 60px rgba(0,0,0,.35);

    margin-bottom:15px;
}

.card-title{

    display:flex;

    align-items:center;

    gap:10px;

    margin-bottom:18px;

    font-size:19px;

    font-weight:900;
}

.card-title i{
    color:#60a5fa;
}


/* INPUTS */

label{

    display:block;

    margin-bottom:7px;

    font-size:13px;

    font-weight:800;
}

input,textarea{

    width:100%;

    color:white;

    background:rgba(2,6,23,.75);

    border:1px solid rgba(255,255,255,.10);

    outline:none;

    border-radius:14px;

    padding:13px 14px;

    font-family:inherit;

    transition:.2s;
}

textarea{

    min-height:190px;

    resize:vertical;

    font-family:monospace;

    direction:ltr;

    text-align:left;
}

input:focus,
textarea:focus{

    border-color:var(--blue);

    box-shadow:
        0 0 0 3px rgba(59,130,246,.10);
}


/* GRID */

.grid{

    display:grid;

    grid-template-columns:
        repeat(2,1fr);

    gap:13px;
}


/* BUTTON */

.btn{

    width:100%;

    border:0;

    border-radius:14px;

    padding:13px 15px;

    color:white;

    font-family:inherit;

    font-weight:900;

    cursor:pointer;

    transition:.2s;
}

.btn:hover{

    transform:translateY(-2px);

    filter:brightness(1.08);
}

.btn-primary{

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

    box-shadow:
        0 10px 30px rgba(59,130,246,.18);
}

.btn-success{

    background:
        linear-gradient(
            135deg,
            #16a34a,
            #059669
        );
}

.btn-danger{

    background:
        linear-gradient(
            135deg,
            #dc2626,
            #be123c
        );
}

.btn-dark{

    background:rgba(255,255,255,.06);

    border:1px solid var(--border);
}

.btn-row{

    display:grid;

    grid-template-columns:
        repeat(2,1fr);

    gap:9px;

    margin-top:12px;
}


/* RESULT */

.result{

    display:none;

    margin-top:18px;

    padding:18px;

    border-radius:19px;

    border:1px solid rgba(34,197,94,.25);

    background:
        linear-gradient(
            135deg,
            rgba(34,197,94,.06),
            rgba(59,130,246,.04)
        );

    animation:show .3s ease;
}

@keyframes show{

    from{
        opacity:0;
        transform:translateY(8px);
    }

    to{
        opacity:1;
        transform:none;
    }
}

.result.show{
    display:block;
}

.success-title{

    color:#86efac;

    font-weight:900;

    margin-bottom:12px;
}

.copybox{

    display:flex;

    gap:7px;

    margin:8px 0;
}

.copybox input{

    min-width:0;

    direction:ltr;

    font-family:monospace;

    font-size:12px;
}

.copy-btn{

    flex:0 0 48px;

    border:0;

    border-radius:12px;

    color:white;

    background:#1e293b;

    cursor:pointer;
}


/* SCRIPT INFO */

.info{

    display:grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:8px;

    margin-top:13px;
}

.info-box{

    padding:11px;

    border-radius:12px;

    background:rgba(255,255,255,.04);

    border:1px solid var(--border);
}

.info-box small{

    display:block;

    color:var(--muted);

    font-size:10px;
}

.info-box b{

    font-size:12px;

    word-break:break-word;
}


/* FEATURES */

.features{

    display:grid;

    grid-template-columns:
        repeat(2,1fr);

    gap:10px;
}

.feature{

    padding:15px;

    border-radius:15px;

    background:rgba(255,255,255,.035);

    border:1px solid var(--border);

}

.feature i{

    color:#60a5fa;

    margin-left:5px;
}

.feature b{
    font-size:13px;
}

.feature p{

    color:var(--muted);

    font-size:11px;

    margin:5px 0 0;

    line-height:1.7;
}


/* TOAST */

#toast{

    position:fixed;

    bottom:20px;

    left:20px;

    z-index:99999;

    display:flex;

    flex-direction:column;

    gap:8px;
}

.toast{

    min-width:240px;

    max-width:calc(100vw - 40px);

    padding:13px 16px;

    border-radius:14px;

    color:white;

    background:rgba(15,23,42,.94);

    border:1px solid rgba(255,255,255,.10);

    box-shadow:0 15px 40px rgba(0,0,0,.5);

    backdrop-filter:blur(20px);

    animation:toast .3s ease;
}

@keyframes toast{

    from{
        opacity:0;
        transform:translateX(-20px);
    }

    to{
        opacity:1;
        transform:none;
    }
}


/* HIDDEN */

.hidden{
    display:none!important;
}


/* MOBILE */

@media(max-width:700px){

    .container-main{
        width:calc(100% - 14px);
        padding-top:8px;
    }

    .header{
        padding-top:15px;
    }

    .stats{
        grid-template-columns:
            repeat(2,1fr);
    }

    .grid{
        grid-template-columns:1fr;
    }

    .features{
        grid-template-columns:1fr;
    }

    .info{
        grid-template-columns:1fr;
    }

    .btn-row{
        grid-template-columns:1fr;
    }

    .card{
        padding:16px;
        border-radius:19px;
    }

    .header h1{
        font-size:32px;
    }

    .tab{
        min-width:125px;
        padding:10px 8px;
        font-size:12px;
    }
}

</style>

</head>

<body>

<canvas id="particles"></canvas>

<div class="container-main">

<header class="header">

    <div class="brand">
        <i class="fa-solid fa-shield-halved"></i>
        MAHDI PLATFORM V3
    </div>

    <h1>
        استضافة <span>السكربتات</span>
    </h1>

    <p>
        منصة حديثة لإنشاء روابط السكربتات وإدارتها
        وتحديثها بسهولة من مكان واحد.
    </p>

    <div class="social">

        <a href="https://discord.gg/j8daZqG9V"
           target="_blank">
            <i class="fa-brands fa-discord"></i>
            Discord
        </a>

        <a href="https://youtube.com/@xoreyt0"
           target="_blank">
            <i class="fa-brands fa-youtube"></i>
            YouTube
        </a>

        <a href="https://www.tiktok.com/@lklkl7777"
           target="_blank">
            <i class="fa-brands fa-tiktok"></i>
            TikTok
        </a>

    </div>

</header>


<section class="stats">

    <div class="stat">
        <i class="fa-solid fa-server"></i>
        <b>Online</b>
        <small>حالة المنصة</small>
    </div>

    <div class="stat">
        <i class="fa-solid fa-bolt"></i>
        <b>Fast</b>
        <small>استجابة سريعة</small>
    </div>

    <div class="stat">
        <i class="fa-solid fa-link"></i>
        <b>Live</b>
        <small>روابط مباشرة</small>
    </div>

    <div class="stat">
        <i class="fa-solid fa-code"></i>
        <b>V3</b>
        <small>الإصدار الحالي</small>
    </div>

</section>


<div class="tabs">

    <button class="tab active"
            onclick="showTab('create',this)">
        <i class="fa-solid fa-plus"></i>
        إنشاء
    </button>

    <button class="tab"
            onclick="showTab('builder',this)">
        <i class="fa-solid fa-wand-magic-sparkles"></i>
        Builder
    </button>

    <button class="tab"
            onclick="showTab('edit',this)">
        <i class="fa-solid fa-pen"></i>
        تعديل
    </button>

    <button class="tab"
            onclick="showTab('tools',this)">
        <i class="fa-solid fa-toolbox"></i>
        أدوات
    </button>

</div>


<!-- CREATE -->

<section id="create" class="tab-content">

<div class="card">

    <div class="card-title">
        <i class="fa-solid fa-cloud-arrow-up"></i>
        إنشاء رابط سكربت
    </div>

    <label>
        كود Lua
    </label>

    <textarea
        id="newScript"
        placeholder='print("Hello Mahdi!")'></textarea>

    <div class="grid" style="margin-top:12px">

        <div>

            <label>
                اسم السكربت
            </label>

            <input
                id="scriptTitle"
                maxlength="80"
                placeholder="Mahdi Hub V1">

        </div>

        <div>

            <label>
                مفتاح التعديل
            </label>

            <input
                id="newKey"
                type="password"
                maxlength="150"
                placeholder="كلمة السر">

        </div>

    </div>

    <button
        class="btn btn-primary"
        style="margin-top:13px"
        onclick="createScript()">

        <i class="fa-solid fa-rocket"></i>

        إنشاء الرابط الآن

    </button>

    <div id="createResult"
         class="result"></div>

</div>

</section>


<!-- BUILDER -->

<section id="builder"
         class="tab-content hidden">

<div class="card">

    <div class="card-title">
        <i class="fa-solid fa-wand-magic-sparkles"></i>
        صانع السكربت
    </div>

    <div class="features">

        <div class="feature">

            <i class="fa-solid fa-gauge-high"></i>

            <b>Speed</b>

            <p>
                إضافة سرعة مخصصة للشخصية.
            </p>

            <input
                id="speedValue"
                type="number"
                value="100"
                min="1"
                max="500"
                style="margin-top:8px">

        </div>


        <div class="feature">

            <i class="fa-solid fa-arrow-up"></i>

            <b>Jump</b>

            <p>
                إضافة قوة قفز مخصصة.
            </p>

            <input
                id="jumpValue"
                type="number"
                value="120"
                min="1"
                max="500"
                style="margin-top:8px">

        </div>


        <div class="feature">

            <i class="fa-solid fa-message"></i>

            <b>Notification</b>

            <p>
                إضافة إشعار عند التشغيل.
            </p>

            <button
                id="notifyBtn"
                class="btn btn-dark"
                onclick="toggleFeature(this)"
                style="margin-top:8px">

                غير مفعل

            </button>

        </div>


        <div class="feature">

            <i class="fa-solid fa-code"></i>

            <b>Template</b>

            <p>
                إنشاء قالب Lua جاهز.
            </p>

            <button
                class="btn btn-dark"
                onclick="buildTemplate()"
                style="margin-top:8px">

                استخدام القالب

            </button>

        </div>

    </div>

    <button
        class="btn btn-primary"
        style="margin-top:14px"
        onclick="buildScript()">

        <i class="fa-solid fa-gears"></i>

        إنشاء الكود

    </button>

</div>

</section>


<!-- EDIT -->

<section id="edit"
         class="tab-content hidden">

<div class="card">

    <div class="card-title">
        <i class="fa-solid fa-pen-to-square"></i>
        تعديل سكربت موجود
    </div>

    <div class="grid">

        <div>

            <label>
                Script ID
            </label>

            <input
                id="editId"
                placeholder="مثال: AbC123xy">

        </div>

        <div>

            <label>
                مفتاح التعديل
            </label>

            <input
                id="editKey"
                type="password"
                placeholder="المفتاح">

        </div>

    </div>

    <label style="margin-top:13px">
        الكود الجديد
    </label>

    <textarea
        id="editScript"
        placeholder="ضع الكود الجديد هنا"></textarea>

    <button
        class="btn btn-success"
        style="margin-top:13px"
        onclick="updateScript()">

        <i class="fa-solid fa-rotate"></i>

        تحديث السكربت

    </button>

    <div id="updateResult"
         class="result"></div>

</div>

</section>


<!-- TOOLS -->

<section id="tools"
         class="tab-content hidden">

<div class="card">

    <div class="card-title">
        <i class="fa-solid fa-toolbox"></i>
        أدوات سريعة
    </div>

    <div class="grid">

        <button
            class="btn btn-dark"
            onclick="clearAll()">

            <i class="fa-solid fa-trash"></i>
            مسح الحقول

        </button>

        <button
            class="btn btn-dark"
            onclick="formatCode()">

            <i class="fa-solid fa-align-left"></i>
            تنظيف الكود

        </button>

        <button
            class="btn btn-dark"
            onclick="demo()">

            <i class="fa-solid fa-flask"></i>
            تجربة Demo

        </button>

        <button
            class="btn btn-dark"
            onclick="scrollTop()">

            <i class="fa-solid fa-arrow-up"></i>
            أعلى الصفحة

        </button>

    </div>

</div>


<div class="card">

    <div class="card-title">
        <i class="fa-solid fa-circle-info"></i>
        المزايا
    </div>

    <div class="features">

        <div class="feature">
            <i class="fa-solid fa-link"></i>
            <b>رابط ثابت</b>
            <p>
                تستطيع تحديث محتوى السكربت
                بدون تغيير الرابط.
            </p>
        </div>

        <div class="feature">
            <i class="fa-solid fa-copy"></i>
            <b>نسخ سريع</b>
            <p>
                نسخ الرابط والـ Loadstring
                مباشرة.
            </p>
        </div>

        <div class="feature">
            <i class="fa-solid fa-clock"></i>
            <b>تاريخ الإنشاء</b>
            <p>
                حفظ وقت إنشاء كل سكربت.
            </p>
        </div>

        <div class="feature">
            <i class="fa-solid fa-chart-simple"></i>
            <b>عداد الاستخدام</b>
            <p>
                معرفة عدد مرات طلب الرابط.
            </p>
        </div>

    </div>

</div>

</section>

</div>


<div id="toast"></div>


<script>

/* =====================================================
   PARTICLES
===================================================== */

const canvas =
    document.getElementById("particles");

const ctx =
    canvas.getContext("2d");

let particles = [];

function resizeCanvas(){

    canvas.width =
        window.innerWidth;

    canvas.height =
        window.innerHeight;
}

resizeCanvas();

window.addEventListener(
    "resize",
    resizeCanvas
);

for(let i=0;i<55;i++){

    particles.push({

        x:Math.random()*innerWidth,

        y:Math.random()*innerHeight,

        r:Math.random()*1.7+.4,

        vx:(Math.random()-.5)*.35,

        vy:(Math.random()-.5)*.35

    });

}

function animateParticles(){

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    particles.forEach(p=>{

        p.x+=p.vx;
        p.y+=p.vy;

        if(p.x<0) p.x=canvas.width;
        if(p.x>canvas.width) p.x=0;

        if(p.y<0) p.y=canvas.height;
        if(p.y>canvas.height) p.y=0;

        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            p.r,
            0,
            Math.PI*2
        );

        ctx.fillStyle=
            "rgba(96,165,250,.30)";

        ctx.fill();

    });

    requestAnimationFrame(
        animateParticles
    );
}

animateParticles();


/* =====================================================
   TOAST
===================================================== */

function toast(message, type="normal"){

    const box =
        document.getElementById("toast");

    const item =
        document.createElement("div");

    item.className="toast";

    let icon =
        type==="success"
        ? "fa-circle-check"
        : type==="error"
        ? "fa-circle-xmark"
        : "fa-circle-info";

    item.innerHTML=`
        <i class="fa-solid ${icon}"></i>
        <span>${escapeHTML(message)}</span>
    `;

    box.appendChild(item);

    setTimeout(()=>{
        item.remove();
    },3000);
}


/* =====================================================
   TABS
===================================================== */

function showTab(id,button){

    document
        .querySelectorAll(".tab-content")
        .forEach(x=>x.classList.add("hidden"));

    document
        .getElementById(id)
        .classList.remove("hidden");

    document
        .querySelectorAll(".tab")
        .forEach(x=>x.classList.remove("active"));

    button.classList.add("active");

    window.scrollTo({
        top:0,
        behavior:"smooth"
    });
}


/* =====================================================
   ESCAPE
===================================================== */

function escapeHTML(value){

    return String(value)
        .replaceAll("&","&amp;")
        .replaceAll("<","&lt;")
        .replaceAll(">","&gt;")
        .replaceAll('"',"&quot;")
        .replaceAll("'","&#039;");
}


/* =====================================================
   COPY
===================================================== */

async function copyText(text){

    try{

        if(
            navigator.clipboard &&
            window.isSecureContext
        ){

            await navigator.clipboard.writeText(text);

            toast(
                "تم النسخ بنجاح!",
                "success"
            );

            return;
        }

    }catch(e){}

    const area =
        document.createElement("textarea");

    area.value=text;

    area.style.position="fixed";
    area.style.left="-9999px";

    document.body.appendChild(area);

    area.focus();
    area.select();

    try{

        document.execCommand("copy");

        toast(
            "تم النسخ!",
            "success"
        );

    }catch(e){

        toast(
            "انسخ النص يدويًا",
            "error"
        );

    }

    area.remove();
}


/* =====================================================
   CREATE
===================================================== */

async function createScript(){

    const script =
        document
        .getElementById("newScript")
        .value
        .trim();

    const key =
        document
        .getElementById("newKey")
        .value
        .trim();

    const title =
        document
        .getElementById("scriptTitle")
        .value
        .trim() ||
        "Mahdi Script";

    const result =
        document
        .getElementById("createResult");

    if(!script){

        toast(
            "اكتب كود Lua أولاً",
            "error"
        );

        return;
    }

    if(!key){

        toast(
            "اكتب مفتاح التعديل",
            "error"
        );

        return;
    }

    result.classList.remove("show");

    try{

        const response =
            await fetch(
                "/api/create",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":
                            "application/json"
                    },

                    body:JSON.stringify({
                        script,
                        key,
                        title
                    })
                }
            );

        const data =
            await response.json();

        if(!response.ok || !data.success){

            throw new Error(
                data.error ||
                "فشل إنشاء السكربت"
            );
        }

        const raw =
            data.raw_url;

        const loadstring =
            `loadstring(game:HttpGet("${raw}"))()`;

        result.innerHTML=`

            <div class="success-title">
                <i class="fa-solid fa-circle-check"></i>
                تم إنشاء الرابط بنجاح
            </div>

            <div class="copybox">

                <input
                    id="createdLoadstring"
                    readonly
                    value="${escapeHTML(loadstring)}">

                <button
                    class="copy-btn"
                    onclick="copyText(document.getElementById('createdLoadstring').value)">

                    <i class="fa-solid fa-copy"></i>

                </button>

            </div>

            <div class="copybox">

                <input
                    id="createdRaw"
                    readonly
                    value="${escapeHTML(raw)}">

                <button
                    class="copy-btn"
                    onclick="copyText(document.getElementById('createdRaw').value)">

                    <i class="fa-solid fa-link"></i>

                </button>

            </div>

            <div class="btn-row">

                <button
                    class="btn btn-primary"
                    onclick="copyText(document.getElementById('createdLoadstring').value)">

                    <i class="fa-solid fa-copy"></i>
                    نسخ Loadstring

                </button>

                <button
                    class="btn btn-success"
                    onclick="copyText(document.getElementById('createdRaw').value)">

                    <i class="fa-solid fa-link"></i>
                    نسخ الرابط

                </button>

                <button
                    class="btn btn-dark"
                    onclick="window.open('${escapeHTML(raw)}','_blank')">

                    <i class="fa-solid fa-globe"></i>
                    فتح الرابط

                </button>

                <button
                    class="btn btn-dark"
                    onclick="downloadScript('${escapeHTML(raw)}')">

                    <i class="fa-solid fa-download"></i>
                    تحميل

                </button>

            </div>

            <div class="info">

                <div class="info-box">
                    <small>Script ID</small>
                    <b>${escapeHTML(data.id)}</b>
                </div>

                <div class="info-box">
                    <small>الاسم</small>
                    <b>${escapeHTML(data.title)}</b>
                </div>

                <div class="info-box">
                    <small>الحالة</small>
                    <b style="color:#86efac">
                        Active
                    </b>
                </div>

            </div>

        `;

        result.classList.add("show");

        document
            .getElementById("editId")
            .value=data.id;

        document
            .getElementById("editKey")
            .value=key;

        toast(
            "تم إنشاء السكربت والرابط!",
            "success"
        );

    }catch(error){

        result.innerHTML=`
            <div style="color:#fca5a5;font-weight:800">
                ${escapeHTML(error.message)}
            </div>
        `;

        result.classList.add("show");

        toast(
            error.message,
            "error"
        );
    }
}


/* =====================================================
   DOWNLOAD
===================================================== */

async function downloadScript(url){

    try{

        const response =
            await fetch(url);

        const text =
            await response.text();

        const blob =
            new Blob(
                [text],
                {type:"text/plain"}
            );

        const link =
            document.createElement("a");

        link.href =
            URL.createObjectURL(blob);

        link.download =
            "script.lua";

        document.body.appendChild(link);

        link.click();

        link.remove();

        URL.revokeObjectURL(
            link.href
        );

        toast(
            "تم تجهيز التحميل",
            "success"
        );

    }catch(e){

        window.open(url,"_blank");

    }
}


/* =====================================================
   UPDATE
===================================================== */

async function updateScript(){

    const id =
        document
        .getElementById("editId")
        .value
        .trim();

    const key =
        document
        .getElementById("editKey")
        .value
        .trim();

    const script =
        document
        .getElementById("editScript")
        .value;

    const result =
        document
        .getElementById("updateResult");

    if(!id || !key || !script){

        toast(
            "املأ جميع الحقول",
            "error"
        );

        return;
    }

    try{

        const response =
            await fetch(
                "/api/update",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":
                            "application/json"
                    },

                    body:JSON.stringify({
                        id,
                        key,
                        script
                    })
                }
            );

        const data =
            await response.json();

        if(!response.ok || !data.success){

            throw new Error(
                data.error ||
                "فشل التحديث"
            );
        }

        result.innerHTML=`
            <div class="success-title">
                <i class="fa-solid fa-circle-check"></i>
                تم تحديث السكربت بنجاح
            </div>
        `;

        result.classList.add("show");

        toast(
            "تم تحديث السكربت!",
            "success"
        );

    }catch(error){

        result.innerHTML=`
            <div style="color:#fca5a5;font-weight:800">
                ${escapeHTML(error.message)}
            </div>
        `;

        result.classList.add("show");

        toast(
            error.message,
            "error"
        );
    }
}


/* =====================================================
   BUILDER
===================================================== */

let notifyEnabled=false;

function toggleFeature(button){

    notifyEnabled=
        !notifyEnabled;

    button.textContent=
        notifyEnabled
        ? "مفعل ✓"
        : "غير مفعل";

    toast(
        notifyEnabled
        ? "تم تفعيل الإشعار"
        : "تم إيقاف الإشعار"
    );
}


function buildScript(){

    const speed =
        document
        .getElementById("speedValue")
        .value || 100;

    const jump =
        document
        .getElementById("jumpValue")
        .value || 120;

    let code=[
        "-- MAHDI PLATFORM",
        "-- Generated Script",
        "",
        "local Players = game:GetService('Players')",
        "local player = Players.LocalPlayer",
        "local character = player.Character or player.CharacterAdded:Wait()",
        "local humanoid = character:WaitForChild('Humanoid')",
        ""
    ];

    code.push(
        `humanoid.WalkSpeed = ${Number(speed)}`
    );

    code.push(
        `humanoid.JumpPower = ${Number(jump)}`
    );

    if(notifyEnabled){

        code.push("");

        code.push(
            `pcall(function()
    game:GetService("StarterGui"):SetCore(
        "SendNotification",
        {
            Title="MAHDI PLATFORM",
            Text="تم تشغيل السكربت بنجاح",
            Duration=5
        }
    )
end)`
        );
    }

    document
        .getElementById("newScript")
        .value=code.join("\n");

    const tabs =
        document.querySelectorAll(".tab");

    showTab(
        "create",
        tabs[0]
    );

    toast(
        "تم إنشاء الكود!",
        "success"
    );
}


function buildTemplate(){

    document
        .getElementById("newScript")
        .value=
`-- MAHDI PLATFORM

local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer

print("MAHDI SCRIPT LOADED")

pcall(function()

    game:GetService("StarterGui"):SetCore(
        "SendNotification",
        {
            Title = "MAHDI PLATFORM",
            Text = "تم تشغيل السكربت",
            Duration = 5
        }
    )

end)`;

    toast(
        "تم وضع القالب في مربع الكود",
        "success"
    );
}


/* =====================================================
   TOOLS
===================================================== */

function formatCode(){

    const textarea =
        document.getElementById("newScript");

    const lines =
        textarea.value
        .split("\n")
        .map(x=>x.trim())
        .filter(x=>x.length);

    textarea.value=
        lines.join("\n");

    toast(
        "تم تنظيف الكود",
        "success"
    );
}


function clearAll(){

    [
        "newScript",
        "scriptTitle",
        "newKey",
        "editId",
        "editKey",
        "editScript"
    ].forEach(id=>{

        const element =
            document.getElementById(id);

        if(element)
            element.value="";

    });

    document
        .getElementById("createResult")
        .classList.remove("show");

    document
        .getElementById("updateResult")
        .classList.remove("show");

    toast(
        "تم مسح الحقول"
    );
}


function demo(){

    document
        .getElementById("newScript")
        .value=
`print("Hello from MAHDI PLATFORM!")

game:GetService("StarterGui"):SetCore(
    "SendNotification",
    {
        Title="MAHDI",
        Text="Demo يعمل بنجاح!",
        Duration=5
    }
)`;

    document
        .getElementById("scriptTitle")
        .value="MAHDI Demo";

    document
        .getElementById("newKey")
        .value="demo-key";

    toast(
        "تم وضع Demo جاهز"
    );
}


/* =====================================================
   GLOBAL
===================================================== */

function scrollTop(){

    window.scrollTo({
        top:0,
        behavior:"smooth"
    });
}

</script>

</body>
</html>
'''


# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def home():

    return render_template_string(
        INDEX_HTML
    )


# =========================================================
# CREATE
# =========================================================

@app.route(
    "/api/create",
    methods=["POST"]
)
def create_script():

    data =
        request.get_json(
            silent=True
        ) or {}

    script =
        data.get("script")

    key =
        data.get("key")

    title =
        data.get(
            "title",
            "Untitled Script"
        )

    script =
        safe_text(
            script,
            MAX_SCRIPT_SIZE
        )

    key =
        safe_text(
            key,
            MAX_KEY_SIZE
        )

    title =
        safe_text(
            title,
            MAX_TITLE_SIZE
        )

    if not script:

        return jsonify({
            "success":False,
            "error":"كود السكربت مطلوب"
        }),400

    if not key:

        return jsonify({
            "success":False,
            "error":"مفتاح التعديل مطلوب"
        }),400

    script_id =
        generate_id()

    store =
        load_data()

    store[script_id] = {

        "script":script,

        "key":key,

        "title":
            title or
            "Untitled Script",

        "created_at":
            time.time(),

        "views":0

    }

    if not save_data(store):

        return jsonify({
            "success":False,
            "error":"تعذر حفظ السكربت"
        }),500

    raw_url =
        request.host_url.rstrip("/") + \
        "/raw/" + script_id

    return jsonify({

        "success":True,

        "id":script_id,

        "title":
            store[script_id]["title"],

        "raw_url":raw_url

    })


# =========================================================
# UPDATE
# =========================================================

@app.route(
    "/api/update",
    methods=["POST"]
)
def update_script():

    data =
        request.get_json(
            silent=True
        ) or {}

    script_id =
        safe_text(
            data.get("id"),
            100
        )

    key =
        safe_text(
            data.get("key"),
            MAX_KEY_SIZE
        )

    new_script =
        safe_text(
            data.get("script"),
            MAX_SCRIPT_SIZE
        )

    if not script_id or not key or not new_script:

        return jsonify({
            "success":False,
            "error":"جميع الحقول مطلوبة"
        }),400

    store =
        load_data()

    item =
        store.get(script_id)

    if not item:

        return jsonify({
            "success":False,
            "error":"السكربت غير موجود"
        }),404

    if item.get("key") != key:

        return jsonify({
            "success":False,
            "error":"مفتاح التعديل غير صحيح"
        }),403

    item["script"] =
        new_script

    item["updated_at"] =
        time.time()

    save_data(store)

    return jsonify({
        "success":True
    })


# =========================================================
# RAW
# =========================================================

@app.route(
    "/raw/<script_id>"
)
def raw_script(script_id):

    store =
        load_data()

    item =
        store.get(script_id)

    if not item:

        return Response(
            "-- Script Not Found",
            status=404,
            mimetype="text/plain"
        )

    user_agent =
        request.headers.get(
            "User-Agent",
            ""
        ).lower()

    browsers = [
        "mozilla",
        "chrome",
        "safari",
        "edge",
        "opera",
        "firefox",
        "msie"
    ]

    executors = [
        "roblox",
        "delta",
        "synapse",
        "fluxus",
        "krnl",
        "hydrogen",
        "electron",
        "solara"
    ]

    is_executor =
        any(
            x in user_agent
            for x in executors
        )

    is_browser =
        any(
            x in user_agent
            for x in browsers
        ) and not is_executor

    if is_browser:

        return (
            WARNING_HTML,
            200,
            {
                "Content-Type":
                    "text/html; charset=utf-8"
            }
        )

    item["views"] =
        int(item.get("views",0)) + 1

    save_data(store)

    return Response(
        item["script"],
        status=200,
        mimetype="text/plain"
    )


# =========================================================
# SCRIPT INFO
# =========================================================

@app.route(
    "/api/info/<script_id>"
)
def script_info(script_id):

    store =
        load_data()

    item =
        store.get(script_id)

    if not item:

        return jsonify({
            "success":False,
            "error":"السكربت غير موجود"
        }),404

    return jsonify({

        "success":True,

        "id":script_id,

        "title":
            item.get(
                "title",
                "Untitled"
            ),

        "views":
            item.get(
                "views",
                0
            ),

        "created_at":
            item.get(
                "created_at"
            ),

        "updated_at":
            item.get(
                "updated_at"
            )

    })


# =========================================================
# DELETE
# =========================================================

@app.route(
    "/api/delete",
    methods=["POST"]
)
def delete_script():

    data =
        request.get_json(
            silent=True
        ) or {}

    script_id =
        safe_text(
            data.get("id"),
            100
        )

    key =
        safe_text(
            data.get("key"),
            MAX_KEY_SIZE
        )

    store =
        load_data()

    item =
        store.get(script_id)

    if not item:

        return jsonify({
            "success":False,
            "error":"السكربت غير موجود"
        }),404

    if item.get("key") != key:

        return jsonify({
            "success":False,
            "error":"مفتاح التعديل غير صحيح"
        }),403

    del store[script_id]

    save_data(store)

    return jsonify({
        "success":True
    })


# =========================================================
# HEALTH
# =========================================================

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
