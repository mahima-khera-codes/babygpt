#from app import mongo
from flask import (Blueprint, flash, jsonify, abort, request)
from app.util.serializer import serialize_doc
from app.auth import token
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,
                                get_jwt_identity, get_current_user,
                                jwt_refresh_token_required,
                                verify_jwt_in_request)

import datetime
from app.account import initDB
from app.utils import check_and_validate_account

bp = Blueprint('settings', __name__, url_prefix='/')


@bp.route('/settings', methods=["PUT", "GET"])
@token.SecretKeyAuth
@check_and_validate_account
def system_settings_setings():
    mongo = initDB(request.account_name, request.account_config)
    if request.method == "GET":
        system_settings = mongo.system_settings.find_one({},{"_id":0})
        return jsonify(system_settings)

    if request.method == "PUT":
        pdf_allow = request.json.get("pdf",False)
        ret = mongo.system_settings.update({}, {
            "$set": {
                "pdf": pdf_allow
            }
        },upsert=True)
        return jsonify({"message":"upserted","status":True}), 200
