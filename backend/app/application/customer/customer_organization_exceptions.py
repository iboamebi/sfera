"""
Application exceptions for Customer ↔ Organization associations.
"""


class CustomerOrganizationNotFoundApplicationError(Exception):
    """Customer or organization was not found."""


class CustomerOrganizationAlreadyLinkedApplicationError(Exception):
    """Customer is already linked to the organization."""


class CustomerOrganizationLinkNotFoundApplicationError(Exception):
    """Customer is not linked to the organization."""
