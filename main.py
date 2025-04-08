import datetime
import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import arrow
import typer
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.webdriver import webdriver
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from dateutil.parser import parser as dateutil_parser
from rich.console import Console
from rich.logging import RichHandler

ANDROID_APP_ID = "com.aqsmartphone.android.nissan"

LAUNCH_SIGN_IN_BUTTON = f"{ANDROID_APP_ID}:id/btnsignin"
USER_ID_TEXT_FIELD_ELEMENT_ID = f"{ANDROID_APP_ID}:id/username"
PASSWORD_TEXT_FIELD_ELEMENT_ID = f"{ANDROID_APP_ID}:id/passwordEdit"
SUBMIT_SIGN_IN_BUTTON = f"{ANDROID_APP_ID}:id/signin"

ENTER_DEMO_MODE_BUTTON_ID = f"{ANDROID_APP_ID}:id/demoMode"
TV_SKIP_STEP_1_BUTTON_ID = f"{ANDROID_APP_ID}:id/tv_skip_step1"
DO_NOT_SHOW_AGAIN_BUTTON_ID = f"{ANDROID_APP_ID}:id/not_show_again"

REFRESH_BUTTON_ELEMENT_ID = f"{ANDROID_APP_ID}:id/refresh_icon"

REFRESH_STATUS_TEXT_ELEMENT_ID = f"{ANDROID_APP_ID}:id/refreshdate"
BATTERY_STATE_OF_CHARGE_TEXT_ELEMENT_ID = f"{ANDROID_APP_ID}:id/pluginstatus"
CHARGER_STATE_TEXT_ELEMENT_ID = f"{ANDROID_APP_ID}:id/charge"
MILE_RANGE_MINIMUM_TEXT_ELEMENT_ID = f"{ANDROID_APP_ID}:id/minval"
MILE_RANGE_MAXIMUM_TEXT_ELEMENT_ID = f"{ANDROID_APP_ID}:id/maxval"
LEVEL_TWO_CHARGER_ETA_TEXT_ELEMENT_ID = f"{ANDROID_APP_ID}:id/standard_value"
INTERIOR_TEMPERATURE_TEXT_ELEMENT_ID = f"{ANDROID_APP_ID}:id/interiortemp"


logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=Console(stderr=True))],
)

logger = logging.getLogger()

app = typer.Typer(add_completion=False, pretty_exceptions_show_locals=False)


@dataclass
class VehicleData:
    last_refresh_date: str
    battery_state_of_charge: str
    charger_state: str
    range_minimum: str
    range_maximum: str
    interior_temperature_range: str
    level_two_charger_eta: str


@contextmanager
def appium_service(**kwargs):
    service = AppiumService()
    logger.info("Starting Appium service...")
    service.start(**kwargs)
    yield service
    service.stop()


@contextmanager
def appium_driver(server_url: str, server_port: str, capabilities: dict):
    logger.info("Starting UiAutomator2 driver...")
    driver = webdriver.WebDriver(
        f"http://{server_url}:{server_port}",
        options=UiAutomator2Options().load_capabilities(capabilities),
    )
    yield driver
    driver.quit()


def navigate_to_vehicle_screen_from_logged_out(driver, demo, user_id, password):
    if not demo and user_id and password:
        logger.info("Tapping sign in button...")
        launch_sign_in_button = driver.find_element(by=AppiumBy.ID, value=LAUNCH_SIGN_IN_BUTTON)
        launch_sign_in_button.click()
        logger.info("Typing in provided username...")
        user_id_text_field = driver.find_element(by=AppiumBy.ID, value=USER_ID_TEXT_FIELD_ELEMENT_ID)
        user_id_text_field.send_keys(user_id)
        logger.info("Typing in provided password...")
        password_text_field = driver.find_element(by=AppiumBy.ID, value=PASSWORD_TEXT_FIELD_ELEMENT_ID)
        password_text_field.send_keys(password)
        logger.info("Tapping sign in button...")
        submit_sign_in_button = driver.find_element(by=AppiumBy.ID, value=SUBMIT_SIGN_IN_BUTTON)
        submit_sign_in_button.click()
    else:
        if not demo:
            logger.warning("User ID or password missing, entering demo mode...")
        logger.info("Tapping demo mode button...")
        demo_mode_button = driver.find_element(by=AppiumBy.ID, value=ENTER_DEMO_MODE_BUTTON_ID)
        demo_mode_button.click()


