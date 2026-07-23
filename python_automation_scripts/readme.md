SecOps & Infrastructure Security Automation Library
A comprehensive collection of production-ready, zero-dependency Python automation scripts for security auditing, compliance enforcement, cloud governance, static binary analysis, and system hardening.

1. Kubernetes & Container Security
01_k8s_rbac_auditor.py

Audits Kubernetes Role-Based Access Control (RBAC) definitions for overly permissive cluster roles, such as wildcard resource access (*). It highlights administrative privileges assigned to service accounts to prevent privilege escalation risks.

02_k8s_pod_security_linter.py

Inspects Kubernetes Pod specification files for missing security contexts, privileged container execution, and root user defaults. It flags non-compliant configurations against the Kubernetes Pod Security Standards baseline.

03_k8s_network_policy_auditor.py

Scans cluster namespaces to identify pods lacking ingress or egress NetworkPolicy restrictions. It ensures default-deny boundaries are established to restrict unauthorized lateral movement within the cluster.

04_container_image_tag_validator.py

Parses deployment manifests to verify that container images use specific digest hashes or immutable release tags instead of latest. This prevents untracked image updates and potential supply chain vulnerabilities.

05_dockerfile_security_linter.py

Lints Dockerfile build instructions for root user execution, sensitive environment variable exposure, and unverified package downloads. It ensures container builds adhere to secure image construction standards.

2. Database & Data Store Governance
06_sql_connection_sanitizer.py

Scans application configuration files for hardcoded database connection strings containing plaintext credentials. It verifies that credentials are supplied via environment variables or external secret managers.

07_db_privilege_linter.py

Parses database grant scripts to flag accounts assigned excessive database permissions like SUPERUSER, DROP, or ALTER. It helps enforce the principle of least privilege across relational database schemas.

08_redis_security_config_auditor.py

Inspects Redis configuration parameters to verify that password authentication (requirepass) is active and dangerous commands like FLUSHALL are disabled. It prevents unauthorized in-memory data access and service disruption.

09_mongodb_auth_auditor.py

Audits MongoDB instance export metadata to ensure role-based access control and TLS transport encryption are enforced. It identifies unauthenticated endpoints or overly permissive database roles.

10_database_backup_encryption_verifier.py

Inspects database backup storage metadata to ensure export artifacts are encrypted at rest using approved algorithms. It flags unencrypted backup dumps before they are transferred to long-term storage.

3. Cloud Identity & Infrastructure Security
11_aws_mfa_compliance_auditor.py

Parses AWS IAM user credential reports to identify console-enabled accounts lacking Multi-Factor Authentication (MFA). It assists identity governance teams in enforcing mandatory MFA policies across IAM users.

12_tfstate_secret_detector.py

Scans local Terraform state files (.tfstate) for unencrypted sensitive values, API tokens, and passwords stored in plain text. It helps prevent accidental credential leakage in infrastructure state tracking.

13_s3_policy_linter.py

Audits AWS S3 bucket policy JSON manifests for public access statements ("Principal": "*") or missing HTTPS enforcement (aws:SecureTransport). It reduces the risk of accidental cloud storage bucket exposure.

14_gcp_iam_least_privilege_auditor.py

Evaluates Google Cloud IAM policy bindings to detect primitive roles like Owner or Editor assigned to service accounts. It recommends granular predefined or custom roles to limit service account impact.

15_azure_nsg_rule_linter.py

Inspects Azure Network Security Group (NSG) configuration files to detect inbound rules allowing unrestricted access (0.0.0.0/0) to sensitive management ports. It ensures remote administrative interfaces are restricted to trusted networks.

4. System Hardening & OS Governance
16_sshd_config_auditor.py

Evaluates OpenSSH server configurations (sshd_config) against security hardening baselines. It flags insecure directives such as enabled root login, password authentication, and weak SSH ciphers.

17_file_integrity_monitor.py

Generates and verifies SHA-256 baseline checksum manifests for critical system directories. It detects unauthorized file modifications, additions, or deletions across monitored operating system files.

