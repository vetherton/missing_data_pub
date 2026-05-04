# Vincent Etherton and Marcus Nelson, Extending upon "Missing Financial Data"

## Extension: Heterogeneity in the Missingness Return Premium

This section documents our original extension to the replication, which investigates 
whether the missingness return premium documented in Section 5.1 of Bryzgalova et al. 
is stable across time, industry, and firm quality dimensions.

### Running the Extension

The extension notebook can be run independently of the main replication notebooks. 
It requires that the base data pipeline has already been run (steps 1–4 above).

### Extension Results and Their Locations

37. **Figure E.1: Return Premium by Sub-Period**
    - Notebook: `run_ablation_return_premium.ipynb`
    - Description: Decomposes the missingness return premium (missing minus observed, 
      % p.a.) by characteristic across two sub-periods: 1977–1998 and 1999–2020. 
      Sorted by the full-sample average premium in ascending order.
    - Result written to: `images-pdfs/ablation/ReturnPremiumBySubperiod.pdf`

38. **Figure E.2: Return Premium by Firm Quality Segment**
    - Notebook: `run_ablation_return_premium.ipynb`
    - Description: Six-panel figure decomposing the average missingness premium 
      (missing minus observed mean return, % p.a.) across firm quality segments. 
      Dashed line denotes the full-sample average premium. Panels include:
        - By Market Size (ME quintile, 1=small)
        - By FF10 Industry
        - By Operating Profitability (OP quintile, 1=low)
        - By Leverage (LEV quintile, 1=low)
        - By Book-to-Market (B2M quintile, 1=growth)
        - By Sub-period (1977–1998 vs. 1999–2020)
    - Result written to: `images-pdfs/ablation/ReturnPremiumBySegment.pdf`

### Notes on the Extension

- Unlike the main replication, these results use **value-weighted** portfolios 
  within each segment, consistent with Figure 13 of the original paper.
- The full-sample average premium (dashed reference line in Figure E.2) is 
  computed across all characteristics and the full 1977–2020 sample period.
- The sub-period split at 1999 follows the train/test split used in the 
  logistic regression analysis of Table 1 in the original paper.
- These figures require the true CRSP returns (not the noise-contaminated 
  placeholder returns) to replicate quantitatively. Users with WRDS access 
  should restore true returns before running this notebook (see Data Notes above).

# Missing Financial Data Result Replication Code

## Data

The data file we have provided `raw_rank_trunk_chars.npz` should be placed in the `data/` directory in the project if it is not already there. This file can be found under this link: 

https://www.dropbox.com/scl/fi/424yiolvlkowhd41v4c7h/raw_rank_trunk_chars.npz?rlkey=43eyoozyei16qs2huyuf46aq7&dl=0

### Notes about Data

Note, there are two differences between the data-set we have provided and the data-set used in the paper
1. The data-set we have provided is a truncated version of the data-set in the paper. This is because the full data-set is around 20 GB, and running all the results requires making multiple copies of the data-set, which is very time and space consuming. For this replication package, we have taken the last 5 years of the characteristic data. Note that we also provide the full data set of the characteristic data for all the years and the code can be applied accordingly to the full data. 
2. The returns in the data-set we have provided have been altered such as not to violate the terms of service from their source, we have done this by adding noise to them. Specifically, we have added i.i.d noise with a Normal(0, 0.1) distribution to each return observation. Therefore, one should not expect this data to exactly replicate any of the numerical results in the paper concerning returns, nor should it replicate standard results. However, the qualitative results are similar. The permos corresponding to returns have not been modified in any way, and therefore users with WRDS access can easily replace the contaminated returns with the correct returns and can exactly replicate the numerical results in the paper.

## Replication Utilities and AI Assistance

The following files were created with the assistance of Claude (Anthropic) to 
extend the replication package beyond the original code release:

- **`src/replace_returns.py`**: Queries WRDS directly to replace the noise-contaminated 
  placeholder returns in the provided dataset with true CRSP returns. Users with WRDS 
  access should run this before executing any return-dependent results to exactly 
  replicate the numerical findings of the paper. See Data Notes above for details on 
  why the provided returns are altered.

