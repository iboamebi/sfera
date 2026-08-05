"""
Delete Customer command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DeleteCustomerCommand:
    """Delete customer command."""

    customer_id: UUID
