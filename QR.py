import qrcode

def generate_qr(data, filename="qr_code.png"):
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR Code generated and saved as '{filename}'.")

def main():
    print("=== QR Code Generator ===")
    data = input("Enter text or URL to encode: ")
    filename = input("Enter filename to save (e.g., myqr.png): ").strip()
    if filename == "":
        filename = "qr_code.png"
    generate_qr(data, filename)

if __name__ == "__main__":
    main()