"""
Basic usage examples for easy_pandas
Demonstrates core functionality with practical examples
"""

from easy_pandas import EasyDataFrame
import pandas as pd


def example_basic_filtering():
    """Basic filtering examples"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Filtering")
    print("=" * 60)
    
    # Create sample data
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
        'age': [25, 30, 35, 28, 32, 45],
        'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin', 'London'],
        'salary': [50000, 60000, 75000, 55000, 70000, 80000]
    }
    df = EasyDataFrame(data)
    
    print("\nOriginal DataFrame:")
    print(df)
    
    # Filter by age
    print("\n\nFilter: age > 30")
    result = df.filter_age_greaterthan_30()
    print(result)
    
    # Filter by city
    print("\n\nFilter: city equals London")
    result = df.filter_city_equals_london()
    print(result)
    
    # Multiple conditions with AND
    print("\n\nFilter: age > 30 AND salary > 65000")
    result = df.filter_age_greaterthan_30_and_salary_greaterthan_65000()
    print(result)


def example_sorting():
    """Sorting examples"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 2: Sorting")
    print("=" * 60)
    
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'salary': [50000, 60000, 75000, 55000, 70000]
    }
    df = EasyDataFrame(data)
    
    print("\nOriginal DataFrame:")
    print(df)
    
    # Sort by single column
    print("\n\nSort by age (ascending):")
    result = df.sort_by_age()
    print(result)
    
    # Sort descending
    print("\n\nSort by salary (descending):")
    result = df.sort_by_salary_desc()
    print(result)
    
    # Sort by multiple columns
    print("\n\nSort by age (asc) then salary (desc):")
    result = df.sort_by_age_asc_and_salary_desc()
    print(result)


def example_aggregation():
    """Aggregation examples"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 3: Aggregation")
    print("=" * 60)
    
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
        'city': ['New York', 'London', 'New York', 'Tokyo', 'London', 'Paris'],
        'salary': [50000, 60000, 75000, 55000, 70000, 80000]
    }
    df = EasyDataFrame(data)
    
    print("\nOriginal DataFrame:")
    print(df)
    
    # Simple aggregation
    print("\n\nTotal salary (sum):")
    result = df.aggregate_salary_sum()
    print(result)
    
    print("\n\nAverage salary (mean):")
    result = df.aggregate_salary_mean()
    print(result)
    
    # Group by aggregation
    print("\n\nAverage salary by city:")
    result = df.groupby_city_and_aggregate_salary_mean()
    print(result)


def example_chaining():
    """Method chaining examples"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 4: Method Chaining")
    print("=" * 60)
    
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace'],
        'age': [25, 30, 35, 28, 32, 45, 29],
        'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin', 'London', 'Paris'],
        'salary': [50000, 60000, 75000, 55000, 70000, 80000, 65000],
        'department': ['IT', 'HR', 'IT', 'Sales', 'IT', 'HR', 'Sales']
    }
    df = EasyDataFrame(data)
    
    print("\nOriginal DataFrame:")
    print(df)
    
    # Complex chain: filter, sort, select
    print("\n\nChain: Filter age > 28, sort by salary desc, select name and salary:")
    result = (df
        .filter_age_greaterthan_28()
        .sort_by_salary_desc()
        .select_name_and_salary()
    )
    print(result)
    
    # Another chain
    print("\n\nChain: Filter IT department, sort by age, select name, age, salary:")
    result = (df
        .filter_department_equals_it()
        .sort_by_age()
        .select_name_and_age_and_salary()
    )
    print(result)


