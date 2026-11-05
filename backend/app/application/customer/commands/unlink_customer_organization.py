"""
Unlink customer-organization association command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UnlinkCustomerOrganizationCommand:
    """Command for unlinking an organization from a customer."""

    customer_id: UUID
    organization_id: UUID
