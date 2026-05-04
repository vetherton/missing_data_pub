import numpy as np
import pandas as pd
import pandas_datareader.data as web

FEATHER_PATH = '../data/characteristics_without_imputation.fthr'
OUT_PATH     = '../data/raw_rank_trunk_chars.npz'

# ── Load feather ─────────────────────────────────────────────────────────────
print("Loading feather file...")
data = pd.read_feather(FEATHER_PATH)

char_cols = sorted([c for c in data.columns if c not in ['return', 'date', 'permno', 'monthly_update']])
chars   = np.array(char_cols)
dates   = np.sort(data['date'].astype(int).unique())
permnos = np.sort(data['permno'].astype(int).unique())

T, N, C = len(dates), len(permnos), len(chars)
print(f"Panel: {T} dates × {N} permnos × {C} characteristics")

# ── Build panel arrays ───────────────────────────────────────────────────────
rank_chars     = np.full((T, N, C), np.nan)
returns        = np.full((T, N), np.nan)
monthly_updates = np.zeros((T, N))

date_to_idx   = {d: i for i, d in enumerate(dates)}
permno_to_idx = {p: i for i, p in enumerate(permnos)}

data['t'] = data['date'].astype(int).map(date_to_idx)
data['n'] = data['permno'].astype(int).map(permno_to_idx)

t_idx = data['t'].values
n_idx = data['n'].values

print("Filling characteristic panel...")
for i, c in enumerate(char_cols):
    rank_chars[t_idx, n_idx, i] = data[c].values

returns[t_idx, n_idx]         = data['return'].values
monthly_updates[t_idx, n_idx] = data['monthly_update'].values

# ── Risk-free rates (Ken French) ─────────────────────────────────────────────
print("Fetching risk-free rates from Ken French...")
ff = web.DataReader('F-F_Research_Data_Factors', 'famafrench', start='1960-01-01')[0]
ff.index = ff.index.to_timestamp()
rf_lookup = {
    int(f"{idx.year}{str(idx.month).zfill(2)}"): ff.loc[idx, 'RF'] / 100
    for idx in ff.index
}

rfs = []
for d in dates:
    yyyymm = (d // 10000) * 100 + (d // 100) % 100
    rfs.append(rf_lookup.get(yyyymm, np.nan))
rfs = np.array(rfs)

missing_rf = np.sum(np.isnan(rfs))
if missing_rf > 0:
    print(f"Warning: {missing_rf} dates missing risk-free rate")

# ── Financial firm filter ────────────────────────────────────────────────────
print("Applying financial firm filter...")
sic_fic = pd.read_csv('../data/sic_fic.csv')
financial_permnos = sic_fic.loc[sic_fic['sic'] // 1000 == 6]['LPERMNO'].unique()
non_financial = ~np.isin(permnos, financial_permnos)

rank_chars      = rank_chars[:, non_financial, :]
returns         = returns[:, non_financial]
monthly_updates = monthly_updates[:, non_financial]
permnos         = permnos[non_financial]
print(f"Kept {non_financial.sum()} of {N} permnos after financial filter")

# ── Save ─────────────────────────────────────────────────────────────────────
print(f"Saving to {OUT_PATH}...")
np.savez(
    OUT_PATH,
    rank_chars=rank_chars,
    raw_chars=rank_chars,
    chars=chars,
    dates=dates,
    returns=returns,
    permnos=permnos,
    rfs=rfs,
    monthly_updates=monthly_updates,
)
print("Done.")
print(f"Final panel: {rank_chars.shape[0]} dates × {rank_chars.shape[1]} permnos × {rank_chars.shape[2]} characteristics")
print(f"Date range: {dates.min()} – {dates.max()}")
print(f"Non-nan returns: {int(np.sum(~np.isnan(returns)))}")
