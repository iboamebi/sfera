import { useQuery } from "@tanstack/react-query";

import { getUsers } from "../api/userAdministration";

export function useUsers(includeArchived: boolean) {
  return useQuery({
    queryKey: ["users", { includeArchived }],
    queryFn: () => getUsers(includeArchived),
  });
}
