from fastapi.templating import Jinja2Templates
import json
from app.i18n.strings import t, STRINGS, CATEGORY_LABELS,STATUS_LABELS ,ROLE_LABELS

templates = Jinja2Templates(directory='app/frontend/templates')
templates.env.globals['t'] = t
templates.env.globals['STRINGS_JSON'] = json.dumps(STRINGS, ensure_ascii=False)
templates.env.globals['CATEGORY_LABELS_JSON'] = json.dumps(CATEGORY_LABELS, ensure_ascii=False)
templates.env.globals['STATUS_LABELS_JSON'] = json.dumps(STATUS_LABELS, ensure_ascii=False)
templates.env.globals['ROLE_LABELS_JSON'] = json.dumps(ROLE_LABELS, ensure_ascii=False)
