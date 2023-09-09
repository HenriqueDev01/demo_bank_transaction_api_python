import time
from typing import TypeAlias
from decimal import Decimal
from enum import IntEnum
import json
from .error_related import ErrCode

# for mocks only
import random

# StartOf: users
class UserType(IntEnum):
    common = 0
    merchant = 1

class User:
    id:int
    document:int
    email:str
    firstName:str
    lastName:str
    user_type:UserType
    ballance:Decimal

class UserHelper:
    @staticmethod
    def get_user(user_id):
        # Fetch user info from database here
        # TODO
        pass

        # mock
        mock_user = User()
        mock_user.id = user_id
        mock_user.email = "some@email.com"
        mock_user.document = "random_cpf_or_cnpj"
        # mock_user.user_type = random.choice(tuple(UserType._member_map_.values()))
        if random.randint(0,1):
            mock_user.firstName = 'Foo'
            mock_user.user_type = UserType.common
        else:
            mock_user.firstName = 'Shop Foo'
            mock_user.user_type = UserType.merchant        
        int_part = random.randint(300,1000)
        dec_part = random.randint(0,99)
        str_value = "%d.%02d"%(int_part, dec_part)
        print('balance', str_value)
        mock_user.ballance = float(str_value)
        return mock_user

    @staticmethod
    def add_to_ballance(user_id, value):
        # Add the value to the passed user_id wallet
        # TODO
        pass

    @staticmethod
    def sub_from_ballance(user_id, value):
        # Subtract the value from the passed user_id wallet
        # TODO
        pass
# EndOf: users

# StartOf: transfers and transactions
class Transfer:
    sender:int
    receiver:int
    value:Decimal
    timestamp:float

    @classmethod
    def from_dict(cls, obj:dict):
        result = cls()
        try:
            result.sender = int(obj['sender'])
            result.receiver = int(obj['receiver'])
            result.value = Decimal(obj['value'])
            result.timestamp = obj.get('timestamp', time.time())
        except (KeyError, ValueError):
            return None
        return result

    # for tests
    def __repr__(self) -> str:
        return str(self.__dict__)

class TransactionRequest(Transfer):
    pass

class Transaction(Transfer):
    ID_TYPE: TypeAlias = int
    id:ID_TYPE
    undone:bool = False

    def to_json(self):
        return json.dumps({
            'id': self.id,
            'sender': self.sender,
            'receiver': self.receiver,
            'value': float(self.value),
            'undone': self.undone,
            'timestamp': self.timestamp,
        })

class TransactionDbHelper:
    @staticmethod
    def get(transaction_id) -> Transaction|ErrCode:
        # Fetch and parse transaction from database
        # TODO
        pass

        # mock
        transaction = Transaction()
        transaction.id = transaction_id
        transaction.receiver = random.randint(1000, 9999)
        transaction.sender = random.randint(1000, 9999)
        transaction.value = random.randint(100, 2000)
        transaction.timestamp = time.time()
        return transaction
        # return ErrCode.cannot_read_transaction

    @staticmethod
    def create(transfer:Transfer):
        # Saves the transaction to database
        # TODO
        pass

        # mock
        transaction = Transaction.from_dict(transfer.__dict__)
        transaction.id = random.randint(1000, 9999)
        print('transaction created', transaction.__dict__)
        return transaction

    @staticmethod
    def mark_undone(transaction_id):
        # Mark transaction as undone
        # TODO
        pass
# EndOf: transfers and transactions
