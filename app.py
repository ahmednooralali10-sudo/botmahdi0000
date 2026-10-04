from flask import Flask, request, Response

app = Flask(__name__)

# كود اللوا الأصلي الذي تريد حمايته
LUA_SCRIPT = '''
local player = game.Players.LocalPlayer
print("تم تشغيل السكربت بنجاح لـ: " .. player.Name)

game:GetService("StarterGui"):SetCore("SendNotification", {
    Title = "أهلاً مهدي!";
    Text = "السكربت شغال و Vercel حاميه بنجاح 🚀";
    Duration = 5;
})
'''

# رسالة "سنقر لا تسرق" للمتصفح
WARNING_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>سنقر لا تسرق!</title>
    <style>
        body {
            background-color: #0f172a;
            color: #ffffff;
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        .card {
            background: #1e293b;
            padding: 2rem 3rem;
            border-radius: 1rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            border: 2px solid #ef4444;
        }
        h1 {
            color: #ef4444;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        p {
            color: #94a3b8;
            font-size: 1.2rem;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🦊🛑 سنقر لا تسرق!</h1>
        <p>لا يمكنك عرض كود Lua من خلال المتصفح.</p>
    </div>
</body>
</html>
'''

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # قائمة الـ User-Agents المعروفة للمتصفحات العادية
    browsers = ['mozilla', 'chrome', 'safari', 'edge', 'opera', 'firefox', 'msie']
    
    # هل الطلب قادم من متصفح؟
    is_browser = any(b in user_agent for b in browsers)
    
    # إذا كان الطلب من متصفح عادي -> إرجاع صفحة التحذير
    if is_browser:
        return WARNING_HTML, 200, {'Content-Type': 'text/html; charset=utf-8'}
    
    # إذا كان الطلب من Roblox / Executor -> إرجاع كود الـ Lua
    return Response(LUA_SCRIPT, status=200, mimetype='text/plain')

if __name__ == '__main__':
    app.run()
