class ToggleBracketsResponse:
    @classmethod
    def on_enabled(cls) -> str:
        return "Oka, I will now do a little trolling with brackets))))))))"

    @classmethod
    def on_disabled(cls) -> str:
        return (
            "kk I will NOT react to your stupid brackets anymore.\n\n"
            "I know you won't miss it, ecks-dee."
        )
