from enum import Enum

# Should correspond to the values in the order database
class OrderStatus(Enum):
    PENDING = 'Pending'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'

class ForbiddenCancellationItems(Enum):
    PERISHABLE = 'Perishable'
    DIGITAL = 'Digital'