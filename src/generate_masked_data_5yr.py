import numpy as np
import imputation_utils
import imputation_metrics
import logit_models_and_masking
import pandas as pd

imputation_utils.CACHE_BASE_PATH = '../data/imputation_cache/5yr/'

from generate_masked_data import (
    char_map,
    get_random_masks,
)


def generate_MAR_missing_data(percentile_rank_chars, return_panel, chars, monthly_updates, dates, permnos):
    np.random.seed(0)
    update_chars = np.copy(percentile_rank_chars)
    for i, c in enumerate(chars):
        if char_map[c] != 'M':
            update_chars[~(monthly_updates == 1), i] = np.nan
    np.random.seed(0)
    random_nan_mask = get_random_masks(update_chars, p=0.1)
    masked_lagged_chars = np.copy(percentile_rank_chars)
    only_mimissing_chars = np.copy(percentile_rank_chars)
    only_mimissing_chars[:, :, :] = np.nan
    for c in range(percentile_rank_chars.shape[2]):
        if char_map[chars[c]] != 'M':
            for t in range(random_nan_mask.shape[0]):
                missing = random_nan_mask[t, :, c]
                only_mimissing_chars[t:t+3, missing, c] = np.copy(masked_lagged_chars[t:t+3, missing, c])
                masked_lagged_chars[t:t+3, missing, c] = np.nan
        else:
            for t in range(random_nan_mask.shape[0]):
                missing = random_nan_mask[t, :, c]
                only_mimissing_chars[t, missing, c] = np.copy(masked_lagged_chars[t, missing, c])
                masked_lagged_chars[t, missing, c] = np.nan

    flags_panel = imputation_metrics.get_flags(masked_lagged_chars, return_panel)
    imputation_utils.save_imputation(flags_panel, dates, permnos, chars, "MAR_flag_panel")
    imputation_utils.save_imputation(masked_lagged_chars, dates, permnos, chars, "MAR_fit_data")
    imputation_utils.save_imputation(only_mimissing_chars, dates, permnos, chars, "MAR_eval_data")


def generate_LOGIT_missing_data(percentile_rank_chars, return_panel, chars, monthly_updates, dates, permnos):
    np.random.seed(0)
    start_model_l = logit_models_and_masking.create_logit_model('START', np.copy(percentile_rank_chars), chars,
                                                                 monthly_updates, model_type='logit')
    middle_model_l = logit_models_and_masking.create_logit_model('MIDDLE', np.copy(percentile_rank_chars), chars,
                                                                  monthly_updates, model_type='logit')
    masked_lagged_chars, only_missing_chars = logit_models_and_masking.generate_logit_masked_data(
        start_model_l, middle_model_l, None, np.copy(percentile_rank_chars), chars, monthly_mask_tgt_perc=0.0,
        monthly_updates=monthly_updates, multiplier=1
    )
    flags_panel = imputation_metrics.get_flags(masked_lagged_chars, return_panel)
    imputation_utils.save_imputation(only_missing_chars, dates, permnos, chars, "logit_eval_data")
    imputation_utils.save_imputation(masked_lagged_chars, dates, permnos, chars, "logit_fit_data")
    imputation_utils.save_imputation(flags_panel, dates, permnos, chars, "logit_flag_panel")


def get_block_mask_prob_weighted(percentile_rank_chars, return_panel, chars, monthly_updates, dates, permnos,
                                  tgt_total=0.1, tgt_start=0.4):
    np.random.seed(0)
    update_chars = np.copy(percentile_rank_chars)
    for i, c in enumerate(chars):
        if char_map[c] != 'M':
            update_chars[~(monthly_updates == 1), i] = np.nan
    new_mask = np.isnan(update_chars)
    additional_mask = np.copy(new_mask) * 0

    T = new_mask.shape[0]
    for t in range(12, T, 12):
        start = np.all(new_mask[:t], axis=0, keepdims=True)
        not_start = ~start
        start *= np.any(~new_mask[t:t+12], keepdims=True, axis=0)
        not_start *= np.any(~new_mask[t:t+12], keepdims=True, axis=0)
        total = np.sum(start) + np.sum(not_start)
        start = np.logical_and(start,
                               np.any(np.sum(~new_mask[t:t+12], axis=2, keepdims=True) > 15, axis=0, keepdims=True))
        not_start = np.logical_and(not_start,
                               np.any(np.sum(~new_mask[t:t+12], axis=2, keepdims=True) > 15, axis=0, keepdims=True))
        sample_freq_start = tgt_start * (tgt_total * total) / np.sum(start)
        if sample_freq_start > 0.5:
            continue
        sample_freq_mid = (1 - tgt_start) * (tgt_total * total) / np.sum(not_start)
        start_mask = np.logical_and(start, 1 == np.random.binomial(n=1, p=sample_freq_start, size=start.shape))
        mid_mask = np.logical_and(not_start, 1 == np.random.binomial(n=1, p=sample_freq_mid, size=not_start.shape))
        net_mask = np.logical_or(start_mask, mid_mask)
        new_mask[t:t+12, net_mask.reshape(net_mask.shape[1:])] = 1
        additional_mask[t:t+12, net_mask.reshape(net_mask.shape[1:])] = 1

    additional_mask = additional_mask == 1
    only_mimissing_chars = np.copy(update_chars)
    only_mimissing_chars[~(new_mask == 1)] = np.nan
    masked_lagged_chars = np.copy(percentile_rank_chars)
    masked_lagged_chars[additional_mask] = np.nan
    flags_panel = imputation_metrics.get_flags(masked_lagged_chars, return_panel)
    imputation_utils.save_imputation(flags_panel, dates, permnos, chars, "prob_block_flag_panel")
    imputation_utils.save_imputation(only_mimissing_chars, dates, permnos, chars, "prob_block_eval_data")
    imputation_utils.save_imputation(masked_lagged_chars, dates, permnos, chars, "prob_block_fit_data")


if __name__ == '__main__':
    data = np.load('../data/raw_rank_trunk_chars_5yr.npz')
    percentile_rank_chars = data['rank_chars']
    chars = data['chars']
    dates = data['dates']
    return_panel = data['returns']
    permnos = data['permnos']
    monthly_updates = data['monthly_updates']

    generate_MAR_missing_data(percentile_rank_chars, return_panel, chars, monthly_updates, dates, permnos)
    generate_LOGIT_missing_data(percentile_rank_chars, return_panel, chars, monthly_updates, dates, permnos)
    get_block_mask_prob_weighted(percentile_rank_chars, return_panel, chars, monthly_updates, dates, permnos,
                                 tgt_total=0.08, tgt_start=0.3)
