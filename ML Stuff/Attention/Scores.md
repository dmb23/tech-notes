# Perplexity

Perplexity is a quality measure for a language model: A model that provides $P(x_t | x_{t-1}, \ldots, x_1)$.
A perfect model that always predicts probability of 1 for the correct next token, would have a perplexity of 0, higher values are worse.

We can calculate the cross-entropy loss averaged over all tokens of a sequence to have a measure of how well the model is encoding this sequence: $$\frac{1}{n}\sum_{t=1}^n - \log P(x_t | x_{t-1}, \ldots, x_1)$$
NLP prefers **perplexity**, the exponential of that quantity: $$\exp \left(\frac{1}{n}\sum_{t=1}^n - \log P(x_t | x_{t-1}, \ldots, x_1)\right)$$
# BLEU - Bilingual Evaluation Understudy

Measure the quality of of a predicted sequence to a target sequence by calculating

> For any n-gram in the predicted sequence, evaluate whether it appears in the target sequence:
> $$\exp \left( \min \left( 0, 1-\frac{\text{len}_\text{label}}{\text{len}_\text{pred}}\right)\right) \quad \prod_{n=1}^k p_n^{1/2^n}$$

where
- $p_n$ is the precision of an $n$-gram, i.e. the ratio of predicted $n$-grams taht are in the target sequence to total number of predicted $n$-grams
- $k$ is the longest n-gram used in the evaluation
- for a fixed $p_n$, the value of $p_n^{1/2^n}$ grows with $n$, so BLEU values longer $n$-grams stronger
- predicting shorter sequences tends to produce better $p_n$ values, so the first factor penalizes shorter sequences


