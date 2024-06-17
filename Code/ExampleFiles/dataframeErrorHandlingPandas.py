# Safe access using .at attribute
value = df.at[index, column]

# Safe assignment using .iat attribute
df.iat[index, column] = value

# Safe retrieval with default value using .get() method
value = df.get(key, default_value)
