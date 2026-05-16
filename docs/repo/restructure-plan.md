# Zeid Data Research Repository Restructure Plan

Generated plan only. No files were moved.

## Summary

- Tracked files reviewed: `525`
- Planned moves: `509`
- Files kept in place: `16`

## Proposed top-level structure

```text
assets/
content/vendors/
detections/
docs/
projects/
research/
templates/
tools/
workbooks/
```

## Move groups

### `assets/banners/`

- `assets/banners/readme/content.svg` -> `assets/banners/readme/content.svg`
- `assets/banners/readme/content_cisco.svg` -> `assets/banners/readme/content_cisco.svg`
- `assets/banners/readme/content_crowdstrike.svg` -> `assets/banners/readme/content_crowdstrike.svg`
- `assets/banners/readme/content_crowdstrike_crowdstrike_falcon_ai_governance.svg` -> `assets/banners/readme/content_crowdstrike_crowdstrike_falcon_ai_governance.svg`
- `assets/banners/readme/content_crowdstrike_crowdstrike_falcon_audit_evidence_noise_reduction.svg` -> `assets/banners/readme/content_crowdstrike_crowdstrike_falcon_audit_evidence_noise_reduction.svg`
- `assets/banners/readme/content_crowdstrike_crowdstrike_falcon_claude_bot_detection.svg` -> `assets/banners/readme/content_crowdstrike_crowdstrike_falcon_claude_bot_detection.svg`
- `assets/banners/readme/content_island.svg` -> `assets/banners/readme/content_island.svg`
- `assets/banners/readme/content_island_zeid_data_elk_stack_connector.svg` -> `assets/banners/readme/content_island_zeid_data_elk_stack_connector.svg`
- `assets/banners/readme/content_island_zeid_data_evidence_bundle.svg` -> `assets/banners/readme/content_island_zeid_data_evidence_bundle.svg`
- `assets/banners/readme/content_sentinelone.svg` -> `assets/banners/readme/content_sentinelone.svg`
- `assets/banners/readme/content_sentinelone_soc2_content.svg` -> `assets/banners/readme/content_sentinelone_soc2_content.svg`
- `assets/banners/readme/content_snowflake.svg` -> `assets/banners/readme/content_snowflake.svg`
- `assets/banners/readme/content_splunk.svg` -> `assets/banners/readme/content_splunk.svg`
- `assets/banners/readme/content_splunk_zeid_data_claude_bot_content.svg` -> `assets/banners/readme/content_splunk_zeid_data_claude_bot_content.svg`
- `assets/banners/readme/content_splunk_zeid_data_splunk_app_exfil_watch.svg` -> `assets/banners/readme/content_splunk_zeid_data_splunk_app_exfil_watch.svg`
- `assets/banners/readme/detections.svg` -> `assets/banners/readme/detections.svg`
- `assets/banners/readme/detections_claude_bot.svg` -> `assets/banners/readme/detections_claude_bot.svg`
- `assets/banners/readme/detections_cve_2025_20393.svg` -> `assets/banners/readme/detections_cve_2025_20393.svg`
- `assets/banners/readme/detections_cve_2025_40551.svg` -> `assets/banners/readme/detections_cve_2025_40551.svg`
- `assets/banners/readme/detections_cve_2026_24423.svg` -> `assets/banners/readme/detections_cve_2026_24423.svg`
- `assets/banners/readme/detections_cve_2026_24858.svg` -> `assets/banners/readme/detections_cve_2026_24858.svg`
- `assets/banners/readme/malware.svg` -> `assets/banners/readme/malware.svg`
- `assets/banners/readme/malware_claude.svg` -> `assets/banners/readme/malware_claude.svg`
- `assets/banners/readme/malware_promptflux_fruitshell.svg` -> `assets/banners/readme/malware_promptflux_fruitshell.svg`
- `assets/banners/readme/media.svg` -> `assets/banners/readme/media.svg`
- `assets/banners/readme/projects_zeid_data_ai_guard.svg` -> `assets/banners/readme/projects_zeid_data_ai_guard.svg`
- `assets/banners/readme/projects_zeid_data_bruteforce_ssh.svg` -> `assets/banners/readme/projects_zeid_data_bruteforce_ssh.svg`
- `assets/banners/readme/projects_zeid_data_cloak_check.svg` -> `assets/banners/readme/projects_zeid_data_cloak_check.svg`
- `assets/banners/readme/projects_zeid_data_forensics_tools.svg` -> `assets/banners/readme/projects_zeid_data_forensics_tools.svg`
- `assets/banners/readme/projects_zeid_data_forensics_tools_zeid_data_dfir_work_flow_trainer.svg` -> `assets/banners/readme/projects_zeid_data_forensics_tools_zeid_data_dfir_work_flow_trainer.svg`
- `assets/banners/readme/projects_zeid_data_gap_check.svg` -> `assets/banners/readme/projects_zeid_data_gap_check.svg`
- `assets/banners/readme/projects_zeid_data_net_ledger.svg` -> `assets/banners/readme/projects_zeid_data_net_ledger.svg`
- `assets/banners/readme/projects_zeid_data_nist_gen_ai_evidence_pack.svg` -> `assets/banners/readme/projects_zeid_data_nist_gen_ai_evidence_pack.svg`
- `assets/banners/readme/projects_zeid_data_qilin_ransomware_detection.svg` -> `assets/banners/readme/projects_zeid_data_qilin_ransomware_detection.svg`
- `assets/banners/readme/projects_zeid_data_regex_security.svg` -> `assets/banners/readme/projects_zeid_data_regex_security.svg`
- `assets/banners/readme/projects_zeid_data_stack_crasher.svg` -> `assets/banners/readme/projects_zeid_data_stack_crasher.svg`
- `assets/banners/readme/scripts.svg` -> `assets/banners/readme/scripts.svg`
- `assets/banners/readme/scripts_automation.svg` -> `assets/banners/readme/scripts_automation.svg`
- `assets/banners/readme/scripts_automation_zeid_data_backup_verify.svg` -> `assets/banners/readme/scripts_automation_zeid_data_backup_verify.svg`
- `assets/banners/readme/scripts_automation_zeid_data_dns_audit.svg` -> `assets/banners/readme/scripts_automation_zeid_data_dns_audit.svg`
- `assets/banners/readme/scripts_automation_zeid_data_eventlog_export.svg` -> `assets/banners/readme/scripts_automation_zeid_data_eventlog_export.svg`
- `assets/banners/readme/scripts_automation_zeid_data_host_reachability.svg` -> `assets/banners/readme/scripts_automation_zeid_data_host_reachability.svg`
- `assets/banners/readme/scripts_automation_zeid_data_local_admin_audit.svg` -> `assets/banners/readme/scripts_automation_zeid_data_local_admin_audit.svg`
- `assets/banners/readme/scripts_automation_zeid_data_log_summarizer_cpp.svg` -> `assets/banners/readme/scripts_automation_zeid_data_log_summarizer_cpp.svg`
- `assets/banners/readme/scripts_automation_zeid_data_route_snapshot.svg` -> `assets/banners/readme/scripts_automation_zeid_data_route_snapshot.svg`
- `assets/banners/readme/scripts_automation_zeid_data_service_health.svg` -> `assets/banners/readme/scripts_automation_zeid_data_service_health.svg`
- `assets/banners/readme/scripts_automation_zeid_data_sha256_manifest_cpp.svg` -> `assets/banners/readme/scripts_automation_zeid_data_sha256_manifest_cpp.svg`
- `assets/banners/readme/scripts_automation_zeid_data_tls_cert_expiry.svg` -> `assets/banners/readme/scripts_automation_zeid_data_tls_cert_expiry.svg`
- `assets/banners/readme/scripts_inventory.svg` -> `assets/banners/readme/scripts_inventory.svg`
- `assets/banners/readme/scripts_weekly_top_malware_detections_scripted.svg` -> `assets/banners/readme/scripts_weekly_top_malware_detections_scripted.svg`
- `assets/banners/readme/templates.svg` -> `assets/banners/readme/templates.svg`
- `assets/banners/readme/white_papers.svg` -> `assets/banners/readme/white_papers.svg`
- `assets/banners/readme/workbooks.svg` -> `assets/banners/readme/workbooks.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks_aws.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_aws.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks_cisco.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_cisco.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks_crowdstrike.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_crowdstrike.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks_databricks.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_databricks.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks_google_workspace.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_google_workspace.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks_microsoft.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_microsoft.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks_okta.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_okta.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks_palo_alto_networks.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_palo_alto_networks.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks_snowflake.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_snowflake.svg`
- `assets/banners/readme/workbooks_security_operations_playbooks_splunk.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_splunk.svg`

