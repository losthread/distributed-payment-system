# Auth Service Responsibilities

## Overview

The Auth Service manages user identity, authentication, and authorization.
It is responsible for verifying users and issuing identity tokens consumed by
other microservices.

## Responsibilities

### User Registration

- Create new user accounts
- Validate registration data
- Hash passwords securely using Argon2
- Store user credentials in PostgreSQL

### User Authentication

- Authenticate users using:
  - Email and password
  - Username and password
  - Google OAuth

- Verify credentials
- Generate JWT access tokens

### Token Management

- Create JWT tokens
- Validate user identity through tokens
- Provide authenticated user context to other services

### User Profile Management

- Fetch user profile
- Update user profile information
- Delete user accounts

### OAuth Integration

- Verify Google ID tokens
- Create accounts for first-time Google users
- Authenticate returning Google users
