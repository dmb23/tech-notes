
# Preliminary Definitions
### Addition Chain for integer $n$
> a sequence of integers $1 = c_0, c_1, ..., c_r=n$, such that 
> for each $i \in \{1, ..., r\}$ there exist $j, k \in \{0, ..., i-1\}$ such that $c_i = c_j + c_k$

Every entry in the chain of integers is the sum of two earlier entries.

### Differential addition chain for integer $n$
> a sequence of integers $1 = c_0, c_1, ..., c_r=n$, such that 
> for each $i \in \{1, ..., r\}$ there exist $j, k \in \{0, ..., i-1\}$ such that 
> - $c_i = c_j + c_k$
> - and $c_j - c_k \in \{0, c_0, c_1, ..., c_{i-1} \}$

For each addition, the difference is already in the chain or the difference is 0.

### Continued-fraction tuple sequence for $n \geq 3$
> a sequence of tuples of three integers $(a_2, b_2, c_2), ..., (a_r, b_r, c_r)$ where
> - $(a_2, b_2, c_2) = (1, 2, 3)$
> - c_r = n