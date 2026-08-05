"""
Domain entity: Organization.
"""

from dataclasses import dataclass

from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class Organization(Entity):
    """
    Organization domain entity.
    """

    name: str
    short_name: str | None = None
    inn: str | None = None
    kpp: str | None = None
    ogrn: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    comment: str | None = None

    def change_name(
        self,
        name: str,
    ) -> None:
        """Change organization name."""

        self.name = name

    def change_short_name(
        self,
        short_name: str | None,
    ) -> None:
        """Change organization short name."""

        self.short_name = short_name

    def change_inn(
        self,
        inn: str | None,
    ) -> None:
        """Change organization INN."""

        self.inn = inn

    def change_kpp(
        self,
        kpp: str | None,
    ) -> None:
        """Change organization KPP."""

        self.kpp = kpp

    def change_ogrn(
        self,
        ogrn: str | None,
    ) -> None:
        """Change organization OGRN."""

        self.ogrn = ogrn

    def change_address(
        self,
        address: str | None,
    ) -> None:
        """Change organization address."""

        self.address = address

    def change_phone(
        self,
        phone: str | None,
    ) -> None:
        """Change organization phone."""

        self.phone = phone

    def change_email(
        self,
        email: str | None,
    ) -> None:
        """Change organization email."""

        self.email = email

    def change_website(
        self,
        website: str | None,
    ) -> None:
        """Change organization website."""

        self.website = website

    def change_comment(
        self,
        comment: str | None,
    ) -> None:
        """Change organization comment."""

        self.comment = comment
