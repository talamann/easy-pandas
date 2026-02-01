"""
Aggregation operations for easy_pandas
Handles all aggregation and groupby operations
"""

import pandas as pd
from typing import Dict, Any


class AggregationOperations:
    """Handles aggregation operations on DataFrames"""
    
    @staticmethod
    def apply(df: pd.DataFrame, operation_dict: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply aggregation operations to a DataFrame
        
        Args:
            df: The DataFrame to aggregate
            operation_dict: Dictionary containing aggregation specifications
            
        Returns:
            Aggregated DataFrame or Series
        """
        operation = operation_dict.get('operation')
        
        if operation == 'groupby':
            return AggregationOperations._apply_groupby(df, operation_dict)
        elif operation == 'aggregate':
            return AggregationOperations._apply_aggregate(df, operation_dict)
        else:
            raise ValueError(f"Unknown aggregation operation: {operation}")
    
    @staticmethod
    def _apply_groupby(df: pd.DataFrame, operation_dict: Dict[str, Any]) -> pd.DataFrame:
        """Apply groupby operation"""
        groupby_cols = operation_dict.get('columns', [])
        aggregations = operation_dict.get('aggregations', [])
        
        if not groupby_cols:
            raise ValueError("No groupby columns specified")
        
        # Verify columns exist
        for col in groupby_cols:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in DataFrame")
        
        grouped = df.groupby(groupby_cols)
        
        if not aggregations:
            # No specific aggregation, return grouped object as DataFrame
            return grouped.size().reset_index(name='count')
        
        # Apply aggregations
        agg_dict = {}
        for agg_spec in aggregations:
            col = agg_spec.get('column')
            func = agg_spec.get('function', 'sum')
            
            if col and col in df.columns:
                agg_dict[col] = func
        
        if agg_dict:
            result = grouped.agg(agg_dict).reset_index()
        else:
            result = grouped.size().reset_index(name='count')
        
        return result
    
    @staticmethod
    def _apply_aggregate(df: pd.DataFrame, operation_dict: Dict[str, Any]) -> Any:
        """Apply simple aggregation operation"""
        aggregations = operation_dict.get('aggregations', [])
        
        if not aggregations:
            return df
        
        results = {}
        for agg_spec in aggregations:
            col = agg_spec.get('column')
            func = agg_spec.get('function', 'sum')
            
            if col:
                if col not in df.columns:
                    raise ValueError(f"Column '{col}' not found in DataFrame")
                
                # Apply aggregation function
                if func == 'sum':
                    results[f'{col}_{func}'] = df[col].sum()
                elif func == 'mean':
                    results[f'{col}_{func}'] = df[col].mean()
                elif func == 'count':
                    results[f'{col}_{func}'] = df[col].count()
                elif func == 'min':
                    results[f'{col}_{func}'] = df[col].min()
                elif func == 'max':
                    results[f'{col}_{func}'] = df[col].max()
                elif func == 'std':
                    results[f'{col}_{func}'] = df[col].std()
                elif func == 'var':
                    results[f'{col}_{func}'] = df[col].var()
                elif func == 'median':
                    results[f'{col}_{func}'] = df[col].median()
                elif func == 'nunique':
                    results[f'{col}_{func}'] = df[col].nunique()
                elif func == 'first':
                    results[f'{col}_{func}'] = df[col].iloc[0] if len(df) > 0 else None
                elif func == 'last':
                    results[f'{col}_{func}'] = df[col].iloc[-1] if len(df) > 0 else None
                else:
                    raise ValueError(f"Unknown aggregation function: {func}")
        
        # Return as Series or single value
        if len(results) == 1:
            return list(results.values())[0]
        return pd.Series(results)
