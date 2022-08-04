class StartCommandResponse:
    @classmethod
    def private_chat(cls):
        return f"Hi, I can do floppy things...\n\nMaybe you need some /help?"

    @classmethod
    def group_chat(cls):
        return "What are you doing? We're not in PMs"
