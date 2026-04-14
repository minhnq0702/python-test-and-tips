class Solution:
    """
    Break words by word dict
    Ex: catsanddog - [cat, cats, sand, dog]
    """

    def addSpace(self, s: str, word_dict: list[str]) -> list[str]:
        def backTracking(_s: str, _w: str) -> list[list[str]]:
            if _s.startswith(_w):
                return
            return []

        # ? should clean up ?
        for w in word_dict:
            if w not in s:
                word_dict.remove(w)

        results: list[list[str]] = []
        while True:
            for w in word_dict:
                if s.startswith(w):
                    results += backTracking(s, w)
        return []
