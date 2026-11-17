export type KeyCount = { key: string; count: number };

export type EntityStatusCounts = {
  active_count: number;
  total_count: number;
  by_status: KeyCount[];
};

export type VerificationCounts = EntityStatusCounts & {
  by_result: KeyCount[];
};

export type ControlPanelOverview = {
  orders: EntityStatusCounts;
  verifications: VerificationCounts;
  customers: { active_count: number; archived_count: number };
  instruments: EntityStatusCounts;
};
