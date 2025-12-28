import tkinter as tk
from tkinter import ttk, messagebox
import db_operate

# 创建主窗口
root = tk.Tk()
root.title("剧社历年资料查询与管理系统")
root.geometry("800x600")  # 窗口大小，固定无需修改

# ============ 界面布局（极简美观，无复杂控件） ============
# 标题
title_label = tk.Label(root, text="剧社历年资料查询与管理系统", font=("宋体", 18, "bold"))
title_label.pack(pady=10)

# 功能按钮区
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

# 绑定功能按钮事件
def btn_add():
    name = entry_name.get()
    type_ = entry_type.get()
    year = entry_year.get()
    director = entry_dir.get()
    actor = entry_actor.get()
    times = entry_times.get()
    award = entry_award.get()
    remark = entry_remark.get()
    res = db_operate.add_drama(name, type_, year, director, actor, times, award, remark)
    messagebox.showinfo("提示", res)

def btn_query():
    data = db_operate.get_all_drama()
    # 清空表格
    for item in tree.get_children():
        tree.delete(item)
    # 插入数据
    for row in data:
        tree.insert("", "end", values=row)

def btn_update():
    select = tree.selection()
    if not select:
        messagebox.showwarning("警告", "请先选择要修改的剧目！")
        return
    row = tree.item(select)["values"]
    drama_id = row[0]
    res = db_operate.update_drama(drama_id, entry_name.get(), entry_type.get(), entry_year.get(), entry_dir.get())
    messagebox.showinfo("提示", res)

def btn_del():
    select = tree.selection()
    if not select:
        messagebox.showwarning("警告", "请先选择要删除的剧目！")
        return
    row = tree.item(select)["values"]
    drama_id = row[0]
    res = db_operate.del_drama(drama_id)
    messagebox.showinfo("提示", res)

# ✅ 修复核心报错的函数 - 复杂查询 无反斜杠语法错误 + 增加空数据判断防报错
def btn_complex():
    data = db_operate.complex_query()
    if not data:
        messagebox.showinfo("提示", "暂无剧目统计数据！")
        return
    content_list = []
    content_list.append("类型\t剧目数\t总场次\t平均场次")
    content_list.append("-"*30)
    for row in data:
        row_text = f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]:.1f}"
        content_list.append(row_text)
    show_text = '\n'.join(content_list)
    messagebox.showinfo("复杂查询结果-各类型剧目统计", show_text)

def btn_visual():
    res = db_operate.show_visual()
    messagebox.showinfo("提示", res)

# 功能按钮
tk.Button(btn_frame, text="新增资料", width=10, command=btn_add).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="查询所有", width=10, command=btn_query).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="修改资料", width=10, command=btn_update).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="删除资料", width=10, command=btn_del).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="复杂统计", width=10, command=btn_complex, bg="#eee").grid(row=0, column=4, padx=5)
tk.Button(btn_frame, text="数据可视化", width=10, command=btn_visual, bg="#eee").grid(row=0, column=5, padx=5)

# 输入框区
input_frame = tk.Frame(root)
input_frame.pack(pady=10, fill="x", padx=20)

tk.Label(input_frame, text="剧目名称:").grid(row=0, column=0, padx=5)
entry_name = tk.Entry(input_frame, width=10)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="剧目类型:").grid(row=0, column=2, padx=5)
entry_type = tk.Entry(input_frame, width=10)
entry_type.grid(row=0, column=3, padx=5)

tk.Label(input_frame, text="编排年份:").grid(row=0, column=4, padx=5)
entry_year = tk.Entry(input_frame, width=10)
entry_year.grid(row=0, column=5, padx=5)

tk.Label(input_frame, text="导演:").grid(row=0, column=6, padx=5)
entry_dir = tk.Entry(input_frame, width=10)
entry_dir.grid(row=0, column=7, padx=5)

tk.Label(input_frame, text="主演:").grid(row=1, column=0, padx=5)
entry_actor = tk.Entry(input_frame, width=10)
entry_actor.grid(row=1, column=1, padx=5)

tk.Label(input_frame, text="演出场次:").grid(row=1, column=2, padx=5)
entry_times = tk.Entry(input_frame, width=10)
entry_times.grid(row=1, column=3, padx=5)

tk.Label(input_frame, text="获奖情况:").grid(row=1, column=4, padx=5)
entry_award = tk.Entry(input_frame, width=10)
entry_award.grid(row=1, column=5, padx=5)

tk.Label(input_frame, text="备注:").grid(row=1, column=6, padx=5)
entry_remark = tk.Entry(input_frame, width=20)
entry_remark.grid(row=1, column=7, padx=5)

# 数据展示表格
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, fill="both", expand=True, padx=20)

columns = ("剧目编号", "剧目名称", "剧目类型", "编排年份", "导演")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill="both", expand=True)

# 启动主循环
if __name__ == "__main__":
    root.mainloop()