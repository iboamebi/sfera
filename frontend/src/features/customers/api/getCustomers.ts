import { http } from "../../../shared/api/http";
import type { CustomerRead } from "../model/types";
import { mapCustomer } from "./customerMapper";
import type { CustomerApiDto } from "./types";

export async function getCustomers(): Promise<CustomerRead[]> {
  const response = await http.get<CustomerApiDto[]>("/customers/");

  return response.data.map(mapCustomer);
}
