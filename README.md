# WiFiQR-Gen (Wi-Fi QRCode Generator)

![GitHub License](https://img.shields.io/github/license/MelonSmasher/WiFiQRGen)
![PyPI - Version](https://img.shields.io/pypi/v/WiFiQRGen)
![PyPI - Downloads](https://img.shields.io/pypi/dm/WiFiQRGen)

Python package that generates Wi-Fi QR Codes that can be scanned for easily connecting to Wi-Fi.

## Installation

```bash
pip install WiFiQRGen
```

## Usage

### Basic Usage

To generate a Wi-Fi QR Code, you need to create a `WifiNetworkSettings` object. For a basic home network, you'll need to provide the SSID, password, and security type. The security type is an enum from the `WifiSecurity` class. Optionally, if you're network is hidden, you can set the `hidden` parameter to `True`, however it is `False` by default and assumes the network is visible.

Options for the `WifiSecurity` enum are:

- `WifiSecurity.NONE`
- `WifiSecurity.WEP`
- `WifiSecurity.WPA`
- `WifiSecurity.WPA2`
- `WifiSecurity.WPA3`

```python
from WiFiQRGen import WifiSecurity, WifiNetworkSettings

wifi_settings = WifiNetworkSettings(
    ssid="MyWifiNetworkName",
    password="MyWifiPassword12345",
    security=WifiSecurity.WPA2
)

my_qr_code = wifi_settings.generate_qrcode()
my_qr_code.save("wifi_qr_code.png")
```

### Advanced Usage (Enterprise Networks)

For enterprise networks, you'll need to provide additional information. The `WifiNetworkSettings` object has additional parameters for this. You'll need to provide the SSID, password, security type, EAP method, and phase 2 authentication. The EAP method is an enum from the `WifiEapMethod` class and the phase 2 authentication is an enum from the `WifiPhase2Auth` class.

Options for the `WifiEapMethod` enum are:

- `WifiEapMethod.NONE`
- `WifiEapMethod.PEAP`
- `WifiEapMethod.TLS`
- `WifiEapMethod.TTLS`
- `WifiEapMethod.PWD`
- `WifiEapMethod.SIM`
- `WifiEapMethod.AKA`
- `WifiEapMethod.AKA_PRIME`

Options for the `WifiPhase2Auth` enum are:

- `WifiPhase2Auth.NONE`
- `WifiPhase2Auth.PAP`
- `WifiPhase2Auth.CHAP`
- `WifiPhase2Auth.MD5`
- `WifiPhase2Auth.MSCHAP`
- `WifiPhase2Auth.MSCHAPV2`
- `WifiPhase2Auth.GTC`

You can also provide a logo to be displayed in the center of the QR Code. The logo should be a square image. The `generate_qrcode` method takes an optional `embeded_image_path` parameter.

The `generate_base64_qrcode_png` method takes an optional `embeded_image_path` parameter and returns a base64 string of the QR Code image.

```python
from WiFiQRGen import WifiSecurity, WifiEapMethod, WifiPhase2Auth, WifiNetworkSettings

wifi_settings = WifiNetworkSettings(
    ssid="MyWifiNetwork",
    password="MyWifiPassword12345",
    security=WifiSecurity.WPA2,
    eap_method=WifiEapMethod.PEAP,
    phase2_auth=WifiPhase2Auth.MSCHAPV2,
    hidden=True,
    identity="MyUsername"
)

# Generate QR Code with logo in center
my_qr_code = wifi_settings.generate_qrcode('path/to/logo.png')
# Save QR Code to file
my_qr_code.save("wifi_qr_code.png")
# Generate QR Code with a logo in the center and get it as a base64 string
base64_qr_code = my_qr_code.generate_base64_qrcode_png('path/to/logo.png')
```