def example_string_operations():
    """String operation examples"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 5: String Operations")
    print("=" * 60)
    
    data = {
        'name': ['Alice Smith', 'Bob Johnson', 'Charlie Brown', 'David Wilson', 'Eve Davis'],
        'email': ['alice@gmail.com', 'bob@yahoo.com', 'charlie@gmail.com', 'david@outlook.com', 'eve@gmail.com'],
        'city': ['New York', 'New Jersey', 'Los Angeles', 'San Francisco', 'New Orleans']
    }
    df = EasyDataFrame(data)
    
    print("\nOriginal DataFrame:")
    print(df)
    
    # Contains
    print("\n\nFilter: name contains 'Smith':")
    result = df.filter_name_contains_smith()
    print(result)
    
    # Starts with
    print("\n\nFilter: city starts with 'New':")
    result = df.filter_city_startswith_new()
    print(result)
    
    # Ends with
    print("\n\nFilter: email ends with 'gmail.com':")
    result = df.filter_email_endswith_gmail()
    print(result)


def example_column_selection():
    """Column selection examples"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 6: Column Selection")
    print("=" * 60)
    
    data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'London', 'Paris'],
        'salary': [50000, 60000, 75000],
        'department': ['IT', 'HR', 'IT']
    }
    df = EasyDataFrame(data)
    
    print("\nOriginal DataFrame:")
    print(df)
    
    # Select specific columns
    print("\n\nSelect: name and salary:")
    result = df.select_name_and_salary()
    print(result)
    
    print("\n\nSelect: name, age, and city:")
    result = df.select_name_and_age_and_city()
    print(result)


def example_real_world_scenario():
    """Real-world scenario example"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 7: Real-World Scenario - Employee Analysis")
    print("=" * 60)
    
    # Create employee data
    data = {
        'employee_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack'],
        'age': [25, 30, 35, 28, 32, 45, 29, 38, 27, 33],
        'department': ['IT', 'HR', 'IT', 'Sales', 'IT', 'HR', 'Sales', 'IT', 'Sales', 'HR'],
        'salary': [50000, 60000, 75000, 55000, 70000, 80000, 65000, 85000, 58000, 72000],
        'yearsexp': [2, 5, 10, 3, 7, 20, 4, 12, 3, 8]
    }
    df = EasyDataFrame(data)
    
    print("\nEmployee Database:")
    print(df)
    
    # Scenario 1: Find senior IT employees with high salaries
    print("\n\nScenario 1: Senior IT employees (age > 30, salary > 70000)")
    result = (df
        .filter_department_equals_it()
        .filter_age_greaterthan_30()
        .filter_salary_greaterthan_70000()
        .sort_by_salary_desc()
        .select_name_and_age_and_salary_and_yearsexp()
    )
    print(result)
    
    # Scenario 2: Average salary by department
    print("\n\nScenario 2: Average salary by department")
    result = df.groupby_department_and_aggregate_salary_mean()
    print(result)
    
    # Scenario 3: Young high performers (age < 30, salary > 60000)
    print("\n\nScenario 3: Young high performers (age < 30, salary > 60000)")
    result = (df
        .filter_age_lessthan_30()
        .filter_salary_greaterthan_60000()
        .sort_by_age()
        .select_name_and_age_and_department_and_salary()
    )
    print(result)


def example_pandas_compatibility():
    """Pandas compatibility examples"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 8: Pandas Compatibility")
    print("=" * 60)
    
    data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'salary': [50000, 60000, 75000]
    }
    df = EasyDataFrame(data)
    
    print("\nEasyDataFrame:")
    print(df)
    
    # Convert to pandas
    print("\n\nConvert to pandas DataFrame:")
    pandas_df = df.to_pandas()
    print(type(pandas_df))
    print(pandas_df)
    
    # Access underlying DataFrame
    print("\n\nAccess underlying DataFrame:")
    print(df.df)
    
    # Use pandas methods
    print("\n\nUse pandas describe():")
    print(df.describe())
    
    # Mix easy_pandas and pandas operations
    print("\n\nMix operations: Easy filter + pandas head(2):")
    result = df.filter_age_greaterthan_25().head(2)
    print(result)


if __name__ == "__main__":
    # Run all examples
    example_basic_filtering()
    example_sorting()
    example_aggregation()
    example_chaining()
    example_string_operations()
    example_column_selection()
    example_real_world_scenario()
    example_pandas_compatibility()
    
    print("\n\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
