import json
import sys
from flask import Flask, request, jsonify
from my_service.caller_utils import raise_on_bad_input, BaseInputError
from my_service.data_helper import DatabaseAccess
from my_service.persons_extractor import get_persons_name

app = Flask(__name__)


@app.route('/caller_id', methods=['POST'])
def export():
    args = request.data
    print(args, file=sys.stderr)
    args = json.loads(args)
    try:
        p_number = args.get("phone_number")
        raise_on_bad_input(p_number)
        result = get_persons_name(p_number, DB)
        response = {'full_name': result}
        return jsonify(response), 200

    except BaseInputError as e:
        response = {'exception': str(e)}
        print(json.dumps(response), file=sys.stderr)
        return jsonify(response), 400

    except Exception as e:
        # if get an expected will return server error
        response = {'exception': str(e)}
        print(json.dumps(response), file=sys.stderr)
        return jsonify(response), 500


def run_server():
    global DB
    DB = DatabaseAccess()
    app.run(debug=False, host='127.0.0.1', port=8080, threaded=True)


if __name__ == "__main__":
    run_server()
