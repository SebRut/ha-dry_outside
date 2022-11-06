from custom_components.dry_outside.dryoutside import should_dry_outside

async def test_dryoutside():
    assert await should_dry_outside()
