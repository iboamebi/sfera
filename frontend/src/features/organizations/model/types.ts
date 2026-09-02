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

export interface CreateOrganizationForm {
  name: string;
  shortName?: string;
  inn?: string;
  kpp?: string;
  ogrn?: string;
  address?: string;
  phone?: string;
  email?: string;
  website?: string;
  comment?: string;
}
