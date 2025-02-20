# This part is where I list out all my brainstorming ideas and TODOs for the package. Some of them may never be implemented, but I'll keep them here for reference.
# I PROBABLY won't remove my brainstorms and TODOs even if I finished them. I'll just mark them as DONE. -- Author

# I don't know but maybe saving the data to the csv every time a change is made may not be quite a good idea.
# For example, in loops, if we are adding a row in each iteration, then saving the data in each iteration is not a good idea. It costs too much time.
# I may consider add an optional boolean parameter to the functions to save the data to the csv file or save to the self.data only.
# This needs to be marked as a TODO. -- Author (**IMPORTANT**)

# I might consider adding a log, to log the changes made to the csv file, starting from the reading of the file, adding columns, deleting columns, etc.
# This will help in debugging and tracking the changes made to the csv file.
# However, I am not sure where to store the log file. I think the default in C:\Users\username\morecsv\logs\morecsv.log is good.
# But the user should be able to change the log file path, if they want to. We'll have to store the log file path in a string variable.
# This marked as an optional TODO.
# What I can do is to just print the logs to the console. -- Author

# Currently, if you look at the source code, the data is stored as a pandas DataFrame, which may not be a good idea because this package is designed to work with csv files in an innovative way, so I may consider storing the data in some different ways.
# I may consider storing the data as a list of lists, or a list of dictionaries, or a list of tuples, or a list of namedtuples, or a list of dataclasses, or a list of objects of a custom class.
# I may consider adding an optional parameter to the class to store the data in different ways.
# This marked as an optional TODO. -- Author

# Wait, does `pd.read_csv()` (Current reading CSV function) supports web locations? If not, I may consider adding a function to read CSV files from the web.
# I know Windows supports mapping network drives, so I may consider adding a function to read CSV files from network drives.
# This marked as an optional TODO. -- Author

# Should I add some simple data analysis/visualization functions to the package? I am not sure about this. I think it's a good idea to keep the package simple and focused on working with CSV files.
# I may consider adding a function to plot the data in the DataFrame, but I am not sure about this. Matplotlib or Plotly does it well.
# But I think, this package is designed to enhance the CSV builtin package in python, which doesn't have the ability (at least, i think so) to plot the data.
# This marked as a TODO. -- Author

# What's more, I think another important feature to add is the ability to read the data from the csv file in chunks. This is useful when working with large csv files.
# I now have the function to save the csv file in chunks, but I don't have the function to read the csv file in chunks.
# This marked as an optional TODO. -- Author

# Whoa we need a read function to print the data as a pandas.DataFrame. This is important.
# This is marked as a TODO. -- Author (**IMPORTANT**)

# ABOVE ARE THE BRAINSTORMS DURING THE V0.3.0 DEVELOPMENT PERIOD.

# Leave some space for further brainstorming and TODOs.

# MAIN CODE BELOW ↓↓↓

import csv
import concurrent.futures
import pandas as pd
import numpy as np

class CSVProcessor:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.data = pd.DataFrame()
        self.is_empty: bool = False

    def _save_data(self):
        """
        Probably the most important function in the class. This function saves the data to the csv file.
        """
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

    def fill_column(self, column:str, fill_data:int|str|bool|float|list):
        if not isinstance(fill_data, (int, str, bool, float, list)):
            raise ValueError("Fill data must be an integer, string, boolean, or float.")
        if isinstance(fill_data, list):
            if len(fill_data) != len(self.data):
                raise ValueError("Length of fill data list must match the number of rows in the DataFrame.")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found.")
        self.data[column] = fill_data
        self._save_data()

    def fillna(self, column, value):
        """
        Fill missing values in the DataFrame with a specified value.

        :param column: The name of the column to fill missing values in.
        :param value: The value to use for filling missing data.
        """
        self.data[column].fillna(value, inplace=True)
        self._save_data()