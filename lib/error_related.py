from enum import IntEnum, auto as autoEnum

# StartOf: Error helpers
class ErrCode(IntEnum):
    unknown = autoEnum()
    shop_cant_send = autoEnum()
    no_enough_ballance = autoEnum()
    external_assess_danied = autoEnum()
    cannot_read_transaction = autoEnum()
    invalid_received_data = autoEnum()

errMessages = {
    ErrCode.unknown: "Unknown error.",
    ErrCode.shop_cant_send: "Your user type can't send money.",
    ErrCode.no_enough_ballance: "Error. You tried to send more money than you have.",
    ErrCode.external_assess_danied: "Transition danied.",
    ErrCode.cannot_read_transaction: "Invalid data.",
    ErrCode.invalid_received_data: "Invalid received data."
}
# EndOf: Error helpers
