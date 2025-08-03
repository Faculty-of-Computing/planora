import qrcode
from PIL import Image
import base64
from io import BytesIO
import os
from typing import Optional, Dict, Any


def generate_ticket_qr_code(
    name: str,
    email: str,
    event_name: str,
    datetime: str,
    seat: str,
    event_link: str,
    ticket_type: str,
    event_id: str,
    ticket_id: str,
    logo_path: Optional[str] = None,
    qr_box_size: int = 10,
    logo_size_ratio: float = 0.2,
) -> Dict[str, Any]:
    # Build the ticket text
    ticket_text = (
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Event: {event_name}\n"
        f"Time: {datetime}\n"
        f"Seat: {seat}\n"
        f"Link: {event_link}\n"
        f"Ticket: {ticket_type}\n"
        f"EventID: {event_id}\n"
        f"TicketID: {ticket_id}"
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=qr_box_size,
        border=4,
    )
    qr.add_data(ticket_text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)

        qr_width, qr_height = qr_img.size
        logo_size = int(qr_width * logo_size_ratio)
        logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)

        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

    # Convert image to base64 data URL without saving
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    data_url = f"data:image/png;base64,{img_base64}"

    # Return only the data URL and IDs
    return {
        "data_url": data_url,
        "event_id": event_id,
        "ticket_id": ticket_id,
    }


if __name__ == "__main__":
    result = generate_ticket_qr_code(
        name="John Doe",
        email="john@example.com",
        event_name="Summer Fest 2025",
        datetime="2025-08-10 18:00",
        seat="A12",
        event_link="https://example.com/event/12345",
        ticket_type="VIP",
        event_id="EVT12345",
        ticket_id="TICK54321",
        logo_path=None,
    )

    print(f"Event ID: {result['event_id']}")
    print(f"Ticket ID: {result['ticket_id']}")
    print(f"Data URL: {result['data_url']}")