18_sysctl_hardening_auditor.py

Compares running or file-based Linux kernel parameters (sysctl.conf) against security hardening baselines. It checks critical settings for IP forwarding, SYN flood protection, and Address Space Layout Randomization (ASLR).

19_pam_config_auditor.py

Audits Linux Pluggable Authentication Module (PAM) configuration files for mandatory security enforcement modules. It verifies that rules for password quality (pam_pwquality), account lockouts (pam_faillock), and password history are active.

20_apparmor_profile_auditor.py

Scans Linux AppArmor security profile directories to determine enforcement statuses across installed application profiles. It flags profiles left in permissive complain mode rather than active enforce mode.

21_suid_permissions_auditor.py

Recursively inspects system directories for binaries with SUID or SGID permission flags set. It compares discovered executables against an approved baseline to flag unexpected privilege escalation vectors.

22_cron_timer_integrity_auditor.py

Audits scheduled task locations (/etc/cron* and systemd timers) for insecure file permissions and unquoted execution paths. It prevents local privilege escalation through world-writable script dependencies.

23_auditd_rule_auditor.py

Inspects Linux Audit Daemon (auditd) rule files to verify logging coverage for sensitive file modifications and system call executions. It ensures alignment with organizational auditing and monitoring baselines.

24_sudoers_policy_linter.py

Parses /etc/sudoers files and drop-in configuration rules to detect generic NOPASSWD directives or wildcard command executions. It ensures administrative delegation adheres to strict command controls.

25_linux_user_group_auditor.py

Scans /etc/passwd and /etc/group files to detect unauthorized UID 0 accounts, missing passwords, or stale systemic users. It helps maintain clean local user identity inventories.

5. Threat Intelligence, Network & Peripheral Security
26_waf_log_inspector.py

Processes Web Application Firewall (WAF) JSON logs to aggregate client request volumes per IP address. It flags high-frequency source IPs exceeding configured threshold limits or triggering repeated block rules.

27_cert_revocation_auditor.py

Parses X.509 certificate metadata files to verify the presence and validity of Certificate Revocation List (CRL) endpoints and OCSP responders. It ensures PKI infrastructure supports active revocation checks.

28_pe_header_linter.py

Performs byte-level parsing of Windows Portable Executable (.exe, .dll) headers to check for essential compiler security mitigations. It verifies whether ASLR and DEP/NX flags are enabled on target binaries.

29_yara_rule_auditor.py

Audits YARA rule files (.yar) for syntax standards, mandatory metadata fields (author, description, severity), and unoptimized string patterns. It ensures detection engineering rules meet quality and performance baselines.

30_passive_dns_enum.py

Queries passive DNS data endpoints to aggregate historical DNS resolution records for a given root domain. It highlights subdomains and historical IP mappings to assist with external attack surface inventorying.

31_whois_expiration_monitor.py

Parses domain WHOIS metadata to calculate upcoming domain registration expiration dates. It flags domains within 30 days of expiration to prevent drop-registration risks or domain hijacking.

32_ip_reputation_checker.py

Evaluates IP address threat intelligence metadata against reputation score indicators and risk categories. It highlights high-risk addresses associated with malicious activity or unauthorized proxies.

33_usb_authorization_auditor.py

Inspects Linux USBGuard policy configurations to ensure mass storage and unverified peripheral classes are blocked. It prevents unauthorized USB data exfiltration or automated keystroke injection devices.

34_ble_security_linter.py

Parses Bluetooth Low Energy (BLE) scan metadata to flag unencrypted links, default device identities, or missing pairing authentication requirements across discovered peripheral devices.

35_dns_sec_validation_checker.py

Audits DNS zone metadata to confirm DNSSEC signing status and domain key validation chains. It ensures domain resolution configurations are protected against cache poisoning attacks.

6. Web Application & Middleware Security
36_csrf_token_config_verifier.py

Analyzes application framework middleware settings to confirm Anti-CSRF token generation and validation are globally active. It prevents missing CSRF protections on state-changing web endpoints.

37_flask_cookie_flag_inspector.py

