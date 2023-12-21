class OpenAIConfig:
    def __init__(self, api_key, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, best_of) -> None:
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.best_of = best_of