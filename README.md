# Xiaomi Mi Air Purifier & Xiaomi Mi Air Humidifier

This is a custom component for home assistant to integrate the Xiaomi Mi Air Purifier 2, Air Purifier 2S, Air Purifier Pro and Air Humidifier.

Please follow the instructions on [Retrieving the Access Token](https://home-assistant.io/components/xiaomi/#retrieving-the-access-token) to get the API token to use in the configuration.yaml file.

Credits: Thanks to [Rytilahti](https://github.com/rytilahti/python-miio) for all the work.

## Features

### Air Purifier

* On, Off
* Operation modes (auto, silent, favorite, idle)
* Buzzer (on, off)
* Child lock (on, off)
* LED (on, off), LED brightness (bright, dim, off)
* Favorite Level (0...16)
* Attributes
  - power
  - aqi
  - average_aqi
  - humidity
  - temperature
  - mode
  - favorite_level
  - led
  - led_brightness
  - buzzer
  - child_lock
  - purify_volume
  - filter_life_remaining
  - filter_hours_used
  - motor_speed

### Air Humidifier

* On, Off
* Operation modes (silent, medium, high)
* Buzzer (on, off)
* Child lock (on, off)
* LED brightness (bright, dim, off)
* Target humidity (30, 40, 50, 60, 70, 80)
* Attributes
  - power
  - humidity
  - temperature
  - mode
  - led_brightness
  - buzzer
  - child_lock
  - trans_level
  - target_humidity

## Setup

```yaml
# confugration.yaml

fan:
  - platform: xiaomi_miio
    name: Xiaomi Air Purifier 2
    host: 192.168.130.71
    token: b7c4a758c251955d2c24b1d9e41ce47d
    model: zhimi.airpurifier.m1

  - platform: xiaomi_miio
    name: Xiaomi Air Purifier Pro
    host: 192.168.130.73
    token: 70924d6fa4b2d745185fa4660703a5c0
    model: zhimi.airpurifier.v6

  - platform: xiaomi_miio
    name: Xiaomi Air Humidifier
    host: 192.168.130.72
    token: 2b00042f7481c7b056c4b410d28f33cf
    model: zhimi.humidifier.v1
```

Configuration variables:
- **host** (*Required*): The IP of your light.
- **token** (*Required*): The API token of your light.
- **name** (*Optional*): The name of your light.
- **model** (*Optional*): The model of your device. Valid values are `zhimi.airpurifier.m1`, `zhimi.airpurifier.m2`, `zhimi.airpurifier.ma1`, `zhimi.airpurifier.ma2`, `zhimi.airpurifier.sa1`, `zhimi.airpurifier.sa2`, `zhimi.airpurifier.v1`, `zhimi.airpurifier.v2`, `zhimi.airpurifier.v3`, `zhimi.airpurifier.v5`, `zhimi.airpurifier.v6`, `zhimi.humidifier.v1` and `zhimi.humidifier.ca1`. This setting can be used to bypass the device model detection and is recommended if your device isn't always available.

## Platform services

#### Service fan/xiaomi_miio_set_buzzer_on (Air Purifier Pro excluded)

Turn the buzzer on.

| Service data attribute    | Optional | Description                                           |
|---------------------------|----------|-------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_buzzer_off (Air Purifier Pro excluded)

Turn the buzzer off.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_led_on (Air Purifier only)

Turn the led on.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_led_off (Air Purifier only)

Turn the led off.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_child_lock_on

Turn the child lock on.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_child_lock_off

Turn the child lock off.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_led_brightness (Air Purifier Pro excluded)

Set the led brightness. Supported values are 0 (Bright), 1 (Dim), 2 (Off).

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |
| `brightness`              |       no | Brightness, between 0 and 2.                            |

#### Service fan/xiaomi_miio_set_favorite_level (Air Purifier only)

Set the favorite level of the operation mode "favorite".

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |
| `level`                   |       no | Level, between 0 and 16.                                |

#### Service fan/xiaomi_miio_set_target_humidity (Air Humidifier only)

Set the target humidity.

| Service data attribute    | Optional | Description                                                     |
|---------------------------|----------|-----------------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.          |
| `humidity`                |       no | Target humidity. Allowed values are 30, 40, 50, 60, 70 and 80   |

#### Service fan/xiaomi_miio_set_auto_detect_on (Air Purifier Pro only)

Turn the auto detect on.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_auto_detect_off (Air Purifier Pro only)

Turn the auto detect off.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_learn_mode_on (Air Purifier 2 only)

Turn the learn mode on.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_learn_mode_off (Air Purifier 2 only)

Turn the learn mode off.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_volume (Air Purifier Pro only)

Set the sound volume.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |
| `volume`                  |       no | Volume, between 0 and 100.                              |

#### Service fan/xiaomi_miio_reset_filter (Air Purifier 2 only)

Reset the filter lifetime and usage.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |

#### Service fan/xiaomi_miio_set_extra_features (Air Purifier only)

Set the extra features.

| Service data attribute    | Optional | Description                                             |
|---------------------------|----------|---------------------------------------------------------|
| `entity_id`               |      yes | Only act on a specific air purifier. Else targets all.  |
| `features`                |       no | Integer, known values are 0 and 1.                      |