Inspects Python Flask application configurations to verify that session cookies enforce HttpOnly, Secure, and SameSite flags. It protects web sessions against client-side script access and cross-site leaks.

38_graphql_depth_limit_auditor.py

Audits GraphQL schema configurations to ensure query depth and complexity limiting middleware are properly registered. It prevents resource exhaustion attacks caused by deeply nested GraphQL queries.

39_api_cors_policy_linter.py

Scans API gateway configuration manifests for dangerous Cross-Origin Resource Sharing (CORS) settings, such as reflecting arbitrary origin headers with credentials allowed. It ensures trusted domain boundaries are enforced.

40_security_headers_linter.py

Analyzes web application server response header configurations to ensure Content-Security-Policy, X-Frame-Options, and Strict-Transport-Security headers are deployed. It ensures protection against client-side injection vectors.

41_jwt_config_auditor.py

Examines JSON Web Token (JWT) validation settings to ensure the none algorithm is explicitly rejected and strong signature algorithms (like RS256 or HS256) are mandated. It prevents token signature bypass vulnerabilities.

42_rate_limit_middleware_linter.py

Verifies that web application route definitions incorporate rate-limiting middleware on sensitive endpoints like login and password reset routes. It helps mitigate brute-force and credential-stuffing risks.

43_openapi_spec_security_auditor.py

Parses OpenAPI / Swagger specification files to ensure every operational endpoint defines explicit authentication schemes and parameter input schemas. It flags unauthenticated or loosely defined API routes.

44_file_upload_policy_verifier.py

Audits file upload handling logic configurations to ensure MIME-type validation, file extension whitelisting, and execution permission restrictions are enforced on upload target directories.

45_xml_parser_xxe_linter.py

Inspects application source files or configuration manifests to verify that external entity resolution (XXE) is explicitly disabled in XML parsers. It prevents file disclosure through malicious XML payloads.

7. Logging, Auditing & SIEM Pipeline
46_syslog_format_normalizer.py

Parses raw, unstructured Syslog records and converts them into normalized JSON structures following Common Event Format (CEF) standards. It ensures log consistency across centralized log aggregators.

47_elastic_index_policy_auditor.py

Audits Elasticsearch/OpenSearch Index Lifecycle Management (ILM) policies to verify retention periods, snapshot schedules, and cold storage transition phases. It ensures compliance with log retention requirements.

48_log_pii_masking_verifier.py

Inspects application log sample outputs for unmasked Personally Identifiable Information (PII), such as credit card numbers or government IDs. It confirms log scrubbing rules function correctly.

49_cef_log_syntax_validator.py

Validates security event messages against the Common Event Format (CEF) specification to check key-value pair formatting and header completeness. It prevents parsing failures in SIEM ingestion pipelines.

50_cloudtrail_event_anomaly_detector.py

Analyzes AWS CloudTrail log exports to identify suspicious administrative actions, such as disabled logging, modified IAM policies, or unusual geographic logins. It helps detect operational security anomalies.

51_fluentd_pipeline_linter.py

Audits Fluentd log shipper configuration files to ensure secure transport encryption (TLS) and mutual authentication are configured between log agents and central collectors.

52_logstash_filter_auditor.py

Parses Logstash pipeline configurations to check for unhandled parsing errors or missing fallback drop rules. It ensures invalid log formats do not crash downstream ingestion nodes.

53_audit_log_tamper_checker.py

Verifies cryptographic hash chains on append-only audit log files to detect offline modifications or deleted event entries. It ensures log chain-of-custody integrity.

54_siem_detection_rule_linter.py

Audits SIEM correlation rule definitions for missing execution schedules, broad match thresholds, or undefined severity tags. It improves detection quality and minimizes false-positive alerts.

55_vector_shipper_config_auditor.py

Inspects Vector log agent configuration files to verify memory buffer limits, end-to-end TLS encryption, and secure sink destinations. It ensures reliable log delivery under high traffic.

8. Network Infrastructure & Cryptography
56_tls_cipher_suite_auditor.py

