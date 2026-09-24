# Secure Software Development Lifecycle Policy
Document ID: POL-ENG-040
Version: 3.0
Last Updated: 2026-03-31
Department: Engineering
Owner: VP of Engineering
Access Roles: employee, manager, hr, legal, admin

## 1. Code Review and Testing
All code changes need at least 1 peer review before merge. Automated unit tests must pass and code coverage for new code must be at least 80%.

## 2. Security Checks
Static analysis, dependency scanning and secret scanning run on every pull request. Builds with critical findings are blocked from release. Threat modelling is required for new systems that handle customer data.

## 3. Secrets and Releases
Secrets must be stored in the approved vault and never committed to code. Production releases are made only through the approved CI/CD pipeline.