### `assets/images/`

- `assets/images/5 Best Practices.png` -> `assets/images/5 Best Practices.png`
- `assets/images/AIGovernance.png` -> `assets/images/AIGovernance.png`
- `assets/images/DataCenterCleanUp.png` -> `assets/images/DataCenterCleanUp.png`
- `assets/images/DataExfiltration.png` -> `assets/images/DataExfiltration.png`
- `assets/images/HaveAGoodWeekend.png` -> `assets/images/HaveAGoodWeekend.png`
- `assets/images/README.md` -> `assets/images/README.md`
- `assets/images/ClaudeBot.png` -> `assets/images/ClaudeBot.png`
- `assets/images/CrowdStrikeContentRelease.png` -> `assets/images/CrowdStrikeContentRelease.png`
- `assets/images/SnowflakeContentRelease.png` -> `assets/images/SnowflakeContentRelease.png`
- `assets/images/ZD Banner.png` -> `assets/images/ZD Banner.png`
- `assets/images/ZD_Dashboard.png` -> `assets/images/ZD_Dashboard.png`
- `assets/images/zeid_logo_round_fade.png` -> `assets/images/zeid_logo_round_fade.png`
- `assets/images/ceo_coworker.png` -> `assets/images/ceo_coworker.png`
- `assets/images/slamdunkyouraudit.png` -> `assets/images/slamdunkyouraudit.png`
- `assets/images/zd_banner_1.png` -> `assets/images/zd_banner_1.png`
- `assets/images/zd_banner_2.png` -> `assets/images/zd_banner_2.png`
- `assets/images/zd_banner_3.png` -> `assets/images/zd_banner_3.png`

### `content/vendors/`

