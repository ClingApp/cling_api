#!/usr/bin/env python

from flask import jsonify

from app import app


@app.route('/api', methods=['GET'])
def this_func():
    """This is a function. It does nothing."""
    return jsonify({'result': ''})


@app.route('/api/help', methods=['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)


if __name__ == '__main__':
    app.run(debug=True)