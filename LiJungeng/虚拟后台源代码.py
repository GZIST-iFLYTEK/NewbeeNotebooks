from flask import Flask, request, jsonify, render_template  # 新增render_template
from flask_cors import CORS  # 解决跨域，需先安装：pip install flask-cors

# 新增：获取本机Windows的局域网IP（方便直接复制访问）
import socket
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

app = Flask(__name__)
CORS(app)  # 允许跨域（前后端分离时必需）

# ====================== 新增：关联HTML页面的路由 ======================
@app.route('/')  # 访问http://127.0.0.1:5000 直接返回HTML页面
def index():
    # 渲染templates目录下的index.html，可传递数据到前端（可选）
    return render_template('index.html', title="校园服务中心")

# ====================== 原有API接口（保留不变） ======================
# 模拟数据（场地、图书）
venues = [
    {"id": 1, "name": "讨论室A", "location": "教学楼301", "capacity": 10, "equipment": ["投影仪", "白板", "视频会议系统"], "available_times": ["2024-05-20 09:00-10:00", "2024-05-20 14:00-15:00"]},
    {"id": 2, "name": "讨论室B", "location": "教学楼302", "capacity": 6, "equipment": ["投影仪", "白板"], "available_times": ["2024-05-20 10:00-11:00"]}
]
books = [{"id": 1, "title": "人工智能导论", "author": "李开复", "status": "可借阅"}, {"id": 2, "title": "Python编程从入门到实践", "author": "Eric Matthes", "status": "已借出"}]

# 场地查询API
@app.route('/api/venues', methods=['GET'])
def get_venues():
    equipment = request.args.get('equipment')
    filtered_venues = venues
    if equipment:
        filtered_venues = [v for v in venues if equipment in v['equipment']]
    return jsonify({"code": 0, "data": filtered_venues, "message": "success"})

# 图书检索API
@app.route('/api/books', methods=['GET'])
def get_books():
    title = request.args.get('title')
    filtered_books = books
    if title:
        filtered_books = [b for b in books if title in b['title']]
    return jsonify({"code": 0, "data": filtered_books, "message": "success"})

# 宿舍报修API
@app.route('/api/repair', methods=['POST'])
def submit_repair():
    try:
        username = request.json.get("username", "").strip()
        password = request.json.get("password", "").strip()
        if not username or not password:
            return jsonify({"code": 1, "message": "用户名或密码不能为空"}), 400
        return jsonify({"code": 0, "message": "报修单提交成功", "ticket_id": "T20240520001"})
    except Exception as e:
        return jsonify({"code": 2, "message": f"请求错误：{str(e)}"}), 400

# if __name__ == '__main__':
#     print("🚀 服务已启动！访问地址: http://127.0.0.1:5000")
#     app.run(debug=True)

if __name__ == '__main__':
    print("🚀 服务已启动！")
    print(f"本机访问：http://127.0.0.1:5000")
    print(f"局域网访问：http://{get_local_ip()}:5000") # 新增局域网访问地址提示
    app.run(
        host="0.0.0.0",  # 关键：监听所有网络接口，允许局域网/本机访问
        port=0419,       # 端口号，可自定义（如8080、80）
        debug=True       # 开发阶段开启，生产阶段改为False
    )

