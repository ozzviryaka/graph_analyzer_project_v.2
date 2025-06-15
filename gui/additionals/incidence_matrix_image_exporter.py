import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional

class IncidenceMatrixImageExporter:
    """
    Exports an incidence matrix as a PNG image.
    """
    @staticmethod
    def export(matrix: List[List[int]], file_path: str, row_names: Optional[List[str]] = None, col_names: Optional[List[str]] = None):
        """
        Exports the given incidence matrix as a PNG image.
        Args:
            matrix (List[List[int]]): The incidence matrix to export.
            file_path (str): The path to the PNG file to write.
            row_names (Optional[List[str]]): Names for the rows (vertices).
            col_names (Optional[List[str]]): Names for the columns (edges).
        """
        arr = np.array(matrix)
        fig, ax = plt.subplots(figsize=(max(6, arr.shape[1] * 0.5), max(6, arr.shape[0] * 0.5)))
        im = ax.imshow(arr, cmap='Greens', interpolation='nearest')
        plt.colorbar(im, ax=ax)
        if col_names:
            ax.set_xticks(np.arange(len(col_names)))
            ax.set_xticklabels(col_names, rotation=45, ha='right')
        if row_names:
            ax.set_yticks(np.arange(len(row_names)))
            ax.set_yticklabels(row_names)
        ax.set_xlabel('Columns')
        ax.set_ylabel('Rows')
        plt.tight_layout()
        plt.savefig(file_path, dpi=200)
        plt.close(fig)
