-- add global fields to company
ALTER TABLE company
  ADD COLUMN IF NOT EXISTS currency varchar DEFAULT 'USD',
  ADD COLUMN IF NOT EXISTS timezone varchar DEFAULT 'UTC',
  ADD COLUMN IF NOT EXISTS locale varchar DEFAULT 'en_US',
  ADD COLUMN IF NOT EXISTS tax_id varchar,
  ADD COLUMN IF NOT EXISTS tax_id_type varchar,
  ADD COLUMN IF NOT EXISTS data_region varchar;

-- einvoice provider and log (if not present)
CREATE TABLE IF NOT EXISTS einvoice_provider (
  id serial PRIMARY KEY,
  name varchar NOT NULL,
  country varchar NOT NULL,
  priority integer NOT NULL DEFAULT 100,
  config jsonb,
  encrypted_credentials_ref varchar,
  enabled boolean DEFAULT true,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS einvoice_log (
  id serial PRIMARY KEY,
  invoice_id integer,
  provider_id integer,
  company_id integer,
  request_payload jsonb,
  response_payload jsonb,
  status varchar,
  created_at timestamptz DEFAULT now()
);
