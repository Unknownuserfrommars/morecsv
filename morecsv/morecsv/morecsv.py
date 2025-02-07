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

    @staticmethod
    def combine(filepath1: str, filepath2: str, axis=0, output_file: str = None):
        """
        Combine two CSV files into one.

        :param filepath1: Path to the first CSV file.
        :param filepath2: Path to the second CSV file.
        :param axis: 0 for vertical concatenation (rows), 1 for horizontal concatenation (columns).
        :param output_file: Path to the output CSV file. If None, the combined DataFrame is returned without saving.
        :return: A DataFrame containing the combined data if output_file is None, otherwise None.
        """
        try:
            df1 = pd.read_csv(filepath1)
            df2 = pd.read_csv(filepath2)

            if axis == 0:
                combined_data = pd.concat([df1, df2], axis=0, ignore_index=True)
            elif axis == 1:
                combined_data = pd.concat([df1, df2], axis=1)
            else:
                raise ValueError("Invalid axis value. Use 0 for vertical or 1 for horizontal concatenation.")

            if output_file:
                combined_data.to_csv(output_file, index=False)
                print(f"Combined data saved to {output_file}")
                return None
            else:
                return combined_data
        except FileNotFoundError:
            print("One or both of the input files were not found.")
        except Exception as e:
            print(f"An error occurred during combination: {e}")

    @staticmethod
    def create_csv(file_path: str, headers: list = None):
        """
        Create a blank CSV file.

        :param file_path: Path to the CSV file to be created.
        :param headers: Optional list of column headers. If provided, they will be written as the first row.
        """
        try:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if headers:
                    writer.writerow(headers)
            print(f"Blank CSV file created at {file_path}")
        except Exception as e:
            print(f"Error creating CSV file: {e}")

    def print_info(self):
        """
        Print information about the current DataFrame, including its shape and other details.
        """
        print(f"Data shape: {self.data.shape}")
        self.data.info()

    def rename_columns(self, new_column_name: list):
        """
        Rename the columns of the DataFrame.

        :param new_column_name: A list of new column names. The length of this list should match the number of existing columns.
        """
        if len(new_column_name) != len(self.data.columns):
            raise ValueError("The length of the new column names list must match the number of existing columns.")
        self.data.columns = new_column_name
        self._save_data()