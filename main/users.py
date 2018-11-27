"""Purpose is to serve requests related to User Create Delete and update

"""
from flask import abort, Blueprint, session, redirect, render_template, request, url_for
import constants as cts
from utils import validate_json, validate_registration_input, add_user_greylist
from flask import jsonify
from passlib.hash import django_pbkdf2_sha256
import datetime as dttim
from .models.user import User, db, AuthUserGroups
from .models.role import AuthPermissions, AuthGroups
import uuid
from auth_plugin.wrappers import check_credentials
from emails import user_register_email


blueprint = Blueprint('users', __name__)


@blueprint.route('/users/add', methods=['POST'])
@check_credentials(['add_users'])
@validate_json
def user_add():
    """Create user by admin
    sample request
    {
        "email":"hughson.simon@playstack.com",
        "first_name":"hughsonsees1sad2e3",
        "last_name":"hughsonsees1sad2e3",
        "auth_groups":[1,2,3]
    }

    sample response:
    {
      "response_message": "Registration Successfully Completed. Please verify email account.",
      "response_status": "SUCCESS"
    }
    :return:dict with success message and status code

    - Password field is auto generated. An email with password will be sent to user.
    """
    #if request.method == 'POST':
    request_dict = request.get_json()
    err_msg = ""

    if not validate_registration_input(**request_dict)[0]:
        err_msg = validate_registration_input(**request.form)[1]
        return (jsonify({cts.RESPONSE_STATUS: cts.RESPONSE_ERROR,
                         cts.RESPONSE_MESSAGE: err_msg}), 200)

    if request_dict['email'] is not None:
        check_email = User.query.filter_by(email=request_dict['email']).first()
        if check_email:
            err_msg = cts.EMAIL_EXISTS
    else:
        err_msg = "Email address is required"

    if err_msg:
        return (jsonify({cts.RESPONSE_STATUS: cts.RESPONSE_ERROR,
                         cts.RESPONSE_MESSAGE: err_msg}), 200)
    try:
        # password is auto generated
        random_password = str(uuid.uuid1())[:10]
        password = django_pbkdf2_sha256.encrypt(random_password)

        result_items = User(
            email=request_dict['email'],
            first_name=request_dict['first_name'],
            last_name=request_dict['last_name'],
            password=password,
            last_login=dttim.datetime.now(),
            is_superuser=False,
            is_staff=False,
            is_active=True,
            date_joined=dttim.datetime.now(),
            user_uuid=uuid.uuid4())
        db.session.add(result_items)
        db.session.commit()

    except Exception:
        db.session.rollback()
        return (jsonify({cts.RESPONSE_STATUS: cts.RESPONSE_ERROR,
                         'response_message': cts.REGISTER_ERROR}), 200)

    if "auth_groups" in request_dict and len(request_dict["auth_groups"]) >= 1:
        try:
            for auth_group in request_dict["auth_groups"]:
                # check if the permission is in the DB
                check_permit = AuthGroups.query.filter_by(id=auth_group).first()
                if check_permit:
                    # if permission exists in DB then insert into auth group permissions
                    permit_items = AuthUserGroups(
                        user_id=result_items.id,
                        group_id=auth_group,
                        created_on=dttim.datetime.now())
                    db.session.add(permit_items)
                    db.session.commit()
                    # print("valid permissions")
                else:
                    print("invalid auth_group")
        except:
            db.session.rollback()

    # send random generated password to the user.
    user_register_email(result_items, random_password)

    return (jsonify({cts.RESPONSE_STATUS: cts.RESPONSE_SUCCESS,
                     cts.RESPONSE_MESSAGE: cts.REGISTER_SUCCESS}), 200)


