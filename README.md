# 计算器后端服务
技术栈：Python3 + FastAPI + SQLite
## 依赖安装命令
pip install fastapi uvicorn pydantic python-expression-evaluator
## 启动服务命令
uvicorn main:app --reload
访问地址：http://127.0.0.1:8000
## 接口清单
1. POST /api/calculate 提交表达式计算
2. GET /api/history 获取所有计算历史
3. DELETE /api/history/{id} 删除指定id历史记录
## 数据库说明
calc.db 文件运行代码自动生成，持久存储所有计算记录，无需手动配置