- `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_01_internet_facing_exploitation_attempt_kev_prioritized.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_01_internet_facing_exploitation_attempt_kev_prioritized.zip`
- `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_02_suspicious_remote_admin_access_vpn_ssh_rdp.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_02_suspicious_remote_admin_access_vpn_ssh_rdp.zip`
- `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_03_duo_mfa_fatigue_fraudulent_push_and_high_risk_auth.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_03_duo_mfa_fatigue_fraudulent_push_and_high_risk_auth.zip`
- `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_04_phishing_to_credential_harvest_correlation_email_dns.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_04_phishing_to_credential_harvest_correlation_email_dns.zip`
- `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_05_dns_tunneling_and_exfiltration_umbrella.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_05_dns_tunneling_and_exfiltration_umbrella.zip`
- `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_06_encrypted_dns_bypass_doh_dot_third_party_resolvers.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_06_encrypted_dns_bypass_doh_dot_third_party_resolvers.zip`
- `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_07_https_beaconing_c2_rare_domains_low_and_slow.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_07_https_beaconing_c2_rare_domains_low_and_slow.zip`
- `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_08_east_west_scanning_and_lateral_movement_netflow.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_08_east_west_scanning_and_lateral_movement_netflow.zip`
- `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_09_ransomware_staging_pre_encryption_secure_endpoint.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_09_ransomware_staging_pre_encryption_secure_endpoint.zip`
- `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_10_data_exfiltration_large_uploads_to_unsanctioned_cloud.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_10_data_exfiltration_large_uploads_to_unsanctioned_cloud.zip`
- `content/vendors/cisco/Detections/zeid_data_cisco-claude-firewall-endpoint-pack.zip` -> `content/vendors/cisco/Detections/zeid_data_cisco-claude-firewall-endpoint-pack.zip`
- `content/vendors/cisco/PRE_REQ.md` -> `content/vendors/cisco/PRE_REQ.md`
- `content/vendors/cisco/README.md` -> `content/vendors/cisco/README.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/HOWTO.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/HOWTO.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/LICENSE.txt` -> `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/LICENSE.txt`
- `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/README.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/README.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/ZeidData_CrowdStrike_AI_Governance_Rules_Reports_Views_Filters_Package.zip` -> `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/ZeidData_CrowdStrike_AI_Governance_Rules_Reports_Views_Filters_Package.zip`
- `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/manifest.yaml` -> `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/manifest.yaml`
- `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/HOWTO.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/HOWTO.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/LICENSE.txt` -> `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/LICENSE.txt`
- `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/README.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/README.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/Zeid_Data_Falcon_AuditEvidence_Noise_Reduction_Pack.zip` -> `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/Zeid_Data_Falcon_AuditEvidence_Noise_Reduction_Pack.zip`
- `content/vendors/crowdstrike/CrowdStrike Falcon Claude Bot Detection/HOWTO.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon Claude Bot Detection/HOWTO.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon Claude Bot Detection/README.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon Claude Bot Detection/README.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon Claude Bot Detection/zeid_data_crowdstrike-claude-firewall-endpoint-pack.zip` -> `content/vendors/crowdstrike/CrowdStrike Falcon Claude Bot Detection/zeid_data_crowdstrike-claude-firewall-endpoint-pack.zip`
- `content/vendors/crowdstrike/README.md` -> `content/vendors/crowdstrike/README.md`
- `content/vendors/island/README.md` -> `content/vendors/island/README.md`
- `content/vendors/island/zeid_data_elk_stack_connector/.env.example` -> `content/vendors/island/zeid_data_elk_stack_connector/.env.example`
- `content/vendors/island/zeid_data_elk_stack_connector/HOWTO.md` -> `content/vendors/island/zeid_data_elk_stack_connector/HOWTO.md`
- `content/vendors/island/zeid_data_elk_stack_connector/README.md` -> `content/vendors/island/zeid_data_elk_stack_connector/README.md`
- `content/vendors/island/zeid_data_elk_stack_connector/docker-compose.yml` -> `content/vendors/island/zeid_data_elk_stack_connector/docker-compose.yml`
- `content/vendors/island/zeid_data_elk_stack_connector/elastic/index-template-island.json` -> `content/vendors/island/zeid_data_elk_stack_connector/elastic/index-template-island.json`
- `content/vendors/island/zeid_data_elk_stack_connector/examples/island_event_sample.json` -> `content/vendors/island/zeid_data_elk_stack_connector/examples/island_event_sample.json`
- `content/vendors/island/zeid_data_elk_stack_connector/logstash/config/logstash.yml` -> `content/vendors/island/zeid_data_elk_stack_connector/logstash/config/logstash.yml`
- `content/vendors/island/zeid_data_elk_stack_connector/logstash/pipeline/island-http.conf` -> `content/vendors/island/zeid_data_elk_stack_connector/logstash/pipeline/island-http.conf`
- `content/vendors/island/zeid_data_elk_stack_connector/tools/scripts/apply_index_template.sh` -> `content/vendors/island/zeid_data_elk_stack_connector/tools/scripts/apply_index_template.sh`
- `content/vendors/island/zeid_data_elk_stack_connector/tools/scripts/generate_test_event.py` -> `content/vendors/island/zeid_data_elk_stack_connector/tools/scripts/generate_test_event.py`
- `content/vendors/island/zeid_data_elk_stack_connector/tools/scripts/post_test_event.sh` -> `content/vendors/island/zeid_data_elk_stack_connector/tools/scripts/post_test_event.sh`
- `content/vendors/island/zeid_data_elk_stack_connector/training/KQL_QUERIES.md` -> `content/vendors/island/zeid_data_elk_stack_connector/training/KQL_QUERIES.md`
- `content/vendors/island/zeid_data_elk_stack_connector/training/SCENARIOS.md` -> `content/vendors/island/zeid_data_elk_stack_connector/training/SCENARIOS.md`
- `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/01_island_siem_settings_mock.png` -> `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/01_island_siem_settings_mock.png`
- `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/02_logstash_ingest_mock.png` -> `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/02_logstash_ingest_mock.png`
- `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/03_kibana_discover_mock.png` -> `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/03_kibana_discover_mock.png`
- `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/04_kibana_dashboard_mock.png` -> `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/04_kibana_dashboard_mock.png`
- `content/vendors/island/zeid_data_evidence_bundle/HOWTO.md` -> `content/vendors/island/zeid_data_evidence_bundle/HOWTO.md`
- `content/vendors/island/zeid_data_evidence_bundle/README.md` -> `content/vendors/island/zeid_data_evidence_bundle/README.md`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_bundle_schema.json` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_bundle_schema.json`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_collect.py` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_collect.py`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_config.example.yaml` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_config.example.yaml`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_env.example` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_env.example`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_evidence_bundle_spec.md` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_evidence_bundle_spec.md`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_island_policies.jsonl` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_island_policies.jsonl`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_island_users.jsonl` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_island_users.jsonl`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_manifest.json` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_manifest.json`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_gitignore` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_gitignore`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_island_client.py` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_island_client.py`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_data_make_bundle.py` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_make_bundle.py`
- `content/vendors/island/zeid_data_evidence_bundle/zeid_datapip_requirements.txt` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_datapip_requirements.txt`
- `content/vendors/sentinelone/README.md` -> `content/vendors/sentinelone/README.md`
- `content/vendors/sentinelone/SOC2_Content/HOWTO.md` -> `content/vendors/sentinelone/SOC2_Content/HOWTO.md`
- `content/vendors/sentinelone/SOC2_Content/README.md` -> `content/vendors/sentinelone/SOC2_Content/README.md`
- `content/vendors/sentinelone/SOC2_Content/Zeid Data_sentinel_soc2_workbook_multi_source.workbook` -> `content/vendors/sentinelone/SOC2_Content/Zeid Data_sentinel_soc2_workbook_multi_source.workbook`
- `content/vendors/sentinelone/SOC2_Content/Zeid Data_sentinel_soc2_workbook_multi_source_arm.json` -> `content/vendors/sentinelone/SOC2_Content/Zeid Data_sentinel_soc2_workbook_multi_source_arm.json`
- `content/vendors/snowflake/Base_AI_Queries` -> `content/vendors/snowflake/Base_AI_Queries`
- `content/vendors/snowflake/HOWTO.md` -> `content/vendors/snowflake/HOWTO.md`
- `content/vendors/snowflake/LICENSE` -> `content/vendors/snowflake/LICENSE`
- `content/vendors/snowflake/README.md` -> `content/vendors/snowflake/README.md`
- `content/vendors/snowflake/zeid_data_snowflake-ai-governance-compliance-pack.zip` -> `content/vendors/snowflake/zeid_data_snowflake-ai-governance-compliance-pack.zip`
- `content/vendors/README.md` -> `content/vendors/README.md`
- `content/vendors/SPL_Top 10 Threat Hunts (AD + ASA + CrowdStrike)` -> `content/vendors/SPL_Top 10 Threat Hunts (AD + ASA + CrowdStrike)`
- `content/vendors/YAML.md` -> `content/vendors/YAML.md`
- `content/vendors/Zeid Data Claude Bot Content/HOWTO.md` -> `content/vendors/Zeid Data Claude Bot Content/HOWTO.md`
- `content/vendors/Zeid Data Claude Bot Content/README.md` -> `content/vendors/Zeid Data Claude Bot Content/README.md`
- `content/vendors/Zeid Data Claude Bot Content/zeid_data_splunk-claude-firewall-endpoint-pack.zip` -> `content/vendors/Zeid Data Claude Bot Content/zeid_data_splunk-claude-firewall-endpoint-pack.zip`
- `content/vendors/Zeid Data Splunk App - Exfil Watch/HOWTO.md` -> `content/vendors/Zeid Data Splunk App - Exfil Watch/HOWTO.md`
- `content/vendors/Zeid Data Splunk App - Exfil Watch/README.md` -> `content/vendors/Zeid Data Splunk App - Exfil Watch/README.md`
- `content/vendors/Zeid Data Splunk App - Exfil Watch/ZeidData_Splunk_Exfil_Monitor_App.zip` -> `content/vendors/Zeid Data Splunk App - Exfil Watch/ZeidData_Splunk_Exfil_Monitor_App.zip`
- `content/vendors/savedsearches.conf` -> `content/vendors/savedsearches.conf`

### `detections/vendor-packs/`

- `detections/vendor-packs/README.md` -> `detections/vendor-packs/README.md`
- `detections/vendor-packs/claude_bot/README.md` -> `detections/vendor-packs/claude_bot/README.md`
- `detections/vendor-packs/claude_bot/zeid_data_claude_detection` -> `detections/vendor-packs/claude_bot/zeid_data_claude_detection`
- `detections/vendor-packs/cve-2025-20393/README.md` -> `detections/vendor-packs/cve-2025-20393/README.md`
- `detections/vendor-packs/cve-2025-20393/zeid_data_cisco_cve-2025-20393-detection-package.zip` -> `detections/vendor-packs/cve-2025-20393/zeid_data_cisco_cve-2025-20393-detection-package.zip`
- `detections/vendor-packs/cve-2025-40551/HOWTO.md` -> `detections/vendor-packs/cve-2025-40551/HOWTO.md`
- `detections/vendor-packs/cve-2025-40551/LICENSE` -> `detections/vendor-packs/cve-2025-40551/LICENSE`
- `detections/vendor-packs/cve-2025-40551/README.md` -> `detections/vendor-packs/cve-2025-40551/README.md`
- `detections/vendor-packs/cve-2025-40551/test.txt` -> `detections/vendor-packs/cve-2025-40551/test.txt`
- `detections/vendor-packs/cve-2025-40551/zeid_data_CVE-2025-40551.py` -> `detections/vendor-packs/cve-2025-40551/zeid_data_CVE-2025-40551.py`
- `detections/vendor-packs/cve-2026-24423/HOWTO.md` -> `detections/vendor-packs/cve-2026-24423/HOWTO.md`
- `detections/vendor-packs/cve-2026-24423/LICENSE` -> `detections/vendor-packs/cve-2026-24423/LICENSE`
- `detections/vendor-packs/cve-2026-24423/README.md` -> `detections/vendor-packs/cve-2026-24423/README.md`
- `detections/vendor-packs/cve-2026-24423/zeid_data_CVE-2026-24423.py` -> `detections/vendor-packs/cve-2026-24423/zeid_data_CVE-2026-24423.py`
- `detections/vendor-packs/cve-2026-24858/HOWTO.md` -> `detections/vendor-packs/cve-2026-24858/HOWTO.md`
- `detections/vendor-packs/cve-2026-24858/LICENSE` -> `detections/vendor-packs/cve-2026-24858/LICENSE`
- `detections/vendor-packs/cve-2026-24858/README.md` -> `detections/vendor-packs/cve-2026-24858/README.md`
- `detections/vendor-packs/cve-2026-24858/zeid_data_CVE-2026-24858.py` -> `detections/vendor-packs/cve-2026-24858/zeid_data_CVE-2026-24858.py`

### `docs/guides/`

- `docs/guides/index.md` -> `docs/guides/index.md`
- `docs/guides/profile-readme.md` -> `docs/guides/profile-readme.md`
- `docs/guides/standards/evidence.md` -> `docs/guides/standards/evidence.md`
- `docs/guides/standards/naming.md` -> `docs/guides/standards/naming.md`
- `docs/guides/standards/repository-structure.md` -> `docs/guides/standards/repository-structure.md`
- `docs/guides/taxonomy.md` -> `docs/guides/taxonomy.md`

### `projects/active/`

- `projects/active/zeid_data_ai_guard/HOWTO.md` -> `projects/active/zeid_data_ai_guard/HOWTO.md`
- `projects/active/zeid_data_ai_guard/LICENSE` -> `projects/active/zeid_data_ai_guard/LICENSE`
- `projects/active/zeid_data_ai_guard/README.md` -> `projects/active/zeid_data_ai_guard/README.md`
- `projects/active/zeid_data_ai_guard/SECURITY.md` -> `projects/active/zeid_data_ai_guard/SECURITY.md`
- `projects/active/zeid_data_ai_guard/Zeid Data GenAIGuard.zip` -> `projects/active/zeid_data_ai_guard/Zeid Data GenAIGuard.zip`
- `projects/active/zeid_data_ai_guard/pyproject.toml` -> `projects/active/zeid_data_ai_guard/pyproject.toml`
- `projects/active/zeid_data_bruteforce_ssh/README.md` -> `projects/active/zeid_data_bruteforce_ssh/README.md`
- `projects/active/zeid_data_bruteforce_ssh/ZD_SSH Brute Force` -> `projects/active/zeid_data_bruteforce_ssh/ZD_SSH Brute Force`
- `projects/active/zeid_data_cloak_check/HOWTO.md` -> `projects/active/zeid_data_cloak_check/HOWTO.md`
- `projects/active/zeid_data_cloak_check/LICENSE.txt` -> `projects/active/zeid_data_cloak_check/LICENSE.txt`
- `projects/active/zeid_data_cloak_check/README.md` -> `projects/active/zeid_data_cloak_check/README.md`
- `projects/active/zeid_data_cloak_check/checklists/zeid_data_cloakcheck_scorecard.md` -> `projects/active/zeid_data_cloak_check/checklists/zeid_data_cloakcheck_scorecard.md`
- `projects/active/zeid_data_cloak_check/checklists/zeid_data_evidence_bundle_template.md` -> `projects/active/zeid_data_cloak_check/checklists/zeid_data_evidence_bundle_template.md`
- `projects/active/zeid_data_cloak_check/data/zeid_data_sample_proxy_logs.csv` -> `projects/active/zeid_data_cloak_check/data/zeid_data_sample_proxy_logs.csv`
- `projects/active/zeid_data_cloak_check/data/zeid_data_sample_redirect_telemetry.jsonl` -> `projects/active/zeid_data_cloak_check/data/zeid_data_sample_redirect_telemetry.jsonl`
- `projects/active/zeid_data_cloak_check/detections/zeid_data_elastic_esql_cloakcheck.esql` -> `projects/active/zeid_data_cloak_check/detections/zeid_data_elastic_esql_cloakcheck.esql`
- `projects/active/zeid_data_cloak_check/detections/zeid_data_elastic_kql_cloakcheck.txt` -> `projects/active/zeid_data_cloak_check/detections/zeid_data_elastic_kql_cloakcheck.txt`
- `projects/active/zeid_data_cloak_check/detections/zeid_data_sentinel_cloakcheck.kql` -> `projects/active/zeid_data_cloak_check/detections/zeid_data_sentinel_cloakcheck.kql`
- `projects/active/zeid_data_cloak_check/detections/zeid_data_sigma_cloaked_phishing.yml` -> `projects/active/zeid_data_cloak_check/detections/zeid_data_sigma_cloaked_phishing.yml`
- `projects/active/zeid_data_cloak_check/detections/zeid_data_splunk_cloakcheck.spl` -> `projects/active/zeid_data_cloak_check/detections/zeid_data_splunk_cloakcheck.spl`
- `projects/active/zeid_data_cloak_check/requirements.txt` -> `projects/active/zeid_data_cloak_check/requirements.txt`
- `projects/active/zeid_data_cloak_check/tools/scripts/zeid_data_compare_runs.py` -> `projects/active/zeid_data_cloak_check/tools/scripts/zeid_data_compare_runs.py`
- `projects/active/zeid_data_cloak_check/tools/scripts/zeid_data_differential_fetch.py` -> `projects/active/zeid_data_cloak_check/tools/scripts/zeid_data_differential_fetch.py`
- `projects/active/zeid_data_cloak_check/tools/scripts/zeid_data_urls_sample.txt` -> `projects/active/zeid_data_cloak_check/tools/scripts/zeid_data_urls_sample.txt`
- `projects/active/zeid_data_cloak_check/templates/zeid_data_ioc_schema.csv` -> `projects/active/zeid_data_cloak_check/templates/zeid_data_ioc_schema.csv`
- `projects/active/zeid_data_cloak_check/templates/zeid_data_ioc_schema.json` -> `projects/active/zeid_data_cloak_check/templates/zeid_data_ioc_schema.json`
- `projects/active/zeid_data_cloak_check/templates/zeid_data_stix_bundle_example.json` -> `projects/active/zeid_data_cloak_check/templates/zeid_data_stix_bundle_example.json`
- `projects/active/zeid_data_cloak_check/zeid_data_cloak_checking_email.md` -> `projects/active/zeid_data_cloak_check/zeid_data_cloak_checking_email.md`
- `projects/active/zeid_data_forensics_tools/README.md` -> `projects/active/zeid_data_forensics_tools/README.md`
- `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/INSTRUCTOR_GUIDE.md` -> `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/INSTRUCTOR_GUIDE.md`
- `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/README.md` -> `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/README.md`
- `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/SECURITY.md` -> `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/SECURITY.md`
- `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/run_tests.sh` -> `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/run_tests.sh`
- `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/zeid_data_drt.zip` -> `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/zeid_data_drt.zip`
- `projects/active/zeid_data_gap_check/HOWTO.md` -> `projects/active/zeid_data_gap_check/HOWTO.md`
- `projects/active/zeid_data_gap_check/LICENSE` -> `projects/active/zeid_data_gap_check/LICENSE`
- `projects/active/zeid_data_gap_check/README.md` -> `projects/active/zeid_data_gap_check/README.md`
- `projects/active/zeid_data_gap_check/Zeid_Data_GapCheck.zip` -> `projects/active/zeid_data_gap_check/Zeid_Data_GapCheck.zip`
- `projects/active/zeid_data_gap_check/gapcheck.py` -> `projects/active/zeid_data_gap_check/gapcheck.py`
- `projects/active/zeid_data_gap_check/policy.sample.json` -> `projects/active/zeid_data_gap_check/policy.sample.json`
- `projects/active/zeid_data_gap_check/requirements.txt` -> `projects/active/zeid_data_gap_check/requirements.txt`
- `projects/active/zeid_data_net_ledger/README.md` -> `projects/active/zeid_data_net_ledger/README.md`
- `projects/active/zeid_data_net_ledger/Zeid Data NetLedger` -> `projects/active/zeid_data_net_ledger/Zeid Data NetLedger`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/.gitignore` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/.gitignore`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/HOWTO.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/HOWTO.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/LICENSE` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/LICENSE`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/README.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/README.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_control_matrix.csv` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_control_matrix.csv`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_control_matrix.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_control_matrix.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_model_system_card_template.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_model_system_card_template.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_risk_register_template.csv` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_risk_register_template.csv`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_vendor_questionnaire.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_vendor_questionnaire.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/diagrams/zeid_data_ai_governance_architecture.mmd` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/diagrams/zeid_data_ai_governance_architecture.mmd`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_ai_event_schema.json` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_ai_event_schema.json`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_ai_event_schema.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_ai_event_schema.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_elastic_ingest_pipeline.json` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_elastic_ingest_pipeline.json`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_splunk_props.conf` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_splunk_props.conf`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_splunk_transforms.conf` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_splunk_transforms.conf`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/policies/zeid_data_ai_policy_minimum.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/policies/zeid_data_ai_policy_minimum.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/requirements.txt` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/requirements.txt`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_ai_events.jsonl` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_ai_events.jsonl`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_risk_register.csv` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_risk_register.csv`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_system_card.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_system_card.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/tools/scripts/bundle_evidence.py` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/tools/scripts/bundle_evidence.py`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/tools/scripts/generate_coverage_report.py` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/tools/scripts/generate_coverage_report.py`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/tools/scripts/validate_events.py` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/tools/scripts/validate_events.py`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/zeid_data_ai_governance.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/zeid_data_ai_governance.md`
- `projects/active/zeid_data_qilin_ransomware_detection/HOWTO.md` -> `projects/active/zeid_data_qilin_ransomware_detection/HOWTO.md`
- `projects/active/zeid_data_qilin_ransomware_detection/README.md` -> `projects/active/zeid_data_qilin_ransomware_detection/README.md`
- `projects/active/zeid_data_qilin_ransomware_detection/qilin_ransomware_scanner` -> `projects/active/zeid_data_qilin_ransomware_detection/qilin_ransomware_scanner`
- `projects/active/zeid_data_regex_security/HOWTO.md` -> `projects/active/zeid_data_regex_security/HOWTO.md`
- `projects/active/zeid_data_regex_security/LICENSE.md` -> `projects/active/zeid_data_regex_security/LICENSE.md`
- `projects/active/zeid_data_regex_security/README.md` -> `projects/active/zeid_data_regex_security/README.md`
- `projects/active/zeid_data_regex_security/zeid_data_broken_vs_safe_regex_examples.md` -> `projects/active/zeid_data_regex_security/zeid_data_broken_vs_safe_regex_examples.md`
- `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_auth_anchor_grouping_bypass_samples.jsonl` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_auth_anchor_grouping_bypass_samples.jsonl`
- `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_filename_extension_bypass_samples.jsonl` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_filename_extension_bypass_samples.jsonl`
- `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_ip_literal_unescaped_dot_samples.log` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_ip_literal_unescaped_dot_samples.log`
- `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_kv_greedy_overcapture_samples.log` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_kv_greedy_overcapture_samples.log`
- `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_payload_samples.log` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_payload_samples.log`
- `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_proxy_url_allowlist_trap_samples.csv` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_proxy_url_allowlist_trap_samples.csv`
- ... 8 more

