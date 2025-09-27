# OpenNSPM

OpenNSPM is an open-source Network Security Policy Management platform focused on Fortinet devices. It normalizes configuration data, evaluates firewall rule hygiene, and provides reports across snapshots.

## Key Features

- Snapshot collection from FortiGate REST API or offline configuration exports.
- Vendor-agnostic data model for devices, address objects, services, and policies.
- Hygiene checks for any-any and disabled policies (with stubs for advanced analysis).
- HTML report exports and REST API for automation.
- Containerized deployment with PostgreSQL and Redis.
