import pandas as pd

df = pd.read_csv(r'C:\Users\PI\Downloads\customer_shopping_behaviour.csv')
print(df.head())

print(df.info())

print(df.describe(include = "all"))

print(df.isnull().sum())

df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median()))
print(df.isnull().sum())

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')

df.rename(columns = {'purchase_amount_(usd)':'purchase_amount'},inplace=True)
print(df.columns)

#Create a column "age_group"
labels = ["Young Adult","Adult","Middle-aged","Senior"]
df["age_group"] = pd.qcut(df["age"],q=4,labels=labels)
print(df[["age","age_group"]].head(10))

"""
Based on age values, pandas automatically:
sorts ages
divides into 4 equal groups
assigns your labels

"qcut()" divides data into equal-sized groups, while "cut()" divides data into equal value ranges.
qcut() (Quantile Cut)
cut() (Bin Cut)
"""

#Create column purchase_frequency_days
frequency_mapping = {
    "Fortnightly":14,
    "Weekly":7,
    "Monthly":30,
    "Quarterly":90,
    "Bi-Weekly":14,
    "Annually":365,
    "Every 3 Months":90
}
df["purchase_frequency_days"] = df["frequency_of_purchases"].map(frequency_mapping)
print(df[["purchase_frequency_days","frequency_of_purchases"]].head(10))

#“This code converts purchase frequency (text) into number of days using a dictionary.”


#As we know the data in "discount_applied" and "promo_code_used" columns is same 
# we might remove one of the column 

#To check if 2 cols has same data use:
print(df[["discount_applied","promo_code_used"]].all())
"""
discount_applied    True
promo_code_used     True
dtype: bool
"""

df = df.drop("promo_code_used",axis=1)
print(df)
"""
Pandas creates a new dataframe
Removes "promo_code_used" column
Returns the new dataframe
You store it back into df
"""
#axis=0 --> Rows
#axis=1 --> Columns

from sqlalchemy import create_engine

server = "localhost\\SQLEXPRESS03"
database = "CUSTOMER_BEHAVIOUR"

engine = create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

table_name = "customer"

df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}'")

"""
from sqlalchemy import create_engine

server = "localhost\\SQLEXPRESS03"
database = "CUSTOMER_BEHAVIOUR"
username = "sa"          # or your SQL login
password = "your_password"

engine = create_engine(
    f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
)

df.to_sql("customer", engine, if_exists="replace", index=False)

print("Data loaded successfully ✅")
"""

print(df.info())

print(df.describe(include = "all"))