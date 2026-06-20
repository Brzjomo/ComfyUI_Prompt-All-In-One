from openai import OpenAI
import os


class DeepSeek:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "model": (
                    [
                        "deepseek-v4-flash",
                        "deepseek-v4-pro",
                    ],
                    {"default": "deepseek-v4-flash"},
                ),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "thinking")
    FUNCTION = "generate"
    CATEGORY = "🎤MW/MW-Prompt-All-In-One"

    def generate(
        self,
        api_key,
        system_prompt,
        prompt,
        model,
        seed,
    ):
        if os.getenv("DEEPSEEK_API_KEY") is not None:
            API_KEY = os.getenv("DEEPSEEK_API_KEY")
        elif api_key.strip() != "":
            API_KEY = api_key
        else:
            raise ValueError("API Key is not set")

        client = OpenAI(
            api_key=API_KEY,
            base_url="https://api.deepseek.com",
        )

        messages = []
        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            seed=seed,
            stream=False,
        )

        thinking = getattr(completion.choices[0].message, "reasoning_content", "") or ""

        return (completion.choices[0].message.content, thinking)
