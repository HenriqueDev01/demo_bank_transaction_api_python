import json
from flask import request
from .data_related import *
from .error_related import ErrCode, errMessages

# for mocks only
import random
USE_MOCK = 1

OK = 0
SIMPLE_MONETARY_SIMBLE = '$'

def resp_data_for(err_code):
    err_code = err_code or ErrCode.unknown
    return json.dumps({
        'code': err_code,
        'message': errMessages[err_code]
    })

# StartOf: data fetchs

def req_external_assess(transaction:TransactionRequest):
    # Fetch external assess here
    # TODO
    pass

    # Just a mock
    return {
        'message': 'Authorized' if random.randint(0,1) else 'Unauthorized'
    }
# EndOf: data fetchs

def external_assess(transaction:TransactionRequest):
    """ Request for external assess and verify the validation """
    resp = req_external_assess(transaction)
    return resp['message'] == 'Authorized'

def assess_send(transaction:TransactionRequest):
    user = UserHelper.get_user(transaction.sender)
    if user.user_type == UserType.merchant:
        return ErrCode.shop_cant_send
    if user.ballance < transaction.value:
        return ErrCode.no_enough_ballance
    if not external_assess(transaction):
        return ErrCode.external_assess_danied
    return OK

def get_received_obj():
    """ 
    Get the data passed with http request.
    Returns: a simple python object or None if received data is invalid.
    """
    # Since transaction data is not big. 
    # Limit the size to block strange data.
    if len(request.data) > 300:
        return None
    data = request.json
    return data

if USE_MOCK:
    def get_received_obj():    
        # For tests with html form
        if request.content_type == 'application/x-www-form-urlencoded':
            # from html form
            data = dict(request.form)
        else:
            # json
            data = request.json
        return data

def get_parsed_requested_transaction():
    """
    Parse and return the received transaction object (from http request) or returns None if data it's invalid.
    """
    data = get_received_obj()
    transaction = TransactionRequest.from_dict(data)
    return transaction

def get_parsed_requested_undo_transaction_id():
    received_obj = get_received_obj()
    try:
        transaction_id = received_obj['transaction_id']
        # parse id here if needs
        if isinstance(transaction_id, str):
            transaction_id = int(transaction_id)
    except (TypeError, KeyError, ValueError):
        ## If it's not a dict or don't contains the key for
        ## transaction id or cannot parse to right type 
        return None
    return transaction_id

def build_notification_massage_for_receiver(transaction:TransactionRequest):
    sender_name = UserHelper.get_user(transaction.sender).firstName
    # can parse sender name here for privacity or any needs
    monetary_symbol = SIMPLE_MONETARY_SIMBLE
    parsed_str_value = "%.2f"%float(transaction.value)
    message = f"{sender_name} sent you {monetary_symbol}{parsed_str_value}"
    return message
    
def notify_receiver(transaction:Transaction):
    receiver = UserHelper.get_user(transaction.receiver)
    message = build_notification_massage_for_receiver(transaction)
    # Send the notification here
    # TODO

    # mock
    try:
        print('notifying receiver')
        print('email:\t', receiver.email)
        print('message:\t', message)
    except AttributeError:
        # Here can retry notify after sometime, store in somewhere to 
        # retry later, repass to another service to handle or wharever
        # needs to do.
        pass

def do_transfer(transaction:Transfer):
    ## Do wallet transference of values
    UserHelper.sub_from_ballance(transaction.sender, transaction.value)
    UserHelper.add_to_ballance(transaction.receiver, transaction.value)

def do_transaction(transaction_request:TransactionRequest):
    do_transfer(transaction_request)
    transaction = TransactionDbHelper.create(transaction_request)
    return transaction

def undo_transaction(transaction:Transaction):
    back_transfer = Transfer()
    back_transfer.receiver = transaction.sender
    back_transfer.sender = transaction.receiver
    back_transfer.value = transaction.value
    back_transfer.timestamp = transaction.timestamp
    TransactionDbHelper.mark_undone(transaction.id)
    transaction.undone = True
    return back_transfer

def notify_undone_transaction(transaction:Transaction):
    # TODO
    pass
