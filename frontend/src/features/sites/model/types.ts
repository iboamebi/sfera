export interface SiteRead {
  id: string;
  customerId: string;
  name: string;
  address: string;
  archived: boolean;
}

export interface CreateSiteForm {
  name: string;
  address: string;
}
