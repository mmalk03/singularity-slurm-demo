import openai

from demo.vllm.prompt import Prompt
from demo.vllm.server import VllmServer


class VllmModel:
    def __init__(
        self,
        model_id: str,
        temperature: float = 1.0,
        max_tokens: int = 2048,
        max_output_tokens: int = 1536,
        tensor_parallel_size: int = 1,
    ):
        assert max_output_tokens < max_tokens
        self.server = VllmServer(
            model_id=model_id,
            custom_args=(
                "--max-model-len",
                str(max_tokens),
                *VLLM_MODEL_EXTRA_ARGS.get(model_id, []),
                *(
                    ("--tensor-parallel-size", str(tensor_parallel_size))
                    if tensor_parallel_size > 1
                    else ()
                ),
            ),
        )
        self.has_reasoning_content = "--enable-reasoning" in VLLM_MODEL_EXTRA_ARGS.get(
            model_id, []
        )
        self.model_id = model_id
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_output_tokens = max_output_tokens
        self.client = openai.Client(
            base_url=f"{self.server.url}/v1", api_key=self.server.api_key
        )

    def forward(self, prompt: Prompt, **kwargs) -> str:
        message = {
            "role": "user",
            "content": [{"type": "text", "text": prompt.format()}],
        }
        print(f"Model input:\n{message}")
        response = self.client.chat.completions.create(
            messages=[message],
            model=self.model_id,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
        )
        if self.has_reasoning_content:
            reasoning_content = response.choices[0].message.reasoning_content
            if reasoning_content:
                reasoning_content = reasoning_content.strip()
            print(f"Reasoning content:\n{reasoning_content}")
        content = response.choices[0].message.content
        if content:
            content = content.strip()
        print(f"Model response:\n{content}")
        return content


VLLM_MODEL_EXTRA_ARGS = {
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B": (
        # "--enable-reasoning",
        "--reasoning-parser",
        "deepseek_r1",
        "--gpu-memory-utilization",
        "0.95",
    ),
}
