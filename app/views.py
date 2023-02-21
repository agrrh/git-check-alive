from app import app_flask
from flask import request, render_template
from app import token_flask, forms
from analytical import database
import asyncio


@app_flask.route("/api", methods=["POST"])
def post_api():
    token_api = request.json["token"]
    repository_path = request.json["repository_path"]
    instance_db_client = database.DataBaseHandler()
    return asyncio.run(instance_db_client.get_report(repository_path, token_api))


@app_flask.route("/", methods=["GET"])
def get_index():
    form = forms.RepositoryPathForm()
    return render_template("index.html", form=form), 200


@app_flask.route("/", methods=["POST"])
def post_index():
    form = forms.RepositoryPathForm()
    repository_path = request.form["link_repository"]
    instance_db_client = database.DataBaseHandler()
    json, code = asyncio.run(
        instance_db_client.get_report(repository_path, token_flask)
    )
    return render_template("index.html", form=form, json=json), code


@app_flask.errorhandler(404)
def page_not_found(error):
    return "Страницы не существует!!", 404
