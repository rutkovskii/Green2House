from flask import Blueprint, request

from app.database.models import BBBIPAddress
from app.database.database import session_scope

receive_ip_bp = Blueprint('receive_ip_bp', __name__)


@receive_ip_bp.route('/ip', methods=['POST'])
def ip():
    if request.method == 'POST':
        body = request.get_json()

        user_id = body.get('user_id')
        ip = body.get('ip')

        print(f"User ID: {user_id}, IP: {ip}")

        with session_scope() as s:
            user_bbb = s.query(BBBIPAddress).filter(
                BBBIPAddress.user_id == user_id
            ).first()

            if user_bbb:
                # Update existing entry
                user_bbb.ip = ip
                s.add(user_bbb)
                return {"message": "IP updated"}, 200

            else:
                # Create new entry
                bbb_ip = BBBIPAddress(
                    user_id=user_id,
                    ip=ip
                )

                s.add(bbb_ip)
                return {"message": "IP created"}, 200

    return {"error": "Request must be JSON"}, 415
