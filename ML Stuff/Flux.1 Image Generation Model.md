# "Works on my machine"

- fix versions, state 2024/08/15 (torch current = 2.4.0)
	- `torch==2.3.1`
	- `torchvision==0.18.1`
	- `torchaudio==2.3.1`
- use python script from random person on the internet:
```python
# Adjust ROPE (Rotary Positional Encodings?) to offload MPS-breaking steps to CPU
_flux_rope = diffusers.models.transformers.transformer_flux.rope

def new_flux_rope(pos: torch.Tensor, dim: int, theta: int) -> torch.Tensor:
    assert dim % 2 == 0, "The dimension must be even."
    if pos.device.type == "mps":
        return _flux_rope(pos.to("cpu"), dim, theta).to(device=pos.device)
    else:
        return _flux_rope(pos, dim, theta)

diffusers.models.transformers.transformer_flux.rope = new_flux_rope

# Load the Flux Schnell model to MPS
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell", revision="refs/pr/1", torch_dtype=torch.bfloat16
).to("mps")
```

- [ ] interesting to use DEV instead of SCHNELL
- [ ] check how long I have to wait for an image...