### `research/research/malware/`

- `research/research/malware/README.md` -> `research/research/research/malware/README.md`
- `research/research/malware/claude/HOWTO.md` -> `research/research/research/malware/claude/HOWTO.md`
- `research/research/malware/claude/LICENSE` -> `research/research/research/malware/claude/LICENSE`
- `research/research/malware/claude/MANIFEST_SHA256.txt` -> `research/research/research/malware/claude/MANIFEST_SHA256.txt`
- `research/research/malware/claude/README.md` -> `research/research/research/malware/claude/README.md`
- `research/research/malware/claude/detections/sigma/zeid_data_claude_code_baseurl_env_override.yml` -> `research/research/research/malware/claude/detections/sigma/zeid_data_claude_code_baseurl_env_override.yml`
- `research/research/malware/claude/detections/sigma/zeid_data_claude_code_shell_spawn.yml` -> `research/research/research/malware/claude/detections/sigma/zeid_data_claude_code_shell_spawn.yml`
- `research/research/malware/claude/detections/sigma/zeid_data_claude_code_suspicious_config_change.yml` -> `research/research/research/malware/claude/detections/sigma/zeid_data_claude_code_suspicious_config_change.yml`
- `research/research/malware/claude/detections/yara/zeid_data_claude_code_config_risky_strings.yar` -> `research/research/research/malware/claude/detections/yara/zeid_data_claude_code_config_risky_strings.yar`
- `research/research/malware/claude/queries/sentinel/zeid_data_mde_file_events_claude_config.kql` -> `research/research/research/malware/claude/queries/sentinel/zeid_data_mde_file_events_claude_config.kql`
- `research/research/malware/claude/queries/sentinel/zeid_data_mde_network_unexpected_from_claude.kql` -> `research/research/research/malware/claude/queries/sentinel/zeid_data_mde_network_unexpected_from_claude.kql`
- `research/research/malware/claude/queries/sentinel/zeid_data_mde_process_shell_from_claude.kql` -> `research/research/research/malware/claude/queries/sentinel/zeid_data_mde_process_shell_from_claude.kql`
- `research/research/malware/claude/queries/splunk/zeid_data_file_change_claude_config.spl` -> `research/research/research/malware/claude/queries/splunk/zeid_data_file_change_claude_config.spl`
- `research/research/malware/claude/queries/splunk/zeid_data_network_unexpected_from_claude.spl` -> `research/research/research/malware/claude/queries/splunk/zeid_data_network_unexpected_from_claude.spl`
- `research/research/malware/claude/queries/splunk/zeid_data_process_shell_from_claude.spl` -> `research/research/research/malware/claude/queries/splunk/zeid_data_process_shell_from_claude.spl`
- `research/research/malware/claude/tools/scripts/zeid_data_ci_block_risky_claude_config.ps1` -> `research/research/research/malware/claude/tools/scripts/zeid_data_ci_block_risky_claude_config.ps1`
- `research/research/malware/claude/tools/scripts/zeid_data_ci_block_risky_claude_config.sh` -> `research/research/research/malware/claude/tools/scripts/zeid_data_ci_block_risky_claude_config.sh`
- `research/research/malware/promptflux_fruitshell/HOWTO.md` -> `research/research/research/malware/promptflux_fruitshell/HOWTO.md`
- `research/research/malware/promptflux_fruitshell/LICENSE.md` -> `research/research/research/malware/promptflux_fruitshell/LICENSE.md`
- `research/research/malware/promptflux_fruitshell/README.md` -> `research/research/research/malware/promptflux_fruitshell/README.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_crowdstrike_deployment_steps.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_crowdstrike_deployment_steps.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_crowdstrike_detections.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_crowdstrike_detections.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_crowdstrike_overview.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_crowdstrike_overview.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_crowdstrike_queries.txt` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_crowdstrike_queries.txt`
- `research/research/malware/promptflux_fruitshell/zeid_data_crowdstrike_tuning_guidance.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_crowdstrike_tuning_guidance.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_detection_strategy.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_detection_strategy.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_executive_summary.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_executive_summary.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_false_positive_guidance.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_false_positive_guidance.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_iocs.csv` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_iocs.csv`
- `research/research/malware/promptflux_fruitshell/zeid_data_microsoft_deployment_steps.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_microsoft_deployment_steps.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_microsoft_detections.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_microsoft_detections.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_microsoft_overview.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_microsoft_overview.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_microsoft_queries.txt` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_microsoft_queries.txt`
- `research/research/malware/promptflux_fruitshell/zeid_data_microsoft_tuning_guidance.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_microsoft_tuning_guidance.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_mitre_mapping.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_mitre_mapping.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_references.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_references.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_splunk_deployment_steps.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_splunk_deployment_steps.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_splunk_detections.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_splunk_detections.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_splunk_overview.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_splunk_overview.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_splunk_queries.txt` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_splunk_queries.txt`
- `research/research/malware/promptflux_fruitshell/zeid_data_splunk_tuning_guidance.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_splunk_tuning_guidance.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_threat_overview.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_threat_overview.md`
- `research/research/malware/promptflux_fruitshell/zeid_data_triage_checklist.md` -> `research/research/research/malware/promptflux_fruitshell/zeid_data_triage_checklist.md`
- `research/research/malware/qilin/Qilin_Ransomware Scanner.py` -> `research/research/research/malware/qilin/Qilin_Ransomware Scanner.py`

