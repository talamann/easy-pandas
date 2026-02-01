"""
Quick demonstration of easy_pandas library
"""

from easy_pandas import EasyDataFrame

print("=" * 70)
print("EASY PANDAS - Quick Demo")
print("=" * 70)

# Create sample data
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'age': [25, 30, 35, 28, 32, 45],
    'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin', 'London'],
    'salary': [50000, 60000, 75000, 55000, 70000, 80000]
}

df = EasyDataFrame(data)

print("\n📊 Original Data:")
print(df)

print("\n\n🔍 Example 1: Filter age > 30")
print(df.filter_age_greaterthan_30())

print("\n\n🔍 Example 2: Filter city = London")
print(df.filter_city_equals_london())

print("\n\n🔗 Example 3: Chain - Filter age > 28 AND sort by salary descending")
result = df.filter_age_greaterthan_28().sort_by_salary_desc()
print(result)

print("\n\n📊 Example 4: Group by city and calculate average salary")
print(df.groupby_city_and_aggregate_salary_mean())

print("\n\n✂️ Example 5: Select only name and salary columns")
print(df.select_name_and_salary())

print("\n\n🎯 Example 6: Complex chain - Filter, Sort, Select")
result = (df
    .filter_age_greaterthan_25()
    .sort_by_salary_desc()
    .select_name_and_age_and_salary()
)
print(result)

print("\n\n📈 Example 7: Aggregation - Total salary")
total = df.aggregate_salary_sum()
print(f"Total Salary: ${total:,.2f}")

print("\n\n📈 Example 8: Aggregation - Average age")
avg_age = df.aggregate_age_mean()
print(f"Average Age: {avg_age:.1f} years")

print("\n\n" + "=" * 70)
print("✅ All examples completed successfully!")
print("=" * 70)
