"""Controllers for emulated_hue."""
import asyncio
import logging

from . import scheduler
from .config import Config
from .homeassistant import HomeAssistantController
from .models import Controller
from .scheduler import add_scheduler, remove_scheduler  # noqa

LOGGER = logging.getLogger(__name__)


async def async_start(
    url, token, data_path, http_port, https_port, use_default_ports
) -> Controller:
    """Initialize all controllers."""
    ctl = Controller()
    ctl.loop = asyncio.get_event_loop()
    # the HA client is initialized in the async_start because it needs a running loop
    ctl.controller_hass = HomeAssistantController(url=url, token=token)
    ctl.config_instance = Config(
        ctl, data_path, http_port, https_port, use_default_ports
    )
    await ctl.controller_hass.connect()
    # optional filter: only export lights carrying one of these HA label_ids
    include_labels = ctl.config_instance.get_storage_value("include_labels")
    if include_labels:
        if isinstance(include_labels, str):
            include_labels = [include_labels]
        ctl.controller_hass.include_labels = set(include_labels)
        LOGGER.info(
            "include_labels %s: exporting %s of %s lights",
            sorted(include_labels),
            len(ctl.controller_hass.get_entities()),
            len(ctl.controller_hass.items_by_domain("light")),
        )
    return ctl


async def async_stop(ctl: Controller) -> None:
    """Shutdown all controllers."""
    await scheduler.async_stop()
    try:
        await ctl.controller_hass.disconnect()
    except AttributeError:
        # controller_hass is not initialized if home assistant isn't connected
        pass