Parses web server SSL/TLS configuration blocks to verify that legacy protocol versions (SSLv3, TLS 1.0, TLS 1.1) and weak ciphers (RC4, 3DES) are disabled in favor of modern TLS 1.2+ suites.

57_ssh_known_hosts_scrubber.py

Scans SSH known_hosts files to verify host key hash representations and remove stale or unreachable host entries. It prevents host spoofing risks during automated remote administrative connections.

58_dhcp_snooping_config_linter.py

Audits network switch configuration files to verify that DHCP Snooping and Option 82 insertion are enabled on untrusted access ports. It guards against rogue DHCP server rogue assignments.

59_arp_spoof_detection_auditor.py

Inspects dynamic ARP inspection (DAI) switch settings against trusted IP-MAC binding databases. It ensures network hardware is configured to block ARP cache poisoning attacks on local segments.

60_bgp_route_leak_verifier.py

Evaluates Border Gateway Protocol (BGP) router peering configurations to confirm key route filtering policies and RPKI origin validation are active. It mitigates accidental BGP route leaks and hijacks.

61_openvpn_config_hardener.py

Audits OpenVPN client and server configuration profiles (.ovpn) for secure cipher selection (AES-GCM), strong digest algorithms, and active TLS authentication controls (tls-auth/tls-crypt).

62_ipsec_proposal_auditor.py

Parses IPsec VPN configuration files to verify that IKE Phase 1 and Phase 2 proposals enforce Diffie-Hellman groups 14+ and strong encryption suites. It ensures secure site-to-site tunnels.

63_snmp_community_string_checker.py

Scans network management configuration files for default or public SNMP community strings (public, private). It recommends updating to SNMPv3 with USM user authentication and encryption.

64_radius_tacacs_config_linter.py

Audits AAA server integration files to verify shared secret strength and TLS/IPsec encapsulation on AAA management traffic. It prevents administrative credential interception on management networks.

65_macsec_policy_verifier.py

Inspects Layer 2 network interface configurations to confirm MACsec (802.1AE) point-to-point encryption is enforced on inter-switch link interfaces. It protects local link traffic from sniffing.

9. Vulnerability Management & Patching
66_cve_feed_parser.py

Parses vulnerability data feeds (JSON/XML) to extract high-severity vulnerabilities affecting target software components. It categorizes disclosures based on CVSS scores to prioritize patching.

67_package_lock_security_auditor.py

Analyzes application package lock files (package-lock.json, poetry.lock) to verify dependency provenance and identify known vulnerable library versions.

68_unattended_upgrades_auditor.py

Inspects Linux system auto-update configuration files to verify that automatic security patches are enabled and configured to apply without manual intervention.

69_osv_vulnerability_checker.py

Queries Open Source Vulnerability (OSV) dataset exports to correlate installed open-source library versions against disclosed vulnerability databases.

70_kernel_patch_level_verifier.py

Compares running kernel version metadata against vendor security patch release streams to highlight missing security updates or reboot requirements.

71_sbom_spdx_validator.py

Parses Software Bill of Materials (SBOM) files in SPDX format to confirm structural validity and complete component metadata attestation.

72_cyclonedx_license_auditor.py

Inspects CycloneDX SBOM documents to verify component license declarations and flag unapproved open-source software licenses.

73_container_base_image_auditor.py

Analyzes base image declarations across Dockerfiles to ensure builds originate from minimal, vendor-supported minimal distribution baselines (e.g., Distroless, Alpine).

74_patch_compliance_reporter.py

Aggregates system patch assessment logs across target host inventories to compute overall patch compliance metrics and identify overdue system updates.

75_exploit_db_cve_cross_checker.py

Cross-references internal vulnerability assessment findings with public exploit availability metadata to highlight vulnerabilities with public exploit code.

10. Identity, Access & PKI Management
76_active_directory_priv_auditor.py

Parses Active Directory object metadata exports to identify users assigned to high-privilege groups (e.g., Domain Admins, Enterprise Admins) and highlights inactive privileged accounts.

77_pki_ca_chain_validator.py

