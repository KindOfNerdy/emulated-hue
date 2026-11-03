"""Controllers for emulated_hue."""
import asyncio
import logging

from emulated_hue.utils import load_json

from . import scheduler
from .config import Config
from .homeassistant import HomeAssistantController, parse_include_labels
from .models import Controller
from .scheduler import add_scheduler, remove_scheduler  # noqa

LOGGER = logging.getLogger(__name__)

# written by the Supervisor with the add-on options
SUPERVISOR_OPTIONS_FILE = "/data/options.json"


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
    # optional filter: only export lights carrying one of these HA label_ids.
    # The add-on option (comma separated) takes precedence over the key in
    # emulated_hue.json.
    option_labels = parse_include_labels(
        load_json(SUPERVISOR_OPTIONS_FILE).get("include_labels")
    )
    json_labels = parse_include_labels(
        ctl.config_instance.get_storage_value("include_labels")
    )
    if json_labels and not option_labels:
        LOGGER.info(
            "emulated_hue.json contains include_labels %s (still used). To manage it "
            "in the add-on configuration, enter this in the option include_labels: %s",
            sorted(json_labels),
            ",".join(sorted(json_labels)),
        )
    elif json_labels and json_labels != option_labels:
        LOGGER.warning(
            "include_labels in emulated_hue.json %s is ignored, the add-on option %s "
            "takes precedence.",
            sorted(json_labels),
            sorted(option_labels),
        )
    include_labels = option_labels or json_labels
    if include_labels:
        ctl.controller_hass.include_labels = include_labels
        LOGGER.info(
            "include_labels %s (from %s): exporting %s of %s lights",
            sorted(include_labels),
            "add-on option" if option_labels else "emulated_hue.json",
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
