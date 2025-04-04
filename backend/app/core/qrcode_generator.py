import qrcode
from PIL import Image
import io
import base64
import os

LOGO_PATH = os.path.join(os.path.dirname(__file__), "../core/logo.png")

def generate_qr_with_logo(url: str, box_size: int = 10) -> str:
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    try:
        logo = Image.open(LOGO_PATH)
    except FileNotFoundError:
        print("⚠️ ロゴ画像が見つかりません:", LOGO_PATH)
        return None

    qr_width, qr_height = qr_img.size
    logo_size = int(qr_width * 0.25)
    logo = logo.resize((logo_size, logo_size))
    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
    qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    buffered = io.BytesIO()
    qr_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"