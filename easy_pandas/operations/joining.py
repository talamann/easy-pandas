"""
Joining operations for easy_pandas
Handles all join/merge operations
"""

import pandas as pd
from typing import Dict, Any


class JoinOperations:
    """Handles join operations on DataFrames"""
    
    @staticmethod
    def apply(df: pd.DataFrame, operation_dict: Dict[str, Any], **kwargs) -> pd.DataFrame:
        """
        Apply join operations to a DataFrame
        
        Args:
            df: The left DataFrame
            operation_dict: Dictionary containing join specifications
            **kwargs: Additional arguments, should contain 'other' DataFrame
            
        Returns:
            Joined DataFrame
        """
        join_type = operation_dict.get('join_type', 'inner')
        on_columns = operation_dict.get('on', [])
        other_name = operation_dict.get('other')
        
        # Get the other DataFrame from kwargs
        other_df = kwargs.get('other')
        if other_df is None:
            raise ValueError(f"No DataFrame provided for join operation. Expected '{other_name}'")
        
        if not isinstance(other_df, pd.DataFrame):
            raise ValueError(f"'other' must be a pandas DataFrame, got {type(other_df)}")
        
        # Determine join type
        how = 'inner'
        if join_type == 'left':
            how = 'left'
        elif join_type == 'right':
            how = 'right'
        elif join_type == 'outer':
            how = 'outer'
        
        # Perform join
        if on_columns:
            # Verify columns exist
            for col in on_columns:
                if col not in df.columns:
                    raise ValueError(f"Column '{col}' not found in left DataFrame")
                if col not in other_df.columns:
                    raise ValueError(f"Column '{col}' not found in right DataFrame")
            
            return df.merge(other_df, on=on_columns, how=how)
        else:
            # No specific columns, try to merge on index or common columns
            return df.merge(other_df, how=how)
