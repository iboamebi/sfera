import { http } from "../../../shared/api/http";
import type { CreateCustomerForm, CustomerRead } from "../model/types";
import { mapCustomer } from "./customerMapper";
import type { CustomerApiDto } from "./types";

export async function updateCustomer(
  customerId: string,
  data: CreateCustomerForm,
): Promise<CustomerRead> {
  const response = await http.patch<CustomerApiDto>(
    `/customers/${customerId}`,
    {
      name: data.name,
      contact_person: data.contactPerson?.trim() || null,
      phone: data.phone?.trim() || null,
      email: data.email?.trim() || null,
      comment: data.comment?.trim() || null,
      discount_percent: data.discountPercent,
    },
  );

  return mapCustomer(response.data);
}
