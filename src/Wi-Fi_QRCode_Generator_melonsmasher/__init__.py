import io
import base64
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from enum import Enum
from PIL import Image


class WifiSecurity(Enum):
    """
    Enum for the different types of Wi-Fi security
    """
    NONE = 'NONE'
    WEP = 'WEP'
    WPA = 'WPA'
    WPA2 = 'WPA2'
    WPA3 = 'WPA3'

    def __str__(self):
        return self.value


class WifiEapMethod(Enum):
    """
    Enum for the different types of EAP methods
    """
    NONE = 'NONE'
    PEAP = 'PEAP'
    TLS = 'TLS'
    TTLS = 'TTLS'
    PWD = 'PWD'
    SIM = 'SIM'
    AKA = 'AKA'
    AKA_PRIME = 'AKA_PRIME'

    def __str__(self):
        return self.value


class WifiPhase2Auth(Enum):
    """
    Enum for the different types of Phase 2 authentication methods
    """
    NONE = 'NONE'
    PAP = 'PAP'
    CHAP = 'CHAP'
    MD5 = 'MD5'
    MSCHAP = 'MSCHAP'
    MSCHAPV2 = 'MSCHAPV2'
    GTC = 'GTC'

    def __str__(self):
        return self.value


class WifiNetworkSettings:
    """
    Class to represent the settings of a Wi-Fi network
    """

    def __init__(
            self,
            ssid: str,
            security: WifiSecurity=None,
            hidden: bool = False,
            identity: str = None,
            password: str=None,
            eap_method: WifiEapMethod = None,
            phase_2_auth: WifiPhase2Auth = None,
            anon_outer_identity: bool = False,
    ):
        """
        Initialize the Wi-Fi network settings
        :param ssid: The SSID of the Wi-Fi network
        :type ssid: str
        :param password: The password to use to connect to the Wi-Fi network
        :type password: str
        :param security: The security type of the Wi-Fi network
        :type security: WifiSecurity
        :param hidden: Whether the Wi-Fi network SSID is visible or not
        :type hidden: bool
        :param identity: The username to use for enterprise Wi-Fi networks
        :type identity: str
        :param eap_method: The EAP method to use for enterprise Wi-Fi networks
        :type eap_method: WifiEapMethod
        :param phase_2_auth: The Phase 2 authentication method to use for enterprise Wi-Fi networks
        :type phase_2_auth: WifiPhase2Auth
        :param anon_outer_identity: Whether to use an anonymous outer identity for enterprise Wi-Fi networks
        :type anon_outer_identity: bool
        """
        self.ssid = ssid
        self.password = password
        self.security = security
        self.hidden = hidden
        self.identity = identity
        self.eap_method = eap_method
        self.phase_2_auth = phase_2_auth
        self.anon_outer_identity = anon_outer_identity

    def get_qrcode_data_string(self) -> str:
        """
        Generate the Wi-Fi settings string for the QR code
        :return: String with the Wi-Fi settings to be encoded in the QR code
        :rtype: str
        """
        wifi_settings_string = f'WIFI:S:{self.ssid};'
        if self.hidden:
            wifi_settings_string += 'H:true;'
        if self.security and self.security != WifiSecurity.NONE:
            wifi_settings_string += f'T:{str(self.security.value)};'
        if self.eap_method and self.eap_method != WifiEapMethod.NONE:
            wifi_settings_string += f'E:{str(self.eap_method.value)};'
        if self.phase_2_auth and self.phase_2_auth != WifiPhase2Auth.NONE:
            wifi_settings_string += f'PH2:{str(self.phase_2_auth.value)};'
        if self.anon_outer_identity:
            wifi_settings_string += 'A:anon;'
        if self.identity:
            wifi_settings_string += f'I:{self.identity};'
        if self.password:
            wifi_settings_string += f'P:{self.password};'
        wifi_settings_string += ';'
        return wifi_settings_string

    def generate_qrcode(self, embeded_image_path: str = None):
        """
        Generate the QR code with the Wi-Fi settings
        :param embeded_image_path: Path to the image to embed in the QR code, if any
        :type embeded_image_path: str
        :return: The QR code image object
        """
        wifi_settings = self.get_qrcode_data_string()
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(wifi_settings)
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color="black",
            back_color="white"
        )
        if embeded_image_path:
            embed_image = Image.open(embeded_image_path)
            basewidth = 100
            wpercent = (basewidth / float(embed_image.size[0]))
            hsize = int((float(embed_image.size[1]) * float(wpercent)))
            embeded_image = embed_image.resize(
                (basewidth, hsize), Image.LANCZOS)
            pos = ((qr_img.size[0] - embeded_image.size[0]) // 2,
                   (qr_img.size[1] - embeded_image.size[1]) // 2)
            qr_img.paste(embeded_image, pos)
        return qr_img

    def generate_base64_qrcode_png(self, embeded_image_path: str = None) -> str:
        """
        Generate the QR code with the Wi-Fi settings and return it as a base64 encoded PNG image
        :param embeded_image_path: Path to the image to embed in the QR code, if any
        :type embeded_image_path: str
        :return: The base64 encoded PNG image string
        :rtype: str
        """
        qr = self.generate_qrcode(embeded_image_path)
        img = io.BytesIO()
        qr.save(img, format='PNG')
        return base64.b64encode(img.getvalue()).decode('utf-8')
