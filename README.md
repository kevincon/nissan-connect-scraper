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

This repo contains a [reusable GitHub Actions workflow](https://docs.github.com/en/actions/sharing-automations/reusing-workflows) that can be called from another GitHub repo to:

1. launch the [NissanConnect® EV & Services Android app](https://play.google.com/store/apps/details?id=com.aqsmartphone.android.nissan) in an Android emulator
1. sign into an account in the app using provided credentials (or alternatively launch the app in a "demo mode")
1. scrape and output the information available about the [Nissan LEAF®](https://en.wikipedia.org/wiki/Nissan_Leaf) vehicle registered to the account

For an example of a repo that uses this workflow, see https://github.com/kevincon/nissan-leaf-widget-updater.
