from flask import Flask, jsonify, request
from flask.views import MethodView
from db import Add, Session
from schema import validate_create_ad
from error import HttpError
from flask_bcrypt import Bcrypt

app = Flask('app')
bcrypt = Bcrypt(app)


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', "description": error.message})
    http_response.status_code = error.status_code
    return http_response


def get_add(add_id: int, session: Session):
    add = session.query(Add).get(add_id)
    if add is None:
        raise HttpError(404, 'add not found')
    return add


class Advertisement(MethodView):
    def get(self, add_id: int):
        with Session() as session:
            add = get_add(add_id, session)
            return jsonify({'id': add.id,
                            'title': add.title,
                            'description': add.description,
                            'creation_time': add.creation_time,
                            'owner': add.owner,
                            })
    def post(self):
        json_data = validate_create_ad(request.json)
        with Session() as session:
            new_add = Add(**json_data)
            session.add(new_add)
            session.commit()
            return jsonify({'id': new_add.id,
                            'title': new_add.title,
                            'description': new_add.description,
                            'creation_time': new_add.creation_time,
                            'owner': new_add.owner,
                            })

    def patch(self, add_id: int):
        json_data = request.json
        with Session() as session:
            add = get_add(add_id, session)
            for field, value in json_data.items():
                setattr(add, field, value)
            session.add(add)
            session.commit()
        return jsonify({'status': 'success'})

    def delete(self, add_id: int):
        with Session() as session:
            add = get_add(add_id, session)
            session.delete(add)
            session.commit()
            return jsonify({'status': 'success'})


app.add_url_rule("/adv/<int:ad_id>/", view_func=Advertisement.as_view('advertisement'),
                 methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule("/adv", view_func=Advertisement.as_view('advertisement1'), methods=['POST'])


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)