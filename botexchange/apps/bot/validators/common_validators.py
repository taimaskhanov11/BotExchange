thematics = ("auto", "sport", "crypt", "investment", "blog", "news", "memes", "music", "films", "18+")
platforms = ("channel", "bot", "chat", "any")


def platform_type_validator(platform: str) -> bool:
    if platform not in platforms:
        return False
    return True


def thematic_validator(thematic):
    if thematic not in thematics:
        return False
    return True
