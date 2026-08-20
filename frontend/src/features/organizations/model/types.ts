export interface OrganizationRead {
  id: string;
  name: string;
  shortName: string | null;
  inn: string | null;
  kpp: string | null;
  ogrn: string | null;
  address: string | null;
  phone: string | null;
  email: string | null;
  website: string | null;
  comment: string | null;
}
