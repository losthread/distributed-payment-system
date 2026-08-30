# **Transaction Service Responsibilities**

## **Overview**

The Transaction Service manages money transfers between users.
It coordinates wallet operations and maintains the transaction lifecycle
from creation to completion or failure.

## **Responsibilities**

### **Transaction Creation**

- Create pending transactions
- Validate transaction requests
- Identify the authenticated sender
- Store transaction details in PostgreSQL

### **Money Transfer**

- Debit money from the sender's wallet
- Credit money to the receiver's wallet
- Mark transactions as completed after successful transfer
- Handle failures during the transfer process

### **Transaction Failure Handling**

- Mark transactions as failed when the debit operation fails
- Attempt to refund the sender when receiver credit fails
- Publish Kafka refund events if the refund operation fails

### **Transaction History**

- Fetch all transactions involving an authenticated user
- Fetch individual transaction details
- Ensure users can only access their own transactions

### **Transaction State Management**

- Track transaction status
- Update transaction timestamps
- Maintain transaction states such as:
  - pending
  - completed
  - failed
  - refund_failed
  