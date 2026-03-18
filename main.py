# -*- coding: utf-8 -*-
# main.py
from network import app
from database.connect import init_db

if __name__ == "__main__":
    # # 初始化数据库
    init_db()
    print("✅ Database initialized")

    # 启动 Flask 服务器
    app.run(
        host="0.0.0.0",    # 局域网可访问
        port=5000,
        debug=False,         # 开发调试模式
        use_reloader=False,
        threaded = False
    )