### `research/research/white-papers/`

- `research/research/white-papers/README.md` -> `research/research/white-papers/README.md`
- `research/research/white-papers/SECURITY.md` -> `research/research/white-papers/SECURITY.md`
- `research/research/white-papers/controls/zeid_data_ai_governance.md` -> `research/research/white-papers/controls/zeid_data_ai_governance.md`
- `research/research/white-papers/controls/zeid_data_broken_vs_safe_regex_examples.md` -> `research/research/white-papers/controls/zeid_data_broken_vs_safe_regex_examples.md`
- `research/research/white-papers/controls/zeid_data_regex_security.md` -> `research/research/white-papers/controls/zeid_data_regex_security.md`
- `research/research/white-papers/detections/zeid_data_akira_ransomware_detection_report.md` -> `research/research/white-papers/detections/zeid_data_akira_ransomware_detection_report.md`
- `research/research/white-papers/detections/zeid_data_black_basta_detection_report.md` -> `research/research/white-papers/detections/zeid_data_black_basta_detection_report.md`
- `research/research/white-papers/detections/zeid_data_cl0p_data_extortion_detection_report.md` -> `research/research/white-papers/detections/zeid_data_cl0p_data_extortion_detection_report.md`
- `research/research/white-papers/detections/zeid_data_cve_2025_22225_vmware_esxi_detection_report.md` -> `research/research/white-papers/detections/zeid_data_cve_2025_22225_vmware_esxi_detection_report.md`
- `research/research/white-papers/detections/zeid_data_cve_2025_34026_versa_concerto_auth_bypass_detection_report.md` -> `research/research/white-papers/detections/zeid_data_cve_2025_34026_versa_concerto_auth_bypass_detection_report.md`
- `research/research/white-papers/detections/zeid_data_cve_2025_68645_zimbra_rfi_detection_report.md` -> `research/research/white-papers/detections/zeid_data_cve_2025_68645_zimbra_rfi_detection_report.md`
- `research/research/white-papers/detections/zeid_data_cve_2025_8110_gogs_rce_detection_report.md` -> `research/research/white-papers/detections/zeid_data_cve_2025_8110_gogs_rce_detection_report.md`
- `research/research/white-papers/detections/zeid_data_cve_2026_21509_office_bypass_detection_report.md` -> `research/research/white-papers/detections/zeid_data_cve_2026_21509_office_bypass_detection_report.md`
- `research/research/white-papers/detections/zeid_data_qilin_extortion_detection_report.md` -> `research/research/white-papers/detections/zeid_data_qilin_extortion_detection_report.md`
- `research/research/white-papers/detections/zeid_data_safepay_ransomware_detection_report.md` -> `research/research/white-papers/detections/zeid_data_safepay_ransomware_detection_report.md`

