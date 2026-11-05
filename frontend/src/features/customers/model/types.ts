export interface CustomerRead {
  id: string;
  name: string;
  contactPerson: string | null;
  phone: string | null;
  email: string | null;
  comment: string | null;
  discountPercent: number;
  archived: boolean;
}

export interface CreateCustomerForm {
  name: string;
  contactPerson?: string;
  phone?: string;
  email?: string;
  comment?: string;
  discountPercent: number;
}
