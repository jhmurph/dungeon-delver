"""Shared utility functions for Dungeon Delver."""


def clamp(value: int, min_val: int, max_val: int) -> int:
    return max(min_val, min(max_val, value))


def roll_dice(num_dice: int, sides: int, modifier: int = 0) -> int:
    """Roll NdS+modifier. Example: roll_dice(2, 6, 3) rolls 2d6+3."""
    import random
    return sum(random.randint(1, sides) for _ in range(num_dice)) + modifier


def format_hp_bar(current: int, maximum: int, width: int = 20) -> str:
    """Return a text HP bar, e.g. [####......] 30/50."""
    if maximum <= 0:
        filled = 0
    else:
        filled = int((current / maximum) * width)
    bar = "#" * filled + "." * (width - filled)
    return f"[{bar}] {current}/{maximum}"


def center_text(text: str, width: int = 50) -> str:
    return text.center(width)


def paginate(lines: list, page_size: int = 10):
    """Print a list of lines in pages, pausing for input between pages."""
    for i in range(0, len(lines), page_size):
        print("\n".join(lines[i : i + page_size]))
        if i + page_size < len(lines):
            input("-- more -- (press Enter)")


def parse_direction(raw: str) -> str:
    """Expand direction shortcuts to full names. Returns raw input if unrecognized."""
    mapping = {
        "n": "north",
        "s": "south",
        "e": "east",
        "w": "west",
        "u": "up",
        "d": "down",
    }
    return mapping.get(raw.strip().lower(), raw)


def pluralize(count: int, singular: str, plural: str = "") -> str:
    if count == 1:
        return f"{count} {singular}"
    return f"{count} {plural or singular + 's'}"


# TODO: add colorama-based helpers: red(), green(), yellow(), bold()
# These would wrap combat output to make hits/misses visually distinct
