from contextlib import contextmanager
from pathlib import Path
import time
from typing import Annotated

from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import typer


LAUNCH_SIGN_IN_BUTTON = "com.aqsmartphone.android.nissan:id/btnsignin"
USER_ID_TEXT_FIELD_ELEMENT_ID = "com.aqsmartphone.android.nissan:id/username"
PASSWORD_TEXT_FIELD_ELEMENT_ID = "com.aqsmartphone.android.nissan:id/passwordEdit"
SUBMIT_SIGN_IN_BUTTON = "com.aqsmartphone.android.nissan:id/signin"

ENTER_DEMO_MODE_BUTTON_ID = "com.aqsmartphone.android.nissan:id/demoMode"
TV_SKIP_STEP_1_BUTTON_ID = "com.aqsmartphone.android.nissan:id/tv_skip_step1"
DO_NOT_SHOW_AGAIN_BUTTON_ID = "com.aqsmartphone.android.nissan:id/not_show_again"

REFRESH_BUTTON_ELEMENT_ID = "com.aqsmartphone.android.nissan:id/refresh_icon"

REFRESH_STATUS_TEXT_ELEMENT_ID = "com.aqsmartphone.android.nissan:id/refreshdate"
BATTERY_STATE_OF_CHARGE_TEXT_ELEMENT_ID = "com.aqsmartphone.android.nissan:id/pluginstatus"
CHARGER_STATE_TEXT_ELEMENT_ID = "com.aqsmartphone.android.nissan:id/charge"
MILE_RANGE_MINIMUM_TEXT_ELEMENT_ID = "com.aqsmartphone.android.nissan:id/minval"
MILE_RANGE_MAXIMUM_TEXT_ELEMENT_ID = "com.aqsmartphone.android.nissan:id/maxval"
LEVEL_TWO_CHARGER_ETA_TEXT_ELEMENT_ID = "com.aqsmartphone.android.nissan:id/standard_value"
INTERIOR_TEMPERATURE_TEXT_ELEMENT_ID = "com.aqsmartphone.android.nissan:id/interiortemp"


@contextmanager
def appium_service(**kwargs):
    service = AppiumService()
    service.start(**kwargs)
    yield service
    service.stop()


@contextmanager
def appium_driver(server_url: str, server_port: str, capabilities: dict):
    driver = webdriver.Remote(f"http://{server_url}:{server_port}", options=UiAutomator2Options().load_capabilities(capabilities))
    yield driver
    driver.quit()


def main(
    nissan_connect_app_apk: Annotated[Path, typer.Argument(resolve_path=True, file_okay=True, dir_okay=False, exists=True, help="Path to Nissan Connect app APK", envvar="NISSAN_CONNECT_APP_APK")],
    user_id: Annotated[str | None, typer.Option(help="user ID", envvar="NISSAN_CONNECT_USER_ID")] = None,
    password: Annotated[str | None, typer.Option(help="password", envvar="NISSAN_CONNECT_PASSWORD")] = None,
    demo: Annotated[bool, typer.Option(help="Use demo mode", envvar="NISSAN_CONNECT_DEMO")] = False,
    appium_server_url: Annotated[str, typer.Option(help="Appium server URL", envvar="APPIUM_SERVER_URL")] = 'localhost',
    appium_server_port: Annotated[int, typer.Option(help="Appium server port", envvar="APPIUM_SERVER_PORT")] = 4723,
):
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName='Android',
        language='en',
        locale='US',
    )
    capabilities["appium:avd"] = "Medium_Phone_API_35"
    capabilities["appium:app"] = str(nissan_connect_app_apk)

    with (
        appium_service(args=['--address', appium_server_url, '-p', str(appium_server_port)], timeout_ms=10000),
        appium_driver(appium_server_url, appium_server_port, capabilities) as driver,
    ):
        driver.implicitly_wait(30)

        if not demo and user_id and password:
            launch_sign_in_button = driver.find_element(by=AppiumBy.ID, value=LAUNCH_SIGN_IN_BUTTON)
            launch_sign_in_button.click()
            user_id_text_field = driver.find_element(by=AppiumBy.ID, value=USER_ID_TEXT_FIELD_ELEMENT_ID)
            user_id_text_field.send_keys(user_id)
            password_text_field = driver.find_element(by=AppiumBy.ID, value=PASSWORD_TEXT_FIELD_ELEMENT_ID)
            password_text_field.send_keys(password)
            submit_sign_in_button = driver.find_element(by=AppiumBy.ID, value=SUBMIT_SIGN_IN_BUTTON)
            submit_sign_in_button.click()
        else:
            if not demo:
                print("User ID or password missing, entering demo mode...")
            demo_mode_button = driver.find_element(by=AppiumBy.ID, value=ENTER_DEMO_MODE_BUTTON_ID)
            demo_mode_button.click()

        for button_id in [TV_SKIP_STEP_1_BUTTON_ID, DO_NOT_SHOW_AGAIN_BUTTON_ID]:
            button = driver.find_element(by=AppiumBy.ID, value=button_id)
            button.click()

        refresh_status_element = driver.find_element(by=AppiumBy.ID, value=REFRESH_STATUS_TEXT_ELEMENT_ID)
        refresh_status_timeout_seconds = 30
        deadline = time.time() + refresh_status_timeout_seconds
        while time.time() < deadline:
            if refresh_status_element.text != "Please wait...":
                break
            time.sleep(1)
        else:
            raise TimeoutError(f"Timed out waiting for refresh after {refresh_status_timeout_seconds} seconds")
        print(f"Last Refresh Date: {refresh_status_element.text}")

        battery_state_of_charge = driver.find_element(by=AppiumBy.ID, value=BATTERY_STATE_OF_CHARGE_TEXT_ELEMENT_ID).text
        print(f"Battery State of Charge: {battery_state_of_charge}")

        charger_state = driver.find_element(by=AppiumBy.ID, value=CHARGER_STATE_TEXT_ELEMENT_ID).text
        print(f"Charger State: {charger_state}")

        mile_range_minimum = driver.find_element(by=AppiumBy.ID, value=MILE_RANGE_MINIMUM_TEXT_ELEMENT_ID).text
        print(f"Mile Range Minimum: {mile_range_minimum}")

        mile_range_maximum = driver.find_element(by=AppiumBy.ID, value=MILE_RANGE_MAXIMUM_TEXT_ELEMENT_ID).text
        print(f"Mile Range Maximum: {mile_range_maximum}")

        interior_temperature = driver.find_element(by=AppiumBy.ID, value=INTERIOR_TEMPERATURE_TEXT_ELEMENT_ID).text
        print(f"Interior Temperature: {interior_temperature}")

        level_two_charger_eta = driver.find_element(by=AppiumBy.ID, value=LEVEL_TWO_CHARGER_ETA_TEXT_ELEMENT_ID).text
        print(f"Level Two Charger ETA: {level_two_charger_eta}")


if __name__ == "__main__":
    app = typer.Typer(add_completion=False, pretty_exceptions_show_locals=False)
    app.command()(main)
    app()
