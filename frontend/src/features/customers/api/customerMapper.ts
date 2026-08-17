import type { CustomerRead } from "../model/types";
import type { CustomerApiDto } from "./types";

export function mapCustomer(dto: CustomerApiDto): CustomerRead {
  return {
    id: dto.id,
    organizationId: dto.organization_id,
    name: dto.name,
    contactPerson: dto.contact_person,
    phone: dto.phone,
    email: dto.email,
    comment: dto.comment,
    discountPercent: dto.discount_percent,
    archived: dto.archived,
  };
}
