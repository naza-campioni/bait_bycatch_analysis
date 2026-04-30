import pandas as pd
from scipy.stats import chi2_contingency

def calc_contingency(df: pd.DataFrame, feats: list, target: str):
  '''
  Calcualtes chi2 contingency test on dataframe.
  '''

  for feat in feats:
    cont = pd.crosstab(df[feat], df[target])
    chi2, p, dof, expected = chi2_contingency(cont)

    print(f"{feat:20s}    chi2 = {chi2:.3f}, p = {p:.4f}")
