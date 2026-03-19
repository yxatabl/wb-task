class OrderError(Exception):
    pass

class InsufficientBalanceError(OrderError):
    pass

class InsufficientStockError(OrderError):
    pass

class EmptyCartError(OrderError):
    pass