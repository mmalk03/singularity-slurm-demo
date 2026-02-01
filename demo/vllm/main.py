import sys

from demo.vllm.model import VllmModel
from demo.vllm.prompt import ConstantPrompt

if __name__ == "__main__":
    print(f"Arguments: {sys.argv}")
    if len(sys.argv) == 1:
        print(f"Starting single-GPU inference")
        model = VllmModel("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
    elif len(sys.argv) == 2:
        tensor_parallel_size = int(sys.argv[1])
        print(
            f"Starting multi-GPU inference with tensor parallelism: {tensor_parallel_size}"
        )
        model = VllmModel(
            "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
            tensor_parallel_size=tensor_parallel_size,
        )
    else:
        raise ValueError(f"Usage: {sys.argv[0]} [tensor parallelism (int)]")
    prompt = ConstantPrompt("What's the capital of Poland?")
    response = model.forward(prompt)
    assert "Warsaw" in response
