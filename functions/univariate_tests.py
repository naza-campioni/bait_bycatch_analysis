from scipy.stats import mannwhitneyu, chi2_contingency, fisher_exact
import pandas as pd
import numpy as np

def rank_biserial(U, n1, n2):
    return 1 - (2 * U) / (n1 * n2)

def run_tests(df_subset, continuous_feats, categorical_feats,
              target, label, bonferroni_n=50):

    results = []
    g0 = df_subset[df_subset[target] == df_subset[target].unique()[0]]
    g1 = df_subset[df_subset[target] == df_subset[target].unique()[1]]

    # Mann-Whitney for continuous features
    for feat in continuous_feats:
      v0 = g0[feat].dropna()
      v1 = g1[feat].dropna()
      if len(v0) < 5 or len(v1) < 5:
        results.append({
            'feature': feat, 'test': 'MWU',
            'statistic': np.nan, 'p': np.nan,
            'effect_size_r': np.nan, 'note': 'insufficient N'
        })
        continue
      U, p = mannwhitneyu(v0, v1, alternative='two-sided')
      r = rank_biserial(U, len(v0), len(v1))
      results.append({
          'feature':      feat,
          'test':         'MWU',
          'n_sgombro':    len(v0),
          'n_totano':     len(v1),
          'statistic':    round(U, 1),
          'p':            round(p, 4),
          'effect_size_r': round(r, 3),
          'note':         ''
      })

    # Chi-squared / Fisher for categorical features
    for feat in categorical_feats:
      if feat not in df_subset.columns:
        continue
      ct = pd.crosstab(df_subset[feat], df_subset[target])
      if ct.shape == (2, 2) and ct.min().min() < 5:
        stat, p = fisher_exact(ct)
        test = 'Fisher'
      else:
        stat, p, _, _ = chi2_contingency(ct)
        test = 'Chi2'
        
      results.append({
          'feature':       feat,
          'test':          test,
          'n_sgombro':     len(g0),
          'n_totano':      len(g1),
          'statistic':     round(stat, 3),
          'p':             round(p, 4),
          'effect_size_r': np.nan,
          'note':          ''
      })

    threshold = round(0.05 / bonferroni_n, 5)
    res_df = pd.DataFrame(results)
    res_df['significant'] = res_df['p'] < threshold

    print(f"\n{'='*65}")
    print(f"Subset: {label}  |  "
          f"n={len(df_subset)}  "
          f"({len(g0)} Sgombro / {len(g1)} Totano)")
    print(f"Bonferroni threshold: {threshold}")
    print(f"{'='*65}")
    print(res_df.to_string(index=False))

    return res_df
