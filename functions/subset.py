import pandas as pd

def subset(df: pd.DataFrame, divide_by: list):

  assert all(item in ['sex', 'length'] for item in divide_by), "Invalid divide_by. Allowed values: 'sex', 'length'."

  if len(divide_by) == 1:
    length = 1
    assert divide_by == ['sex'], "Subsetting by length only allowed after subsetting by sex."

  if 'sex' in divide_by:
    df_sub_m = df[df['Sesso'] == 'M']
    df_sub_f = df[df['Sesso'] == 'F']

  if 'length' in divide_by:
    length = 2
    df_sub_m_small = df_sub_m[df_sub_m['Lunghezza tot (cm)'] < 150]
    df_sub_f_small = df_sub_f[df_sub_f['Lunghezza tot (cm)'] < 180]

    df_sub_m_big = df_sub_m[df_sub_m['Lunghezza tot (cm)'] >= 150]
    df_sub_f_big = df_sub_f[df_sub_f['Lunghezza tot (cm)'] >= 180]

  if length == 1:
    return df_sub_m, df_sub_f
  else:
    return df_sub_m_small, df_sub_f_small, df_sub_m_big, df_sub_f_big