- **`src/build_full_npz.py`**: Constructs the full characteristic panel `.npz` file 
  from the `.feather` file provided by the original authors. This is necessary for 
  users who have obtained the full (non-truncated) data release and wish to run the 
  complete 1977–2020 sample rather than the 5-year truncated version.

- **`src/*_5yr.ipynb` notebooks**: Adapted versions of the original replication 
  notebooks configured to run on the 5-year truncated dataset for presentation and 
  demonstration purposes. These include `run_section_2_plots_5yr.ipynb` through 
  `run_section_6_plots_5yr.ipynb` and `run_ablation_return_premium_5yr.ipynb`.

These files were generated with AI assistance and have been reviewed for correctness, 
but users should exercise judgment when using them for research purposes.

## Running the Code

#### NOTE all of the commands below expect that the user is running them from the base directory of the repository

1. install the required packages `$ pip install -r requirements.txt`

2. create the necessary directions `$ ./setup_directories.sh`

3. generate the masked data `$ cd src && python generate_masked_data.py`

4. run the imputations `$ cd src && python run_data_imputations.py`

5. run the desired notebook for the particular results in question, ensure to run the first cell of the notebook to import the required modules and load the required data. to start the notebook server run `$ cd src && jupyter notebook`
- We have indicated in each result in the notebook how long it took us to run on a Macbook Pro with 2.8 GHz Quad-Core Intel Core i7 processor and 16 GB 2133 MHz LPDDR3 for memory.
- Some of the results take quite some time to run (for example the simulations).
- Generating the data and running the imputations should take on the order of an hour or two


## Paper Results and Their Locations
Each of the paper results can be found in the notebook corresponding to it's section in the paper. 
- src/appendix.ipynb
- src/section2.ipynb
- src/section3.ipynb
- src/section4.ipynb
- src/section5.ipynb
- src/section6.ipynb

Within each notebook, the first cell corresponds to data-loading and imports, and then each section corresponds to a table or figure from the text. These are clearly labeled along with a description of what is being done. Running the cell corresponding to a result will produce and display the table or figure for the result as well as writing either a pdf of the plot for figures or a tex file of the table for tables to the `images-pdfs` directory. Additionally, below we have listed (1) the notebook containing each result in the paper (2) the file and line number of the code to generate that result in the repository and (3) the location of files which are generated for that plot.

