Final Project: Details and Guidelines
Hi Class,

Here are the expectations for the final project. (We highly recommend working in groups of three to manage the workload):

Step 1: Replicate the core findings of your chosen paper.
Step 2: Build upon the replication by conducting your own ablation studies or exploring an alternative approach that adds value to the research.
Deliverables: At the end of the semester, your group must deliver a 10-minute class presentation and submit a 10-page final report detailing your work, along with your code.

# Missing Financial Data — Paper Outline
## Replication + Extension Sections

---

## Section 1: Motivation (~ 1 page)

Missing data is one of the most pervasive yet underaddressed problems in empirical asset pricing. Standard datasets of firm characteristics — book-to-market, R&D intensity, accruals, leverage — are riddled with gaps that affect the majority of publicly traded firms. Despite this, most empirical work either silently drops firms with incomplete records (listwise deletion) or fills gaps with the cross-sectional median, treating missingness as an inconvenience rather than a structural feature of the data.

Bryzgalova, Lerner, Lettau, and Pelger (2025) challenge this view directly. They document four stylized facts about the structure of missing firm fundamentals: missingness is widespread, it is severe when multiple characteristics are required simultaneously, it is systematically non-random (clustering both cross-sectionally and over time), and it is return-relevant — stocks with missing characteristics earn different returns than observationally similar firms with complete data. Together, these facts imply that ad-hoc imputation methods introduce selection biases that distort downstream portfolio construction and factor estimation.

This paper replicates those four core findings using WRDS data, extends the analysis by constructing a characteristic-level return spread to identify which variables drive the return-relevance result, and proposes a predictive framework for missingness itself — demonstrating that the structured, forecastable nature of missing data provides the clearest justification for the authors' principled PCA-based imputation approach.

---

## Section 2: Methodology (~ 1 page)

### 2.1 Data

We obtain firm-level characteristics from Compustat and CRSP via WRDS, constructing a panel of the 45 characteristics commonly used in the asset pricing literature (as documented in the paper). Our sample spans [DATE RANGE]. We follow the authors' variable construction conventions to ensure comparability.

### 2.2 Documenting Missingness Structure

For each characteristic $c$ and firm $i$ in month $t$, we define a binary indicator:

$$M_{i,c,t} = \mathbf{1}[\text{characteristic } c \text{ is missing for firm } i \text{ at time } t]$$

We compute:
- **Prevalence**: the fraction of firm-months with at least one missing characteristic
- **Clustering**: the correlation of $M_{i,c,t}$ across characteristics (cross-sectional) and across time (serial)
- **Non-randomness**: OLS regression of $M_{i,c,t}$ on observable firm attributes (size, age, leverage, profitability)
- **Return relevance**: the average return spread between firms with and without each characteristic present

### 2.3 Benchmarking Imputation Approaches

To motivate principled imputation, we compare three simple approaches against the authors' recommendation:
- **Listwise deletion**: drop any firm-month with missing values
- **Cross-sectional median imputation**: fill missing values with the median across firms in the same month
- **Forward-fill**: use the firm's own last observed value

We do not implement the full PCA-based imputation but illustrate its motivation through the failure modes of ad-hoc methods.

---

## Section 3: Replication Results (~ 2 pages)

### 3.1 Stylized Fact 1 — Missingness is Widespread

