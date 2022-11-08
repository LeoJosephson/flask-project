def createValidationErrorMessage(e, error_name="ValidationError"):
    msg = {}
    for k, i in e.messages.items():
        msg[k] = i
    return {"message": error_name,
        "fields": msg}