import csv
from typing import List, Optional

class IncidenceMatrixExporter:
    """
    Exports an incidence matrix to a CSV file.
    """
    @staticmethod
    def export(matrix: List[List[int]], file_path: str, row_names: Optional[List[str]] = None, col_names: Optional[List[str]] = None):
        """
        Exports the given incidence matrix to a CSV file with optional row and column names.
        Args:
            matrix (List[List[int]]): The incidence matrix to export.
            file_path (str): The path to the CSV file to write.
            row_names (Optional[List[str]]): Names for the rows (vertices).
            col_names (Optional[List[str]]): Names for the columns (edges).
        """
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            if col_names:
                writer.writerow([''] + col_names)
            for idx, row in enumerate(matrix):
                if row_names:
                    writer.writerow([row_names[idx]] + row)
                else:
                    writer.writerow(row)
