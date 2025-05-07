# General Task
given an integer (bigbigbig ??? 2 ** 128 ???)

- start with x1 = 1, x2 = 2, x3 = 3
- apply either
	- rule 1: x4 = x1 + x3, new triple = (x1, x3, x4)
	- rule 0: x4 = x2 + x3, new triple = (x2, x3, x4)
- until you arrive at the number
- goal: the shorter the better


### anderer stuff:
- original introduction for something else: https://cr.yp.to/ecdh/diffchain-20060219.pdf
- recent algorithms: https://eprint.iacr.org/2024/1044.pdf
# Approach
