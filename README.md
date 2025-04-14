# Nissan Connect Scraper

![GitHub Release](https://img.shields.io/github/v/release/kevincon/nissan-connect-scraper)
![GitHub License](https://img.shields.io/github/license/kevincon/nissan-connect-scraper)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/kevincon/nissan-connect-scraper/.github%2Fworkflows%2Fmainci.yml?branch=main)](https://github.com/kevincon/nissan-connect-scraper/actions/workflows/mainci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/kevincon/nissan-connect-scraper/main.svg)](https://results.pre-commit.ci/latest/github/kevincon/nissan-connect-scraper/main)

> [!IMPORTANT]
> The NissanConnect® Application Terms of Use (contained in the app itself, effective January 23, 2018) state (**emphasis** mine):
>
> > The Sites, the App, or any of the content provided in the Site or the App, including, but not limited to, text, images, buttons, html code, audio and video, may not be copied, reverse engineered, reproduced, republished, uploaded, posted, transmitted or distributed without our prior written consent. You may not mirror any of the content from the Site on another website or in any other media. **You may, however, download, display, and/or print one copy of the Site or of the App, or a part thereof, for your personal, non-commercial use without modifying the content displayed from either the Site or the App, including all copyright, trademark, and other proprietary notices.**
>
> This repo is for educational/demonstrative purposes. I have no affiliation with Nissan and neither I nor the software may be held liable for any consequences resulting from its use.

This repo contains a [reusable GitHub Action](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions#actions) that can be called from another GitHub repo to:

1. launch the [NissanConnect® EV & Services Android app](https://play.google.com/store/apps/details?id=com.aqsmartphone.android.nissan) on an Android device
1. sign into an account in the app using provided credentials (or alternatively launch the app in a "demo mode")
1. scrape and output the information available about the [Nissan LEAF®](https://en.wikipedia.org/wiki/Nissan_Leaf) vehicle registered to the account

For an example of a repo that uses this action, see https://github.com/kevincon/nissan-leaf-widget-updater.

See [this blog post](https://kevintechnology.com/posts/leaf-widget/) for more information.

<!-- action-docs-inputs source="action.yml" -->

## Inputs

| name                        | description                                                                                                                                                                                                                                                         | required | default                 |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------- |
| `user-id`                   | <p>NissanConnect® account user ID to use to sign into the app. If either <code>user-id</code> or <code>password</code> is not provided, the app will enter "demo mode" instead of signing in.</p>                                                                   | `false`  | `""`                    |
| `password`                  | <p>NissanConnect® account password to use to sign into the app. If either <code>user-id</code> or <code>password</code> is not provided, the app will enter "demo mode" instead of signing in.</p>                                                                  | `false`  | `""`                    |
| `android-app-version`       | <p>The version of the NissanConnect® Android app to use. If not provided, defaults to latest version. Caching of the app binary is only enabled if provided.</p>                                                                                                    | `false`  | `""`                    |
| `last-refresh-date-format`  | <p>The format to use for the last refresh date. See https://arrow.readthedocs.io/en/latest/guide.html#supported-tokens for accepted tokens.</p>                                                                                                                     | `false`  | `MMM DD, YYYY, hh:mm A` |
| `convert-times-to-timezone` | <p>A timezone to convert times to, e.g. "US/Pacific". See the "TZ identifier" column on this page for accepted values: <a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones">https://en.wikipedia.org/wiki/List_of_tz_database_time_zones</a>.</p> | `false`  | `""`                    |
| `debug-out`                 | <p>Folder in which to save debug info (e.g. a screenshot of the device in case of failure). Will be created if it does not exist.</p>                                                                                                                               | `false`  | `""`                    |
| `set-up-only`               | <p>Set up the environment only, do not scrape, and include the command that can be executed to scrape in outputs.</p>                                                                                                                                               | `false`  | `""`                    |

<!-- action-docs-inputs source="action.yml" -->

<!-- action-docs-outputs source="action.yml" -->

## Outputs

| name                         | description                                                                                                                                                             |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `last-refresh-date`          | <p>The last refresh date (e.g. "MAR 05, 2025, 06:31 AM"). The format of this string can be customized using the <code>last-refresh-date-format</code> input option.</p> |
| `battery-state-of-charge`    | <p>The state of charge of the battery (out of 100, e.g. "75").</p>                                                                                                      |
| `charger-state`              | <p>The charger state (e.g. "UNPLUGGED…").</p>                                                                                                                           |
| `range-minimum`              | <p>The minimum range in your account's preferred units (e.g. "125" miles).</p>                                                                                          |
| `range-maximum`              | <p>The maximum range in your account's preferred units (e.g. "129" miles).</p>                                                                                          |
| `interior-temperature-range` | <p>The interior temperature range in your account's preferred units (e.g. "74-84°F").</p>                                                                               |
| `level-two-charger-eta`      | <p>The level two charger ETA (e.g. "4h:30m").</p>                                                                                                                       |
| `command`                    | <p>A command to run to scrape the NissanConnect® Android app. This is only set if the input <code>set-up-only</code> is set to true.</p>                                |

<!-- action-docs-outputs source="action.yml" -->

<!-- action-docs-usage source="action.yml" project="kevincon/nissan-connect-scraper" version="v1" -->

## Usage

```yaml
- uses: kevincon/nissan-connect-scraper@v1
  with:
    user-id:
    # NissanConnect® account user ID to use to sign into the app. If either `user-id` or `password` is not provided, the app will enter "demo mode" instead of signing in.
    #
    # Required: false
    # Default: ""

    password:
    # NissanConnect® account password to use to sign into the app. If either `user-id` or `password` is not provided, the app will enter "demo mode" instead of signing in.
    #
    # Required: false
    # Default: ""

    android-app-version:
    # The version of the NissanConnect® Android app to use. If not provided, defaults to latest version. Caching of the app binary is only enabled if provided.
    #
    # Required: false
    # Default: ""

    last-refresh-date-format:
    # The format to use for the last refresh date. See https://arrow.readthedocs.io/en/latest/guide.html#supported-tokens for accepted tokens.
    #
    # Required: false
    # Default: MMM DD, YYYY, hh:mm A

    convert-times-to-timezone:
    # A timezone to convert times to, e.g. "US/Pacific". See the "TZ identifier" column on this page for accepted values: <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>.
    #
    # Required: false
    # Default: ""

    debug-out:
    # Folder in which to save debug info (e.g. a screenshot of the device in case of failure). Will be created if it does not exist.
    #
    # Required: false
    # Default: ""

    set-up-only:
    # Set up the environment only, do not scrape, and include the command that can be executed to scrape in outputs.
    #
    # Required: false
    # Default: ""
```

<!-- action-docs-usage source="action.yml" project="kevincon/nissan-connect-scraper" version="v1" -->
