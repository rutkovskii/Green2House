import sqlalchemy
from sqlalchemy.sql import func
from flask import request, render_template, Blueprint

import json

from app.models import DataSample
from app.database import Session

datasample_page_bp = Blueprint('datasample_page_bp',__name__)


@datasample_page_bp.route('/all_data_samples')
def serve_page_data_samples():
    """
    Brings to the table with Haros
    """
    return render_template('/DATASAMPLES_PAGE/data_sample_table.html', title='Data Samples')


@datasample_page_bp.route('/api/serve_data_samples')
def serve_data_samples():
    """Sorts the table, returns searched data"""
    session = Session()
    query = session.query(DataSample).order_by(DataSample.id.desc())
    session.close()

    func.to_char()

    # search filter
    search = request.args.get('search[value]')

    if search:
        query = query.filter(sqlalchemy.or_(
            DataSample.user_id.like(f'%{search}%'),
            DataSample.time.like(f'%{search}%'),
            DataSample.date.like(f'%{search}%')
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
        if col_name not in ['user_id','time','date']:
            col_name = 'date'

        # gets descending sorting
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        desired_col = getattr(DataSample,col_name)

        #decending
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

    # print([sample.to_dict() for sample in query])
    # print()
    # print(json.dumps([sample.to_dict() for sample in query],default=str))

    # response to be shown on HTML side
    return json.dumps(
        {
            'data': [sample.to_dict() for sample in query],
            'recordsFiltered': total_filtered,
            'recordsTotal': query.count(),
            'draw': request.args.get('draw', type=int),
        },default=str)