def ok(body: str = None): return __response(200, body)
def created(body: str = None): return __response(201, body)

def __response(status: int, body: str): return {
    "statusCode": status,
    "body": body
}