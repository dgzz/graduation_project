from flask import current_app, jsonify
from flask import render_template
from flask import request

from person import db
from person.utils.response_code import RET
from . import Superson
from person.models import Admin


@Superson.route("/")
def index():
    return render_template('index.html')


# 添加管理员数据
@Superson.route("/add_admin", methods=['POST'])
def add_admin():
    # 获取参数
    admin_id = request.json.get('admin_id')
    admin_psw = request.json.get('admin_psw')
    # 检查参数的完整性
    if not all([admin_id, admin_psw]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        admin_id = int(admin_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')
    # 构建模型类对象
    admin = Admin()
    admin.admin_id = admin_id
    admin.admin_psw = admin_psw
    # 存入数据库
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')


# 修改管理员数据
@Superson.route("/editor_admin", methods=['POST'])
def editor_admin():
    # 获取参数
    admin_id = request.json.get('admin_id')
    editor_admin_id = request.json.get('editor_admin_id')
    editor_admin_psw = request.json.get('editor_admin_psw')
    # 检查参数的完整性
    if not all([admin_id, editor_admin_id, editor_admin_psw]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        editor_admin_id = int(editor_admin_id)
        admin_id = int(admin_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')

    # 检查用户输入id和列表id是否一致
    if admin_id != editor_admin_id:
        return jsonify(errno=RET.DATAERR, errmsg='请输入正确要修改的管理员id错误')
    # 构建模型类对象
    try:
        admin = Admin.query.filter_by(admin_id=editor_admin_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询管理员错误')
    admin.admin_psw = editor_admin_psw
    # 存入数据库
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')

# 删除管理员数据
@Superson.route("/delete_admin", methods=['DELETE'])
def delete_admin():
    # 获取参数
    admin_id = request.json.get('admin_id')
    editor_admin_id = request.json.get('editor_admin_id')
    # 检查参数的完整性
    if not all([admin_id, editor_admin_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        editor_admin_id = int(editor_admin_id)
        admin_id = int(admin_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')

    # 检查用户输入id和列表id是否一致
    if admin_id != editor_admin_id:
        return jsonify(errno=RET.DATAERR, errmsg='请输入正确要删除的管理员id错误')
    # 构建模型类对象
    try:
        admin = Admin.query.filter_by(admin_id=editor_admin_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询管理员错误')

    # 存入数据库
    try:
        db.session.delete(admin)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='删除数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')

# 显示管理员列表数据
@Superson.route("/Supersons.html")
def Supersons():
    # 从数据库获取数据
    try:
        admins = Admin.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询管理员数据失败')
    # 判断查询结果
    if not admins:
        return jsonify(errno=RET.NODATA, errmsg='无管理员数据')
    # 定义列表，存储数据
    data = {
        'admins': admins
    }
    return render_template('Supersons.html', data=data)
