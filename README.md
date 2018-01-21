# Xiaomi Air Humidifier

This is a custom component for home assistant to integrate the Xiaomi Air Humidifier.

Please follow the instructions on [Retrieving the Access Token](https://home-assistant.io/components/xiaomi/#retrieving-the-access-token) to get the API token to use in the configuration.yaml file.

Credits: Thanks to [Rytilahti](https://github.com/rytilahti/python-miio) for all the work.

## Features
* On, Off
* Operation modes (silent, medium, high)
* Buzzer (on, off)
* LED (on, off), LED brightness (bright, dim, off)
* States
  - power
  - humidity
  - temperature
  - mode
  - led
  - led_brightness
  - buzzer

## Setup

```yaml
# confugration.yaml

fan:
  - platform: xiaomi_airhumidifier
    name: Xiaomi Air Humidifier
    host: 192.168.130.71
    token: b7c4a758c251955d2c24b1d9e41ce47d
```

## Platform services

#### Service fan/xiaomi_miio_set_buzzer_on

Turn the buzzer on.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on specific air humidifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_buzzer_off

Turn the buzzer off.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on specific air humidifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_led_on

Turn the led on.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on specific air humidifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_led_off

Turn the led off.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on specific air humidifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_led_brightness

Set the led brightness. Supported values are 0 (Bright), 1 (Dim), 2 (Off).

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on specific air humidifier. Else targets all.  |
| `brightness`              |       no | Brightness, between 0 and 2.                            |
