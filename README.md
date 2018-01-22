# Xiaomi Air Humidifier

This is a custom component for home assistant to integrate the Xiaomi Air Humidifier.

Please follow the instructions on [Retrieving the Access Token](https://home-assistant.io/components/xiaomi/#retrieving-the-access-token) to get the API token to use in the configuration.yaml file.

Credits: Thanks to [Rytilahti](https://github.com/rytilahti/python-miio) for all the work.

## Features
* On, Off
* Operation modes (silent, medium, high)
* Buzzer (on, off)
* LED brightness (bright, dim, off)
* Child lock (on, off)
* Target humidity (40, 50, 60, 70, 80)
* States
  - power
  - temperature
  - humidity
  - mode
  - buzzer
  - led_brightness
  - child_lock
  - trans_level
  - target_humidity

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

| Service data attribute    | Optional | Description                                              |
|---------------------------|----------|----------------------------------------------------------|
| `entity_id`               |      yes | Only act on specific air humidifier. Else targets all.   |

#### Service fan/xiaomi_miio_set_buzzer_off

Turn the buzzer off.

| Service data attribute    | Optional | Description                                              |
|---------------------------|----------|----------------------------------------------------------|
| `entity_id`               |      yes | Only act on specific air humidifier. Else targets all.   |

#### Service fan/xiaomi_miio_set_child_lock_on

Turn the child lock on.

| Service data attribute    | Optional | Description                                              |
|---------------------------|----------|----------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air humidifier. Else targets all. |

#### Service fan/xiaomi_miio_set_child_lock_off

Turn the child lock off.

| Service data attribute    | Optional | Description                                              |
|---------------------------|----------|----------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air humidifier. Else targets all. |

#### Service fan/xiaomi_miio_set_led_brightness

Set the led brightness. Supported values are 0 (Bright), 1 (Dim), 2 (Off).

| Service data attribute    | Optional | Description                                              |
|---------------------------|----------|----------------------------------------------------------|
| `entity_id`               |      yes | Only act on specific air humidifier. Else targets all.   |
| `brightness`              |       no | Brightness, between 0 and 2.                             |

#### Service fan/xiaomi_miio_set_target_humidity

Set the target humidity. Supported values are 40, 50, 60, 70 and 80 percent.

| Service data attribute    | Optional | Description                                              |
|---------------------------|----------|----------------------------------------------------------|
| `entity_id`               |      yes | Only act on specific air humidifier. Else targets all.   |
| `humidity`                |       no | Humidity in percent: 40, 50, 60, 70 or 80                |
