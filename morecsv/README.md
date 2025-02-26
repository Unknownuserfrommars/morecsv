# morecsv

`morecsv` 是一个增强型的 CSV 处理库，旨在为用户提供更便捷、高效的 CSV 文件处理方式，支持自动数据类型处理、多线程读写、数据清洗等功能。
同时，`morecsv` 也支持将数据画出来

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

### 画图
```python
plot = Plot(file)
plot.plot('x', 'y')
plot.show()
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

### 画图
- 目前仅支持折线图，会在后续版本增加

## API 文档

### API 文档正在全面升级！~

## 贡献指南

如果你想为 `morecsv` 项目做出贡献，请遵循以下步骤：

1. Fork 本项目。
2. 创建一个新的分支：`git checkout -b feature/your-feature-name`。
3. 提交你的更改：`git commit -m 'Add some feature'`。
4. 推送至分支：`git push origin feature/your-feature-name`。
5. 提交 Pull Request。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
If the superlink doesn't work, please see the GitHub repo.

## 更新日志

- v0.4.0 Release: Logging implemented; Basic plotting class built-in main class; Tiny bug fix; Fixed the testings, for old tests please see older versions.
- v0.3.0 Release: Brainstorms (See source code and you'll know); New functions; Tiny bug fix.
- v0.2.0 Release: Minor bug fix; New functions.

### I really should offer a full Chinese and full English version of this...