CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE transaction_status AS ENUM (
  'pending',
  'completed',
  'failed',
  'refund_failed'
);

CREATE TABLE transactions (
  transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sender_id UUID NOT NULL,
  receiver_id UUID NOT NULL,
  amount NUMERIC(18,2) NOT NULL,
  status transaction_status NOT NULL DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP

  CHECK (sender_id <> receiver_id)
);