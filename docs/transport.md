# transport.py — 传输层

## 模块功能

`transport.py` 定义传输层抽象基类 `Transport` 及其 UART 实现 `UartTransport`。传输层对上层（设备驱动）屏蔽底层通信细节（串口、I2C、SPI 等），提供统一的打开 / 关闭 / 读写接口，并支持 `with` 上下文管理。设备驱动可基于 `Transport` 接口编程，从而不依赖具体物理链路。

## Transport（抽象基类）

继承自 `abc.ABC`。所有传输实现必须实现下列抽象成员：

| 成员 | 类型 | 说明 |
|---|---|---|
| `open()` | 方法 | 打开连接，失败时抛出异常 |
| `close()` | 方法 | 关闭连接 |
| `is_open` | 只读属性 | 连接是否已打开 |
| `read(nbytes, timeout=None)` | 方法 | 读取数据：`UartTransport` 最多读取 `nbytes` 字节（超时返回已读到的部分）；I2C/SPI 实现应精确返回 `nbytes` 字节 |
| `write(data) -> int` | 方法 | 发送原始字节，返回实际写入的字节数 |

### 默认 / 可选行为

- `transfer(data) -> bytes`：全双工传输（同时收发），基类默认抛出 `NotImplementedError`，需要时由子类重写；
- `flush()`：清空输入 / 输出缓冲区，基类默认空操作（`pass`）；
- `wait()`：等待数据全部写完，基类默认抛出 `NotImplementedError`；
- 上下文管理器：`__enter__` 打开连接并返回自身，`__exit__` 关闭连接，因此支持 `with` 语句。

## UartTransport

基于 pyserial 的串口传输实现。

### 构造

```python
UartTransport(**kwargs)
```

`kwargs` 直接透传给 `serial.Serial(**kwargs)`（pyserial 构造参数，如 `port`、`baudrate`、`timeout`、`bytesize`、`parity` 等）。

### 成员

| 成员 | 说明 |
|---|---|
| `open()` / `close()` | 转发 `serial.Serial.open() / close()` |
| `is_open` | 转发 `serial.is_open` |
| `read(nbytes, timeout=None)` | 传入 `timeout` 时，临时修改 `serial.timeout` 完成读取后恢复原值；不传时按 pyserial 当前的超时设置读取；返回读到的字节（可能少于 `nbytes`） |
| `write(data) -> int` | 转发 `serial.write`，返回实际写入的字节数 |
| `flush()` | 依次调用 `reset_output_buffer()` 与 `reset_input_buffer()`，清空发送与接收缓冲 |
| `wait()` | 调用 `serial.flush()`，阻塞等待所有数据写入完成 |

### 使用示例

```python
from transport import UartTransport

with UartTransport(port="COM3", baudrate=115200, timeout=0.1) as t:
    t.write(b"\x00\x00\xff")
    resp = t.read(64)
```

## 依赖

- `pyserial`：`UartTransport` 使用 `serial` 模块，需要安装 `pyserial`。
