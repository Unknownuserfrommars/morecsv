import csv
import concurrent.futures
import pandas as pd
import numpy as np

class CSVProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.DataFrame()
        self.is_empty:bool = False

    def _save_data(self):
        try:
            self.data.to_csv(self.file_path, index=False)
            print(f'Data saved to {self.file_path}')
        except Exception as e:
            print(f"Error: Failed to save the fileto {self.file_path}: {e}")

    def _save_chunk(self, chunk, chunk_index):
        if chunk_index == 0:
            mode = 'w'
        else:
            mode = 'a'
        chunk.to_csv(self.file_path, mode=mode, index=False, header=(chunk_index == 0))

    def get(self, empty:bool=False):
        attempts = 0
        while attempts < 3:
            try:
                print(f"Attempt read file {self.file_path}, Attempt #{attempts+1}")
                self.data = pd.read_csv(self.file_path)
                if self.data.empty:
                    if empty:
                        self.is_empty = True
                        print("File is empty, but proceeding as `empty=True` is set.")
                    else:
                        raise ValueError("File is empty. Set `empty=True` if you want to proceed.")
                print("Success")
                return
            except Exception as e:
                attempts += 1
                if attempts == 3:
                    print(f"Error: Failed to read the file: {e}")

    def get_with_csv(self, empty=False):
        data = []
        try:
            with open(self.file_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)
            if not data:
                if empty:
                    self.is_empty = True
                    print("File is empty, but proceeding as 'empty=True' is set.")
                else:
                    raise ValueError("File is empty. Set 'empty=True' if you want to proceed.")
            self.data = pd.DataFrame(data)
            print("Successfully read file using csv module")
        except Exception as e:
            print(f"Error reading file: {e}")
    
    def print_columns(self):
        if self.data.empty and not self.is_empty:
            raise Exception("File is empty. Or please use file.get() first.")
        if self.data.empty:
            print("File empty.")
        else:
            print(self.data.columns)

    def add_columns(self, column_name:str|list[str], rows:int=None, overwrite:bool=False):
        if isinstance(column_name, str):
            column_name = [column_name]
        
        if self.is_empty:
            if not isinstance(rows, int) or rows < 1:
                raise ValueError("File is empty, so rows must be a positive integer")
            new_data = pd.DataFrame(columns=column_name if isinstance(column_name, list) else [column_name],
                                    index=range(rows))
            self.data = pd.concat([self.data, new_data], axis=1)
        else:
            if overwrite:
                for col in column_name:
                    self.data[col] = None
            else:
                unique_cols = np.setdiff1d(column_name, self.data.columns)
                for col in unique_cols:
                    self.data[col] = None
        self._save_data()

    def del_columns(self, column_name:str):
        if not isinstance(column_name, str):
            raise ValueError("Column name must be a string.")
        if self.data.empty and not self.is_empty:
            raise Exception("File is empty. Or please use file.get() first.")
        if column_name in self.data.columns:
            self.data.drop(column_name, axis=1, inplace=True)
            self._save_data()
        else:
            print(f"Column '{column_name}' not found.")

    def save_data_multithreaded(self, chunksize=1000):
        try:
            data_length = len(self.data)
            num_chunks = data_length // chunksize + (1 if data_length % chunksize != 0 else 0)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for i in range(num_chunks):
                    start = i * chunksize
                    end = start + chunksize
                    chunk = self.data[start:end]
                    futures.append(executor.submit(self._save_chunk, chunk, i))
                for future in concurrent.futures.as_completed(futures):
                    future.result()
            print(f"Data saved to {self.file_path} using multithreading")
        except Exception as e:
            print(f"Error saving data using multithreading: {type(e).__name__}: {e}")