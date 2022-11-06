async def should_dry_outside(temp_in_c: float, humidity: float) -> bool:
    if temp_in_c <= 0:
        return True

    if humidity <= 40:
        return True

    return False
