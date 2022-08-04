class DecideCommandResponse:
    @classmethod
    def no_options(cls) -> str:
        return (
            "Then give me options to choose from!\n\n"
            "Either in one line:\n"
            "/decide <1> <2> <3>\n\n"
            "Or one per line:\n"
            "/decide <0>\n"
            "<1>\n"
            "<2>"
        )

    @classmethod
    def chosen(cls, one: str) -> str:
        return "I would choose:\n" f"{one}"
