import pandas_profiling
import pandas as pd

df = pd.read_csv('./data/raw/heart_cleveland_upload.csv')
profile = df.profile_report(title='Pandas Profiling Report', progress_bar=False)
profile.to_file("reports/eda_report.html")
profile.to_file("reports/eda_report.json")