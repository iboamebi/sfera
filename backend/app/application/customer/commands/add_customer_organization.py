"""
Add customer-organization association command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddCustomerOrganizationCommand:
    """Command for linking an organization to a customer."""

    customer_id: UUID
    organization_id: UUID
