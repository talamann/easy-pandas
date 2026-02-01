# Easy Pandas

A declarative Python library built on top of pandas that uses human-readable function names to perform data operations. Inspired by ActiveQuery patterns in PHP, Easy Pandas makes data manipulation more intuitive and expressive.

## Installation

```bash
pip install easy_pandas
```

Or install from source:

```bash
git clone https://github.com/yourusername/easy_pandas.git
cd easy_pandas
pip install -e .
```

## Quick Start

```python
from easy_pandas import EasyDataFrame
import pandas as pd

# Create an EasyDataFrame from a regular pandas DataFrame
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 35, 28, 32],
    'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin'],
    'salary': [50000, 60000, 75000, 55000, 70000]
}
df = EasyDataFrame(data)

# Use human-readable function names!
result = df.filter_age_greaterthan_30()
print(result)
```

## Features

### 🎯 Declarative Function Names

Write data operations using natural, human-readable function names:

```python
# Filter data
df.filter_age_greaterthan_25()
df.filter_city_equals_london()
df.filter_name_contains_alice()

# Sort data
df.sort_by_age()
df.sort_by_salary_desc()
df.sort_by_age_asc_and_salary_desc()

# Aggregate data
df.aggregate_salary_sum()
df.groupby_city_and_aggregate_salary_mean()

# Select columns
df.select_name_and_age()

# Chain operations
df.filter_age_greaterthan_25().sort_by_salary_desc().select_name_and_salary()
```

### 🔗 Method Chaining

Chain multiple operations together for complex queries:

```python
result = (df
    .filter_age_greaterthan_25_and_city_equals_newyork()
    .sort_by_salary_desc()
    .select_name_and_age_and_salary()
)
```

### 🔄 Pandas Compatibility

Easy Pandas wraps pandas DataFrames, so you can:
- Convert back to pandas: `df.to_pandas()`
- Access the underlying DataFrame: `df.df`
- Use all standard pandas methods and properties

## Operation Types

### Filtering

Filter data using comparison and string operators:

```python
# Comparison operators
df.filter_age_equals_30()
df.filter_age_greaterthan_25()
df.filter_age_lessthan_40()
df.filter_age_greaterthanorequal_30()
df.filter_salary_between_50000_and_70000()

# String operators
df.filter_name_contains_alice()
df.filter_city_startswith_new()
df.filter_email_endswith_com()

# Null checks
df.filter_age_notna()
df.filter_city_isna()

# Multiple conditions
df.filter_age_greaterthan_25_and_city_equals_london()
df.filter_age_lessthan_30_or_salary_greaterthan_60000()
```

**Supported operators:**
- `equals`, `eq` → `==`
- `notequals`, `ne` → `!=`
- `greaterthan`, `gt` → `>`
- `lessthan`, `lt` → `<`
- `greaterthanorequal`, `gte` → `>=`
- `lessthanorequal`, `lte` → `<=`
- `contains` → String contains
- `startswith` → String starts with
- `endswith` → String ends with
- `isin` → Value in list
- `notin` → Value not in list
- `between` → Value between range
- `isna`, `isnull` → Is null/NA
- `notna`, `notnull` → Not null/NA

### Sorting

Sort by one or multiple columns:

```python
# Single column
df.sort_by_age()
df.sort_by_salary_desc()

# Multiple columns
df.sort_by_age_asc_and_salary_desc()
df.sort_by_city_and_name()
```

### Aggregation

Perform aggregations and group operations:

```python
# Simple aggregations
df.aggregate_salary_sum()
df.aggregate_age_mean()
df.aggregate_salary_max()

# Group by operations
df.groupby_city_and_aggregate_salary_mean()
df.groupby_city_and_aggregate_age_count()
```

**Supported aggregation functions:**
- `sum` → Sum of values
- `mean`, `avg`, `average` → Mean/average
- `count` → Count of values
- `min` → Minimum value
- `max` → Maximum value
- `std` → Standard deviation
- `var` → Variance
- `median` → Median value
- `nunique` → Number of unique values
- `first` → First value
- `last` → Last value

### Column Selection

Select specific columns:

```python
df.select_name_and_age()
df.select_name_and_city_and_salary()
```

### Column Operations

Rename or drop columns:

```python
# Rename columns
df.rename_old_name_to_new_name()

# Drop columns
df.drop_column1_and_column2()
```

### Joining

Join with other DataFrames:

```python
other_df = EasyDataFrame({'city': ['London', 'Paris'], 'country': ['UK', 'France']})

# Join operations
df.join_other_on_city(other=other_df)
df.leftjoin_other_on_city(other=other_df)
df.rightjoin_other_on_city(other=other_df)
df.outerjoin_other_on_city(other=other_df)
```

### Appending

Append DataFrames:

```python
df2 = EasyDataFrame({'name': ['Frank'], 'age': [40]})
df.appendto_other(other=df2)
```

## Advanced Examples

### Complex Filtering and Aggregation

```python
# Find high earners in specific cities
result = (df
    .filter_salary_greaterthan_60000_and_city_isin_london_paris()
    .groupby_city_and_aggregate_salary_mean()
)
```

### Multi-step Data Pipeline

```python
# Complete data transformation pipeline
result = (df
    .filter_age_greaterthan_25()
    .filter_salary_notna()
    .sort_by_salary_desc()
    .select_name_and_age_and_salary()
    .reset_index()
)
```

### Working with Strings

```python
# Filter by string patterns
tech_companies = (df
    .filter_company_contains_tech()
    .filter_email_endswith_com()
    .sort_by_name()
)
```

## Comparison with Standard Pandas

### Easy Pandas
```python
df.filter_age_greaterthan_30_and_city_equals_london().sort_by_salary_desc()
```

### Standard Pandas
```python
df[(df['age'] > 30) & (df['city'] == 'london')].sort_values('salary', ascending=False)
```

## API Reference

### EasyDataFrame

The main class that wraps pandas DataFrame.

**Constructor:**
```python
EasyDataFrame(data=None, **kwargs)
```

**Methods:**
- `to_pandas()` → Convert to pandas DataFrame
- All pandas DataFrame methods are available
- Dynamic declarative methods based on function names

**Properties:**
- `df` → Access underlying pandas DataFrame
- `columns` → DataFrame columns
- `index` → DataFrame index
- `shape` → DataFrame shape
- `dtypes` → Column data types
- `values` → DataFrame values

## Function Naming Convention

Function names follow this pattern:

```
<operation>_<column>_<operator>_<value>_<connector>_...
```

**Components:**
- **Operation**: `filter`, `sort`, `groupby`, `aggregate`, `select`, `join`, etc.
- **Column**: Name of the column to operate on
- **Operator**: Comparison or string operator
- **Value**: The value to compare against
- **Connector**: `and`, `or`, `by`, `to`, `on`, etc.

**Examples:**
- `filter_age_greaterthan_30`
- `sort_by_name_desc`
- `groupby_city_and_aggregate_salary_mean`
- `select_name_and_age_and_email`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Roadmap

- [ ] Add more aggregation functions
- [ ] Support for window functions
- [ ] Custom function registration
- [ ] Performance optimizations
- [ ] More comprehensive documentation
- [ ] Additional examples and tutorials

## Credits

Inspired by ActiveQuery patterns in PHP frameworks like Yii and Laravel.

Built with ❤️ using pandas.
