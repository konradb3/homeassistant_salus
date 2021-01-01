# HomeAssistant - Salus iT600 Custom Component

# What This Is

This is a custom component to allows you to control and monitor your Salus iT600 smart home devices locally through Salus UG600 universal gateway.

# Supported devices

See the [readme of underlying pyit600 library](https://github.com/jvitkauskas/pyit600/blob/master/README.md)

# Installation and Configuration

Copy files from this repository to `/config/custom_components/salus` of your Home Assistant instalation.

To configure this integration, go to Home Assistant web interface Configuration -> Integrations and then press "+" button and select "Salus iT600".

When you are done with configuration you should see your devices in Configuration -> Integrations -> Entities

# Troubleshooting

Check if you have "Local Wifi Mode" enabled:
* Open Smart Home app on your phone
* Sign in
* Double tap your Gateway to open info screen
* Press gear icon to enter configuration
* Scroll down a bit and check if "Disable Local WiFi Mode" is set to "No"
* Restart Gateway after changing the setting
