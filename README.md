# Home Assistant integration of Salus iT600 smart thermostates

## Instalation
Checkout this repository to `config/custom_components/salus` of your Home Assistant instalation.

## Configuration
This integration is configured through `configaration.yaml`.
Example :
```yaml
climate:
  - platform: salus
    host: "192.168.0.15"
    token: 001E5C020214B243
```

* host - hostname or IP address of your Salus gateway
* token - EUID printed on bottom of your gateway