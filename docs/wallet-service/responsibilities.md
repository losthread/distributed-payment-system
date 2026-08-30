# Wallet Service Responsibilities

## Overview

The Wallet Service manages user wallets and balances.
It is responsible for creating wallets, handling deposits and withdrawals,
and providing internal wallet operations for other microservices.

## Responsibilities

### Wallet Management

- Create wallets for new users (triggered by `user.created` event)
- Initialize wallet balance to 0.00
- Fetch authenticated user wallet
- Store wallet data in PostgreSQL

### Balance Operations

- Deposit money into user wallets
- Withdraw money from user wallets
- Validate sufficient balance before debiting
- Update wallet balances atomically

### Internal Wallet Operations

- Provide internal API endpoints protected by internal service token
- Credit money to specific user wallets (used by Transaction Service)
- Debit money from specific user wallets (used by Transaction Service)
- Return updated wallet information after operations

### Authentication & Authorization

- Validate JWT tokens for user endpoints
- Verify internal service tokens for internal endpoints
- Extract user_id from authenticated tokens

### Event Processing

- Consume `user.created` events from Kafka to create wallets
- Consume `refund.requested` events from Kafka to process refunds
- Credit sender wallet on refund
- Publish `refund.completed` or `refund.failed` events back to Kafka

### Kafka Integration

- Subscribe to `user-events` and `refund-events` topics
- Produce to `transaction-events` topic for refund completion/failure
- Retry refund events up to 3 times on failure
