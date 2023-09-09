from flask import Flask, Response
from flask_cors import CORS, cross_origin
# from markupsafe import escape
from lib import *
from lib.data_related import *

# for test only
from flask import send_file

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

STATUS_CODE_ERR = 400
STATUS_CODE_OK = 200

@app.route("/transaction", methods=['POST'])
def on_req_do_transaction():
    transaction_request = get_parsed_requested_transaction()
    resp = Response()
    # resp.content_type = 'application/json'
    if not transaction_request:
        resp.status = STATUS_CODE_ERR
        resp.data = resp_data_for(ErrCode.cannot_read_transaction)
        return resp

    ## Don't need assess permission for transaction (like if 
    ## it's really the user sending or authenticate)?

    code = assess_send(transaction_request)
    if code != OK:
        resp.status = STATUS_CODE_ERR
        resp.data = resp_data_for(code)
        return resp

    transaction = do_transaction(transaction_request)
    notify_receiver(transaction)
    resp.status = STATUS_CODE_OK
    resp.data = transaction.to_json()
    return resp

@app.route("/undo-transaction", methods=['POST'])
def on_req_undo_transaction():
    resp = Response()
    
    transaction_id = get_parsed_requested_undo_transaction_id()
    if not transaction_id or not isinstance(transaction_id, Transaction.ID_TYPE):
        resp.status = STATUS_CODE_ERR
        resp.data = resp_data_for(ErrCode.invalid_received_data)
        return resp

    ## Don't need assess permission to undo the transaction (like if 
    ## it's really the user sending or authenticate)?

    obj = TransactionDbHelper.get(transaction_id)
    if isinstance(obj, int): # if it's a error code (int)
        err_code = obj
        resp.status = STATUS_CODE_ERR
        resp.data = resp_data_for(err_code)
        return resp

    transaction = obj
    transfer_back_obj = undo_transaction(transaction)
    notify_undone_transaction(transaction)
    resp.status = STATUS_CODE_OK
    resp.data = transaction.to_json()
    return resp

if USE_MOCK:
    @app.route("/", methods=['GET'])
    def test_page():
        return send_file('test.html')
