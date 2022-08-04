import re


class _Animation:
    def __init__(self, regex: str, link: str):
        self.regex = regex
        self.link = link


class RegexKeywordSearchUseCase:
    _animations = [
        _Animation(
            r"(/flop_issue)|(flop_issue)|(flop issue)|(flop.+issue)",
            "https://tenor.com/view/diagnosis-issue-flop-flop-floppa-bingus-gif-22901732",
        ),
        _Animation(
            r"(cube)|(куб)",
            "https://tenor.com/view/floppa-me-when-definitely-gif-25266239",
        ),
        _Animation(
            r"(flop)|(шлеп)|(шлёп)",
            "https://tenor.com/view/sam-moser-niluv-patel-shake-caracal-big-floppa-gif-20103660",
        ),
    ]

    def __init__(self, text: str):
        self.text = text.lower()

    async def execute(self) -> str | None:
        for animation in self._animations:
            if re.search(animation.regex, self.text) is not None:
                return animation.link
        return None
