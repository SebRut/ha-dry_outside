from homeassistant.helpers.update_coordinator import CoordinatorEntity


class DryOutsideEntity(CoordinatorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)