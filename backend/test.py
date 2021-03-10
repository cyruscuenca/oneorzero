import pandas as pd

foo = pd.to_datetime('Q3 2019', errors='coerce')

print(foo)