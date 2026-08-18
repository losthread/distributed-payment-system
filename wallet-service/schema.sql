CREATE TABLE wallets (
  id SERIAL PRIMARY KEY,
  user_id UUID NOT NULL,
  balance NUMERIC(18,2) NOT NULL DEFAULT 0.00,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  CONSTRAINT unique_user_currency UNIQUE(user_id, currency)
);