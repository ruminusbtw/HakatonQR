import qrcode
from io import BytesIO
import hashlib
import base64

def generate_qr_code(data):
    print("Данные для QR-кода:", data)
    if not data:
        raise ValueError("Данные для QR-кода не могут быть пустыми")

    short_hash = hash_qr_data(data)
    print("Короткий хэш данных:", short_hash)

    encoded_data = base64.b64encode(data.encode()).decode()
    print("Закодированные данные:", encoded_data)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"{encoded_data} | hash: {short_hash}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def hash_qr_data(data):
    full_hash = hashlib.sha256(data.encode()).hexdigest()
    return full_hash[:8]

if __name__ == "__main__":
    data = "Пример данных"
    qr_image = generate_qr_code(data)
    with open("qr_code.png", "wb") as f:
        f.write(qr_image.getvalue())
    print("QR-код сохранён в файл 'qr_code.png'.")