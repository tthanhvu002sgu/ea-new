import pandas as pd
import numpy as np
from scipy import stats

# 1. Load data
print("Loading M1 CSV...")
df = pd.read_csv('XAUUSD_M1_202001020600_202606122259.csv', sep=r'\s+|,|\t', engine='python')
df.columns = [c.strip().replace('<', '').replace('>', '') for c in df.columns]
df['datetime'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'])
df = df.sort_values('datetime').reset_index(drop=True)

# Filter to Discovery Split strictly: 2020-01-01 to 2023-06-30
df_disc = df[(df['datetime'] >= '2020-01-01') & (df['datetime'] <= '2023-06-30 23:59:59')].copy()
print("Discovery M1 rows:", len(df_disc))

# Construct H1 bars
df_disc['date'] = df_disc['datetime'].dt.date
df_disc['hour'] = df_disc['datetime'].dt.hour

h1 = df_disc.groupby(['date', 'hour']).agg(
    open=('OPEN', 'first'),
    high=('HIGH', 'max'),
    low=('LOW', 'min'),
    close=('CLOSE', 'last'),
    start_time=('datetime', 'first')
).reset_index()

h1['range'] = h1['high'] - h1['low']
h1['ret'] = h1['close'] - h1['open']
h1['direction'] = np.sign(h1['ret'])

# Filter specifically for 07:00 London open bar
london_open = h1[h1['hour'] == 7].copy().sort_values('date').reset_index(drop=True)

# Calculate 20-day median range of 07:00 bar (strictly past 20 trading days, index [1] to [20] before current day)
london_open['median_range_20'] = london_open['range'].shift(1).rolling(window=20).median()
london_open = london_open.dropna(subset=['median_range_20']).copy()
london_open['ratio'] = london_open['range'] / london_open['median_range_20']

# For each qualified day, let's measure continuation returns:
# (a) 08:00 to 14:00 (exact 6h holding window as defined in mechanism test)
# (b) 09:00 to 15:00 (+1 bar delayed window for shift test)
# To get exact prices at 08:00 open, 14:00 close, 09:00 open, 15:00 close:
h1_dict = h1.set_index(['date', 'hour']).to_dict(orient='index')

results = []
for idx, row in london_open.iterrows():
    d = row['date']
    if (d, 8) in h1_dict and (d, 13) in h1_dict: # 08:00 open to 13:00 close (= 14:00 exact)
        entry_08 = h1_dict[(d, 8)]['open']
        exit_14 = h1_dict[(d, 13)]['close']
        ret_08_14 = exit_14 - entry_08
    else:
        continue
        
    if (d, 9) in h1_dict and (d, 14) in h1_dict: # 09:00 open to 14:00 close (= 15:00 exact)
        entry_09 = h1_dict[(d, 9)]['open']
        exit_15 = h1_dict[(d, 14)]['close']
        ret_09_15 = exit_15 - entry_09
    else:
        ret_09_15 = np.nan
        
    results.append({
        'date': d,
        'range_07': row['range'],
        'median_range_20': row['median_range_20'],
        'ratio': row['ratio'],
        'dir_07': row['direction'],
        'ret_08_14': ret_08_14,
        'ret_08_14_aligned': ret_08_14 * row['direction'], # continuation return along 07:00 direction
        'ret_09_15_aligned': ret_09_15 * row['direction']  # delayed continuation return
    })

res_df = pd.DataFrame(results)

print("\n--- MECHANISM TEST RESULTS (DISCOVERY 2020-01 to 2023-06) ---")
print("Total qualified London open dates checked:", len(res_df))

# 1. Event / Conditional Return (when ratio > 1.25 vs unconditional)
cond_125 = res_df[res_df['ratio'] > 1.25]
n_125 = len(cond_125)
mean_ret_125 = cond_125['ret_08_14_aligned'].mean()
std_ret_125 = cond_125['ret_08_14_aligned'].std(ddof=1)
se_ret_125 = std_ret_125 / np.sqrt(n_125)
t_stat_125, p_val_t = stats.ttest_1samp(cond_125['ret_08_14_aligned'], 0, alternative='greater')
pos_count_125 = (cond_125['ret_08_14_aligned'] > 0).sum()
sign_test_res = stats.binomtest(pos_count_125, n_125, p=0.5, alternative='greater')
p_val_sign = sign_test_res.pvalue

print(f"\n[Test 1] Event / Conditional Return (Ratio > 1.25):")
print(f"  Sample size N = {n_125}")
print(f"  Mean aligned return (08:00->14:00) = {mean_ret_125:.4f} USD (SE={se_ret_125:.4f})")
print(f"  Win rate = {pos_count_125}/{n_125} ({pos_count_125/n_125*100:.2f}%)")
print(f"  One-sample t-test stat = {t_stat_125:.4f}, p-value = {p_val_t:.6f}")
print(f"  Sign-test p-value = {p_val_sign:.6f}")
print("  Unconditional mean aligned return (All Days N={}): {:.4f} USD".format(len(res_df), res_df['ret_08_14_aligned'].mean()))

# 2. Dose-Response (Bins: 1.0-1.25, 1.25-1.50, >1.50)
bin1 = res_df[(res_df['ratio'] > 1.0) & (res_df['ratio'] <= 1.25)]['ret_08_14_aligned']
bin2 = res_df[(res_df['ratio'] > 1.25) & (res_df['ratio'] <= 1.50)]['ret_08_14_aligned']
bin3 = res_df[res_df['ratio'] > 1.50]['ret_08_14_aligned']

print(f"\n[Test 2] Dose-Response (Monotonicity Check):")
print(f"  Bin 1 (1.00 < ratio <= 1.25): N={len(bin1)}, Mean Return = {bin1.mean():.4f} USD")
print(f"  Bin 2 (1.25 < ratio <= 1.50): N={len(bin2)}, Mean Return = {bin2.mean():.4f} USD")
print(f"  Bin 3 (ratio > 1.50):         N={len(bin3)}, Mean Return = {bin3.mean():.4f} USD")
is_monotonic = (bin3.mean() > bin2.mean() > bin1.mean())
print(f"  Monotonicity (Bin 3 > Bin 2 > Bin 1): {is_monotonic}")

# 3. Timing / Shift Test (+1 bar delay: 09:00->15:00 vs 08:00->14:00)
mean_delay_125 = cond_125['ret_09_15_aligned'].mean()
print(f"\n[Test 3] Timing / Shift Test (+1 Bar Delay to 09:00->15:00):")
print(f"  Exact Entry (08:00->14:00) Mean Return = {mean_ret_125:.4f} USD")
print(f"  Delayed Entry (09:00->15:00) Mean Return = {mean_delay_125:.4f} USD")
print(f"  Drop with delay: {mean_delay_125 < mean_ret_125} (Difference: {mean_delay_125 - mean_ret_125:.4f} USD)")

# Evaluate Pass Condition against Prereg rules strictly
# Prereg condition for Test 1: sign-test p < 0.05 or t-test p < 0.05. If < 0 or p >= 0.05 -> KILL G5 right away!
pass_test1 = (mean_ret_125 > 0) and (p_val_t < 0.05 or p_val_sign < 0.05)
print("\n--- MECHANISM PASS/FAIL EVALUATION ---")
print("Test 1 Pass (p < 0.05 and return > 0):", pass_test1)
print("Test 2 Dose-Response Monotonicity:", is_monotonic)
print("Test 3 Timing Drop Valid:", mean_delay_125 < mean_ret_125)
