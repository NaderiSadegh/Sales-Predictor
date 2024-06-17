import numpy as np    # Created by: Sadegh Naderi
import pandas as pd

# Object creation
s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s)

dates = pd.date_range("20130101", periods=6)
print(dates)

df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
print(df)

# Viewing data
df.head()
df.tail(3)
df.describe()
df.sort_values(by="B")


# Selection
    # getting
df["A"]
df[0:3]

    # selection by label
df.loc[:, ["A", "B"]]
    # Selection by position
df.iloc[3]
df.iloc[3:5, 0:2]
    # Boolean indexing
df[df["A"] > 0]

    # Setting
df.iloc[0, 1] = 0
df.iloc[0, 1]


# Missing data

df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ["E"])
df1.loc[dates[0] : dates[1], "E"] = 1
df1

df1.dropna(how="any")
pd.isna(df1)


# Operations
df.apply(lambda x: x.max() - x.min())

# Merge

    # Concat
df = pd.DataFrame(np.random.randn(10, 4))
df

pieces = [df[:3], df[3:7], df[7:]]
pd.concat(pieces)

    # merge
left = pd.DataFrame({"key": ["foo", "foo"], "lval": [1, 2]})
right = pd.DataFrame({"key": ["foo", "foo"], "rval": [4, 5]})
left
right

pd.merge(left, right, on="key")


# Grouping
df = pd.DataFrame({'Animal': ['Falcon', 'Falcon',
                              'Parrot', 'Parrot'],
                   'Max Speed': [380., 370., 24., 26.]})
df

df.groupby(['Animal']).mean()

# Reshaping
    # Stack
df_single_level_cols = pd.DataFrame([[0, 1], [2, 3]],
                                    index=['cat', 'dog'],
                                    columns=['weight', 'height'])
df_single_level_cols

# Stacking a dataframe with a single level column axis returns a Series:
stacked  = df_single_level_cols.stack()
stacked 
# the inverse operation of stack() is unstack(), which by default unstacks the last level:
#df_single_level_cols.stack()
stacked.unstack()


# Importing and exporting data for CSV
df.to_csv("foo.csv")
pd.read_csv("foo.csv")

