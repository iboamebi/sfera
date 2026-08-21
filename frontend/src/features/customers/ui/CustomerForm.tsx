import { useOrganizations } from "../../organizations/model/useOrganizations";
import type { CreateCustomerForm } from "../model/types";

interface CustomerFormProps {
  value: CreateCustomerForm;
  onChange: (value: CreateCustomerForm) => void;
  onSubmit: () => void;
  disabled?: boolean;
}

export function CustomerForm({
  value,
  onChange,
  onSubmit,
  disabled = false,
}: CustomerFormProps) {
  const organizations = useOrganizations();

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      <label>
        Organization
        <select
          value={value.organizationId}
          onChange={(event) =>
            onChange({ ...value, organizationId: event.target.value })
          }
          disabled={disabled || organizations.isLoading}
          required
        >
          <option value="">Select organization</option>
          {organizations.data?.map((organization) => (
            <option key={organization.id} value={organization.id}>
              {organization.name}
            </option>
          ))}
        </select>
      </label>

      {organizations.isSuccess && organizations.data.length === 0 && (
        <p>
          No organizations available. Create an organization before saving a
          customer.
        </p>
      )}

      <label>
        Name
        <input
          value={value.name}
          onChange={(event) => onChange({ ...value, name: event.target.value })}
          disabled={disabled}
          required
        />
      </label>

      <label>
        Contact person
        <input
          value={value.contactPerson ?? ""}
          onChange={(event) =>
            onChange({ ...value, contactPerson: event.target.value })
          }
          disabled={disabled}
        />
      </label>

      <label>
        Phone
        <input
          value={value.phone ?? ""}
          onChange={(event) => onChange({ ...value, phone: event.target.value })}
          disabled={disabled}
        />
      </label>

      <label>
        Email
        <input
          type="email"
          value={value.email ?? ""}
          onChange={(event) => onChange({ ...value, email: event.target.value })}
          disabled={disabled}
        />
      </label>

      <label>
        Comment
        <textarea
          value={value.comment ?? ""}
          onChange={(event) => onChange({ ...value, comment: event.target.value })}
          disabled={disabled}
        />
      </label>

      <label>
        Discount percent
        <input
          type="number"
          min="0"
          value={value.discountPercent ?? 0}
          onChange={(event) =>
            onChange({
              ...value,
              discountPercent: Number(event.target.value),
            })
          }
          disabled={disabled}
        />
      </label>

      <button type="submit" disabled={disabled || !value.organizationId}>
        Create customer
      </button>
    </form>
  );
}
