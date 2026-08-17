export interface CustomerApiDto {
  id: string;
  organization_id: string;
  name: string;
  contact_person: string | null;
  phone: string | null;
  email: string | null;
  comment: string | null;
  discount_percent: number;
  archived: boolean;
}
