def calc_manwu(df: pd.DataFrame, feats: list, target: str):
  '''
  Calculates Mannwhitneyu test on dataframe where target is assumed
  to be binary.
  '''

  for feat in feats:
    sgombro = df.loc[df[target] == df[target].unique()[0], feat]
    totano = df.loc[df[target] == df[target].unique()[1], feat]

    stat, p = mannwhitneyu(sgombro, totano, alternative='two-sided')
    print(f"{feat:20s}    U = {stat}, p = {p:.4f}")

  
