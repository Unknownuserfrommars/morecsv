# morecsv

`morecsv` 是一个增强型的 CSV 处理库，旨在为用户提供更便捷、高效的 CSV 文件处理方式，支持自动数据类型处理、多线程读写、数据清洗等功能。

## 安装

你可以使用 `pip` 来安装 `morecsv`：
```bash
pip install morecsv
```

## 使用示例

### 读取 CSV 文件
```python
import morecsv

# 初始化 CSVProcessor 对象
file = morecsv.CSVProcessor('example.csv')

# 读取 CSV 文件
file.get(empty=True)
```

### 添加列
```python
file.add_columns(['new_col1', 'new_col2'])
```

### 删除列
```python
file.del_columns('column_to_delete')
```

### 多线程保存数据
```python
file.save_data_multithreaded()
```

### 填充NaN数据
```python
file.fillna('column', value=10)
```

## 功能特性

### 自动数据类型处理
在读取 CSV 文件时，自动推断数据类型，如将字符串转换为合适的数值类型。

### 多线程读写
支持多线程读取和写入 CSV 文件，提高处理大量数据时的性能。

### 数据操作
- **添加列**：可灵活添加单个或多个列，支持处理重复列名的情况。
- **删除列**：方便地删除指定列。

### 数据保存
- 支持单线程和多线程保存数据到 CSV 文件，多线程保存可加快大文件的保存速度。

## API 文档

###### This API Document is quite outdated. I need to major fix it before the v1.0.0 release. -- Author

### `CSVProcessor(file_path)`
- **参数**：
  - `file_path`：CSV 文件的路径。

### `get(empty=False)`
- **参数**：
  - `empty`：布尔值，当文件为空时，若设置为 `True` 则继续处理，否则抛出异常。
- **返回值**：无

### `add_columns(column_name, rows=None, overwrite=False)`
- **参数**：
  - `column_name`：要添加的列名，可以是字符串或字符串列表。
  - `rows`：可选参数，指定行数，默认为 `None`。当文件为空时，若未指定 `rows` 或 `rows` 小于 1，则默认行数为 1。
  - `overwrite`：布尔值，是否覆盖已存在的列，默认为 `False`。
- **返回值**：无

### `del_columns(column_name)`
- **参数**：
  - `column_name`：要删除的列名，必须为字符串。
- **返回值**：无

### `save_data_multithreaded(chunksize=1000)`
- **参数**：
  - `chunksize`：每个数据块的行数，默认为 1000。
- **返回值**：无

## 贡献指南

如果你想为 `morecsv` 项目做出贡献，请遵循以下步骤：

1. Fork 本项目。
2. 创建一个新的分支：`git checkout -b feature/your-feature-name`。
3. 提交你的更改：`git commit -m 'Add some feature'`。
4. 推送至分支：`git push origin feature/your-feature-name`。
5. 提交 Pull Request。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 更新日志

- v0.3.0 Release: Brainstorms (See source code and you'll know); New functions; Tiny bug fix.
- v0.2.0 Release: Minor bug fix; New functions.