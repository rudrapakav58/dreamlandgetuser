"""Purpose is to serve requests related to Groups Create Delete, Read and update

"""
from flask import abort, Blueprint, session, redirect, render_template, request, url_for
import constants as cts
from utils import validate_json, validate_group_create_input, add_user_greylist
from flask import jsonify
import datetime as dttim
from .models.role import AuthGroups, AuthPermissions, AuthGroupPermissions, db
from .models.user import AuthUserGroups, User
import uuid
from auth_plugin.wrappers import check_credentials

blueprint = Blueprint('groups', __name__)


@blueprint.route('/groups/add', methods=['POST'])
@check_credentials(['manage_groups'])
@validate_json
def group_add():
    """Create group method
    sample request
    {
        "group_name":"testing group",
        "permissions":[]

    }
    sample response:
    {
      "response_message": "Group Successfully Created",
      "response_status": "SUCCESS"
    }
    "permissions": list of permissions. All are integers
    :return:dict with success message and status code
    """
    request_dict = request.get_json()
    err_msg = ""

    if not validate_group_create_input(**request_dict)[0]:
        err_msg = validate_group_create_input(**request.form)[1]
        return (jsonify({cts.RESPONSE_STATUS: cts.RESPONSE_ERROR,
                         cts.RESPONSE_MESSAGE: err_msg}), 200)

    if request_dict['group_name'] is not None:
        check_group = AuthGroups.query.filter_by(name=request_dict['group_name']).first()
        if check_group:
            err_msg = cts.GROUP_EXISTS
    else:
        err_msg = cts.GROUP_REQUIRED

    if err_msg:
        return (jsonify({cts.RESPONSE_STATUS: cts.RESPONSE_ERROR,
                         cts.RESPONSE_MESSAGE: err_msg}), 200)
    response_dict = {}
    try:
        result_items = AuthGroups(
            name=request_dict['group_name'],
            created_on=dttim.datetime.now())
        db.session.add(result_items)
        db.session.commit()
        response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
        response_dict[cts.RESPONSE_MESSAGE] = cts.GROUP_CREATE_SUCCESS

        # check if permissions include in request dict
        if "permissions" in request_dict and len(request_dict["permissions"]) >= 1:
            # print(len(request_dict["permissions"]))
            try:
                for permits in request_dict["permissions"]:
                    # print(permits)
                    # check if the permission is in the DB
                    check_permit = AuthPermissions.query.filter_by(id=permits).first()
                    if check_permit:
                        # if permission exists in DB then insert into auth group permissions
                        permit_items = AuthGroupPermissions(
                            group_id=result_items.id,
                            permission_id=permits,
                            created_on=dttim.datetime.now())
                        db.session.add(permit_items)
                        db.session.commit()
                        # print("valid permissions")
                    else:
                        print("invalid permissions")
                response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
                response_dict[cts.RESPONSE_MESSAGE] = cts.GROUP_CREATE_SUCCESS
            except:
                db.session.rollback()
                response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
                response_dict[cts.RESPONSE_MESSAGE] = cts.GROUP_PARTIAL_ERROR

    except Exception:
        db.session.rollback()
        response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
        response_dict[cts.RESPONSE_MESSAGE] = cts.GROUP_ERROR

    return jsonify(response_dict), 200


@blueprint.route("/groups/delete", methods=['DELETE'])
@check_credentials(['manage_groups'])
@validate_json
def groups_remove():
    """Remove group from the DB using uuid
    sample request
    {
        "group_id":"18fcbb87-d56a-48ed-b589-47a26166eb8c34"
    }

    sample response:
    {
      "response_message": "Successfully Delete.",
      "response_status": "SUCCESS"
    }
    :return: Boolean
    """
    request_dict = request.get_json()
    response_dict = {}
    if 'group_id' in request_dict and request_dict['group_id'] != "":
        # print(request_dict['user_id'])
        try:
            group_exists = AuthGroups.query.filter_by(id = request_dict['group_id']).first()
            if group_exists:
                # print("group exists")
                # print(group_exists.id)

                # Delete permissions related to the group
                AuthGroupPermissions.query.filter_by(group_id=group_exists.id).delete()
                db.session.commit()

                # Delete user auth groups
                AuthUserGroups.query.filter_by(group_id=group_exists.id).delete()
                db.session.commit()

                # Delete the group
                AuthGroups.query.filter_by(id=group_exists.id).delete()
                db.session.commit()

                response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
                response_dict[cts.RESPONSE_MESSAGE] = cts.GROUP_DELETED
            else:
                response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
                response_dict[cts.RESPONSE_MESSAGE] = cts.RECORD_NOTFOUND
        except:
            db.session.rollback()
            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
            response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST

    else:
        response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
        response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST

    return jsonify(response_dict), 200


