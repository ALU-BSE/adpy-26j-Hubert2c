import asyncio
from .models import ShipmentLog

async def send_sms_notification(tracking_code: str, status: str) -> None:
    # Simulate external SMS gateway delay
    await asyncio.sleep(2)
    print(f"SMS sent for {tracking_code}: {status}")


async def process_status_update(shipment, new_status: str) -> None:
    shipment.status = new_status
    shipment.save()

    ShipmentLog.objects.create(
        shipment=shipment,
        status=new_status,
        message=f"Shipment status updated to {new_status}",
    )

    try:
        await send_sms_notification(shipment.tracking_code, new_status)
    except Exception as e:
        print(f"Notification failed: {e}")
