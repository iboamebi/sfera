import { http } from "../../../shared/api/http";
import { mapCustomer } from "./customerMapper";
import type { CustomerApiDto } from "./types";
import type { CreateCustomerForm } from "../model/types";
import type { CustomerRead } from "../model/types";

export async function createCustomer(
  data: CreateCustomerForm,
): Promise<CustomerRead> {
  const response = await http.post<CustomerApiDto>("/customers/", {
    organization_id: data.organizationId,
    name: data.name,
    contact_person: data.contactPerson?.trim() || null,
    phone: data.phone?.trim() || null,
    email: data.email?.trim() || null,
    comment: data.comment?.trim() || null,
    discount_percent: data.discountPercent,
  });

  return mapCustomer(response.data);
}
