import mysql.connector
from mysql.connector import Error
import config
import matplotlib.pyplot as plt

# 设置matplotlib中文显示，解决图表中文乱码问题（必须加）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ============ 1. 建立数据库连接（复用你的初始代码） ============
def create_conn():
    conn = None
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            passwd=config.DB_PASSWORD,
            database=config.DB_NAME
        )
    except Error as e:
        print(f"数据库连接失败：{e}")
    return conn

# ============ 2. 基础CRUD功能 - 增删改查（课程设计必做，全部实现，极简版） ============
# 2.1 新增剧目资料 (Create)
def add_drama(drama_name, drama_type, create_year, director, actor, times, award, remark):
    conn = create_conn()
    if conn:
        try:
            cursor = conn.cursor()
            # 先插入剧目主表
            sql1 = "INSERT INTO drama_info(drama_name,drama_type,create_year,director) VALUES(%s,%s,%s,%s)"
            cursor.execute(sql1, (drama_name, drama_type, create_year, director))
            drama_id = cursor.lastrowid  # 获取刚插入的剧目编号
            # 再插入演出资料从表
            sql2 = "INSERT INTO drama_data(drama_id,actor_name,perform_times,award,remark) VALUES(%s,%s,%s,%s,%s)"
            cursor.execute(sql2, (drama_id, actor, times, award, remark))
            conn.commit()
            cursor.close()
            conn.close()
            return "✅ 剧目资料新增成功！"
        except Error as e:
            conn.rollback()
            return f"❌ 新增失败：{e}"

# 2.2 查询所有剧目资料 (Read - 单表查询，基础查询)
def get_all_drama():
    conn = create_conn()
    data = []
    if conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT * FROM drama_info ORDER BY create_year DESC"
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
        except Error as e:
            print(f"查询失败：{e}")
    return data

# 2.3 修改剧目资料 (Update)
def update_drama(drama_id, drama_name, drama_type, create_year, director):
    conn = create_conn()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE drama_info SET drama_name=%s,drama_type=%s,create_year=%s,director=%s WHERE drama_id=%s"
            cursor.execute(sql, (drama_name, drama_type, create_year, director, drama_id))
            conn.commit()
            cursor.close()
            conn.close()
            return "✅ 剧目资料修改成功！"
        except Error as e:
            conn.rollback()
            return f"❌ 修改失败：{e}"

# 2.4 删除剧目资料 (Delete)
def del_drama(drama_id):
    conn = create_conn()
    if conn:
        try:
            cursor = conn.cursor()
            # 先删从表，再删主表（外键约束）
            sql1 = "DELETE FROM drama_data WHERE drama_id=%s"
            sql2 = "DELETE FROM drama_info WHERE drama_id=%s"
            cursor.execute(sql1, (drama_id,))
            cursor.execute(sql2, (drama_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return "✅ 剧目资料删除成功！"
        except Error as e:
            conn.rollback()
            return f"❌ 删除失败：{e}"

# ============ 3. 复杂查询 【课程设计硬性要求 ✔✔✔ 必做】 ============
# 多表联查 + 聚合函数 + 分组统计 （完美满足要求，直接用）
# 查询：按剧目类型分组，统计每种类型的剧目数量、总演出场次、平均演出场次
def complex_query():
    conn = create_conn()
    data = []
    if conn:
        try:
            cursor = conn.cursor()
            # 核心复杂查询SQL：2表联查 + COUNT/SUM/AVG聚合函数 + GROUP BY分组
            sql = """
                SELECT di.drama_type, COUNT(di.drama_id) as 剧目数量,
                       SUM(dd.perform_times) as 总演出场次,
                       AVG(dd.perform_times) as 平均演出场次
                FROM drama_info di
                JOIN drama_data dd ON di.drama_id = dd.drama_id
                GROUP BY di.drama_type
                ORDER BY 剧目数量 DESC
            """
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
        except Error as e:
            print(f"复杂查询失败：{e}")
    return data

# ============ 4. 数据可视化 【课程设计硬性要求 ✔✔✔ 必做】 ============
# 极简实现：根据复杂查询结果，生成柱状图展示 各类型剧目演出场次统计
def show_visual():
    data = complex_query()
    if not data:
        return "❌ 暂无数据，无法生成图表！"
    # 提取数据
    type_list = [row[0] for row in data]
    total_times = [row[2] for row in data]
    # 绘制柱状图
    plt.figure(figsize=(8, 5))
    plt.bar(type_list, total_times, color=['lightblue', 'lightgreen', 'pink', 'orange'])
    plt.title('剧社各类型剧目总演出场次统计', fontsize=14)
    plt.xlabel('剧目类型', fontsize=12)
    plt.ylabel('总演出场次', fontsize=12)
    plt.tight_layout()
    plt.show()
    return "✅ 可视化图表生成成功！"