@app.command(no_args_is_help=True)
def main(
    nissan_connect_app_apk: Annotated[
        Path,
        typer.Argument(
            resolve_path=True,
            file_okay=True,
            dir_okay=False,
            exists=True,
            help="Path to Nissan Connect app APK",
            envvar="NISSAN_CONNECT_APP_APK",
        ),
    ],
    user_id: Annotated[str | None, typer.Option(help="user ID", envvar="NISSAN_CONNECT_USER_ID")] = None,
    password: Annotated[str | None, typer.Option(help="password", envvar="NISSAN_CONNECT_PASSWORD")] = None,
    demo: Annotated[bool, typer.Option(help="Use demo mode", envvar="NISSAN_CONNECT_DEMO")] = False,
    appium_server_url: Annotated[str, typer.Option(help="Appium server URL", envvar="APPIUM_SERVER_URL")] = "localhost",
    appium_server_port: Annotated[int, typer.Option(help="Appium server port", envvar="APPIUM_SERVER_PORT")] = 4723,
    avd: Annotated[
        str | None,
        typer.Option(help="Android Virtual Device name", envvar="ANDROID_VIRTUAL_DEVICE"),
    ] = None,
    convert_times_to_timezone: Annotated[
        str | None,
        typer.Option(help="Convert times to timezone (e.g. 'US/Pacific')", envvar="CONVERT_TIMES_TO_TIMEZONE"),
    ] = None,
):
    capabilities = dict(
        platformName="Android",
        automationName="uiautomator2",
        deviceName="Android",
        language="en",
        locale="US",
        autoGrantPermissions=True,
        uiautomator2ServerInstallTimeout=120000,
    )
    if avd:
        capabilities["appium:avd"] = avd
    capabilities["appium:app"] = str(nissan_connect_app_apk)

    with (
        appium_service(
            args=["--address", appium_server_url, "-p", str(appium_server_port)],
            timeout_ms=10000,
        ),
        appium_driver(appium_server_url, str(appium_server_port), capabilities) as driver,
    ):
        try:
            driver.implicitly_wait(60)

            navigate_to_vehicle_screen_from_logged_out(driver, demo, user_id, password)

            for button_name, button_id in [
                ("skip button", TV_SKIP_STEP_1_BUTTON_ID),
                ("do not show again button", DO_NOT_SHOW_AGAIN_BUTTON_ID),
            ]:
                logger.info(f"Tapping {button_name}...")
                button = driver.find_element(by=AppiumBy.ID, value=button_id)
                button.click()

            # On some devices the app gets backgrounded here; if that happens, bring
            # it back to the foreground then get the app back to where we were
            APP_STATE_IS_RUNNING_IN_FOREGROUND = 4
            if driver.query_app_state(ANDROID_APP_ID) != APP_STATE_IS_RUNNING_IN_FOREGROUND:
                logger.info("App was backgrounded, bringing it back to the foreground...")
                driver.activate_app(ANDROID_APP_ID)
                navigate_to_vehicle_screen_from_logged_out(driver, demo, user_id, password)

            refresh_status_timeout_seconds = 30
            logger.info(f"Waiting up to {refresh_status_timeout_seconds} seconds for data refresh to complete...")
            refresh_status_element = driver.find_element(by=AppiumBy.ID, value=REFRESH_STATUS_TEXT_ELEMENT_ID)
            deadline = time.time() + refresh_status_timeout_seconds
            while time.time() < deadline:
                if refresh_status_element.text != "Please wait...":
                    break
                time.sleep(1)
            else:
                raise TimeoutError(f"Timed out waiting for refresh after {refresh_status_timeout_seconds} seconds")

            # e.g. "UPDATED MAR 05, 2025, 06:31 AM"
            last_refresh_date = refresh_status_element.text.removeprefix("UPDATED").strip()
            last_refresh_date = arrow.get(dateutil_parser().parse(last_refresh_date).astimezone(datetime.timezone.utc))
            if convert_times_to_timezone:
                last_refresh_date = last_refresh_date.to(convert_times_to_timezone)

            for key, value in VehicleData(
                # e.g. "Mon, Apr 7, 8:03 PM"
                last_refresh_date=last_refresh_date.format("ddd, MMM D, h:mm A"),
                battery_state_of_charge=driver.find_element(
                    by=AppiumBy.ID, value=BATTERY_STATE_OF_CHARGE_TEXT_ELEMENT_ID
                ).text,
                charger_state=driver.find_element(by=AppiumBy.ID, value=CHARGER_STATE_TEXT_ELEMENT_ID).text,
                range_minimum=driver.find_element(by=AppiumBy.ID, value=MILE_RANGE_MINIMUM_TEXT_ELEMENT_ID).text,
                range_maximum=driver.find_element(by=AppiumBy.ID, value=MILE_RANGE_MAXIMUM_TEXT_ELEMENT_ID).text,
                interior_temperature_range=driver.find_element(
                    by=AppiumBy.ID, value=INTERIOR_TEMPERATURE_TEXT_ELEMENT_ID
                ).text,
                level_two_charger_eta=driver.find_element(
                    by=AppiumBy.ID, value=LEVEL_TWO_CHARGER_ETA_TEXT_ELEMENT_ID
                ).text,
            ).__dict__.items():
                print(f"{key.replace('_', '-')}={value}")
        except Exception:
            time.sleep(3)
            driver.save_screenshot("last_screenshot.png")
            raise


if __name__ == "__main__":
    app()
