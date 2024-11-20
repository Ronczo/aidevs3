from typing import List, Dict, Tuple
import re


class TextSplitter:
    SPECIAL_TOKENS = {
        "<|im_start|>": 100264,
        "<|im_end|>": 100265,
        "<|im_sep|>": 100266,
    }

    def __init__(self, model_name: str = "gpt-4o"):
        self.MODEL_NAME = model_name
        self.tokenizer = None

    async def initialize_tokenizer(self):
        if not self.tokenizer:
            # Replace with actual tokenizer initialization logic
            self.tokenizer = await create_by_model_name(
                self.MODEL_NAME, self.SPECIAL_TOKENS
            )

    def count_tokens(self, text: str) -> int:
        if not self.tokenizer:
            raise ValueError("Tokenizer not initialized")
        formatted_content = self.format_for_tokenization(text)
        tokens = self.tokenizer.encode(
            formatted_content, list(self.SPECIAL_TOKENS.keys())
        )
        return len(tokens)

    def format_for_tokenization(self, text: str) -> str:
        return f"<|im_start|>user\n{text}<|im_end|>\n<|im_start|>assistant<|im_end|>"

    async def split(self, text: str, limit: int) -> List[Dict]:
        await self.initialize_tokenizer()
        chunks = []
        position = 0
        total_length = len(text)
        current_headers = {}

        while position < total_length:
            chunk_text, chunk_end = self.get_chunk(text, position, limit)
            tokens = self.count_tokens(chunk_text)
            headers_in_chunk = self.extract_headers(chunk_text)
            self.update_current_headers(current_headers, headers_in_chunk)

            content, urls, images = self.extract_urls_and_images(chunk_text)

            chunks.append(
                {
                    "text": content,
                    "metadata": {
                        "tokens": tokens,
                        "headers": current_headers.copy(),
                        "urls": urls,
                        "images": images,
                    },
                }
            )
            position = chunk_end

        return chunks

    def get_chunk(self, text: str, start: int, limit: int) -> Tuple[str, int]:
        overhead = self.count_tokens(
            self.format_for_tokenization("")
        ) - self.count_tokens("")
        end = min(
            start + int((len(text) - start) * limit / self.count_tokens(text[start:])),
            len(text),
        )
        chunk_text = text[start:end]
        tokens = self.count_tokens(chunk_text)

        while tokens + overhead > limit and end > start:
            end = self.find_new_chunk_end(text, start, end)
            chunk_text = text[start:end]
            tokens = self.count_tokens(chunk_text)

        end = self.adjust_chunk_end(text, start, end, tokens + overhead, limit)
        return text[start:end], end

    def adjust_chunk_end(
        self, text: str, start: int, end: int, current_tokens: int, limit: int
    ) -> int:
        min_chunk_tokens = limit * 0.8
        next_newline = text.find("\n", end)
        prev_newline = text.rfind("\n", start, end)

        if next_newline != -1 and next_newline < len(text):
            extended_end = next_newline + 1
            chunk_text = text[start:extended_end]
            tokens = self.count_tokens(chunk_text)
            if tokens <= limit and tokens >= min_chunk_tokens:
                return extended_end

        if prev_newline > start:
            reduced_end = prev_newline + 1
            chunk_text = text[start:reduced_end]
            tokens = self.count_tokens(chunk_text)
            if tokens <= limit and tokens >= min_chunk_tokens:
                return reduced_end

        return end

    def find_new_chunk_end(self, text: str, start: int, end: int) -> int:
        new_end = end - max(1, (end - start) // 10)
        return max(new_end, start + 1)

    def extract_headers(self, text: str) -> Dict[str, List[str]]:
        headers = {}
        header_regex = re.compile(r"(^|\n)(#{1,6})\s+(.*)")
        for match in header_regex.finditer(text):
            level = len(match.group(2))
            content = match.group(3).strip()
            key = f"h{level}"
            headers.setdefault(key, []).append(content)
        return headers

    def update_current_headers(
        self, current: Dict[str, List[str]], extracted: Dict[str, List[str]]
    ):
        for level in range(1, 7):
            key = f"h{level}"
            if key in extracted:
                current[key] = extracted[key]
                self.clear_lower_headers(current, level)

    def clear_lower_headers(self, headers: Dict[str, List[str]], level: int):
        for l in range(level + 1, 7):
            headers.pop(f"h{l}", None)

    def extract_urls_and_images(self, text: str) -> Tuple[str, List[str], List[str]]:
        urls, images = [], []
        url_index, image_index = 0, 0

        def replace_image(match):
            nonlocal image_index
            images.append(match.group(2))
            return f"![{match.group(1)}]({{$img{image_index}}})"

        def replace_url(match):
            nonlocal url_index
            urls.append(match.group(2))
            return f"[{match.group(1)}]({{$url{url_index}}})"

        content = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, text)
        content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_url, content)
        return content, urls, images
