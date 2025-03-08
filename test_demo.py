import json
import os
import re
from datetime import datetime, timezone

import pytest
from dateutil.parser import parser as dateutil_parser
from typer.testing import CliRunner

from main import VehicleData, app


@pytest.fixture()
def demo_output() -> VehicleData:
    if demo_output_json := os.getenv("DEMO_OUTPUT_JSON"):
        demo_output = json.loads(demo_output_json)
        return VehicleData(**{k.replace("-", "_"): v for k, v in demo_output.items()})

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["--demo", "com.aqsmartphone.android.nissan.apk", "--avd", "Medium_Phone_API_35"],
    )
    assert result.exit_code == 0

    data = {}
    demo_output = result.stdout
    for line in demo_output.splitlines():
        k, v = line.split("=")
        data[k.replace("-", "_")] = v
    return VehicleData(**data)


def test_demo_output(demo_output: VehicleData) -> None:
    assert 0 <= int(demo_output.battery_state_of_charge) <= 100
    assert dateutil_parser().parse(demo_output.last_refresh_date).date() == datetime.now(timezone.utc).date()
    assert demo_output.charger_state == "UNPLUGGED..."
    assert 0 <= int(demo_output.range_minimum) <= 500
    assert 0 <= int(demo_output.range_maximum) <= 500
    assert re.match(r"\d+-\d+°F", demo_output.interior_temperature_range)
    assert re.match(r"\d+h:\d+m", demo_output.level_two_charger_eta)
