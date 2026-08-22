# Security Notes
- Never put Jenkins tokens, GitHub tokens, cloud keys, or private certificates in the package.
- Use environment variables or your approved secret manager.
- Prefer OIDC/federated cloud authentication over long-lived cloud credentials.
- Generated workflows default to `contents: read`; add only the permissions actually required.
- Pin third-party actions according to your organization's action-governance policy.
- Keep TLS verification enabled. If an internal CA is required, install/trust the CA rather than disabling verification.
