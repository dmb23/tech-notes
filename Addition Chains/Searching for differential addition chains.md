
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
> - $c_r = n$
> - for each $i \in \{3, ..., r\}$ one has
> 	- either $(a_i, b_i, c_i) = (b_{i-1}, c_{i-1}, c_{i-1} + b_{i-1})$
> 	- or $(a_i, b_i, c_i) = (a_{i-1}, c_{i-1}, c_{i-1} + a_{i-1})$

each tuple satisfies $c_i = a_i + b_i$

### Contined-fraction differential addition chain for $n \geq 3$
> a chain of the form $1, 2, c_2, ..., c_r=n$ 
> where $(a_2, b_2, c_2), ..., (a_r, b_r, c_r)$ is a continued-fraction tuple sequence for $n$

The chain is 1, 2 followed by the last entry in each tuple. 
This creates a differential addition chain.

### Compression
A continued-fraction tuple sequence can be determined by one bit at each position:
- rule 0 (Bit $f_i=0$): $(a_i, b_i, c_i) = (b_{i-1}, c_{i-1}, c_{i-1} + b_{i-1})$
- rule 1 (Bit $f_i = 1$): $(a_i, b_i, c_i) = (a_{i-1}, c_{i-1}, c_{i-1} + a_{i-1})$

That way a length-$r$ continued-fraction differential addition chain $1, 2, c_2, ..., c_r$ can be compressed to just $r-2$ bits $f_3, ..., f_r$ 


# Searching for differential addition chains