Verifies internal PKI X.509 certificate chains to confirm root and intermediate CA certificate authority flags, path length constraints, and signature validity.

78_kerberos_ticket_policy_checker.py

Audits Active Directory Kerberos policy settings to ensure maximum ticket lifetimes and renewal windows conform to domain security baselines.

79_ldap_tls_enforcement_verifier.py

Inspects LDAP directory server configurations to confirm unauthenticated simple binds are disabled and startTLS / LDAPS transport security is required.

80_saml_metadata_security_linter.py

Parses SAML 2.0 Identity Provider (IdP) metadata XML files to verify assertion signing, response encryption certificates, and secure binding endpoints.

81_oauth2_redirect_uri_validator.py

Audits OAuth 2.0 client registration metadata to flag wildcard redirect URIs or non-HTTPS callback endpoints. It guards against authorization code interception attacks.

82_ssh_ca_key_auditor.py

Inspects SSH Certificate Authority configuration files and signed user certificates to verify validity periods, restricted principal mapping, and command options.

83_vault_policy_least_privilege_linter.py

Audits HashiCorp Vault HCL policy definitions to detect wildcard path grants (path "secret/*") and overly permissive capabilities like sudo or write.

84_api_key_rotation_monitor.py

Parses service account key metadata exports to calculate API key age, flagging keys older than the mandatory rotation threshold (e.g., 90 days).

85_gpg_keyring_expiration_auditor.py

Scans GPG keyrings to audit key usage flags, key lengths, and subkey expiration dates, highlighting expired or weak signing keys.

11. Code Security & Static Analysis
86_ast_secret_scanner.py

Parses Python source code into Abstract Syntax Trees (AST) to identify hardcoded string assignment variables matching high-entropy secret patterns.

87_eval_injection_linter.py

Scans source code for dynamic execution functions (e.g., eval(), exec()) passed unvalidated input, flagging potential arbitrary code execution risks.

88_bandit_config_customizer.py

Audits Python static analysis configuration files to ensure high-severity security rules are active and unnecessary rule suppressions are removed.

89_git_pre_commit_secret_linter.py

A lightweight pre-commit hook script that inspects staged file diffs for private keys, API tokens, and credentials prior to local Git commits.

90_command_injection_ast_verifier.py

Uses AST traversal to detect system shell invocation calls (e.g., subprocess.Popen(..., shell=True)) accepting concatenated user strings.

91_unsafe_deserialization_scanner.py

Inspects application source files for unsafe object deserialization calls (e.g., pickle.loads(), yaml.unsafe_load()) handling untrusted data.

92_sql_concatenation_detector.py

Scans codebase files for raw SQL query strings constructed using string formatting or concatenation rather than parameterized queries.

93_path_traversal_linter.py

Analyzes file system access calls to verify user-supplied path inputs are sanitized using path resolution and containment checks before execution.

94_crypto_algorithm_auditor.py

Inspects application source code to flag outdated cryptographic algorithms (MD5, SHA1, DES) in favor of modern standards (AES-GCM, SHA-256).

95_regex_dos_pattern_checker.py

Audits application regular expressions for catastrophic backtracking patterns (ReDoS) that could cause high CPU utilization under crafted inputs.

12. Security Operations & Automation
96_threat_feed_deduplicator.py

Ingests threat intelligence indicator feeds (IPs, domain names, hashes), removing duplicate entries and merging overlapping indicator records.

97_incident_ticket_severity_calculator.py

Calculates standardized incident severity scores based on impact vectors, asset criticality values, and data exposure levels to prioritize response workflows.

98_quarantine_file_hasher.py

Processes isolated suspect files to generate cryptographic hashes (MD5, SHA1, SHA256) and extract metadata attributes for analyst review.

99_forensic_timeline_builder.py

Aggregates system timestamps across log files, filesystem modification records, and event entries to construct unified forensic investigation timelines.

100_soc_alert_threshold_optimizer.py

Analyzes historical alert volume statistics to identify noisy alert rules and recommend optimized trigger thresholds to reduce analyst fatigue.
