# Claude Camp W3 — CSV 学员数据分析器

本目录包含 **项目 1**：读取学员 CSV，用 Pandas 统计人数与国家分布、对赌完成率，并将结果写入 `report.json`。

---

## 功能说明 `csv_student_analyzer.py`

**输入**：UTF-8 编码的 CSV，须包含以下列（列名需完全一致）：

| 列名 | 说明 |
|------|------|
| 姓名 | 学员姓名 |
| 邮箱 | 邮箱地址 |
| 加入日期 | 建议格式 `YYYY-MM-DD` |
| 所在国家 | 国家名称 |
| 对赌状态 | 如：已达成、进行中、待确认、未达成、已退出 |

**统计内容**（由 Pandas 完成，非手写循环）：

- **总人数**：CSV 数据行数
- **各国家人数**：按「所在国家」分组计数，国家名按字母序排列
- **对赌完成率**：`对赌状态 == "已达成"` 的人数 ÷ 总人数，在 JSON 中为小数（如 `0.3` 表示 30%）；同时输出「对赌完成人数」

**输出**：默认在同目录生成 `report.json`（UTF-8、中文不转义）。

---

## 环境准备（首次）

依赖见 `requirements.txt`（仅需 `pandas`）。建议使用项目内虚拟环境，避免与系统 Python 冲突：

```bash
cd claude-camp-w3
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

---

## 如何运行

### 推荐：虚拟环境中的 Python

```bash
cd claude-camp-w3
.venv/bin/python csv_student_analyzer.py
```

默认读取同目录下的 `users_sample.csv`，结果写入 `report.json`。

### 指定输入 / 输出文件

```bash
.venv/bin/python csv_student_analyzer.py -i users_sample.csv -o report.json
```

### 可选：一键脚本

若已创建 `.venv`，也可使用（会自动创建 venv 并安装依赖）：

```bash
./run_analyzer.sh
```

---

## 运行示例

终端可能显示：

```text
已分析 users_sample.csv，共 20 人
对赌完成率：30.00%（6/20）
报告已保存：/path/to/claude-camp-w3/report.json
```

`report.json` 结构示例：

```json
{
  "总人数": 20,
  "各国家人数": {
    "中国": 10,
    "美国": 1
  },
  "对赌完成人数": 6,
  "对赌完成率": 0.3
}
```

---

## 注意事项

1. **请用虚拟环境里的 Python**  
   直接执行 `python3 csv_student_analyzer.py` 若报错 `No module named 'pandas'`，说明当前解释器未安装依赖，应改用 `.venv/bin/python`（见上文「环境准备」）。

2. **CSV 列名与编码**  
   缺少任一必需列会抛出错误；文件需为 UTF-8，且第一行为表头。

3. **对赌完成率口径**  
   仅将「对赌状态」**精确等于** `已达成` 的记录计为完成；其它状态（进行中、待确认等）不计入完成人数。

4. **空文件**  
   若 CSV 无数据行，总人数为 0，完成率为 `0.0`。

5. **输出覆盖**  
   每次运行会**覆盖** `-o` 指定的 `report.json`（默认为同目录 `report.json`）。

6. **`.venv` 目录**  
   虚拟环境仅本地使用，一般不必提交到 Git；换机器后需重新执行「环境准备」。

---

## 目录文件

| 文件 | 说明 |
|------|------|
| `csv_student_analyzer.py` | 分析脚本 |
| `users_sample.csv` | 示例学员数据（20 条） |
| `report.json` | 运行后生成的统计报告 |
| `requirements.txt` | Python 依赖 |
| `run_analyzer.sh` | 可选：自动使用 venv 运行 |
| `.venv/` | 本地虚拟环境（执行环境准备后出现） |

---

## 环境说明

- 使用 **Python 3**。
- 统计分析依赖 **Pandas 2.x**（见 `requirements.txt`）。