Main Text
1. Figure 1: Missing Values over Time `run_section_2_plots.ipynb` code located (src/plots_and_tables/section_2.py) `images-pdfs/section2/MissingValuesOverTime.pdf`
2. Figure 2: Missing Observations by Characteristic `run_section_2_plots.ipynb` code located (src/plots_and_tables/section_2.py) `images-pdfs/section2/MissingObservationByCharacteristic_by_permno_first.pdf`
3. Figure 3: Missing Observations by Characteristic Quintiles `run_section_2_plots.ipynb` code located (src/plots_and_tables/section_2.py) `images-pdfs/section2/[MissingValuesByCharQuintile.pdf, MissingValuesBySizeQuintile.pdf]`
4. Table 1: Logistic Regressions Explaining Missingess `run_section_2_plots.ipynb` code located (src/plots_and_tables/section_2.py) `images-pdfs/section2/MissingLogitRegressions.tex`
5. Figure 4: Autocorrelation of Characteristic Ranks `run_section_2_plots.ipynb` code located (src/plots_and_tables/section_2.py) `images-pdfs/section2/AutocorrOfChars.pdf`
6. Figure 5: Heatmap of Pairwise Correlation `run_section_2_plots.ipynb` code located (src/plots_and_tables/section_2.py) `images-pdfs/section2/HeatmatOfCorr.pdf`
7. Figure 6: Joint Distribution of Missing Patterns `run_section_3_plots.ipynb`  code located (src/plots_and_tables/section_3.py) result written to `images-pdfs/section3/missing--20180331.pdf`
8. Figure 7: Eigenvalues of Σ `run_section_4_plots.ipynb` code located (src/plots_and_tables/section_4.py)  result written to `images-pdfs/section4/figure_2_avg_cov_ev.pdf`
9. Figure 8: Number of Factors and Regularization `run_section_4_plots.ipynb` code located (src/plots_and_tables/section_4.py)  result written to `images-pdfs/section4/[number_of_factors_determination_xs-MAR0-True.pdf, number_of_factors_determination_xs-MAR0_0001-True.pdf, number_of_factors_determination_xs-MAR0_001-True.pdf,  number_of_factors_determination_xs-MAR0_01-True.pdf, number_of_factors_determination_xs-logit0-True.pdf, number_of_factors_determination_xs-logit0_0001-True.pdf, number_of_factors_determination_xs-logit0_001-True.pdf, number_of_factors_determination_xs-logit0_01-True.pdf, number_of_factors_determination_xs-prob_block0-True.pdf, number_of_factors_determination_xs-prob_block0_0001-True.pdf, number_of_factors_determination_xs-prob_block0_001-True.pdf,  number_of_factors_determination_xs-prob_block0_01-True.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-MAR0-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-MAR0_0001-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-MAR0_001-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-MAR0_01-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-logit0-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-logit0_0001-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-logit0_001-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-logit0_01-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-prob_block0-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-prob_block0_0001-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-prob_block0_001-True-incremental.pdf, metrics_by_char_vol_sort-number_of_factors_determination_xs-prob_block0_01-True-incremental.pdf]`
11. Figure 9: Optimal Regularization `run_section_4_plots.ipynb` code located (src/plots_and_tables/section_4.py)  result written to `images-pdfs/section4/[optimal_reg_determination_xs-MARk=200_0,0001_0,0005_0,001_0,005_0,01_0,05_0,1_0,5_1-.pdf, optimal_reg_determination_xs-logitk=200_0,0001_0,0005_0,001_0,005_0,01_0,05_0,1_0,5_1-.pdf, optimal_reg_determination_xs-prob_blockk=200_0,0001_0,0005_0,001_0,005_0,01_0,05_0,1_0,5_1-.pdf]`
12. Table 3: Imputation Error for Different Imputation Methods `run_section_5_plots.ipynb` code located (src/plots_and_tables/section_5.py) and (src/plots_and_tables/section_5.py)  result written to `images-pdfs/section5/[AggregateImputationErrorsFullDataset.tex, AggregateImputationR2FullDataset.tex]`
13. Table 4: Imputation Error for Extreme Characteristic Quintiles `run_section_5_plots.ipynb` code located (src/plots_and_tables/section_5.py) result written to `images-pdfs/section5/ImputationErrorsByCharQuintileFullDS.tex`
14. Figure 10: Illustrative Model-Implied and Imputed Time-Series `run_section_5_plots.ipynb` code located (src/plots_and_tables/section_5.py) result written to `images-pdfs/section5/[HAS-one-year-mask-AT.pdf, HAS-one-year-mask-ME.pdf, HAS-one-year-mask-Q.pdf, HAS-one-year-mask-VAR.pdf, MSFT-one-year-mask-AT.pdf, MSFT-one-year-mask-ME.pdf, MSFT-one-year-mask-Q.pdf, MSFT-one-year-mask-VAR.pdf]`
15. Table 5: Imputation Error for Types of Missingness `run_section_5_plots.ipynb` code located (src/plots_and_tables/section_5.py) result written to `images-pdfs/section5/[ImputationErrorsByMissingTypeEnd.tex, ImputationErrorsByMissingTypeMiddle.tex, ImputationErrorsByMissingTypeStart.tex]`
16. Figure 11: Imputation Error for Individual Characteristics `run_section_5_plots.ipynb` code located (src/plots_and_tables/section_5.py) result written to `images-pdfs/section5/[metrics_by_char_vol_sort-table_1_in_sample.pdf, metrics_by_char_vol_sort-table_1_out_of_sample_MAR.pdf, metrics_by_char_vol_sort-table_1_out_of_sample_block.pdf, metrics_by_char_vol_sort-table_1_out_of_sample_logit.pdf]`
17. Figure 12: Information Used for Imputation `run_section_5_plots.ipynb` code located (src/plots_and_tables/section_5.py) result written to `images-pdfs/section5/InfoUsedForImputationBW-bw_beta_weights.pdf`
18. Table 6: Imputation Error for Alternative Methods `run_section_5_plots.ipynb` code located (src/plots_and_tables/section_5.py) result written to `images-pdfs/section5/ComparisonWithAlternativeMethods.tex`
19. Figure 13: Market Premium Conditional on Observing a Firm Characteristic `run_section_6_plots.ipynb` code located (src/plots_and_tables/section_6.py) result written to `images-pdfs/section6/ls-missing-obs-ports.pdf`
20. Figure 14: Sharpe Ratios with IPCA Factors `run_section_6_plots.ipynb` code located (src/plots_and_tables/section_6.py) result written to `images-pdfs/section6/[ipca_sharpes_in_sample.pdf, ipca_sharpes_outof_sample.pdf]`
21. Figure 15: Univariate Sorts with and without Missing Values `run_section_6_plots.ipynb` code located (src/plots_and_tables/section_6.py) result written to `images-pdfs/section6/[portfolio-sorts-B2M-Mean_Return.pdf, portfolio-sorts-B2M-Percent_Used.pdf, portfolio-sorts-B2M-Sharpe_Ratio.pdf, portfolio-sorts-B2M-Volatility.pdf, portfolio-sorts-INV-Mean_Return.pdf, portfolio-sorts-INV-Percent_Used.pdf, portfolio-sorts-INV-Sharpe_Ratio.pdf, portfolio-sorts-INV-Volatility.pdf, portfolio-sorts-ME-Mean_Return.pdf, portfolio-sorts-ME-Percent_Used.pdf, portfolio-sorts-ME-Sharpe_Ratio.pdf, portfolio-sorts-ME-Volatility.pdf, portfolio-sorts-OP-Mean_Return.pdf, portfolio-sorts-OP-Percent_Used.pdf, portfolio-sorts-OP-Sharpe_Ratio.pdf, portfolio-sorts-OP-Volatility.pdf]`
22. Figure 16: Imputation Bias in Pure-Play Mimicking Portfolios `run_section_6_plots.ipynb` code located (src/plots_and_tables/section_6.py) result written to `images-pdfs/section6/[masked-factor_regression-pure_play-bw-xsmed-mean-abs-error.pdf, masked-factor_regression-pure_play-bw-xsmed-corr.pdf]`
23. Figure 17: Characteristic Mimicking Factor Portfolios `run_section_6_plots.ipynb` code located (src/plots_and_tables/section_6.py) result written to `images-pdfs/section6/[masked-factor_regression-pure_play-B2M-bw-xsmed.pdf, masked-factor_regression-pure_play-INV-bw-xsmed.pdf, masked-factor_regression-pure_play-ME-bw-xsmed.pdf, masked-factor_regression-pure_play-S2P-bw-xsmed.pdf]`
24. Table A.1: Imputation Error for Alternative Implementations `run_appendix_plots.ipynb` code located (src/plots_and_tables/appendix.py) result written to `images-pdfs/appendix/[ComparisonOfModelConfigs.tex]`
25. Simulations
    - Figure A.1: Errors with Missing-Completely-at-Random `run_appendix_plots.ipynb` code located (src/plots_and_tables/appendix.py) result written to `images-pdfs/appendix/[MAR_simulation_CCMSE_residreg_L=100_K=10.pdf, MAR_simulation_CCMSE_residreg_L=100_K=15.pdf, MAR_simulation_CCMSE_residreg_L=100_K=5.pdf, MAR_simulation_CCMSE_residreg_L=500_K=10.pdf, MAR_simulation_CCMSE_residreg_L=500_K=15.pdf, MAR_simulation_CCMSE_residreg_L=500_K=5.pdf, MAR_simulation_CCMSE_residreg_L=50_K=10.pdf, MAR_simulation_CCMSE_residreg_L=50_K=15.pdf, MAR_simulation_CCMSE_residreg_L=50_K=5.pdf]`
    - Figure A.2: Imputation Errors with Missing-Conditionally-at-Random `run_appendix_plots.ipynb` code located (src/plots_and_tables/appendix.py) result written to `images-pdfs/appendix/[Lmbda_simulation_CCMSE_residreg_L=100_K=10.pdf, Lmbda_simulation_CCMSE_residreg_L=100_K=15.pdf, Lmbda_simulation_CCMSE_residreg_L=100_K=5.pdf, Lmbda_simulation_CCMSE_residreg_L=500_K=10.pdf, Lmbda_simulation_CCMSE_residreg_L=500_K=15.pdf, Lmbda_simulation_CCMSE_residreg_L=500_K=5.pdf, Lmbda_simulation_CCMSE_residreg_L=50_K=10.pdf, Lmbda_simulation_CCMSE_residreg_L=50_K=15.pdf,Lmbda_simulation_CCMSE_residreg_L=50_K=5.pdf]`
