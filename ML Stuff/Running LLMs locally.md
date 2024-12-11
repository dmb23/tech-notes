>[INFO]Everything is based around llama-cpp
>Some solutions take over building llama-cpp, some apparently ship a pre-built release?


- [llama.cpp](https://github.com/ggerganov/llama.cpp) the GOAT
- [GPT4All](https://github.com/nomic-ai/gpt4all) - Visual Interface + Python Bindings, but limited functionality (since it tries to make it accessible to everyone)
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) speech-to-text locally - sounds promising
- [llama-cpp-python](https://llama-cpp-python.readthedocs.io/en/stable/) - Python bindings to llama.cpp - build process is included in installation, but seems to run on similar optimization levels


# Training Models locally

> [!HINT]
> so far it seems that there are lots of issues with MPS in pytorch

- using `transformers`: training BERT on MPS runs fine, training SmolLM2 has a memory leak apparently
- `llama.cpp` has dropped support for finetuning models
- `unsloth` uses custom Triton kernels (that only work on CUDA)

To test:
- MLX ? super specific...