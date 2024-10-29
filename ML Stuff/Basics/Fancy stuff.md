
# Maximum Likelihood 

## Linear regression with squared loss

Assume that observations arise from noisy measurements with normally distributed noise
$$y = \bm{w}^T \bm{x} + b + \epsilon \quad \text{ where } \epsilon \sim \mathcal{N}(0, \sigma^2) $$
Then the *likelihood* of $y$ for a given $\bm{x}$ is
$$P(y | \bm{x}) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp \left(-\frac{1}{2\sigma^2}(y - \bm{w}^T\bm{x} - b)^2\right)$$
