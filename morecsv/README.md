# morecsv

`morecsv` 是一个增强型的 CSV 处理库，旨在为用户提供更便捷、高效的 CSV 文件处理方式，支持自动数据类型处理、多线程读写、数据清洗等功能。
同时，`morecsv` 也支持将数据画出来。

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
- 支持多种图表类型：折线图、柱状图、直方图、散点图
- 支持两种绘图库：`plotly.express` 和 `matplotlib.pyplot`
- 支持自定义标题、轴标签等图表属性

## API 文档

### CSVProcessor 类

#### 初始化
```python
file = morecsv.CSVProcessor('example.csv', log_path=None)
```
- `file_path`: CSV文件路径
- `log_path`: 日志文件路径（可选）

#### 文件操作

##### get(empty=False)
从文件中读取数据
- `empty`: 是否允许空文件（默认False）

##### get_with_csv(empty=False)
使用Python内置csv模块读取数据
- `empty`: 是否允许空文件（默认False）

##### create_csv(file_path, headers=None)
创建新的CSV文件
- `file_path`: 新文件的路径
- `headers`: 列标题列表（可选）

#### 数据查看

##### print_info()
打印数据集信息，包括形状和详细信息

##### printdata()
打印整个数据集

##### printhead(rows=5)
打印数据集的前几行
- `rows`: 要显示的行数（默认5）

##### printtail(rows=5)
打印数据集的后几行
- `rows`: 要显示的行数（默认5）

##### print_columns()
打印所有列名

#### 数据操作

##### add_columns(column_name, rows=None, overwrite=False)
添加新列
- `column_name`: 列名（字符串或列表）
- `rows`: 空文件时指定行数
- `overwrite`: 是否覆盖已存在的列

##### del_columns(column_name)
删除列
- `column_name`: 要删除的列名

##### rename_columns(new_column_name)
重命名列
- `new_column_name`: 新列名列表

##### fill_column(column, fill_data)
填充列数据
- `column`: 列名
- `fill_data`: 填充值（整数、字符串、布尔值、浮点数或列表）

##### fillna(column, value)
填充缺失值
- `column`: 列名
- `value`: 填充值

#### 文件保存

##### save_data_multithreaded(chunksize=1000)
使用多线程保存数据
- `chunksize`: 每个块的大小

##### save_json(output_file, orient='records')
保存为JSON格式
- `output_file`: 输出文件路径
- `orient`: JSON格式（默认'records'）

##### save_excel(output_file, sheet_name='Sheet1', split_sheets=False, chunk_size=1000)
保存为Excel格式
- `output_file`: 输出文件路径
- `sheet_name`: 工作表名称
- `split_sheets`: 是否分割成多个工作表
- `chunk_size`: 每个工作表的行数

#### 文件合并

##### combine(filepath1, filepath2, axis=0, output_file=None)
合并两个CSV文件
- `filepath1`: 第一个文件路径
- `filepath2`: 第二个文件路径
- `axis`: 合并方向（0为纵向，1为横向）
- `output_file`: 输出文件路径（可选）

### Logger 类

#### 初始化
```python
logger = Logger(log_path="D:\\LogFiles\\")
```
- `log_path`: 日志文件路径（可选）

#### 方法

##### log(msg)
记录日志信息
- `msg`: 日志消息

##### default_log_path(place='main')
获取默认日志路径
- `place`: 'main'或'cwd'，确定日志文件位置

### CSVProcessor.Plot 类

#### 初始化
```python
plot = file.Plot(file, uses='plotly.express')  # 或 uses='matplotlib.pyplot'
```
- `uses`: 指定使用的绘图库，可选 'plotly.express' 或 'matplotlib.pyplot'
**请注意：使用CSVProcessor.Plot类时必须传入一个CSVProcessor类作为第一个参数**

#### 绘图方法

##### plot_line(x, y, title=None, x_title=None, y_title=None)
创建折线图
- `x`: x轴数据列名
- `y`: y轴数据列名
- `title`: 图表标题（可选）
- `x_title`: x轴标题（可选）
- `y_title`: y轴标题（可选）

##### plot_bar(x, y, title=None, x_title=None, y_title=None)
创建柱状图
- `x`: x轴数据列名
- `y`: y轴数据列名
- `title`: 图表标题（可选）
- `x_title`: x轴标题（可选）
- `y_title`: y轴标题（可选）

##### plot_histogram(column, bins=None, title=None, x_title=None, y_title="Count")
创建直方图
- `column`: 要创建直方图的数据列名
- `bins`: 直方图的箱数（可选）
- `title`: 图表标题（可选）
- `x_title`: x轴标题（可选）
- `y_title`: y轴标题（可选，默认为"Count"）

##### plot_scatter(x, y, color=None, title=None, x_title=None, y_title=None)
创建散点图
- `x`: x轴数据列名
- `y`: y轴数据列名
- `color`: 用于区分点颜色的列名（可选）
- `title`: 图表标题（可选）
- `x_title`: x轴标题（可选）
- `y_title`: y轴标题（可选）

##### show()
显示绘制的图表

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

## 数据类型支持

### 基础数据类型
- 数值型：整数、浮点数
- 文本型：字符串
- 布尔值：True/False
- 日期时间：支持标准日期时间格式

### 特殊数据处理
- 支持自动类型推断
- 支持空值(NaN)处理
- 支持重复值处理

## 文件格式支持

### 读取格式
- CSV文件（.csv）
- Excel文件（.xlsx）

### 导出格式
- CSV文件（.csv）
- Excel文件（.xlsx）
- JSON文件（.json）

## 性能优化

### 多线程支持
- 文件读取：支持大文件分块读取
- 文件保存：支持多线程并发写入

### 内存优化
- 支持数据分块处理
- 支持大文件分片保存

## 更新日志

### v1.0.0
- 新增多种可视化功能：柱状图、直方图、散点图
- 完善API文档
- 增加单元测试覆盖

### v0.4.0
- 实现日志功能
- 添加基础绘图类
- 修复若干bug
- 更新测试用例

### v0.3.0
- 新增多个功能
- 架构优化
- Bug修复

### v0.2.0
- Bug修复
- 新增基础功能

## 未来规划

### 数据分析增强
- 基础统计分析
- 数据透视功能
- 数据清洗工具

### 可视化增强
- 更多图表类型
- 交互式图表
- 自定义主题

### 性能优化
- 并行处理优化
- 内存使用优化
- IO性能提升

## 多语言支持

未来版本将提供完整的中文和英文文档支持。

## Github
[此处](https://github.com/Unknownuserfrommars/morecsv)可以查看（略微有些老旧的）Github repo