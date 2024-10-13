from openai import OpenAI

def modelList(mode: str) -> list:
    if mode == "General Chat":
        model_list = [
            "deepseek-ai/DeepSeek-V2.5",
            "Qwen/Qwen2.5-72B-Instruct-128K",
            "meta-llama/Meta-Llama-3.1-405B-Instruct",
            "deepseek-ai/DeepSeek-Coder-V2-Instruct",
            "Qwen/Qwen2.5-Math-72B-Instruct"]
    elif mode == "Link Reader":
        model_list = [
            "deepseek-ai/DeepSeek-V2.5",
            "Qwen/Qwen2.5-72B-Instruct-128K",
            "meta-llama/Meta-Llama-3.1-405B-Instruct"]
    elif mode == "Translator":
        model_list = [
            "deepseek-ai/DeepSeek-V2.5"]
    return model_list

class Chat:
    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key: str = api_key
        self.base_url: str = base_url
    
    def general_chat(
        self,
        model: str,
        messages: list,
        max_tokens: int,
        temperature: float,
        top_p: float,
        frequency_penalty: float,
        presence_penalty: float,
        stop: list = None,
        stream: bool = True):
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            stream=stream)
        return response