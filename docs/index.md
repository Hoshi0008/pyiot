# pyiot 项目文档

pyiot 是一个 Python IoT 设备交互项目。目前包含两部分核心代码：二进制协议解析（`parser.py`）与串口传输层（`transport.py`），另有一个尚未实现的 PN532（`pcr532`）设备子包占位。

## Python 文件一览与文档索引

| 源文件 | 内容 | 文档 |
|---|---|---|
| `__init__.py` | 根包标记，仅含编码声明，无实际代码 | — |
| `main.py` | 演示程序：用 `dsl_parser` 解析一段 PN532 UART 帧 | [main.md](main.md) |
| `parser.py` | DSL 二进制协议解析器 | [parser.md](parser.md) |
| `transport.py` | 传输层抽象 `Transport` 与串口实现 `UartTransport` | [transport.md](transport.md) |
| `device/__init__.py` | `device` 包标记，空 | [device/index.md](device/index.md) |
| `device/pcr532/__init__.py` | `pcr532` 子包标记，空 | [device/pcr532/index.md](device/pcr532/index.md) |
| `device/pcr532/driver.py` | 空占位模块 | [driver.md](device/pcr532/driver.md) |
| `device/pcr532/mode.py` | 空占位模块 | [mode.md](device/pcr532/mode.md) |
| `device/pcr532/frame.py` | 空占位模块 | [frame.md](device/pcr532/frame.md) |

## 补充参考

- [DSL 语法参考](DSL.md) — `parser.dsl_parser` 使用的帧结构描述语言语法