@blueprint.route("/users/delete", methods=['DELETE'])
@check_credentials(['edit_users'])
@validate_json
def users_remove():
    """Remove user from the DB using uuid
    sample request
    {
        "user_id":"18fcbb87-d56a-48ed-b589-47a26166eb8c34"
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

    if "user_id" in request_dict:
        try:
            user_exists = User.query.filter_by(user_uuid=request_dict['user_id']).first()
            # print(request_dict['user_id'])
            if user_exists:
                # Delete user auth groups
                AuthUserGroups.query.filter_by(user_id=user_exists.id).delete()
                db.session.commit()

                User.query.filter_by(user_uuid = user_exists.user_uuid).delete()
                db.session.commit()

                response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
                response_dict[cts.RESPONSE_MESSAGE] = cts.USER_DELETED
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


@blueprint.route("/users/reset", methods=['PUT'])
@check_credentials(['reset_password'])
@validate_json
def users_reset_password():
    """Reset user password using uuid
    sample request
    {
        "user_id":"18fcbb87-d56a-48ed-b589-47a26166eb8c34"
    }

    sample response:
    {
      "response_message": "Successfully Password Reset.",
      "response_status": "SUCCESS"
    }
    :return: Dict
    """
    request_dict = request.get_json()
    if "user_id" in request_dict and User.query.filter_by(user_uuid=request_dict['user_id']).first():
        # print(request_dict['user_id'])
        random_new_password = str(uuid.uuid1())[:10]
        password = django_pbkdf2_sha256.encrypt(random_new_password)
        user_details = User.query.filter_by(user_uuid=request_dict['user_id']).first()
        user_details.password = password
        db.session.commit()
    else:
        return (jsonify({cts.RESPONSE_STATUS: cts.RESPONSE_ERROR,
                         cts.RESPONSE_MESSAGE: cts.INVALID_REQUEST}), 200)

    return (jsonify({cts.RESPONSE_STATUS: cts.RESPONSE_SUCCESS,
                     cts.RESPONSE_MESSAGE: cts.PASSWORD_RESET}), 200)


@blueprint.route("/users/update", methods=['PUT'])
@check_credentials(['edit_users'])
def users_update():
    """Update user details in the DB using uuid
    sample request
    {
        "user_id":"18fcbb87-d56a-48ed-b589-47a26166eb8c34",
        "first_name":"hughsonsees1sad2e3",
        "last_name":"hughsonsees1sad2e3",
        "status":True,
        "add_groups":[],
        "remove_groups":[]
    }

    sample response:
    {
      "response_message": "Successfully edited.",
      "response_status": "SUCCESS"
    }
    :return:
    """
    response_dict = {}
    form_details = request.get_json()
    try:
        userprofile = User.query.filter_by(user_uuid=form_details['user_id']).first()
        if userprofile:
            if "first_name" in form_details:
                userprofile.first_name = form_details["first_name"]
            if "last_name" in form_details:
                userprofile.last_name = form_details["last_name"]
            if "status" in form_details:  # this is a boolean value
                userprofile.is_active = form_details["status"]
            db.session.commit()

            # add groups to user
            if "add_groups" in form_details and len(form_details["add_groups"]) >= 1:
                # print(len(form_details["add_groups"]))
                response_dict[cts.RESPONSE_STATUS], \
                    response_dict[cts.RESPONSE_MESSAGE] = add_group_to_user(form_details,
                                                                            userprofile.id,
                                                                            userprofile.user_uuid)

            # remove user groups
            if "remove_groups" in form_details and len(form_details["remove_groups"]) >= 1:
                # print(len(form_details["remove_groups"]))
                response_dict[cts.RESPONSE_STATUS], \
                    response_dict[cts.RESPONSE_MESSAGE] = remove_group_to_user(form_details,
                                                                               userprofile.id,
                                                                               userprofile.user_uuid)

            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
            response_dict[cts.RESPONSE_MESSAGE] = cts.RECORD_SUCCESS
        else:
            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
            response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST
    except:
        db.session.rollback()
        response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
        response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST
    return jsonify(response_dict), 200


def add_group_to_user(request_dict, user_id, useruuid):
    """Add group(s) to user

    :param request_dict:
    :param user_id: user uuid
    :return: response dict with status and message
    """
    try:
        #print(len(request_dict["add_permissions"]))
        for group in request_dict["add_groups"]:
            # check if the permission is in the DB
            check_group = AuthGroups.query.filter_by(id=group).first()
            if check_group:

                # if group exists in DB then then check if group is in user auth group
                check_auth_group = AuthUserGroups.query.filter_by(user_id=user_id,
                                                                          group_id=group).first()
                # if group is not in user auth group then insert
                if not check_auth_group:
                    # print("its not in group permissions")
                    permit_items = AuthUserGroups(
                        group_id=group,
                        user_id=user_id,
                        created_on=dttim.datetime.now())
                    db.session.add(permit_items)
                    db.session.commit()

                    # add to grey list if there is a change is in user auth group
                    add_user_greylist(useruuid)
                else:
                    print("groups already exist")
            else:
                print("invalid group")
        #return cts.RESPONSE_SUCCESS, cts.GROUP_UPDATED
    except:
        db.session.rollback()
        return cts.RESPONSE_ERROR, cts.USERUPDATE_PARTIAL_ERROR
    return cts.RESPONSE_SUCCESS, cts.RECORD_SUCCESS


def remove_group_to_user(request_dict, user_id, useruuid):
    """Remove group to user

    :param request_dict:
    :param user_id: user uuid
    :return: response dict with status and message
    """
    try:
        for group in request_dict["remove_groups"]:
            # print(permits)
            # check if the permission is in the DB
            check_user_group = AuthUserGroups.query.filter_by(group_id=group, user_id=user_id).first()
            if check_user_group:
                # if permission exists then remove permission from auth group permissions
                AuthUserGroups.query.filter_by(group_id=group, user_id=user_id).delete()
                db.session.commit()
                # print("valid permissions to delete")

                # add to grey list if there is a change is in user auth group
                add_user_greylist(useruuid)
            else:
                print("invalid group to delete")
    except:
        db.session.rollback()
        return cts.RESPONSE_ERROR, cts.USERUPDATE_PARTIAL_ERROR
    return cts.RESPONSE_SUCCESS, cts.RECORD_SUCCESS


@blueprint.route("/users/list")
@check_credentials(['view_admin_panel'])
def users_list():
    """list all available users and respective permissions
    sample request
    /users/list
    {
        "response_message": {
            "total": 1,
            "users": [
                {
                    "email": "hughson.simon@gmail.com",
                    "id": "18fcbb87-d56a-48ed-b589-47a26166eb8c",
                    "last_login": "Wed, 09 Aug 2017 19:06:24 GMT",
                    "name": "hughsonsees1sad2e3 hughsonsees1sad2e3",
                    "auth_user_groups": [],
                    "status": true
                }
            ]
        },
        "response_status": "SUCCESS"
    }
    :return: dict: users dict items with available permissions
    """
    response_dict = {}
    try:
        all_users = User.query.all()
        total_users = len(all_users)
        users_list = []
        if total_users >= 1:
            for user in all_users:
                users_dict = {}
                group_list = []
                users_dict['id'] = user.user_uuid
                users_dict['name'] = user.full_name
                users_dict['email'] = user.email
                users_dict['status'] = user.is_active()
                users_dict['last_login'] = user.last_login
                for group in user.auth_user_groups.all():
                    group_list.append(group.group_id)
                users_dict['auth_user_groups'] = group_list
                users_list.append(users_dict)
            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
            response_dict[cts.RESPONSE_MESSAGE] = {}
            response_dict[cts.RESPONSE_MESSAGE]['total'] = total_users
            response_dict[cts.RESPONSE_MESSAGE]['users'] = users_list
        else:
            response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
            response_dict[cts.RESPONSE_MESSAGE] = {}
            response_dict[cts.RESPONSE_MESSAGE]['total'] = 0
            response_dict[cts.RESPONSE_MESSAGE]['users'] = []
    except:
        db.session.rollback()
        response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_ERROR
        response_dict[cts.RESPONSE_MESSAGE] = cts.INVALID_REQUEST
        raise
    return jsonify(response_dict), 200


@blueprint.route("/user/view", methods=['POST'])
@check_credentials(['view_admin_panel'])
@validate_json
def user_view():
    """View user details
    sample request
    {
        "user_id":"18fcbb87-d56a-48ed-b589-47a26166eb8c34"
    }

    sample response:
    {
      "response_status": "SUCCESS",
      "response_message":{
                    "email": "hughson.simon@gmail.com",
                    "id": "18fcbb87-d56a-48ed-b589-47a26166eb8c",
                    "last_login": "Wed, 09 Aug 2017 19:06:24 GMT",
                    "name": "hughsonsees1sad2e3 hughsonsees1sad2e3",
                    "auth_user_groups": [1,2],
                    "status": true
                }
    }
    :return: response dict with status and users dict items with available groups
    """
    request_dict = request.get_json()
    response_dict = {}

    if "user_id" in request_dict:
        try:
            user_exists = User.query.filter_by(user_uuid=request_dict['user_id']).first()
            # print(request_dict['user_id'])
            if user_exists:
                # View user auth groups
                users_dict = {}
                group_list = []
                users_dict['id'] = user_exists.user_uuid
                users_dict['name'] = user_exists.full_name
                users_dict['email'] = user_exists.email
                users_dict['status'] = user_exists.is_active()
                users_dict['last_login'] = user_exists.last_login
                for group in user_exists.auth_user_groups.all():
                    group_list.append(group.group_id)
                users_dict['auth_user_groups'] = group_list
                response_dict[cts.RESPONSE_STATUS] = cts.RESPONSE_SUCCESS
                response_dict[cts.RESPONSE_MESSAGE] = users_dict

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

