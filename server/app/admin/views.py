import sqlalchemy
from sqlalchemy.sql import func
from flask import request, render_template, Blueprint, abort
from flask_login import login_required

from app.models import User
from app.database import session_scope
from app.admin.config import ServerConfig
from app.admin.decorators import admin_required

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route(ServerConfig.ADMIN_DATA_SAMPLES_ROUTE, methods=['GET'])
@login_required
@admin_required
def serve_admin_data_samples():
    return render_template('/admin_data_records_table.html', title='Data Samples')


@admin_bp.route(ServerConfig.ADMIN_PAGE_ROUTE)
@login_required
@admin_required
def serve_admin_main():
    return render_template('/admin_page_main.html', title='Admin Page')


@admin_bp.route(ServerConfig.ADMIN_PAGE_USERS_ROUTE)
@login_required
@admin_required
def serve_page_users():
    return render_template('/admin_users_table.html', title='Users')


@admin_bp.route(ServerConfig.ADMIN_PAGE_SERVE_USERS_ROUTE, methods=['GET'])
@login_required
@admin_required
def serve_users():
    """Sorts the table, returns searched data"""

    if not request.args.get('token'):
        return abort(403)

    with session_scope() as s:
        query = s.query(User)

    func.to_char()

    # search filter
    search = request.args.get('search[value]')

    if search:
        query = query.filter(sqlalchemy.or_(
            User.name.like(f'%{search}%'),
            User.phone_number.like(f'%{search}%'),
            User.email.like(f'%{search}%'),
            User.datetime_joined.like(f'%{search}%')
        ))

    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:

        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['name', 'phone_number', 'email', 'datetime_joined']:
            col_name = 'phone_number'

        # gets descending sorting
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        desired_col = getattr(User, col_name)

        # decending
        if descending:
            desired_col = desired_col.desc()
        order.append(desired_col)

        i += 1

    # ordering
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response to be shown on HTML side
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': query.count(),
        'draw': request.args.get('draw', type=int),
    }
