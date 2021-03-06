import os

from flask import request, send_file
from flask_login import login_required, current_user
from flask_uploads import UploadNotAllowed

from app import app, photos
from app.forms import AdminMasterForm2
from app.db_api.clients import *
from app.db_api.masters import *
from app.login import admin_only
from app.rest_api.utils import *


@app.route('/api/masters', methods=['GET'])
@login_required
@admin_only
def api_masters_get():
    return build_list_data_reply(get_masters())


@app.route('/api/masters/relevant', methods=['GET'])
def api_masters_get_relevant():
    return build_list_data_reply(get_relevant_masters_short())


@app.route('/api/masters/<int:master_id>', methods=['GET'])
def api_master_get(master_id):
    if current_user.is_authenticated and current_user.is_admin:
        return build_one_data_reply(get_master(master_id),
                                    {'favourite_clients_amount': (get_master_favourite_clients_amount(master_id))})
    return build_one_data_reply(get_master_short(master_id))


@app.route('/api/masters/categories/<int:category_id>', methods=['GET'])
@login_required
@admin_only
def api_masters_does_whole_category_get(category_id):
    return build_list_data_reply(get_masters_does_all_procedures_in_category(category_id))


@app.route('/api/masters/procedures', methods=['GET'])
@login_required
@admin_only
def api_all_masters_procedures_get():
    return build_list_data_reply(get_all_masters_doing_procedures())


@app.route('/api/masters/<int:master_id>/procedures', methods=['GET'])
@login_required
@admin_only
def api_master_procedures_get(master_id):
    return build_list_data_reply(get_all_procedures_join_master(master_id))


@app.route('/api/masters/<int:master_id>/procedures', methods=['PUT'])
@login_required
@admin_only
def api_master_procedures_put(master_id):
    json = request.get_json()
    for json_part in json:
        if 'procedure_id' not in json_part or 'duration' not in json_part:
            return build_message_reply((False, 'Не вказано процедуру чи тривалість'))
        if type(json_part['procedure_id']) != int or type(json_part['duration']) != int:
            return build_message_reply((False, 'Мають бути цілі числа'))

    return build_message_reply(update_master_procedures(master_id, json))


@app.route('/api/masters', methods=['POST'])
@login_required
@admin_only
def api_master_post():
    form = AdminMasterForm2(data=request.args)
    form.id.choices = [('', 'Не обрано')] + \
                      [(str(user['id']), user['surname'] + ' ' + user['first_name'] + ', +38' + user['phone'])
                       for user in get_clients()]

    if not form.validate():
        return build_form_invalid_reply(form)

    master = Master()
    form.populate_obj(master)

    if master.info.strip() == '':
        master.info = None

    return build_message_reply(add_master(master))


@app.route('/api/masters/<int:master_id>/photo', methods=['GET'])
def api_master_photo_get(master_id):
    filename = '_' + str(master_id) + '.png'
    if os.path.exists(os.path.join('.', 'app', 'photos', filename)):
        return send_file(os.path.join('photos', filename))
    return send_file(os.path.join('photos', 'default.png'))


def generate_photo_name(master_id):
    return '_' + str(master_id) + '.png'


@app.route('/api/masters/<int:master_id>/photo', methods=['POST'])
@login_required
@admin_only
def api_master_photo_post(master_id):
    if 'photo' not in request.files:
        return build_message_reply((False, 'Не вказано фото'))

    try:
        photo = request.files.get('photo')
        api_master_photo_delete(master_id)

        photos.save(photo, name=generate_photo_name(master_id))
        return build_message_reply((True, 'Успішно оновлено фото майстра'))

    except UploadNotAllowed as e:
        return build_message_reply((False, 'Сталася помилка, некоректний формат'))


@app.route('/api/masters/<int:master_id>/photo', methods=['DELETE'])
@login_required
@admin_only
def api_master_photo_delete(master_id):
    try:
        os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], generate_photo_name(master_id)))
        return build_message_reply((True, 'Успішно видалено фото'))
    except FileNotFoundError:
        return build_message_reply((False, 'У майстра немає фото, окрім за замовченням'))


@app.route('/api/masters/<int:master_id>', methods=['PUT'])
@login_required
@admin_only
def api_master_put(master_id):
    form = AdminMasterForm2(data=request.args)
    form.id.choices = [(str(master_id), '')]

    if not form.validate():
        return build_form_invalid_reply(form)

    master = Master(id=master_id)
    form.populate_obj(master)

    if master.info.strip() == '':
        master.info = None

    return build_message_reply(update_master(master))


@app.route('/api/masters/<int:master_id>', methods=['DELETE'])
@login_required
@admin_only
def api_master_delete(master_id):
    return build_message_reply(delete_master(master_id))
