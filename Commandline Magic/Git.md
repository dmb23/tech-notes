# Working with multiple identities in github

What works for me: connect via ssh, and use different SSH identities by manipulating the host:
- Create two SSH keys, `company1_id_rsa`, `personal_id_rsa`
- Create two entries in `~/.ssh/config`: 
```
HOST github.com-company1
	IdentityFile ~/.ssh/company1_id_rsa
	IdentitiesOnly yes
HOST github.com
	IdentityFile ~/.ssh/personal_id_rsa
	IdentitiesOnly yes
```
- connect the SSH keys to the corresponding accounts in github
- change the remote address from `*github.com*` to `*github.com-company1` when you want to connect via the company account