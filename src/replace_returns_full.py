import os
import shutil

import numpy as np
import pandas as pd
import wrds

DATA_PATH = '../data/raw_rank_trunk_chars.npz'
DEPRECATED_PATH = '../data/raw_rank_trunk_chars_deprecated.npz'

# ── Load existing data ──────────────────────────────────────────────────────
data = np.load(DATA_PATH)
permnos        = data['permnos']
dates          = data['dates']   # YYYYMMDD integers
rank_chars     = data['rank_chars']
chars          = data['chars']
rfs            = data['rfs']
monthly_updates = data['monthly_updates']

# ── Pull correct returns and raw ME from CRSP ───────────────────────────────
db = wrds.Connection()

permno_list = ','.join(str(p) for p in permnos)
def fmt_date(d):
    s = str(int(d))  # YYYYMMDD
    return f"{s[:4]}-{s[4:6]}-{s[6:]}"

date_min = fmt_date(min(dates))
date_max = fmt_date(max(dates))

print(f"Querying CRSP msf for {len(permnos)} permnos from {date_min} to {date_max}...")
crsp = db.raw_sql(f"""
    SELECT permno, date, ret, abs(prc) * shrout / 1000 as me
    FROM crsp.msf
    WHERE permno IN ({permno_list})
      AND date >= '{date_min}'
      AND date <= '{date_max}'
""")
db.close()

crsp['date'] = pd.to_datetime(crsp['date'])
crsp['yyyymm'] = crsp['date'].dt.year * 100 + crsp['date'].dt.month

# ── Realign into (T, N) panels ───────────────────────────────────────────────
permno_to_idx = {int(p): i for i, p in enumerate(permnos)}
date_to_idx = {
    (int(d) // 10000) * 100 + (int(d) // 100) % 100: i
    for i, d in enumerate(dates)
}

T, N = len(dates), len(permnos)
correct_returns = np.full((T, N), np.nan)
raw_me = np.full((T, N), np.nan)

ret_matched = 0
me_matched = 0
for _, row in crsp.iterrows():
    p = int(row['permno'])
    d = int(row['yyyymm'])
    if p in permno_to_idx and d in date_to_idx:
        ti, ni = date_to_idx[d], permno_to_idx[p]
        if not pd.isna(row['ret']):
            correct_returns[ti, ni] = row['ret']
            ret_matched += 1
        if not pd.isna(row['me']):
            raw_me[ti, ni] = row['me']
            me_matched += 1

print(f"Filled {ret_matched} return observations out of {T * N} possible slots.")
print(f"Filled {me_matched} raw ME observations out of {T * N} possible slots.")

# ── Build raw_chars: same as rank_chars except ME column has actual values ──
me_idx = list(chars).index('ME')
raw_chars = np.copy(rank_chars)
raw_chars[:, :, me_idx] = raw_me

# ── Rename existing file, save new one ─────────────────────────────────────
if os.path.exists(DATA_PATH):
    shutil.move(DATA_PATH, DEPRECATED_PATH)
    print(f"Renamed existing file to {DEPRECATED_PATH}")

np.savez(
    DATA_PATH,
    rank_chars=rank_chars,
    raw_chars=raw_chars,
    chars=chars,
    dates=dates,
    returns=correct_returns,
    permnos=permnos,
    rfs=rfs,
    monthly_updates=monthly_updates,
)
print(f"Saved new file to {DATA_PATH}")
