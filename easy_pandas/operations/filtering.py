"""
Filtering operations for easy_pandas
Handles all filter-related operations
"""

import pandas as pd
from typing import Dict, Any


class FilterOperations:
    """Handles filtering operations on DataFrames"""
    
    @staticmethod
    def apply(df: pd.DataFrame, operation_dict: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply filter operations to a DataFrame
        
        Args:
            df: The DataFrame to filter
            operation_dict: Dictionary containing filter specifications
            
        Returns:
            Filtered DataFrame
        """
        conditions = operation_dict.get('conditions', [])
        logic = operation_dict.get('logic', 'and')
        
        if not conditions:
            return df
        
        # Build filter mask
        masks = []
        for condition in conditions:
            mask = FilterOperations._build_condition_mask(df, condition)
            masks.append(mask)
        
        # Combine masks with logical operator
        if logic == 'and':
            final_mask = masks[0]
            for mask in masks[1:]:
                final_mask = final_mask & mask
        else:  # or
            final_mask = masks[0]
            for mask in masks[1:]:
                final_mask = final_mask | mask
        
        return df[final_mask]
    
    @staticmethod
    def _build_condition_mask(df: pd.DataFrame, condition: Dict[str, Any]) -> pd.Series:
        """Build a boolean mask for a single condition"""
        column = condition['column']
        operator = condition['operator']
        value = condition['value']
        
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        
        col_data = df[column]
        
        # Handle different operators
        if operator == '==':
            return col_data == value
        elif operator == '!=':
            return col_data != value
        elif operator == '>':
            return col_data > value
        elif operator == '<':
            return col_data < value
        elif operator == '>=':
            return col_data >= value
        elif operator == '<=':
            return col_data <= value
        elif operator == 'contains':
            return col_data.astype(str).str.contains(str(value), case=False, na=False)
        elif operator == 'startswith':
            return col_data.astype(str).str.startswith(str(value), na=False)
        elif operator == 'endswith':
            return col_data.astype(str).str.endswith(str(value), na=False)
        elif operator == 'isin':
            # Value should be a list
            if not isinstance(value, (list, tuple)):
                value = [value]
            return col_data.isin(value)
        elif operator == 'notin':
            if not isinstance(value, (list, tuple)):
                value = [value]
            return ~col_data.isin(value)
        elif operator == 'isna':
            return col_data.isna()
        elif operator == 'notna':
            return col_data.notna()
        elif operator == 'between':
            # Value should be a tuple/list of (min, max)
            if isinstance(value, (list, tuple)) and len(value) == 2:
                return col_data.between(value[0], value[1])
            else:
                raise ValueError(f"Between operator requires a tuple of (min, max), got {value}")
        else:
            raise ValueError(f"Unknown operator: {operator}")
