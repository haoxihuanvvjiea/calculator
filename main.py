from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from simpleeval import SimpleEval
from fastapi.middleware.cors import CORSMiddleware

# 创建服务
app = FastAPI()

# 跨域配置，允许前端访问后端接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库，自动建表
def init_db():
    conn = sqlite3.connect("calc.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expression TEXT NOT NULL,
        result TEXT NOT NULL,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# 接收前端表达式的数据格式
class CalcReq(BaseModel):
    expression: str

# 计算接口
@app.post("/api/calculate")
def calculate(req: CalcReq):
    expr = req.expression.strip()
    try:
        evaluator = SimpleEval()
        res = evaluator.eval(expr)
        res_str = str(res)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"表达式错误：{str(e)}")

    # 存入数据库
    conn = sqlite3.connect("calc.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO history(expression, result) VALUES (?, ?)", (expr, res_str))
    conn.commit()
    conn.close()
    return {"success": True, "expression": expr, "result": res_str}

# 查询全部历史记录
@app.get("/api/history")
def get_history():
    conn = sqlite3.connect("calc.db")
    cur = conn.cursor()
    cur.execute("SELECT id, expression, result, create_time FROM history ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    res_list = []
    for row in data:
        res_list.append({
            "id": row[0],
            "expression": row[1],
            "result": row[2],
            "time": row[3]
        })
    return {"success": True, "data": res_list}

# 删除单条历史记录
@app.delete("/api/history/{hid}")
def del_history(hid: int):
    conn = sqlite3.connect("calc.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM history WHERE id=?", (hid,))
    conn.commit()
    conn.close()
    return {"success": True, "msg": "删除成功"}
