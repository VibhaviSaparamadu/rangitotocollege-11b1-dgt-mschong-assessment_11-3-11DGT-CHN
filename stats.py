player_stats = {
    "wins": 0,
    "losses": 0,
    "high_score": 0,
    "rarest_item": "None"
}

def update_stats(wins=None, losses=None, high_score=None, rarest_item=None):
    if wins is not None:
        player_stats["wins"] = wins
    if losses is not None:
        player_stats["losses"] = losses
    if high_score is not None:
        player_stats["high_score"] = high_score
    if rarest_item is not None:
        player_stats["rarest_item"] = rarest_item