### `tools/tools/scripts/`

- `tools/tools/scripts/README.md` -> `tools/tools/tools/scripts/README.md`
- `tools/tools/scripts/audit_dashboard_sources.py` -> `tools/tools/tools/scripts/audit_dashboard_sources.py`
- `tools/tools/scripts/automation/README.md` -> `tools/tools/tools/scripts/automation/README.md`
- `tools/tools/scripts/automation/zeid_data_backup_verify/HOWTO.md` -> `tools/tools/tools/scripts/automation/zeid_data_backup_verify/HOWTO.md`
- `tools/tools/scripts/automation/zeid_data_backup_verify/README.md` -> `tools/tools/tools/scripts/automation/zeid_data_backup_verify/README.md`
- `tools/tools/scripts/automation/zeid_data_backup_verify/zeid_data_backup_verify.py` -> `tools/tools/tools/scripts/automation/zeid_data_backup_verify/zeid_data_backup_verify.py`
- `tools/tools/scripts/automation/zeid_data_dns_audit/HOWTO.md` -> `tools/tools/tools/scripts/automation/zeid_data_dns_audit/HOWTO.md`
- `tools/tools/scripts/automation/zeid_data_dns_audit/README.md` -> `tools/tools/tools/scripts/automation/zeid_data_dns_audit/README.md`
- `tools/tools/scripts/automation/zeid_data_dns_audit/zeid_data_dns_audit.py` -> `tools/tools/tools/scripts/automation/zeid_data_dns_audit/zeid_data_dns_audit.py`
- `tools/tools/scripts/automation/zeid_data_eventlog_export/HOWTO.md` -> `tools/tools/tools/scripts/automation/zeid_data_eventlog_export/HOWTO.md`
- `tools/tools/scripts/automation/zeid_data_eventlog_export/README.md` -> `tools/tools/tools/scripts/automation/zeid_data_eventlog_export/README.md`
- `tools/tools/scripts/automation/zeid_data_eventlog_export/zeid_data_eventlog_export.ps1` -> `tools/tools/tools/scripts/automation/zeid_data_eventlog_export/zeid_data_eventlog_export.ps1`
- `tools/tools/scripts/automation/zeid_data_host_reachability/HOWTO.md` -> `tools/tools/tools/scripts/automation/zeid_data_host_reachability/HOWTO.md`
- `tools/tools/scripts/automation/zeid_data_host_reachability/README.md` -> `tools/tools/tools/scripts/automation/zeid_data_host_reachability/README.md`
- `tools/tools/scripts/automation/zeid_data_host_reachability/zeid_data_host_reachability.py` -> `tools/tools/tools/scripts/automation/zeid_data_host_reachability/zeid_data_host_reachability.py`
- `tools/tools/scripts/automation/zeid_data_local_admin_audit/HOWTO.md` -> `tools/tools/tools/scripts/automation/zeid_data_local_admin_audit/HOWTO.md`
- `tools/tools/scripts/automation/zeid_data_local_admin_audit/README.md` -> `tools/tools/tools/scripts/automation/zeid_data_local_admin_audit/README.md`
- `tools/tools/scripts/automation/zeid_data_local_admin_audit/zeid_data_local_admin_audit.ps1` -> `tools/tools/tools/scripts/automation/zeid_data_local_admin_audit/zeid_data_local_admin_audit.ps1`
- `tools/tools/scripts/automation/zeid_data_log_summarizer_cpp/HOWTO.md` -> `tools/tools/tools/scripts/automation/zeid_data_log_summarizer_cpp/HOWTO.md`
- `tools/tools/scripts/automation/zeid_data_log_summarizer_cpp/README.md` -> `tools/tools/tools/scripts/automation/zeid_data_log_summarizer_cpp/README.md`
- `tools/tools/scripts/automation/zeid_data_log_summarizer_cpp/zeid_data_log_summarizer.cpp` -> `tools/tools/tools/scripts/automation/zeid_data_log_summarizer_cpp/zeid_data_log_summarizer.cpp`
- `tools/tools/scripts/automation/zeid_data_route_snapshot/HOWTO.md` -> `tools/tools/tools/scripts/automation/zeid_data_route_snapshot/HOWTO.md`
- `tools/tools/scripts/automation/zeid_data_route_snapshot/README.md` -> `tools/tools/tools/scripts/automation/zeid_data_route_snapshot/README.md`
- `tools/tools/scripts/automation/zeid_data_route_snapshot/zeid_data_route_snapshot.py` -> `tools/tools/tools/scripts/automation/zeid_data_route_snapshot/zeid_data_route_snapshot.py`
- `tools/tools/scripts/automation/zeid_data_service_health/HOWTO.md` -> `tools/tools/tools/scripts/automation/zeid_data_service_health/HOWTO.md`
- `tools/tools/scripts/automation/zeid_data_service_health/README.md` -> `tools/tools/tools/scripts/automation/zeid_data_service_health/README.md`
- `tools/tools/scripts/automation/zeid_data_service_health/zeid_data_service_health.ps1` -> `tools/tools/tools/scripts/automation/zeid_data_service_health/zeid_data_service_health.ps1`
- `tools/tools/scripts/automation/zeid_data_sha256_manifest_cpp/HOWTO.md` -> `tools/tools/tools/scripts/automation/zeid_data_sha256_manifest_cpp/HOWTO.md`
- `tools/tools/scripts/automation/zeid_data_sha256_manifest_cpp/README.md` -> `tools/tools/tools/scripts/automation/zeid_data_sha256_manifest_cpp/README.md`
- `tools/tools/scripts/automation/zeid_data_sha256_manifest_cpp/zeid_data_sha256_manifest.cpp` -> `tools/tools/tools/scripts/automation/zeid_data_sha256_manifest_cpp/zeid_data_sha256_manifest.cpp`
- `tools/tools/scripts/automation/zeid_data_tls_cert_expiry/HOWTO.md` -> `tools/tools/tools/scripts/automation/zeid_data_tls_cert_expiry/HOWTO.md`
- `tools/tools/scripts/automation/zeid_data_tls_cert_expiry/README.md` -> `tools/tools/tools/scripts/automation/zeid_data_tls_cert_expiry/README.md`
- `tools/tools/scripts/automation/zeid_data_tls_cert_expiry/zeid_data_tls_cert_expiry.py` -> `tools/tools/tools/scripts/automation/zeid_data_tls_cert_expiry/zeid_data_tls_cert_expiry.py`
- `tools/tools/scripts/detection/zeid_data_Hunt-NewScheduledTasks.ps1` -> `tools/tools/tools/scripts/detection/zeid_data_Hunt-NewScheduledTasks.ps1`
- `tools/tools/scripts/detection/zeid_data_Hunt-RansomwarePreEncryptCommands.ps1` -> `tools/tools/tools/scripts/detection/zeid_data_Hunt-RansomwarePreEncryptCommands.ps1`
- `tools/tools/scripts/detection/zeid_data_Hunt-linux-staging.sh` -> `tools/tools/tools/scripts/detection/zeid_data_Hunt-linux-staging.sh`
- `tools/tools/scripts/detection/zeid_data_README.md` -> `tools/tools/tools/scripts/detection/zeid_data_README.md`
- `tools/tools/scripts/detection/zeid_data_detection_scripts.zip` -> `tools/tools/tools/scripts/detection/zeid_data_detection_scripts.zip`
- `tools/tools/scripts/detection/zeid_data_hunt_ransomware_fileshare.py` -> `tools/tools/tools/scripts/detection/zeid_data_hunt_ransomware_fileshare.py`
- `tools/tools/scripts/detection/zeid_data_sentinel_infostealer_browser_chain.kql` -> `tools/tools/tools/scripts/detection/zeid_data_sentinel_infostealer_browser_chain.kql`
- `tools/tools/scripts/detection/zeid_data_sentinel_ransomware_prep.kql` -> `tools/tools/tools/scripts/detection/zeid_data_sentinel_ransomware_prep.kql`
- `tools/tools/scripts/detection/zeid_data_sigma_ransomware_prep.yml` -> `tools/tools/tools/scripts/detection/zeid_data_sigma_ransomware_prep.yml`
- `tools/tools/scripts/detection/zeid_data_splunk_exfil_tools.spl` -> `tools/tools/tools/scripts/detection/zeid_data_splunk_exfil_tools.spl`
- `tools/tools/scripts/detection/zeid_data_yara_infostealer_browsercred_access.yar` -> `tools/tools/tools/scripts/detection/zeid_data_yara_infostealer_browsercred_access.yar`
- `tools/tools/scripts/detection/zeid_data_zeek_firstseen_largepost.zeek` -> `tools/tools/tools/scripts/detection/zeid_data_zeek_firstseen_largepost.zeek`
- `tools/tools/scripts/inventory/README.md` -> `tools/tools/tools/scripts/inventory/README.md`
- `tools/tools/scripts/inventory/zeid_data_inventory_bash.sh` -> `tools/tools/tools/scripts/inventory/zeid_data_inventory_bash.sh`
- `tools/tools/scripts/inventory/zeid_data_inventory_csharp.cs` -> `tools/tools/tools/scripts/inventory/zeid_data_inventory_csharp.cs`
- `tools/tools/scripts/inventory/zeid_data_inventory_go.go` -> `tools/tools/tools/scripts/inventory/zeid_data_inventory_go.go`
- `tools/tools/scripts/inventory/zeid_data_inventory_java.java` -> `tools/tools/tools/scripts/inventory/zeid_data_inventory_java.java`
- `tools/tools/scripts/inventory/zeid_data_inventory_node.js` -> `tools/tools/tools/scripts/inventory/zeid_data_inventory_node.js`
- `tools/tools/scripts/inventory/zeid_data_inventory_perl.pl` -> `tools/tools/tools/scripts/inventory/zeid_data_inventory_perl.pl`
- `tools/tools/scripts/inventory/zeid_data_inventory_powershell.ps1` -> `tools/tools/tools/scripts/inventory/zeid_data_inventory_powershell.ps1`
- `tools/tools/scripts/inventory/zeid_data_inventory_python.py` -> `tools/tools/tools/scripts/inventory/zeid_data_inventory_python.py`
- `tools/tools/scripts/inventory/zeid_data_inventory_ruby.rb` -> `tools/tools/tools/scripts/inventory/zeid_data_inventory_ruby.rb`
- `tools/tools/scripts/inventory/zeid_data_inventory_rust.rs` -> `tools/tools/tools/scripts/inventory/zeid_data_inventory_rust.rs`
- `tools/tools/scripts/inventory/zeid_data_network_inventory_scripts.zip` -> `tools/tools/tools/scripts/inventory/zeid_data_network_inventory_scripts.zip`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/README.md` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/README.md`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-NewScheduledTasks.ps1` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-NewScheduledTasks.ps1`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-RansomwarePreEncryptCommands.ps1` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-RansomwarePreEncryptCommands.ps1`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-linux-staging.sh` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-linux-staging.sh`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_hunt_ransomware_fileshare.py` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_hunt_ransomware_fileshare.py`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_sentinel_infostealer_browser_chain.kql` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_sentinel_infostealer_browser_chain.kql`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_sentinel_ransomware_prep.kql` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_sentinel_ransomware_prep.kql`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_sigma_ransomware_prep.yml` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_sigma_ransomware_prep.yml`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_splunk_exfil_tools.spl` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_splunk_exfil_tools.spl`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_yara_infostealer_browsercred_access.yar` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_yara_infostealer_browsercred_access.yar`
- `tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_zeek_firstseen_largepost.zeek` -> `tools/tools/tools/scripts/weekly_top_malware_detections_scripted/zeid_data_zeek_firstseen_largepost.zeek`

