def percentage(current, previous, pct=False):
    return current / previous - 1 if pct is False else (current / previous - 1) * 100