[TABLE: Missingness rates by characteristic, sorted descending. Highlight that >70% of firms have at least one missing value, consistent with the paper's claim that roughly half of total market cap is affected.]

We find missingness rates broadly consistent with the paper. Characteristics related to R&D, employee counts, and pension obligations show the highest rates of absence, while market-based characteristics (momentum, short-term reversal) are nearly fully observed by construction.

### 3.2 Stylized Fact 2 — Multivariate Missingness is Severe

[FIGURE: Bar chart of the fraction of firms with 0, 1–5, 5–10, 10+ missing characteristics simultaneously. Show how the problem compounds when requiring a clean panel across all 45 variables.]

When requiring all 45 characteristics to be non-missing simultaneously, [X]% of the sample is dropped. This is the core practical problem for any cross-sectional regression or factor model that ingests multiple signals.

### 3.3 Stylized Fact 3 — Missingness is Non-Random

[FIGURE: Heatmap of missingness by year and characteristic, showing temporal clustering. FIGURE: Missingness rate by size decile, showing that small firms are disproportionately affected but large-cap missingness is nontrivial.]

A simple logistic regression of $M_{i,c,t}$ on firm size, age, leverage, and profitability yields an in-sample pseudo-$R^2$ of [X], confirming that missingness is not missing-at-random (MAR), let alone missing completely at random (MCAR). This invalidates the median imputation approach, which assumes observations are exchangeable regardless of firm characteristics.

### 3.4 Stylized Fact 4 — Returns Depend on Missingness

[TABLE: Average monthly return, missing group vs. non-missing group, pooled across all characteristics. T-stat on the difference. Consistent with the paper's finding that missing-characteristic firms earn lower average returns.]

Pooled across all 45 characteristics, firms with at least one missing value earn an average monthly return of [X]% vs. [Y]% for complete-data firms, a spread of [Z]% (t-stat = [T]). This is economically meaningful and persistent through time.

---

## Section 4: Extension — Missingness Premium by Characteristic (~ 1 page)

### 4.1 Motivation

The paper establishes that returns depend on missingness in aggregate. A natural follow-up question is: which specific characteristics drive this result? If only a handful of variables account for the entire return spread, the stylized fact is less general than it appears. If the premium is pervasive across characteristics, it strengthens the case that missingness encodes economically meaningful firm-level information regardless of which variable is missing.

### 4.2 Characteristic-Level Return Spreads

For each characteristic $c$, we compute:

$$\text{Missingness Premium}_c = \bar{R}_{\text{missing}, c} - \bar{R}_{\text{non-missing}, c}$$

averaged over all months in the sample. We sort characteristics by the magnitude of this spread and report the top and bottom deciles.

[FIGURE: Bar chart of missingness premium by characteristic, sorted. Annotate the top 5 and bottom 5 variables.]

### 4.3 Results

We find considerable heterogeneity in the missingness premium across characteristics. [RESULTS PLACEHOLDER — e.g., R&D and pension-related variables show the largest negative premiums, consistent with the interpretation that missingness in innovation-related variables is informative about firm type.] Market-based and momentum characteristics, which are nearly always observed, show premiums close to zero as expected.

This heterogeneity suggests that the aggregate return spread documented in the paper is not driven by a single variable but reflects a pervasive pattern — supporting the authors' broad claim about the return-relevance of missingness.

---

## Section 5: Extension — Predicting Missingness (~ 1.5 pages)

### 5.1 Motivation

The prior sections establish that missingness is non-random and return-relevant. A third implication of the authors' framework — less directly tested in the original paper — is whether missingness is *predictable*. If a firm's probability of missing a characteristic next period can be forecast using currently observable attributes, this further confirms that missingness carries structured information rather than noise.

High predictability has a direct implication for imputation: methods that ignore the predictive structure of missingness (e.g., median imputation) will produce biased imputations precisely for firms whose missingness was foreseeable. Principled methods that model the cross-sectional and time-series dependencies — as in Bryzgalova et al. — are thus not just statistically motivated but economically justified.

### 5.2 Predictive Model

For each characteristic $c$, we estimate a logistic regression:

$$P(M_{i,c,t+1} = 1) = \sigma\left(\alpha + \beta_1 \log(\text{Size}_{i,t}) + \beta_2 \text{Age}_{i,t} + \beta_3 \text{Leverage}_{i,t} + \beta_4 \text{Profitability}_{i,t} + \gamma_{\text{industry}} + \epsilon_{i,t}\right)$$

We estimate this model in a rolling expanding window (training on all data up to year $t$, predicting year $t+1$) to avoid look-ahead bias. We report the average out-of-sample AUC across characteristics.

### 5.3 Results

[TABLE: Out-of-sample AUC by characteristic, mean and distribution. Expected result: AUC meaningfully above 0.5 for most characteristics, with highest predictability for accounting-based variables and lowest for market-based variables.]

Across all 45 characteristics, the average out-of-sample AUC is [X], indicating that missingness is substantially predictable from publicly observable firm attributes. Predictability is highest for [CHARACTERISTIC TYPE] and lowest for market-based variables, consistent with accounting data being subject to more structured reporting patterns.

[FIGURE: Distribution of AUC across characteristics as a histogram.]

Importantly, the coefficient on firm size is negative and significant for nearly all characteristics — smaller firms are more likely to go missing, but this relationship is not deterministic, confirming that missingness is informative even after controlling for the well-known small-firm data quality gradient.

### 5.4 Implications for Imputation

The predictability result closes the logical arc of the paper. We have shown that missingness is (1) widespread, (2) return-relevant at the characteristic level, and (3) forecastable from observable firm attributes. Together, these facts establish that missingness is a structured, economically meaningful phenomenon — not noise to be discarded or filled with a simple statistic. Any imputation approach that ignores this structure will produce imputed values that are systematically biased in the direction of the firms least likely to go missing, distorting factor estimates and cross-sectional regressions downstream.

---

## Section 6: Conclusion (~ 0.5 pages)

We replicate the four core stylized facts documented in Bryzgalova et al. (2025) and extend the analysis in two directions. First, we decompose the aggregate return-missingness relationship to the characteristic level, finding that the missingness premium is pervasive rather than driven by a small number of variables. Second, we demonstrate that missingness is predictable out-of-sample using simple firm-level attributes, providing a forward-looking rationale for principled imputation methods.

The results reinforce the paper's central contribution: missing financial data is not an innocuous data management problem but a structured feature of the cross-section that interacts with firm fundamentals, return dynamics, and the reliability of any empirical asset pricing exercise that relies on firm characteristics as inputs.

---

## Appendix: Data Construction Notes

- Characteristics list: [enumerate the 45 variables used]
- WRDS query structure: Compustat annual/quarterly merged with CRSP monthly
- Missing definition: following the paper, a variable is defined as missing if it is not available in the raw data and cannot be computed from available inputs
- Sample: NYSE/AMEX/NASDAQ common shares (share codes 10, 11), excluding financials and utilities where noted
