# https://leetcode.com/problems/employees-earning-more-than-their-managers/description/
import pandas as pd

# Define the data
data = [
    {"id": 1, "name": "Joe", "salary": 70000, "managerId": 3},
    {"id": 2, "name": "Henry", "salary": 80000, "managerId": 4},
    {"id": 3, "name": "Sam", "salary": 60000, "managerId": None},
    {"id": 4, "name": "Max", "salary": 90000, "managerId": None}
]

# Create the DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)

merge_df = pd.merge(df, df, left_on="managerId", right_on="id", how="inner", suffixes=("_emp", "_mng"))
res = merge_df[merge_df["salary_mng"] < merge_df["salary_emp"]].rename(columns={
    "name_emp": "employee"
})[["employee"]]
print(res)
