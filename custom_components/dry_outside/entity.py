from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class DryOutsideEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self) -> str | None:
        return DOMAIN + "-" + str(self.config_entry.weather_entity).split(".")[1]
