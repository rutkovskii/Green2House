from flask import request, Blueprint, render_template
import json

from app.database import Session
from app.models import DataSample
import app.utils as u


home_page_bp = Blueprint('home_bp',__name__)

@home_page_bp.route('/')
def home():
    return render_template('/home_page.html', title='Home — Green2House')