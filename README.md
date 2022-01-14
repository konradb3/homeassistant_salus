<p align="center">
  <a href="https://github.com/jvitkauskas/homeassistant_salus"><img src="https://salus-smarthome.eu/wp-content/themes/salus-controls/img/logo.svg" height="140"></a>
</p>

# HomeAssistant - Salus Controls iT600 Smart Home Custom Component

# What This Is

This is a custom component to allows you to control and monitor your Salus iT600 smart home devices locally through Salus Controls UGE600 / UGE600 universal gateway.

# Supported devices

See the [readme of underlying pyit600 library](https://github.com/jvitkauskas/pyit600/blob/master/README.md)

# Installation and Configuration

## HACS (recommended)

This card is available in [HACS](https://hacs.xyz/) (Home Assistant Community Store).
*HACS is a third party community store and is not included in Home Assistant out of the box.*

## Manual install
Copy `custom_components` folder from this repository to `/config` of your Home Assistant instalation.

To configure this integration, go to Home Assistant web interface Configuration -> Integrations and then press "+" button and select "Salus iT600".

When you are done with configuration you should see your devices in Configuration -> Integrations -> Entities

# Troubleshooting

If you can't connect using EUID written down on the bottom of your gateway (which looks something like this 001E5E0D32906128), try using `0000000000000000` as EUID.

Also check if you have "Local Wifi Mode" enabled:
* Open Smart Home app on your phone
* Sign in
* Double tap your Gateway to open info screen
* Press gear icon to enter configuration
* Scroll down a bit and check if "Disable Local WiFi Mode" is set to "No"
* Scroll all the way down and save settings
* Restart Gateway by unplugging/plugging USB power
