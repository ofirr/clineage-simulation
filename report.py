from io import StringIO
import pandas as pd
import os

path_output = './outputs'
path_scores = os.path.join(path_output, 'scores.out')

# read the first two lines that contain various metrics
df_metrics = pd.read_csv(path_scores, sep='\t', nrows=1)

# transpose and rename the column to 'metrics'
df_metrics = df_metrics.T.rename(columns={0:'metrics'})

# display to the screen
print(df_metrics)
print()

# read the summary section
df_summary = pd.read_csv(path_scores, sep='\t', skiprows=4)

print(df_summary)
