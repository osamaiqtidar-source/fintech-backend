CREATE TABLE IF NOT EXISTS companies (
  id SERIAL PRIMARY KEY,
  name TEXT,
  tally_identifier TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  company_id INT,
  email TEXT,
  password_hash TEXT,
  roles TEXT,
  subscription_plan TEXT DEFAULT 'basic',
  is_admin BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sync_operations (
  id BIGSERIAL PRIMARY KEY,
  company_id INT NOT NULL,
  source TEXT NOT NULL,
  operation_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  idempotency_key TEXT,
  status TEXT DEFAULT 'pending',
  attempts INT DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  processed_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS subscriptions (
  id SERIAL PRIMARY KEY,
  company_id INT,
  plan_type TEXT,
  status TEXT DEFAULT 'active',
  start_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
  end_date TIMESTAMP WITH TIME ZONE,
  price numeric(10,2),
  created_by_admin BOOLEAN DEFAULT false,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS subscription_reminders (
  id SERIAL PRIMARY KEY,
  subscription_id INT,
  sent_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  method TEXT,
  status TEXT,
  message TEXT
);

CREATE TABLE IF NOT EXISTS app_update (
  id SERIAL PRIMARY KEY,
  company_id INT,
  version TEXT,
  notes TEXT,
  payload JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
