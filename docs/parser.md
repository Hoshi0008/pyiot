# parser.py — DSL 二进制协议解析器

## 模块功能

`parser.py` 提供唯一函数 `dsl_parser`：通过一种类正则的 DSL（领域特定语言）字符串描述二进制帧结构，对原始字节流进行匹配、校验与字段提取，最终返回「字段名 → 值」的映射字典。适用于解析固定/半固定格式的协议帧（如 PN532、自定义串口协议）。

## dsl_parser

```python
def dsl_parser(raw: bytes, definition: str, constraints: list, assignments: list,
               mapping: tuple | list, endian: bool = True) -> dict | None
```

### 参数

| 参数 | 类型 | 说明 |
|---|---|---|
| `raw` | `bytes` | 待解析的原始字节数据 |
| `definition` | `str` | DSL 结构定义字符串，描述帧中每个字段的类型与重复次数，语法见 [DSL 语法参考](DSL.md) |
| `constraints` | `list` | 约束表达式列表，每个元素为字符串表达式，在 `raw` 与 `sum` 环境下求值；任一结果为假则解析失败返回 `None`（典型用法：校验和校验） |
| `assignments` | `list` | 赋值表达式列表，形式为 `name=表达式`（如 `n=raw[3]-1`），在 `raw` 与 `sum` 环境下求值，结果供 `definition` 中的 `{name}` 重复计数使用 |
| `mapping` | `tuple \| list` | 字段名列表，按顺序对应 `definition` 中的每个元素（常量段与类型段各占一个名字） |
| `endian` | `bool` | 字节序：`True`（默认）为大端，`False` 为小端，影响多字节字段的整数值转换 |

### 返回值

- **成功**：`dict`，字段名 → 值。类型段为 `int`；常量段单个常量为 `int`、多个常量为 `list[int]`。
- **失败**：`None`。失败原因包括：约束不满足、常量段与数据不匹配、数据长度不足（读取越界）。

### 解析流程

1. 按列表顺序执行 `assignments` 中的全部赋值，结果存入赋值表；
2. 逐一执行 `constraints`，任一为假则直接返回 `None`；
3. 按 `definition` 从左到右逐元素解析：
   - **常量段 `(...)`**：对括号内表达式 `eval` 求值（含逗号视为元组 → 常量列表；否则为单常量），要求 `raw` 当前位置的连续字节与常量完全一致，不一致返回 `None`；成功后按 `size` 将常量存入映射表（多常量存列表，单常量存单值）；
   - **类型段 `B/W/D/Q`**（可带 `{n}` 或 `{name}`）：按类型宽度读取字节，用 `int.from_bytes` 依 `endian` 转为整数存入映射表；
   - 遇到其他字符抛 `ValueError`，未知类型字母抛 `TypeError`；
4. 收尾：将映射表中残留的 `bytes` 值转换——单字节 → `int`，多字节 → `list[int]`；
5. 返回映射表。

### 说明与注意事项

- **`eval` 安全性**：`assignments`、`constraints`、常量段表达式均通过 `eval` 求值，且环境暴露了 `raw` 与 `sum`。**不要**将不可信的外部输入传入这些参数，存在任意代码执行风险。
- **重复段的映射行为**：`B{n}` 会消耗 n 个字节，但循环中每次迭代都用同一个字段名覆盖写入，**最终只保留最后一次匹配的值**（参考 `main.py` 中 `data` 字段）。
- `{name}` 中的 `name` 必须已由 `assignments` 定义，否则抛 `KeyError`；内容以数字开头但不是纯数字时抛 `ValueError`。
- 重复次数 ≤ 0 时，该字段映射值为空列表 `[]`。
- `mapping` 长度需不小于 `definition` 的元素个数，否则抛 `IndexError`；多余的名字不会被赋值。
- 解析过程中 `raw` 指针越界（数据不足）时返回 `None`。
