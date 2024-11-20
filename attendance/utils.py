import qrcode
from io import BytesIO
import hashlib
import base64

def generate_qr_code(data):
    print("Данные для QR-кода:", data)
    if not data:
        raise ValueError("Данные для QR-кода не могут быть пустыми")

    encoded_data = base64.b64encode(data.encode()).decode()

    decoded_data = base64.b64decode(encoded_data).decode()
    print("Декодированные данные:", decoded_data)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(encoded_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def hash_qr_data(data):
    return hashlib.sha256(data.encode()).hexdigest()