### `tools/validators/`

- `tools/validators/automation/zeid_data_regex_safety_tester.py` -> `tools/validators/automation/zeid_data_regex_safety_tester.py`

### `workbooks/dashboards/`

- `workbooks/dashboards/README.md` -> `workbooks/dashboards/README.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB01_suspicious_authentication.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB03_privileged_change_or_admin_grant.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB04_malicious_process_or_edr_detection.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB06_command_and_control_beaconing.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB07_lateral_movement.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB08_ransomware_or_destructive_activity.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB10_oauth_token_api_key_misuse.md`
- `workbooks/dashboards/Security Operations Playbooks/AWS/README.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/README.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB01_suspicious_authentication.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB03_privileged_change_or_admin_grant.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB04_malicious_process_or_edr_detection.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB06_command_and_control_beaconing.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB07_lateral_movement.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB08_ransomware_or_destructive_activity.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB10_oauth_token_api_key_misuse.md`
- `workbooks/dashboards/Security Operations Playbooks/Cisco/README.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/README.md`
- `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB01_suspicious_authentication.md`
- `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB03_privileged_change_or_admin_grant.md`
- `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB08_ransomware_or_destructive_activity.md`
- `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB10_oauth_token_api_key_misuse.md`
- `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/README.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/README.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB01_suspicious_authentication.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB03_privileged_change_or_admin_grant.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB04_malicious_process_or_edr_detection.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB06_command_and_control_beaconing.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB07_lateral_movement.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB08_ransomware_or_destructive_activity.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB10_oauth_token_api_key_misuse.md`
- `workbooks/dashboards/Security Operations Playbooks/Databricks/README.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/README.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB01_suspicious_authentication.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB03_privileged_change_or_admin_grant.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB04_malicious_process_or_edr_detection.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB06_command_and_control_beaconing.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB07_lateral_movement.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB08_ransomware_or_destructive_activity.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB10_oauth_token_api_key_misuse.md`
- `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/README.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/README.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB01_suspicious_authentication.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB03_privileged_change_or_admin_grant.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB04_malicious_process_or_edr_detection.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB06_command_and_control_beaconing.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB07_lateral_movement.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB08_ransomware_or_destructive_activity.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB10_oauth_token_api_key_misuse.md`
- `workbooks/dashboards/Security Operations Playbooks/Microsoft/README.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/README.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB01_suspicious_authentication.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB03_privileged_change_or_admin_grant.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB04_malicious_process_or_edr_detection.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB06_command_and_control_beaconing.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB07_lateral_movement.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB08_ransomware_or_destructive_activity.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB10_oauth_token_api_key_misuse.md`
- `workbooks/dashboards/Security Operations Playbooks/Okta/README.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/README.md`
- `workbooks/dashboards/Security Operations Playbooks/PLAYBOOK_TEMPLATE.md` -> `workbooks/dashboards/Security Operations Playbooks/PLAYBOOK_TEMPLATE.md`
- `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB01_suspicious_authentication.md`
- `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB03_privileged_change_or_admin_grant.md`
- `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB04_malicious_process_or_edr_detection.md`
- `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB05_data_exfiltration_and_large_transfers.md`
- ... 30 more

