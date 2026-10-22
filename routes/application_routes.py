from flask import Blueprint, abort, jsonify, request
from services.application_service import get_application_by_id, get_applications, create_application, modify_application, delete_application
from exceptions import ApplicationNotFoundError, ValidationError


application_bp = Blueprint(
    'applications', # Blueprint name
    __name__, # Import name
    url_prefix="/applications" # Prepends /applications to all routes in this BP
)

# get specific app
@application_bp.route("/<int:app_id>")
def get_app(app_id):
    try:
        application = get_application_by_id(app_id)
    except ApplicationNotFoundError as e:
        return abort(404, description=str(e))
    
    return jsonify(application)

# get all apps
@application_bp.route('')
def get_apps():
    applications = get_applications()

    return jsonify(applications)

# create new app
@application_bp.route("", methods=["POST"])
def create_app():
    data = request.get_json()

    try:
        new_application = create_application(data)

        app_data = new_application

        if app_data is None:
            return abort(500, description="Unexpected error.")

        return jsonify(app_data), 201
    except TypeError as e:
        return abort(400, description="Type Error.")
    except ValidationError as e:
        return abort(400, description=str(e))

# modify existing app
@application_bp.route("/<int:app_id>", methods=["PATCH"])
def modify(app_id):
    data = request.get_json()

    try:
        app_data = modify_application(app_id, data)

        return jsonify(app_data), 200
    
    except ValidationError as e:
        return abort(400, description=str(e))
    except ApplicationNotFoundError as e:
        return abort(404, description=str(e))
    except Exception:
        return abort(500, description="Unexpected server error.")
    

# delete app
@application_bp.route("/<int:app_id>", methods=["DELETE"])
def delete(app_id):
    try:
        deleted_application = delete_application(app_id)

        return "", 204

    except ApplicationNotFoundError as e:
        return abort(404, description=str(e))
    except Exception:
        return abort(500, description="Unexpected server error.")