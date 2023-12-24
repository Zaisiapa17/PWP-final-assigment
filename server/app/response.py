from flask import jsonify, make_response

def ok(values, message):
    res = {
        'values': values,
        'message': message
    }

    return make_response(jsonify(res)), 200

def okAdmin(values, total_page, message):
    res = {
        'values': values,
        'total_page': total_page,
        'message': message
    }

    return make_response(jsonify(res)), 200

def badRequest(values, message):
    res = {
        'values': values,
        'message': message
    }

    return make_response(jsonify(res)), 400