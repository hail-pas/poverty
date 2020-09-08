from io import BytesIO

import qrcode
from starlette.responses import Response
from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def generate_qr_code():
    input_data = "https://dev-api.povertool.cn/web/doc/upload"
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    st = BytesIO()
    img.save(stream=st)
    response = Response(st.getvalue(), media_type="image/png")
    return response
