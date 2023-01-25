import sqlalchemy
from sqlalchemy.sql import func
from flask import request, render_template, Blueprint

from app.models import User
from app.database import Session
from app.admin.config import SERVER_CONFIG

admin_page_bp = Blueprint('admin_page_bp', __name__)


@admin_page_bp.route(SERVER_CONFIG.ADMIN_PAGE_ROUTE)
def serve_admin_main():
    return render_template('/ADMIN_PAGE/admin_page_main.html', title='Admin Page')


@admin_page_bp.route(SERVER_CONFIG.ADMIN_PAGE_USERS_ROUTE)
def serve_page_users():
    """
    Brings to the table with Haros
    """
    return render_template('/ADMIN_PAGE/users_table.html', title='Users')


@admin_page_bp.route(SERVER_CONFIG.ADMIN_PAGE_SERVE_USERS_ROUTE, methods=['GET'])
def serve_users():
    """Sorts the table, returns searched data"""
    session = Session()
    query = session.query(User)
    session.close()

    func.to_char()

    # search filter
    search = request.args.get('search[value]')

    if search:
        query = query.filter(sqlalchemy.or_(
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
        if col_name not in ['phone_number', 'email', 'datetime_joined']:
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
