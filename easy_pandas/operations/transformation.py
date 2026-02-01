"""
Transformation operations for easy_pandas
Handles column selection, renaming, and other transformations
"""

import pandas as pd
from typing import Dict, Any


class TransformationOperations:
    """Handles transformation operations on DataFrames"""
    
    @staticmethod
    def apply(df: pd.DataFrame, operation_dict: Dict[str, Any], **kwargs) -> pd.DataFrame:
        """
        Apply transformation operations to a DataFrame
        
        Args:
            df: The DataFrame to transform
            operation_dict: Dictionary containing transformation specifications
            **kwargs: Additional arguments for specific operations
            
        Returns:
            Transformed DataFrame
        """
        operation = operation_dict.get('operation')
        
        if operation == 'select':
            return TransformationOperations._apply_select(df, operation_dict)
        elif operation == 'rename':
            return TransformationOperations._apply_rename(df, operation_dict)
        elif operation == 'drop':
            return TransformationOperations._apply_drop(df, operation_dict)
        elif operation == 'append':
            return TransformationOperations._apply_append(df, operation_dict, **kwargs)
        else:
            raise ValueError(f"Unknown transformation operation: {operation}")
    
    @staticmethod
    def _apply_select(df: pd.DataFrame, operation_dict: Dict[str, Any]) -> pd.DataFrame:
        """Select specific columns"""
        columns = operation_dict.get('columns', [])
        
        if not columns:
            return df
        
        # Verify columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
        
        return df[columns]
    
    @staticmethod
    def _apply_rename(df: pd.DataFrame, operation_dict: Dict[str, Any]) -> pd.DataFrame:
        """Rename columns"""
        mappings = operation_dict.get('mappings', {})
        
        if not mappings:
            return df
        
        # Verify old column names exist
        missing_cols = [col for col in mappings.keys() if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
        
        return df.rename(columns=mappings)
    
    @staticmethod
    def _apply_drop(df: pd.DataFrame, operation_dict: Dict[str, Any]) -> pd.DataFrame:
        """Drop columns"""
        columns = operation_dict.get('columns', [])
        
        if not columns:
            return df
        
        # Only drop columns that exist
        existing_cols = [col for col in columns if col in df.columns]
        
        if not existing_cols:
            return df
        
        return df.drop(columns=existing_cols)
    
    @staticmethod
    def _apply_append(df: pd.DataFrame, operation_dict: Dict[str, Any], **kwargs) -> pd.DataFrame:
        """Append another DataFrame"""
        other_name = operation_dict.get('other')
        other_df = kwargs.get('other')
        
        if other_df is None:
            raise ValueError(f"No DataFrame provided for append operation. Expected '{other_name}'")
        
        if not isinstance(other_df, pd.DataFrame):
            raise ValueError(f"'other' must be a pandas DataFrame, got {type(other_df)}")
        
        return pd.concat([df, other_df], ignore_index=True)
