import re


class TextPreprocessor:
    def prepare_input_text(self, text: str) -> set[str]:
        t = self.rm_non_eng_letters(text)
        t = self.normalize_words(t)
        return t

    @staticmethod
    def rm_non_eng_letters(text: str) -> str:
        reg = r'[^a-zA-Z-]'
        t = re.sub(
            reg, ' ', text
        )
        return t

    @staticmethod
    def normalize_words(text: str) -> set[str]:
        res = set()
        for w in set(text.split()):
            w = w.strip()  # .lower()
            res.update([w])
        return res
