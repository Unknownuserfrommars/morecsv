# tests/test_morecsv.py
import unittest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from io import StringIO
import matplotlib.pyplot as plt
import plotly.express as px
from ..morecsv import CSVProcessor, Logger

class TestCSVProcessorAndPlot(unittest.TestCase):
    
    @patch('matplotlib.pyplot.show')  # Mock matplotlib's show method
    @patch('plotly.express.line')  # Mock Plotly's line function
    def test_csv_processor_and_plot(self, mock_plotly_line, mock_matplotlib_show):
        # Create a mock CSV dataset as string
        csv_data = """x,y
1,4
2,5
3,6"""
        
        # Simulate reading the CSV into a DataFrame
        csv_file_path = "test_data.csv"
        with open(csv_file_path, 'w') as f:
            f.write(csv_data)
        
        # Create an instance of CSVProcessor
        csv_processor = CSVProcessor(csv_file_path)
        csv_processor.get()  # Load the CSV data
        
        # Check if data was loaded correctly
        self.assertFalse(csv_processor.data.empty)
        self.assertEqual(list(csv_processor.data.columns), ['x', 'y'])
        
        # Modify the dataset by adding a new column
        csv_processor.add_columns("z", rows=3)
        self.assertIn("z", csv_processor.data.columns)  # Check if column 'z' is added
        
        # Modify data within the newly added column
        csv_processor.fill_column("z", [7, 8, 9])
        self.assertEqual(csv_processor.data["z"].tolist(), [7, 8, 9])
        
        # Log the data modifications
        csv_processor.logger.log(f"Column 'z' added and filled: {csv_processor.data['z'].tolist()}")
        
        # Now delete a column
        csv_processor.del_columns("z")
        self.assertNotIn("z", csv_processor.data.columns)  # Ensure column 'z' was deleted
        
        # Check if data is correctly saved
        csv_processor._save_data()
        self.assertTrue(os.path.exists(csv_file_path))  # Ensure file is saved

        # Plotting with Plotly
        mock_plotly_fig = MagicMock()
        mock_plotly_line.return_value = mock_plotly_fig
        
        plot = csv_processor.Plot(csv_processor, uses="plotly.express")
        plot.plot_line('x', 'y', title="Plotly Line Plot", x_title="X-axis", y_title="Y-axis")
        plot.show()
        
        # Assert Plotly plot.show() was called
        mock_plotly_fig.show.assert_called_once()
        
        # Plotting with Matplotlib
        plot.use_lib = 'matplotlib.pyplot'  # Switch to matplotlib
        plot.fig, plot.ax = plt.subplots()  # Mock axes
        plot.plot_line('x', 'y', title="Matplotlib Line Plot", x_title="X-axis", y_title="Y-axis")
        plot.show()
        
        # Assert Matplotlib plot.show() was called
        mock_matplotlib_show.assert_called_once()
        
        # Cleanup: Remove the test CSV file
        os.remove(csv_file_path)

if __name__ == '__main__':
    unittest.main()
