thematics = (
    "auto",
    "sport",
    "crypt",
    "investment",
    "blog",
    "news",
    "memes",
    "music",
    "films",
    "18+",
)
platforms = ("channel", "bot", "chat", "any")

channel_thematic = (
    "auto and moto",
    "author blogs",
    "business and startups",
    "in the world of animals",
    "video games",
    "children and parents",
    "other",
    "food and cooking",
    "health and medicine",
    "celebrities and lifestyle",
    "investments",
    "foreign languages",
    "internet technology",
    "art and design",
    "history",
    "movies",
    "books",
    "beauty and care",
    "cryptocurrencies",
    "culture and events",
    "interesting facts",
    "marketing and PR",
    "fashion and style",
    "motivation and self",
    "music",
    "science and technology",
    "real estate",
    "news and media",
    "education",
    "leisure and entertainment",
    "psychology and relationships",
    "travel and tourism",
    "jobs and vacancies",
    "regional",
    "religion and spirituality",
    "discounts and promotions",
    "sports",
    "betting and gambling",
    "construction and repair",
    "trading",
    "fitness",
    "hobbies and entertainment",
    "economics and finance",
    "humor and memes",
    "jurisprudence",
    "18+",
)
bot_thematic = (
    "auto and moto",
    "business and startups",
    "video games",
    "other",
    "investments",
    "foreign languages",
    "art and design",
    "movies",
    "books",
    "cryptocurrencies",
    "marketing and PR",
    "fashion and style",
    "motivation and self",
    "music",
    "science and technology",
    "real estate",
    "news and media",
    "education",
    "leisure and entertainment",
    "jobs and vacancies",
    "discounts and promotions",
    "sports",
    "betting and gambling",
    "trading",
    "fitness",
    "hobbies and entertainment",
    "economics and finance",
    "humor and memes",
    "18+",
)


def platform_type_validator(platform: str) -> bool:
    if platform not in platforms:
        return False
    return True


def thematic_validator(thematic, platform: str) -> bool:
    if thematic in ("left", "right"):
        return True
    elif platform == "bot":
        if thematic in bot_thematic:
            return True
    else:
        if thematic in channel_thematic:
            return True
    return False
