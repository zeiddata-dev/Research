███████╗███████╗██╗██████╗     ██████╗  █████╗ ████████╗ █████╗
╚══███╔╝██╔════╝██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
  ███╔╝ █████╗  ██║██║  ██║    ██║  ██║███████║   ██║   ███████║
 ███╔╝  ██╔══╝  ██║██║  ██║    ██║  ██║██╔══██║   ██║   ██╔══██║
███████╗███████╗██║██████╔╝    ██████╔╝██║  ██║   ██║   ██║  ██║

# Zeid Data - Copper Hang Back...
# Security Policy — Zeid Data AIGO

## Reporting a vulnerability
If you discover a security issue, please report it privately.

- Provide a description of the issue
- Steps to reproduce
- Impact assessment
- Any suggested fix

## Data handling / privacy
AIGO is designed to be **evidence-first** while supporting privacy constraints:
- Baseline policy hashes prompts/responses instead of storing raw content.
- If you enable raw content storage, ensure you have a data classification/retention policy.

## Supply chain
AIGO is stdlib-only (no runtime dependencies by default). If you add dependencies, pin versions and consider SBOM generation.
