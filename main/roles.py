"""Purpose is to serve requests related to Roles Create Delete and update

"""
from flask import Blueprint
from flask import jsonify
from .models.role import AuthPermissions, db
import constants as cts
from auth_plugin.wrappers import check_credentials

__author__ = 'hughson.simon@playstack.com'

blueprint = Blueprint('roles', __name__)


@blueprint.route("/roles/list", methods=['GET'])
@check_credentials(['view_admin_panel'])
def roles_list():
    """list all available roles/auth permissions
    sample request
    /roles/list

    sample response:
    {
        "response_message": {
            "roles": [
                {
                    "codename": "manage_groups",
                    "content_type_id": 9,
                    "id": 26,
                    "microservice_id": 2,
                    "name": "Manage Groups"
                },
                {
                    "codename": "reset_password",
                    "content_type_id": 9,
                    "id": 25,
                    "microservice_id": 2,
                    "name": "Reset Password"
                }
            ],
            "total": 2
        },
        "response_status": "SUCCESS"
    }
    :return: dict: role items
    """
    response_dict = {}
    try:
        all_roles = AuthPermissions.query.all()
        total_roles = len(all_roles)
        roles_list = []
        if total_roles >= 1:
            for role in all_roles:
                roles_dict = {}
                roles_dict['id'] = role.id
                roles_dict['name'] = role.name
                roles_dict['codename'] = role.codename
                roles_dict['content_type_id'] = role.content_type_id
                roles_dict['microservice_id'] = role.microservice_id
                roles_list.append(roles_dict)
            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
            response_dict[cts.RESPONSE_MESSAGE] = {}
            response_dict[cts.RESPONSE_MESSAGE]['total'] = total_roles
            response_dict[cts.RESPONSE_MESSAGE]['roles'] = roles_list
        else:
            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
            response_dict[cts.RESPONSE_MESSAGE] = {}
            response_dict[cts.RESPONSE_MESSAGE]['total'] = 0
            response_dict[cts.RESPONSE_MESSAGE]['roles'] = []
    except:
        db.session.rollback()
        response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
        response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST
        raise
    return jsonify(response_dict), 200

