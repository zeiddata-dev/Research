███████╗███████╗██╗██████╗     ██████╗  █████╗ ████████╗ █████╗ 
╚══███╔╝██╔════╝██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
  ███╔╝ █████╗  ██║██║  ██║    ██║  ██║███████║   ██║   ███████║
 ███╔╝  ██╔══╝  ██║██║  ██║    ██║  ██║██╔══██║   ██║   ██╔══██║
███████╗███████╗██║██████╔╝    ██████╔╝██║  ██║   ██║   ██║  ██║
╚══════╝╚══════╝╚═╝╚═════╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝

**Zeid Data Research - Copper hang back...**

# Port Scanner

*This Python script performs a simple TCP port scan on a given host and ports.*

## Usage
```
The program takes two command line arguments:
```

- -H, --host: specify target host
- -p, --ports: specify target ports separated by commas (,)

*The -H option is used to specify the target host to scan and the -p option is used to specify the target ports separated by a comma.*

## Example
To scan port 80 on example.com, run the following command:
```
python port_scanner.py -H example.com -p 80
```
To scan ports 80, 443, and 8080 on example.com, run the following command:
```
python port_scanner.py -H example.com -p 80,443,8080

#####################################################################################################################

# ZD_SSH Brute Force (Internal SSH Credential Audit Tool)

*ZD_SSH Brute Force is an **internal security audit utility** used to assess SSH authentication posture within an approved scope. It helps security teams identify weak, default, or reused credentials on systems **owned by the organization** and **explicitly authorized** for testing.*

## Intended Use

* Internal credential hygiene checks (approved targets only)
* Validation of SSH hardening controls and authentication policy enforcement
* Support for compliance evidence (periodic access control testing)

## Authorization & Legal Notice

This tool must only be used:

* On systems your organization owns/operates, **and**
* With explicit written authorization and a defined audit scope

Unauthorized access attempts against systems you do not control may be illegal and harmful.

## Operational Safety

To reduce service impact and avoid unintended lockouts:

* Run only during approved audit/maintenance windows
* Follow internal rate-limiting and escalation procedures
* Ensure monitoring is enabled (SIEM/logging) for audit traceability
* Document scope, start/end times, and results for audit records

## Requirements

* Python 3.x
* Dependencies: `paramiko` (and any other packages listed in your requirements)

## Installation (Internal)

* Clone this repository to your audit workstation
* Install dependencies per your organization’s standard Python workflow (virtualenv recommended)

## Reporting & Evidence

Typical audit outputs may include:

* Target host identifier(s)
* Timestamped audit run metadata
* Attempt counts and high-level outcome status (per your internal evidence requirements)

> Tip: Store results in a controlled location and treat any sensitive output as confidential security data.

## Defensive Recommendations (If Findings Occur)

If weak credentials are detected, consider:

* Enforcing key-based SSH authentication and disabling password auth where possible
* Enabling MFA (where supported)
* Lockout / throttling controls and tools like fail2ban
* Centralized logging + alerting on authentication anomalies

## Contributing

Contributions are welcome via issues and pull requests. Please include:

* What changed and why
* Testing notes
* Operational or security considerations

## Code of Conduct

Please review the Code of Conduct before contributing.

## License

This project is licensed under the MIT License.

---


