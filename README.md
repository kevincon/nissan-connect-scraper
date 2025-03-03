# Nissan Connect Scraper

[![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/kevincon)

```
❯ apkeep -a com.aqsmartphone.android.nissan .
Downloading com.aqsmartphone.android.nissan...
[00:00:09] ██████████████████████████████████████░░ 95.27 MiB/99.42 MiB | com.aqsmartphone.and
com.aqsmartphone.android.nissan downloaded successfully!

❯ sha256sum com.aqsmartphone.android.nissan.apk
00c10f77edb5714f6ec4e30384b19ef250e8f2f9d2eb680d67671f5eacf214ea  com.aqsmartphone.android.nissan.apk

❯ python main.py --demo ./com.aqsmartphone.android.nissan.apk
Last Refresh Date: UPDATED MAR 02, 2025, 08:48 PM
Battery State of Charge: 75
Charger State: UNPLUGGED...
Mile Range Minimum: 125
Mile Range Maximum: 129
Interior Temperature: 74-84°F
Level Two Charger ETA: 4h:30m
```

```
❯ python main.py --help

 Usage: main.py [OPTIONS] NISSAN_CONNECT_APP_APK

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────╮
│ *    nissan_connect_app_apk      FILE  Path to Nissan Connect app APK                        │
│                                        [env var: NISSAN_CONNECT_APP_APK]                     │
│                                        [default: None]                                       │
│                                        [required]                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────╮
│ --user-id                            TEXT     user ID                                        │
│                                               [env var: NISSAN_CONNECT_USER_ID]              │
│                                               [default: None]                                │
│ --password                           TEXT     password                                       │
│                                               [env var: NISSAN_CONNECT_PASSWORD]             │
│                                               [default: None]                                │
│ --demo                  --no-demo             Use demo mode                                  │
│                                               [env var: NISSAN_CONNECT_DEMO]                 │
│                                               [default: no-demo]                             │
│ --appium-server-url                  TEXT     Appium server URL                              │
│                                               [env var: APPIUM_SERVER_URL]                   │
│                                               [default: localhost]                           │
│ --appium-server-port                 INTEGER  Appium server port                             │
│                                               [env var: APPIUM_SERVER_PORT]                  │
│                                               [default: 4723]                                │
│ --help                                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
```
