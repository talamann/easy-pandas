"""
Function name parser for easy_pandas
Tokenizes and parses human-readable function names into operation dictionaries
"""

import re
from typing import Dict, List, Any, Tuple


class FunctionNameParser:
    """Parses declarative function names into structured operations"""
    
    # Operation keywords
    OPERATIONS = {
        'filter', 'select', 'sort', 'sortby', 'groupby', 'aggregate',
        'join', 'leftjoin', 'rightjoin', 'outerjoin', 'innerjoin',
        'rename', 'add', 'drop', 'append', 'appendto', 'transform'
    }
    
    # Comparison operators
    COMPARISONS = {
        'equals': '==',
        'eq': '==',
        'notequals': '!=',
        'ne': '!=',
        'greaterthan': '>',
        'gt': '>',
        'lessthan': '<',
        'lt': '<',
        'greaterthanorequal': '>=',
        'gte': '>=',
        'lessthanorequal': '<=',
        'lte': '<=',
        'contains': 'contains',
        'startswith': 'startswith',
        'endswith': 'endswith',
        'isin': 'isin',
        'notin': 'notin',
        'between': 'between',
        'isna': 'isna',
        'notna': 'notna',
        'isnull': 'isna',
        'notnull': 'notna'
    }
    
    # Aggregation functions
    AGGREGATIONS = {
        'sum', 'mean', 'avg', 'average', 'count', 'min', 'max',
        'std', 'var', 'median', 'first', 'last', 'nunique'
    }
    
    # Logical operators
    LOGICAL = {'and', 'or'}
    
    # Connectors
    CONNECTORS = {'by', 'to', 'from', 'with', 'on', 'as'}
    
    # Sort directions
    DIRECTIONS = {'asc', 'desc', 'ascending', 'descending'}
    
    @classmethod
    def parse(cls, function_name: str) -> Dict[str, Any]:
        """
        Parse a function name into an operation dictionary
        
        Args:
            function_name: The declarative function name
            
        Returns:
            Dictionary containing operation details
        """
        tokens = function_name.lower().split('_')
        
        if not tokens:
            raise ValueError(f"Invalid function name: {function_name}")
        
        # Determine primary operation
        operation = cls._extract_operation(tokens)
        
        if operation == 'filter':
            return cls._parse_filter(tokens)
        elif operation in ('sort', 'sortby'):
            return cls._parse_sort(tokens)
        elif operation == 'groupby':
            return cls._parse_groupby(tokens)
        elif operation == 'aggregate':
            return cls._parse_aggregate(tokens)
        elif operation in ('join', 'leftjoin', 'rightjoin', 'outerjoin', 'innerjoin'):
            return cls._parse_join(tokens, operation)
        elif operation == 'select':
            return cls._parse_select(tokens)
        elif operation in ('append', 'appendto'):
            return cls._parse_append(tokens)
        elif operation == 'rename':
            return cls._parse_rename(tokens)
        elif operation == 'drop':
            return cls._parse_drop(tokens)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    @classmethod
    def _extract_operation(cls, tokens: List[str]) -> str:
        """Extract the primary operation from tokens"""
        for token in tokens:
            if token in cls.OPERATIONS:
                return token
        raise ValueError(f"No valid operation found in tokens: {tokens}")
    
    @classmethod
    def _parse_filter(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse filter operations"""
        result = {
            'operation': 'filter',
            'conditions': [],
            'logic': 'and'
        }
        
        # Remove 'filter' from tokens
        tokens = [t for t in tokens if t != 'filter']
        
        # Split by logical operators
        condition_groups = cls._split_by_logical(tokens)
        
        for group, logic in condition_groups:
            condition = cls._parse_condition(group)
            if condition:
                result['conditions'].append(condition)
                if logic:
                    result['logic'] = logic
        
        return result
    
    @classmethod
    def _parse_condition(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse a single filter condition"""
        if len(tokens) < 2:
            return {}
        
        column = tokens[0]
        
        # Check for comparison operator
        for i, token in enumerate(tokens[1:], 1):
            if token in cls.COMPARISONS:
                operator = cls.COMPARISONS[token]
                # Value is everything after the operator
                value_tokens = tokens[i+1:]
                value = cls._parse_value(value_tokens)
                
                return {
                    'column': column,
                    'operator': operator,
                    'value': value
                }
        
        # Default to equals if no operator found
        value = cls._parse_value(tokens[1:])
        return {
            'column': column,
            'operator': '==',
            'value': value
        }
    
    @classmethod
    def _split_by_logical(cls, tokens: List[str]) -> List[Tuple[List[str], str]]:
        """Split tokens by logical operators (and/or)"""
        groups = []
        current_group = []
        current_logic = 'and'
        
        for token in tokens:
            if token in cls.LOGICAL:
                if current_group:
                    groups.append((current_group, current_logic))
                    current_group = []
                current_logic = token
            else:
                current_group.append(token)
        
        if current_group:
            groups.append((current_group, current_logic))
        
        return groups
    
    @classmethod
    def _parse_value(cls, tokens: List[str]) -> Any:
        """Parse value from tokens, attempting type conversion"""
        if not tokens:
            return None
        
        value_str = '_'.join(tokens)
        
        # Try to convert to number
        try:
            if '.' in value_str:
                return float(value_str)
            return int(value_str)
        except ValueError:
            pass
        
        # Check for boolean
        if value_str in ('true', 'yes'):
            return True
        if value_str in ('false', 'no'):
            return False
        
        # Return as string
        return value_str
    
    @classmethod
    def _parse_sort(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse sort operations"""
        result = {
            'operation': 'sort',
            'columns': []
        }
        
        # Remove operation tokens
        tokens = [t for t in tokens if t not in ('sort', 'sortby', 'by')]
        
        # Split by 'and'
        current_col = []
        
        for token in tokens:
            if token == 'and':
                if current_col:
                    col_info = cls._parse_sort_column(current_col)
                    result['columns'].append(col_info)
                    current_col = []
            else:
                current_col.append(token)
        
        if current_col:
            col_info = cls._parse_sort_column(current_col)
            result['columns'].append(col_info)
        
        return result
    
    @classmethod
    def _parse_sort_column(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse a single sort column specification"""
        direction = 'asc'
        column = None
        
        for token in tokens:
            if token in cls.DIRECTIONS:
                direction = 'asc' if token in ('asc', 'ascending') else 'desc'
            elif token not in cls.CONNECTORS:
                column = token
        
        return {
            'column': column or '_'.join(tokens),
            'direction': direction
        }
    
    @classmethod
    def _parse_groupby(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse groupby operations"""
        result = {
            'operation': 'groupby',
            'columns': [],
            'aggregations': []
        }
        
        # Find 'aggregate' keyword to split groupby columns from aggregations
        try:
            agg_idx = tokens.index('aggregate')
            groupby_tokens = tokens[1:agg_idx]  # Skip 'groupby'
            agg_tokens = tokens[agg_idx+1:]
        except ValueError:
            # No aggregation specified
            groupby_tokens = tokens[1:]
            agg_tokens = []
        
        # Parse groupby columns
        result['columns'] = [t for t in groupby_tokens if t not in cls.CONNECTORS and t != 'and']
        
        # Parse aggregations
        if agg_tokens:
            agg_info = cls._parse_aggregation_spec(agg_tokens)
            result['aggregations'].append(agg_info)
        
        return result
    
    @classmethod
    def _parse_aggregate(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse aggregate operations"""
        result = {
            'operation': 'aggregate',
            'aggregations': []
        }
        
        tokens = [t for t in tokens if t != 'aggregate']
        agg_info = cls._parse_aggregation_spec(tokens)
        result['aggregations'].append(agg_info)
        
        return result
    
    @classmethod
    def _parse_aggregation_spec(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse aggregation specification"""
        column = None
        func = 'sum'
        
        for token in tokens:
            if token in cls.AGGREGATIONS:
                func = 'mean' if token in ('avg', 'average') else token
            elif token not in cls.CONNECTORS:
                column = token
        
        return {
            'column': column,
            'function': func
        }
    
    @classmethod
    def _parse_join(cls, tokens: List[str], operation: str) -> Dict[str, Any]:
        """Parse join operations"""
        result = {
            'operation': 'join',
            'join_type': operation.replace('join', '') or 'inner',
            'other': None,
            'on': []
        }
        
        # Remove operation token
        tokens = [t for t in tokens if t not in cls.OPERATIONS]
        
        # First non-connector token is typically the other dataframe name
        for i, token in enumerate(tokens):
            if token not in cls.CONNECTORS:
                result['other'] = token
                tokens = tokens[i+1:]
                break
        
        # Remaining tokens after 'on' are join columns
        if 'on' in tokens:
            on_idx = tokens.index('on')
            result['on'] = [t for t in tokens[on_idx+1:] if t not in cls.CONNECTORS and t != 'and']
        
        return result
    
    @classmethod
    def _parse_select(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse select operations"""
        result = {
            'operation': 'select',
            'columns': []
        }
        
        tokens = [t for t in tokens if t not in ('select', 'and')]
        result['columns'] = tokens
        
        return result
    
    @classmethod
    def _parse_append(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse append operations"""
        result = {
            'operation': 'append',
            'other': None
        }
        
        tokens = [t for t in tokens if t not in ('append', 'appendto', 'to')]
        if tokens:
            result['other'] = '_'.join(tokens)
        
        return result
    
    @classmethod
    def _parse_rename(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse rename operations"""
        result = {
            'operation': 'rename',
            'mappings': {}
        }
        
        tokens = [t for t in tokens if t != 'rename']
        
        # Look for 'to' or 'as' to split old and new names
        if 'to' in tokens:
            to_idx = tokens.index('to')
            old_name = '_'.join(tokens[:to_idx])
            new_name = '_'.join(tokens[to_idx+1:])
            result['mappings'][old_name] = new_name
        elif 'as' in tokens:
            as_idx = tokens.index('as')
            old_name = '_'.join(tokens[:as_idx])
            new_name = '_'.join(tokens[as_idx+1:])
            result['mappings'][old_name] = new_name
        
        return result
    
    @classmethod
    def _parse_drop(cls, tokens: List[str]) -> Dict[str, Any]:
        """Parse drop operations"""
        result = {
            'operation': 'drop',
            'columns': []
        }
        
        tokens = [t for t in tokens if t not in ('drop', 'and')]
        result['columns'] = tokens
        
        return result
