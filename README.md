# Claude Camp W3 练习说明

本目录包含三个 Python 小项目：**CSV 学员数据分析器**、**JSON 配置文件读写器**、**带单元测试的字符串工具库**。

---

## 项目 1：CSV 学员数据分析器 `csv_student_analyzer.py`

**功能**：读取学员 CSV（含姓名、邮箱、加入日期、所在国家、对赌状态），用 Pandas 统计总人数、各国家人数、对赌完成率，并保存为 `report.json`。

**运行**（需安装 pandas，见 `requirements.txt`）：

```bash
cd claude-camp-w3
.venv/bin/python csv_student_analyzer.py
```

**示例**：默认分析 `users_sample.csv`，终端显示共 20 人、完成率 30%，同目录生成 `report.json`。

**注意**：请使用 `.venv/bin/python`，避免系统 Python 缺少 pandas；对赌完成仅统计状态为 `已达成` 的记录。

---

## 项目 2：JSON 配置文件读写器 `json_config_editor.py`

**功能**：读取 `config.json` 中的用户偏好（主题、语言、字体大小）；命令行菜单可查看或修改任意一项；校验通过后立即写回文件。若配置文件不存在，会自动生成默认 `config.json`。

**运行**（仅标准库，无需 pandas）：

```bash
cd claude-camp-w3
python3 json_config_editor.py
```

**示例**：启动后选 `2`（修改），再选 `1` 修改主题，输入 `dark` 后保存；选 `1` 可查看当前三项设置；选 `0` 退出。

**数据验证（加分项）**：

| 设置 | 规则 |
|------|------|
| 主题 | 仅允许 `light`、`dark`、`auto`（不区分大小写） |
| 语言 | 仅允许 `zh-CN`、`zh-TW`、`en-US`、`ja-JP`、`ko-KR` |
| 字体大小 | 整数，范围 **8～32**（含边界） |

输入不合法时只提示错误，不写入文件，程序继续运行。

**注意**：

- 每次成功修改后会**覆盖**保存 `config.json`（可用 `-c` 指定其它路径）。
- 启动时会校验已有配置；格式错误或取值越界会提示并退出。
- 修改时直接回车可取消当次操作。

---

## 项目 3：带单元测试的字符串工具库

**模块** `string_utils.py`：

| 函数 | 说明 |
|------|------|
| `reverse_words(s)` | 按空白分词后反转顺序，如 `"hello world"` → `"world hello"` |
| `count_vowels(s)` | 统计英文字母元音 a/e/i/o/u（大小写均计） |
| `is_palindrome(s)` | 忽略非字母数字与大小写后判断是否回文 |

**测试** `test_string_utils.py`：使用 pytest，每个函数至少 3 类用例（正常、边界、异常/特殊输入）。

**运行测试**：

```bash
cd claude-camp-w3
.venv/bin/pip install pytest   # 或 pip install -r requirements.txt
.venv/bin/python -m pytest test_string_utils.py -v
```

**示例**：`pytest` 应显示 16 passed（含各函数的正常、空串/单词、多余空格或非 str 参数等用例）。

---

## 环境准备（项目 1 首次）

```bash
cd claude-camp-w3
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

项目 2 不依赖第三方包，用系统 `python3` 即可。

---

## 目录文件

| 文件 | 说明 |
|------|------|
| `csv_student_analyzer.py` | 项目 1：CSV 分析 |
| `json_config_editor.py` | 项目 2：配置读写 |
| `string_utils.py` | 项目 3：字符串工具函数 |
| `test_string_utils.py` | 项目 3：pytest 测试 |
| `users_sample.csv` | 学员示例数据 |
| `config.json` | 用户偏好默认配置 |
| `report.json` | 项目 1 运行后生成的报告 |
| `requirements.txt` | 项目 1 依赖（pandas） |
| `run_analyzer.sh` | 可选：用 venv 运行项目 1 |

---

## 环境说明

- 使用 **Python 3**。
- 项目 1 依赖 **Pandas 2.x**；项目 2 仅用标准库；项目 3 测试依赖 **pytest**。
