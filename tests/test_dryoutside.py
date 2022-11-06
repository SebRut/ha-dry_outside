from custom_components.dry_outside.dryoutside import should_dry_outside

async def test_dryoutside_if_freezing():
    assert await should_dry_outside(-0, 10)
    assert await should_dry_outside(-5, 30)
    assert await should_dry_outside(-10, 50)
    assert await should_dry_outside(-20, 70)

async def test_dryoutside_if_low_humidity():
    assert await should_dry_outside(10, 10)
    assert await should_dry_outside(20, 30)
    assert await should_dry_outside(30, 50) == False
