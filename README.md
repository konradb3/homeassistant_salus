# Home Assistant integration of Salus iT600 smart devices

## Instalation
Checkout this repository to `config/custom_components/salus` of your Home Assistant instalation.

## Configuration

There are two ways to configure this integration.

1. In Home Assistant web interface go to Configuration -> Integrations and then press "+" button and select "Salus iT600".

2. Another way is to configure it through `configuration.yaml`.
Example :
```yaml
climate:
  - platform: salus
    host: "192.168.0.15"
    token: 001E5C020214B243

binary_sensor:
  - platform: salus
    host: "192.168.0.15"
    token: 001E5C020214B243
```

* host - hostname or IP address of your Salus gateway
* token - EUID printed on bottom of your gateway

When you are done with configuration you should see your devices in Configuration -> Integrations -> Entities
