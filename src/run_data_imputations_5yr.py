import numpy as np
import imputation_utils
import imputation_model_simplified
import pandas as pd

imputation_utils.CACHE_BASE_PATH = '../data/imputation_cache/5yr/'

from run_data_imputations import char_map, run_all_imputations

if __name__ == '__main__':
    data = np.load('../data/raw_rank_trunk_chars_5yr.npz')
    percentile_rank_chars = data['rank_chars']
    chars = data['chars']
    dates = data['dates']
    return_panel = data['returns']
    permnos = data['permnos']
    monthly_updates = data['monthly_updates']

    sic_fic = pd.read_csv('../data/sic_fic.csv')
    contained_permnos = sic_fic.LPERMNO.unique()
    industries = np.zeros_like(permnos)
    for i, p in enumerate(permnos):
        if p in contained_permnos:
            industries[i] = sic_fic.loc[sic_fic.LPERMNO == p].sic.unique()[0] // 1000
    industries = industries // 1000

    run_all_imputations(missing_data_type=None, percentile_rank_chars=percentile_rank_chars,
                        dates=dates, return_panel=return_panel, chars=chars, industries=industries,
                        monthly_updates=monthly_updates, permnos=permnos)
    run_all_imputations(missing_data_type='MAR', percentile_rank_chars=percentile_rank_chars,
                        dates=dates, return_panel=return_panel, chars=chars, industries=industries,
                        monthly_updates=monthly_updates, permnos=permnos)
    run_all_imputations(missing_data_type='logit', percentile_rank_chars=percentile_rank_chars,
                        dates=dates, return_panel=return_panel, chars=chars, industries=industries,
                        monthly_updates=monthly_updates, permnos=permnos)
    run_all_imputations(missing_data_type='PROB_BLOCK', percentile_rank_chars=percentile_rank_chars,
                        dates=dates, return_panel=return_panel, chars=chars, industries=industries,
                        monthly_updates=monthly_updates, permnos=permnos)