26. Table C.2: Missing by Characteristic Quintiles `run_appendix_plots.ipynb` code located (src/plots_and_tables/section_2.py) result written to `images-pdfs/section2/MssingByQuintile.tex`
27. Table C.3: Lengths of Missing Blocks `run_appendix_plots.ipynb` code located (src/plots_and_tables/section_2.py) result written to `images-pdfs/section2/MssingBlockLengths.tex`
28. Figure D.1: Missing Observations over Time By Characteristics `run_appendix_plots.ipynb` code located (src/plots_and_tables/section_2.py) result written to `images-pdfs/section2/HeatmatOfMissingPerc.pdf`
29. Figure D.2: Missing Observations by Characteristic Pooled by Stocks `run_appendix_plots.ipynb` code located (src/plots_and_tables/section_2.py) result written to `images-pdfs/section2/[MissingObservationByCharacteristic_by_date_first.pdf, MissingObservationByCharacteristic_by_date_first_value_weight.pdf]`
30. Figure D.3: Heatmap of Pairwise Correlation from 1967–1976 NOT INCLUDED AS TRUNCATED DATA DOES NOT INCLUDE THESE YEARS
31. Figure D.4: Standard Deviation of Characteristic Ranks `run_appendix_plots.ipynb` code located (src/plots_and_tables/section_2.py) result written to `images-pdfs/section2/StdOfChars.pdf`
32. Figure D.5: Generalized Correlation of Global and Local Factor Weights `run_appendix_plots.ipynb` code located (src/plots_and_tables/section_4.py) result written to `images-pdfs/section4/generalized_corr.pdf`
33. Figure D.6: Composition of Proxy Factors by Characteristic Categories `run_appendix_plots.ipynb` code located (src/plots_and_tables/appendix.py) result written to `images-pdfs/appendix/[factor_vis_0_full_factors.pdf, factor_vis_0_sparse_factors.pdf, factor_vis_1_full_factors.pdf, factor_vis_1_sparse_factors.pdf, factor_vis_2_full_factors.pdf, factor_vis_2_sparse_factors.pdf, factor_vis_3_full_factors.pdf, factor_vis_3_sparse_factors.pdf, factor_vis_4_full_factors.pdf, factor_vis_4_sparse_factors.pdf, factor_vis_5_full_factors.pdf, factor_vis_5_sparse_factors.pdf, factor_vis_6_full_factors.pdf, factor_vis_6_sparse_factors.pdf, factor_vis_7_full_factors.pdf, factor_vis_7_sparse_factors.pdf, factor_vis_8_full_factors.pdf, factor_vis_8_sparse_factors.pdf, factor_vis_9_full_factors.pdf, factor_vis_9_sparse_factors.pdf]`
34. Figure D.8: Global and Local Imputation for Individual Characteristics `run_appendix_plots.ipynb` code located (src/plots_and_tables/section_5.py) result written to `images-pdfs/section5/metrics_by_char_vol_sort-table_2_out_of_sample_block.pdf`
35. Figure D.9: Top and Bottom Deciles with and without Missing Values `run_appendix_plots.ipynb` code located (src/plots_and_tables/section_6.py) result written to `images-pdfs/section6/[hl-portfolios-Intangibles,TradingFrictions,Other-MeanReturn.pdf, hl-portfolios-Intangibles,TradingFrictions,Other-SharpeRatio.pdf, hl-portfolios-Investment,Profitability-MeanReturn.pdf, hl-portfolios-Investment,Profitability-SharpeRatio.pdf, hl-portfolios-PastReturns,Value-MeanReturn.pdf, hl-portfolios-PastReturns,Value-SharpeRatio.pdf]`
36. Figure D.10: Sharpe Ratios with Non-parametric IPCA Factors `run_appendix_plots.ipynb` code located (src/plots_and_tables/appendix.py) result written to `images-pdfs/appendix/[decile_ipca_sharpes_in_sample.pdf, decile_ipca_sharpes_outof_sample.pdf]`


