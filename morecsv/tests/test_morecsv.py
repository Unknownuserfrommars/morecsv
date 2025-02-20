# tests/test_morecsv.py
# This is quite outdated too, I have to make sure I write a new one before the v1.0.0 release. -- Author
import os
import pandas as pd
import pytest
from ..morecsv import CSVProcessor


@pytest.fixture
def test_file():
    # 创建一个临时 CSV 文件用于测试
    test_file = 'test.csv'
    data = {
        'col1': [1, 2, 3],
        'col2': [4, 5, 6]
    }
    df = pd.DataFrame(data)
    df.to_csv(test_file, index=False)
    yield test_file
    # 测试结束后删除临时文件
    if os.path.exists(test_file):
        os.remove(test_file)


def test_get(test_file):
    # 测试 get 方法
    file = CSVProcessor(test_file)
    file.get()
    assert not file.data.empty


def test_add_columns(test_file):
    # 测试 add_columns 方法
    file = CSVProcessor(test_file)
    file.get()
    new_columns = ['new_col1', 'new_col2']
    file.add_columns(new_columns)
    for col in new_columns:
        assert col in file.data.columns


def test_del_columns(test_file):
    # 测试 del_columns 方法
    file = CSVProcessor(test_file)
    file.get()
    column_to_delete = 'col1'
    file.del_columns(column_to_delete)
    assert column_to_delete not in file.data.columns


def test_combine(test_file):
    # 测试 combine 静态方法
    file1 = test_file
    file2 = 'test2.csv'
    data2 = {
        'col3': [7, 8, 9],
        'col4': [10, 11, 12]
    }
    df2 = pd.DataFrame(data2)
    df2.to_csv(file2, index=False)

    combined_df = CSVProcessor.combine(file1, file2, axis=1)
    assert len(combined_df.columns) == 4

    # 清理第二个临时文件
    if os.path.exists(file2):
        os.remove(file2)


def test_create_csv():
    # 测试 create_csv 静态方法
    new_file = 'new_test.csv'
    headers = ['header1', 'header2']
    CSVProcessor.create_csv(new_file, headers)
    assert os.path.exists(new_file)
    df = pd.read_csv(new_file)
    assert list(df.columns) == headers
    # 清理临时文件
    if os.path.exists(new_file):
        os.remove(new_file)


def test_rename_columns(test_file):
    # 测试 rename_columns 方法
    file = CSVProcessor(test_file)
    file.get()
    new_column_names = ['new_col1', 'new_col2']
    file.rename_columns(new_column_names)
    assert list(file.data.columns) == new_column_names
