import { http } from "../../../shared/api/http";
import type { CustomerRead } from "../model/types";
import { mapCustomer } from "./customerMapper";
import type { CustomerApiDto } from "./types";

export async function getCustomer(customerId: string): Promise<CustomerRead> {
  const response = await http.get<CustomerApiDto>(`/customers/${customerId}`);

  return mapCustomer(response.data);
}
