# tests/test_morecsv.py
import os
from ..morecsv import CSVProcessor

def test_add_columns():
    # 创建一个临时 CSV 文件用于测试
    test_file = 'test.csv'
    with open(test_file, 'w', newline='') as f:
        f.write('col1,col2\n1,2\n3,4')

    try:
        # 初始化 CSVProcessor 对象
        file = CSVProcessor(test_file)
        file.get(empty=False)

        # 添加新列
        file.add_columns(['new_col'])

        # 验证新列是否添加成功
        assert 'new_col' in file.data.columns

    finally:
        # 删除临时文件
        if os.path.exists(test_file):
            os.remove(test_file)