"""
Core module for easy_pandas
Contains the main EasyDataFrame class
"""

import pandas as pd
from typing import Any, Union
from .parser import FunctionNameParser
from .operations import (
    FilterOperations,
    SortOperations,
    AggregationOperations,
    JoinOperations,
    TransformationOperations
)


class EasyDataFrame:
    """
    A declarative wrapper around pandas DataFrame
    Supports human-readable function names for data operations
    """
    
    def __init__(self, data=None, **kwargs):
        """
        Initialize EasyDataFrame
        
        Args:
            data: Data to create DataFrame from (same as pandas.DataFrame)
            **kwargs: Additional arguments passed to pandas.DataFrame
        """
        if isinstance(data, pd.DataFrame):
            self._df = data.copy()
        elif isinstance(data, EasyDataFrame):
            self._df = data._df.copy()
        else:
            self._df = pd.DataFrame(data, **kwargs)
    
    def __getattr__(self, name: str) -> Any:
        """
        Intercept attribute access to handle declarative function names
        
        Args:
            name: The attribute/method name
            
        Returns:
            Result of the operation or DataFrame attribute
        """
        # First, try to get from underlying DataFrame
        if hasattr(self._df, name):
            attr = getattr(self._df, name)
            # If it's a method, wrap it to return EasyDataFrame
            if callable(attr):
                def wrapped_method(*args, **kwargs):
                    result = attr(*args, **kwargs)
                    if isinstance(result, pd.DataFrame):
                        return EasyDataFrame(result)
                    return result
                return wrapped_method
            return attr
        
        # Try to parse as a declarative function name
        try:
            operation_dict = FunctionNameParser.parse(name)
            
            # Return a callable that executes the operation
            def execute_operation(**kwargs):
                return self._execute_operation(operation_dict, **kwargs)
            
            return execute_operation
        except (ValueError, Exception):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def _execute_operation(self, operation_dict: dict, **kwargs) -> 'EasyDataFrame':
        """
        Execute a parsed operation on the DataFrame
        
        Args:
            operation_dict: Dictionary containing operation specifications
            **kwargs: Additional arguments for the operation
            
        Returns:
            New EasyDataFrame with the operation applied
        """
        operation = operation_dict.get('operation')
        
        if operation == 'filter':
            result = FilterOperations.apply(self._df, operation_dict)
        elif operation == 'sort':
            result = SortOperations.apply(self._df, operation_dict)
        elif operation in ('groupby', 'aggregate'):
            result = AggregationOperations.apply(self._df, operation_dict)
        elif operation == 'join':
            result = JoinOperations.apply(self._df, operation_dict, **kwargs)
        elif operation in ('select', 'rename', 'drop', 'append'):
            result = TransformationOperations.apply(self._df, operation_dict, **kwargs)
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        # Return as EasyDataFrame for chaining
        if isinstance(result, pd.DataFrame):
            return EasyDataFrame(result)
        else:
            # For aggregations that return scalar values or Series
            return result
    
    def to_pandas(self) -> pd.DataFrame:
        """
        Convert back to regular pandas DataFrame
        
        Returns:
            pandas DataFrame
        """
        return self._df.copy()
    
    @property
    def df(self) -> pd.DataFrame:
        """Access the underlying pandas DataFrame"""
        return self._df
    
    def __repr__(self) -> str:
        """String representation"""
        return f"EasyDataFrame(\n{self._df.__repr__()}\n)"
    
    def __str__(self) -> str:
        """String representation"""
        return self.__repr__()
    
    def __len__(self) -> int:
        """Length of DataFrame"""
        return len(self._df)
    
    def __getitem__(self, key):
        """Support indexing like regular DataFrame"""
        result = self._df[key]
        if isinstance(result, pd.DataFrame):
            return EasyDataFrame(result)
        return result
    
    def __setitem__(self, key, value):
        """Support item assignment"""
        self._df[key] = value
    
    # Expose common DataFrame properties
    @property
    def columns(self):
        """DataFrame columns"""
        return self._df.columns
    
    @property
    def index(self):
        """DataFrame index"""
        return self._df.index
    
    @property
    def shape(self):
        """DataFrame shape"""
        return self._df.shape
    
    @property
    def dtypes(self):
        """DataFrame dtypes"""
        return self._df.dtypes
    
    @property
    def values(self):
        """DataFrame values"""
        return self._df.values
    
    # Common methods that should return EasyDataFrame
    def copy(self) -> 'EasyDataFrame':
        """Create a copy of the EasyDataFrame"""
        return EasyDataFrame(self._df.copy())
    
    def reset_index(self, **kwargs) -> 'EasyDataFrame':
        """Reset index and return EasyDataFrame"""
        return EasyDataFrame(self._df.reset_index(**kwargs))
    
    def set_index(self, *args, **kwargs) -> 'EasyDataFrame':
        """Set index and return EasyDataFrame"""
        return EasyDataFrame(self._df.set_index(*args, **kwargs))
