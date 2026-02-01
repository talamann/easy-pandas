"""
Sorting operations for easy_pandas
Handles all sort-related operations
"""

import pandas as pd
from typing import Dict, Any, List


class SortOperations:
    """Handles sorting operations on DataFrames"""
    
    @staticmethod
    def apply(df: pd.DataFrame, operation_dict: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply sort operations to a DataFrame
        
        Args:
            df: The DataFrame to sort
            operation_dict: Dictionary containing sort specifications
            
        Returns:
            Sorted DataFrame
        """
        columns_spec = operation_dict.get('columns', [])
        
        if not columns_spec:
            return df
        
        # Extract column names and directions
        columns = []
        ascending = []
        
        for col_spec in columns_spec:
            col_name = col_spec['column']
            direction = col_spec.get('direction', 'asc')
            
            if col_name not in df.columns:
                raise ValueError(f"Column '{col_name}' not found in DataFrame")
            
            columns.append(col_name)
            ascending.append(direction == 'asc')
        
        return df.sort_values(by=columns, ascending=ascending)