## Reference risk

### `content/`
- `README.md`
- `content/vendors/crowdstrike/README.md`
- `docs/guides/standards/repository-structure.md`
- `research/research/white-papers/detections/zeid_data_cl0p_data_extortion_detection_report.md`

### `detections/`
- `README.md`
- `content/vendors/sentinelone/README.md`
- `content/vendors/sentinelone/SOC2_Content/HOWTO.md`
- `content/vendors/sentinelone/SOC2_Content/Zeid Data_sentinel_soc2_workbook_multi_source_arm.json`
- `detections/vendor-packs/README.md`
- `docs/guides/index.md`
- `docs/guides/standards/naming.md`
- `docs/guides/standards/repository-structure.md`
- `docs/guides/taxonomy.md`
- `research/research/malware/README.md`
- `research/research/malware/claude/HOWTO.md`
- `research/research/malware/claude/MANIFEST_SHA256.txt`
- `research/research/malware/claude/README.md`
- `projects/active/zeid_data_cloak_check/HOWTO.md`
- `projects/active/zeid_data_cloak_check/README.md`
- `projects/active/zeid_data_cloak_check/zeid_data_cloak_checking_email.md`
- `research/research/white-papers/README.md`

### `research/malware/`
- `README.md`
- `docs/guides/standards/naming.md`
- `docs/guides/standards/repository-structure.md`
- `docs/guides/taxonomy.md`
- `research/research/malware/README.md`
- `research/research/white-papers/README.md`

### `assets/images/`
- `README.md`
- `content/vendors/cisco/README.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/README.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/README.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon Claude Bot Detection/README.md`
- `content/vendors/crowdstrike/README.md`
- `content/vendors/island/README.md`
- `content/vendors/island/zeid_data_elk_stack_connector/README.md`
- `content/vendors/island/zeid_data_evidence_bundle/README.md`
- `content/README.md`
- `content/vendors/sentinelone/README.md`
- `content/vendors/sentinelone/SOC2_Content/README.md`
- `content/vendors/snowflake/README.md`
- `content/vendors/README.md`
- `content/vendors/Zeid Data Claude Bot Content/README.md`
- `content/vendors/Zeid Data Splunk App - Exfil Watch/README.md`
- `detections/vendor-packs/README.md`
- `detections/vendor-packs/claude_bot/README.md`
- `detections/vendor-packs/cve-2025-20393/README.md`
- `detections/vendor-packs/cve-2025-40551/README.md`
- `detections/vendor-packs/cve-2026-24423/README.md`
- `detections/vendor-packs/cve-2026-24858/README.md`
- `docs/guides/index.md`
- `docs/guides/profile-readme.md`
- `docs/guides/standards/repository-structure.md`
- ... 44 more

### `projects/`
- `README.md`
- `detections/vendor-packs/README.md`
- `docs/guides/index.md`
- `docs/guides/standards/naming.md`
- `docs/guides/standards/repository-structure.md`
- `docs/guides/taxonomy.md`
- `research/research/white-papers/README.md`

### `tools/scripts/`
- `README.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/HOWTO.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/README.md`
- `content/vendors/island/zeid_data_elk_stack_connector/HOWTO.md`
- `content/vendors/island/zeid_data_elk_stack_connector/README.md`
- `docs/guides/index.md`
- `docs/guides/standards/repository-structure.md`
- `docs/guides/taxonomy.md`
- `research/research/malware/README.md`
- `research/research/malware/claude/HOWTO.md`
- `research/research/malware/claude/MANIFEST_SHA256.txt`
- `research/research/malware/claude/README.md`
- `research/research/malware/claude/tools/scripts/zeid_data_ci_block_risky_claude_config.ps1`
- `research/research/malware/claude/tools/scripts/zeid_data_ci_block_risky_claude_config.sh`
- `projects/active/zeid_data_cloak_check/HOWTO.md`
- `projects/active/zeid_data_cloak_check/README.md`
- `projects/active/zeid_data_cloak_check/zeid_data_cloak_checking_email.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/HOWTO.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/README.md`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/tools/scripts/bundle_evidence.py`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/tools/scripts/generate_coverage_report.py`
- `projects/active/zeid_data_nist_gen_ai_evidence_pack/tools/scripts/validate_events.py`
- `tools/tools/scripts/README.md`
- `tools/tools/scripts/automation/README.md`
- `research/research/white-papers/README.md`

### `templates/`
- `README.md`
- `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/HOWTO.md`
- `content/vendors/island/README.md`
- `content/vendors/sentinelone/README.md`
- `docs/guides/index.md`
- `docs/guides/standards/evidence.md`
- `docs/guides/standards/repository-structure.md`
- `docs/guides/taxonomy.md`
- `projects/active/zeid_data_cloak_check/README.md`
- `projects/active/zeid_data_cloak_check/checklists/zeid_data_evidence_bundle_template.md`
- `projects/active/zeid_data_cloak_check/zeid_data_cloak_checking_email.md`
- `research/research/white-papers/README.md`

### `research/research/white-papers/`
- `README.md`
- `docs/guides/standards/repository-structure.md`

### `workbooks/`
- `README.md`
- `docs/guides/index.md`
- `docs/guides/standards/naming.md`
- `docs/guides/standards/repository-structure.md`
- `docs/guides/taxonomy.md`
- `research/research/malware/README.md`
- `research/research/white-papers/README.md`

## Recommended execution path

1. Review `docs/repo/restructure-map.json`.
2. Move files on a dedicated branch.
3. Rewrite Markdown links and known path references.
4. Run tests, link checks, and README image checks.
5. Commit as one restructure commit.
6. Keep old path compatibility notes in the root README if needed.
