# Timings
- `schnell` - 968 * 544 - 3min 20 sec
- `schnell` - 1920 * 1080 - 
# "Works on my machine"

To set up the environment that lets me run the script:
- git clone the FLUX.1 repo
- create new venv with Python 3.10 `uv venv -p "$(uv python find cpython-3.10)"`
- install the proposed requirements `uv pip install -e .`
- fix versions for torch `uv pip install torch==2.3.1 torchaudio==2.3.1 torchvision==0.18.1`
- add random version for diffusers `uv pip install accelerate git+https://github.com/huggingface/diffusers.git` (at the moment 0.31.0.dev0)

Then use a python script from random person on the internet that found a way to use MPS:
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