@blueprint.route("/groups/update", methods=['PUT'])
@check_credentials(['manage_groups'])
@validate_json
def groups_update():
    """update group from the DB using uuid
    sample request
    {
        "group_id":"18fcbb87-d56a-48ed-b589-47a26166eb8c34",
        "add_permissions":[],
        "remove_permissions":[]
    }

    sample response:
    {
      "response_message": "Successfully updated.",
      "response_status": "SUCCESS"
    }
    :return: Boolean
    """
    request_dict = request.get_json()
    response_dict = {}
    if 'group_id' in request_dict and request_dict['group_id'] != "":
        # print(request_dict['user_id'])
        try:
            group_exists = AuthGroups.query.filter_by(id = request_dict['group_id']).first()
            if group_exists:
                # add permissions to group
                if "add_permissions" in request_dict and len(request_dict["add_permissions"]) >= 1:
                    # print(len(request_dict["add_permissions"]))
                    response_dict[cts.RESPONSE_STATUS], \
                    response_dict[cts.RESPONSE_MESSAGE] = add_permissions_to_group(request_dict, group_exists.id)

                # remove permissions to group
                if "remove_permissions" in request_dict and len(request_dict["remove_permissions"]) >= 1:
                    # print(len(request_dict["remove_permissions"]))
                    response_dict[cts.RESPONSE_STATUS], \
                    response_dict[cts.RESPONSE_MESSAGE] = remove_permissions_to_group(request_dict, group_exists.id)
                response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
                response_dict[cts.RESPONSE_MESSAGE] = cts.GROUP_UPDATED
            else:
                response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
                response_dict[cts.RESPONSE_MESSAGE] = cts.RECORD_NOTFOUND
        except:
            db.session.rollback()
            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
            response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST

    else:
        response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
        response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST

    return jsonify(response_dict), 200


def add_permissions_to_group(request_dict, group_id):
    """Add permissions from the given group

    :param request_dict:
    :param group_id:
    :return: response dict with status and message
    """
    try:
        grey_temp_count = 0
        #print(len(request_dict["add_permissions"]))
        for permits in request_dict["add_permissions"]:
            # check if the permission is in the DB
            check_permit = AuthPermissions.query.filter_by(id=permits).first()
            if check_permit:
                # print("permission exists")
                # if permission exists in DB then then check if permission is in auth group permissions
                check_auth_permit = AuthGroupPermissions.query.filter_by(group_id=group_id,
                                                                          permission_id=permits).first()
                # if permission is not in auth group permissions then insert
                if not check_auth_permit:
                    grey_temp_count += 1
                    # print("its not in group permissions")
                    permit_items = AuthGroupPermissions(
                        group_id=group_id,
                        permission_id=permits,
                        created_on=dttim.datetime.now())
                    db.session.add(permit_items)
                    db.session.commit()
                else:
                    print("permissions already exist")
            else:
                print("invalid permissions")
        #return cts.RESPONSE_SUCCESS, cts.GROUP_UPDATED
    except:
        db.session.rollback()
        return cts.RESPONSE_ERROR, cts.GROUP_PARTIAL_ERROR

    # Add group users to greylist
    if grey_temp_count >=1:
        group_users_to_greylist(group_id)

    return cts.RESPONSE_SUCCESS, cts.GROUP_UPDATED


def remove_permissions_to_group(request_dict, group_id):
    """Remove permissions from the given group

    :param request_dict:
    :param group_id:
    :return: response dict with status and message
    """
    try:
        grey_temp_count = 0
        for permits in request_dict["remove_permissions"]:
            # print(permits)
            # check if the permission is in the DB
            check_permit = AuthGroupPermissions.query.filter_by(group_id=group_id, permission_id=permits).first()
            if check_permit:
                grey_temp_count += 1
                # if permission exists then remove permission from auth group permissions
                AuthGroupPermissions.query.filter_by(group_id=group_id, permission_id=permits).delete()
                db.session.commit()
                # print("valid permissions to delete")
            else:
                print("invalid permissions to delete")
    except:
        db.session.rollback()
        return cts.RESPONSE_ERROR, cts.GROUP_PARTIAL_ERROR

    # Add group users to greylist
    if grey_temp_count >=1:
        group_users_to_greylist(group_id)

    return cts.RESPONSE_SUCCESS, cts.GROUP_UPDATED


def group_users_to_greylist(groupid):
    """Add users to grey list whenever group permissions is changed

    :param group_id:
    :return: True
    """
    users_of_group = AuthUserGroups.query.filter_by(group_id=groupid).all()
    if len(users_of_group) >=1:
        for user in users_of_group:
            user_details = User.query.filter_by(id=user.user_id).first()
            if user_details:
                add_user_greylist(user_details.user_uuid)
    return True


@blueprint.route("/groups/list", methods=['GET'])
@check_credentials(['view_admin_panel'])
def groups_list():
    """list all available groups and respective permissions
    sample request
    /groups/list

    sample response:
    {
        "response_message": {
            "groups": [
                {
                    "id": 1,
                    "name": "hello",
                    "permissions": []
                },
                {
                    "id": 3,
                    "name": "testing",
                    "permissions": [
                        11,
                        15
                    ]
                }

            ],
            "total": 2
        },
        "response_status": "SUCCESS"
    }
    :return: dict: groups dict items
    """
    response_dict = {}
    try:
        all_groups = AuthGroups.query.all()
        total_groups = len(all_groups)
        groups_list = []

        if total_groups >= 1:
            for group in all_groups:
                groups_dict = {}
                permission_list = []
                groups_dict['id'] = group.id
                groups_dict['name'] = group.name
                for permit in group.auth_group_permissions.all():
                    permission_list.append(permit.permission_id)
                groups_dict['permissions'] = permission_list
                groups_list.append(groups_dict)
            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
            response_dict[cts.RESPONSE_MESSAGE] = {}
            response_dict[cts.RESPONSE_MESSAGE]['total'] = total_groups
            response_dict[cts.RESPONSE_MESSAGE]['groups'] = groups_list
        else:
            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
            response_dict[cts.RESPONSE_MESSAGE] = {}
            response_dict[cts.RESPONSE_MESSAGE]['total'] = 0
            response_dict[cts.RESPONSE_MESSAGE]['groups'] = []
    except:
        db.session.rollback()
        response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
        response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST
    return jsonify(response_dict), 200
