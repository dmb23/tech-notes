
# Maximum Likelihood 

## Linear regression with squared loss

Assume that observations arise from noisy measurements with normally distributed noise
$$y = \bm{w}^T \bm{x} + b + \epsilon \quad \text{ where } \epsilon \sim \mathcal{N}(0, \sigma^2) $$
Then the *likelihood* of $y$ for a given $\bm{x}$ is
$$P(y | \bm{x}) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp \left(-\frac{1}{2\sigma^2}(y - \bm{w}^T\bm{x} - b)^2\right)$$
The *principle of maximum likelihood* says the best values for $(\bm{w}, x)$ are those that maximize the *likelihood* of the entire dataset:
$$P(\bm{y} \ \bm{X}) = \prod_{i=1}^n p(y^{(i)} | \bm{x}^{(i)})$$
- we assume all pairs $(\bm{x}^{(i)}, y^{(i)})$ are drawn independently, so we can take the product
- we can equivalently maximize the log of the likelihood to get rid of the product: $$\log P(\bm{y} | \bm{X}) = \sum_{i=1}^n - \frac{1}{2} \log (2\pi\sigma^2) - \frac{1}{2\sigma^2}\left(y^{(i)} - \bm{w}^T\bm{x}^{(i)} - b\right)^2$$
- we can equivalently minimize the negative log, since minimization is easier than maximization: $$- \log P(\bm{y} | \bm{X}) = \sum_{i=1}^n \frac{1}{2} \log (2\pi\sigma^2) + \frac{1}{2\sigma^2}\left(y^{(i)} - \bm{w}^T\bm{x}^{(i)} - b\right)^2$$
- We assume $\sigma$ to be fixed: The first term does not depend on $(\bm{w}, b)$, so it can be ignored. The second term is equivalent to the sum of squared error up to a constant factor. 

So minimizing the squared error is equivalent to finding a maximum likelihood estimation.