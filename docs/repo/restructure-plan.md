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

- `media/readme_banners/content.svg` -> `assets/banners/readme/content.svg`
- `media/readme_banners/content_cisco.svg` -> `assets/banners/readme/content_cisco.svg`
- `media/readme_banners/content_crowdstrike.svg` -> `assets/banners/readme/content_crowdstrike.svg`
- `media/readme_banners/content_crowdstrike_crowdstrike_falcon_ai_governance.svg` -> `assets/banners/readme/content_crowdstrike_crowdstrike_falcon_ai_governance.svg`
- `media/readme_banners/content_crowdstrike_crowdstrike_falcon_audit_evidence_noise_reduction.svg` -> `assets/banners/readme/content_crowdstrike_crowdstrike_falcon_audit_evidence_noise_reduction.svg`
- `media/readme_banners/content_crowdstrike_crowdstrike_falcon_claude_bot_detection.svg` -> `assets/banners/readme/content_crowdstrike_crowdstrike_falcon_claude_bot_detection.svg`
- `media/readme_banners/content_island.svg` -> `assets/banners/readme/content_island.svg`
- `media/readme_banners/content_island_zeid_data_elk_stack_connector.svg` -> `assets/banners/readme/content_island_zeid_data_elk_stack_connector.svg`
- `media/readme_banners/content_island_zeid_data_evidence_bundle.svg` -> `assets/banners/readme/content_island_zeid_data_evidence_bundle.svg`
- `media/readme_banners/content_sentinelone.svg` -> `assets/banners/readme/content_sentinelone.svg`
- `media/readme_banners/content_sentinelone_soc2_content.svg` -> `assets/banners/readme/content_sentinelone_soc2_content.svg`
- `media/readme_banners/content_snowflake.svg` -> `assets/banners/readme/content_snowflake.svg`
- `media/readme_banners/content_splunk.svg` -> `assets/banners/readme/content_splunk.svg`
- `media/readme_banners/content_splunk_zeid_data_claude_bot_content.svg` -> `assets/banners/readme/content_splunk_zeid_data_claude_bot_content.svg`
- `media/readme_banners/content_splunk_zeid_data_splunk_app_exfil_watch.svg` -> `assets/banners/readme/content_splunk_zeid_data_splunk_app_exfil_watch.svg`
- `media/readme_banners/detections.svg` -> `assets/banners/readme/detections.svg`
- `media/readme_banners/detections_claude_bot.svg` -> `assets/banners/readme/detections_claude_bot.svg`
- `media/readme_banners/detections_cve_2025_20393.svg` -> `assets/banners/readme/detections_cve_2025_20393.svg`
- `media/readme_banners/detections_cve_2025_40551.svg` -> `assets/banners/readme/detections_cve_2025_40551.svg`
- `media/readme_banners/detections_cve_2026_24423.svg` -> `assets/banners/readme/detections_cve_2026_24423.svg`
- `media/readme_banners/detections_cve_2026_24858.svg` -> `assets/banners/readme/detections_cve_2026_24858.svg`
- `media/readme_banners/malware.svg` -> `assets/banners/readme/malware.svg`
- `media/readme_banners/malware_claude.svg` -> `assets/banners/readme/malware_claude.svg`
- `media/readme_banners/malware_promptflux_fruitshell.svg` -> `assets/banners/readme/malware_promptflux_fruitshell.svg`
- `media/readme_banners/media.svg` -> `assets/banners/readme/media.svg`
- `media/readme_banners/projects_zeid_data_ai_guard.svg` -> `assets/banners/readme/projects_zeid_data_ai_guard.svg`
- `media/readme_banners/projects_zeid_data_bruteforce_ssh.svg` -> `assets/banners/readme/projects_zeid_data_bruteforce_ssh.svg`
- `media/readme_banners/projects_zeid_data_cloak_check.svg` -> `assets/banners/readme/projects_zeid_data_cloak_check.svg`
- `media/readme_banners/projects_zeid_data_forensics_tools.svg` -> `assets/banners/readme/projects_zeid_data_forensics_tools.svg`
- `media/readme_banners/projects_zeid_data_forensics_tools_zeid_data_dfir_work_flow_trainer.svg` -> `assets/banners/readme/projects_zeid_data_forensics_tools_zeid_data_dfir_work_flow_trainer.svg`
- `media/readme_banners/projects_zeid_data_gap_check.svg` -> `assets/banners/readme/projects_zeid_data_gap_check.svg`
- `media/readme_banners/projects_zeid_data_net_ledger.svg` -> `assets/banners/readme/projects_zeid_data_net_ledger.svg`
- `media/readme_banners/projects_zeid_data_nist_gen_ai_evidence_pack.svg` -> `assets/banners/readme/projects_zeid_data_nist_gen_ai_evidence_pack.svg`
- `media/readme_banners/projects_zeid_data_qilin_ransomware_detection.svg` -> `assets/banners/readme/projects_zeid_data_qilin_ransomware_detection.svg`
- `media/readme_banners/projects_zeid_data_regex_security.svg` -> `assets/banners/readme/projects_zeid_data_regex_security.svg`
- `media/readme_banners/projects_zeid_data_stack_crasher.svg` -> `assets/banners/readme/projects_zeid_data_stack_crasher.svg`
- `media/readme_banners/scripts.svg` -> `assets/banners/readme/scripts.svg`
- `media/readme_banners/scripts_automation.svg` -> `assets/banners/readme/scripts_automation.svg`
- `media/readme_banners/scripts_automation_zeid_data_backup_verify.svg` -> `assets/banners/readme/scripts_automation_zeid_data_backup_verify.svg`
- `media/readme_banners/scripts_automation_zeid_data_dns_audit.svg` -> `assets/banners/readme/scripts_automation_zeid_data_dns_audit.svg`
- `media/readme_banners/scripts_automation_zeid_data_eventlog_export.svg` -> `assets/banners/readme/scripts_automation_zeid_data_eventlog_export.svg`
- `media/readme_banners/scripts_automation_zeid_data_host_reachability.svg` -> `assets/banners/readme/scripts_automation_zeid_data_host_reachability.svg`
- `media/readme_banners/scripts_automation_zeid_data_local_admin_audit.svg` -> `assets/banners/readme/scripts_automation_zeid_data_local_admin_audit.svg`
- `media/readme_banners/scripts_automation_zeid_data_log_summarizer_cpp.svg` -> `assets/banners/readme/scripts_automation_zeid_data_log_summarizer_cpp.svg`
- `media/readme_banners/scripts_automation_zeid_data_route_snapshot.svg` -> `assets/banners/readme/scripts_automation_zeid_data_route_snapshot.svg`
- `media/readme_banners/scripts_automation_zeid_data_service_health.svg` -> `assets/banners/readme/scripts_automation_zeid_data_service_health.svg`
- `media/readme_banners/scripts_automation_zeid_data_sha256_manifest_cpp.svg` -> `assets/banners/readme/scripts_automation_zeid_data_sha256_manifest_cpp.svg`
- `media/readme_banners/scripts_automation_zeid_data_tls_cert_expiry.svg` -> `assets/banners/readme/scripts_automation_zeid_data_tls_cert_expiry.svg`
- `media/readme_banners/scripts_inventory.svg` -> `assets/banners/readme/scripts_inventory.svg`
- `media/readme_banners/scripts_weekly_top_malware_detections_scripted.svg` -> `assets/banners/readme/scripts_weekly_top_malware_detections_scripted.svg`
- `media/readme_banners/templates.svg` -> `assets/banners/readme/templates.svg`
- `media/readme_banners/white_papers.svg` -> `assets/banners/readme/white_papers.svg`
- `media/readme_banners/workbooks.svg` -> `assets/banners/readme/workbooks.svg`
- `media/readme_banners/workbooks_security_operations_playbooks.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks.svg`
- `media/readme_banners/workbooks_security_operations_playbooks_aws.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_aws.svg`
- `media/readme_banners/workbooks_security_operations_playbooks_cisco.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_cisco.svg`
- `media/readme_banners/workbooks_security_operations_playbooks_crowdstrike.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_crowdstrike.svg`
- `media/readme_banners/workbooks_security_operations_playbooks_databricks.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_databricks.svg`
- `media/readme_banners/workbooks_security_operations_playbooks_google_workspace.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_google_workspace.svg`
- `media/readme_banners/workbooks_security_operations_playbooks_microsoft.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_microsoft.svg`
- `media/readme_banners/workbooks_security_operations_playbooks_okta.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_okta.svg`
- `media/readme_banners/workbooks_security_operations_playbooks_palo_alto_networks.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_palo_alto_networks.svg`
- `media/readme_banners/workbooks_security_operations_playbooks_snowflake.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_snowflake.svg`
- `media/readme_banners/workbooks_security_operations_playbooks_splunk.svg` -> `assets/banners/readme/workbooks_security_operations_playbooks_splunk.svg`

### `assets/images/`

- `media/5 Best Practices.png` -> `assets/images/5 Best Practices.png`
- `media/AIGovernance.png` -> `assets/images/AIGovernance.png`
- `media/DataCenterCleanUp.png` -> `assets/images/DataCenterCleanUp.png`
- `media/DataExfiltration.png` -> `assets/images/DataExfiltration.png`
- `media/HaveAGoodWeekend.png` -> `assets/images/HaveAGoodWeekend.png`
- `media/README.md` -> `assets/images/README.md`
- `media/brand/ClaudeBot.png` -> `assets/images/ClaudeBot.png`
- `media/brand/CrowdStrikeContentRelease.png` -> `assets/images/CrowdStrikeContentRelease.png`
- `media/brand/SnowflakeContentRelease.png` -> `assets/images/SnowflakeContentRelease.png`
- `media/brand/ZD Banner.png` -> `assets/images/ZD Banner.png`
- `media/brand/ZD_Dashboard.png` -> `assets/images/ZD_Dashboard.png`
- `media/brand/zeid_logo_round_fade.png` -> `assets/images/zeid_logo_round_fade.png`
- `media/ceo_coworker.png` -> `assets/images/ceo_coworker.png`
- `media/slamdunkyouraudit.png` -> `assets/images/slamdunkyouraudit.png`
- `media/zd_banner_1.png` -> `assets/images/zd_banner_1.png`
- `media/zd_banner_2.png` -> `assets/images/zd_banner_2.png`
- `media/zd_banner_3.png` -> `assets/images/zd_banner_3.png`

### `content/vendors/`

- `content/Cisco/Detections/ZeidData_Cisco_Detection_01_internet_facing_exploitation_attempt_kev_prioritized.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_01_internet_facing_exploitation_attempt_kev_prioritized.zip`
- `content/Cisco/Detections/ZeidData_Cisco_Detection_02_suspicious_remote_admin_access_vpn_ssh_rdp.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_02_suspicious_remote_admin_access_vpn_ssh_rdp.zip`
- `content/Cisco/Detections/ZeidData_Cisco_Detection_03_duo_mfa_fatigue_fraudulent_push_and_high_risk_auth.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_03_duo_mfa_fatigue_fraudulent_push_and_high_risk_auth.zip`
- `content/Cisco/Detections/ZeidData_Cisco_Detection_04_phishing_to_credential_harvest_correlation_email_dns.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_04_phishing_to_credential_harvest_correlation_email_dns.zip`
- `content/Cisco/Detections/ZeidData_Cisco_Detection_05_dns_tunneling_and_exfiltration_umbrella.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_05_dns_tunneling_and_exfiltration_umbrella.zip`
- `content/Cisco/Detections/ZeidData_Cisco_Detection_06_encrypted_dns_bypass_doh_dot_third_party_resolvers.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_06_encrypted_dns_bypass_doh_dot_third_party_resolvers.zip`
- `content/Cisco/Detections/ZeidData_Cisco_Detection_07_https_beaconing_c2_rare_domains_low_and_slow.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_07_https_beaconing_c2_rare_domains_low_and_slow.zip`
- `content/Cisco/Detections/ZeidData_Cisco_Detection_08_east_west_scanning_and_lateral_movement_netflow.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_08_east_west_scanning_and_lateral_movement_netflow.zip`
- `content/Cisco/Detections/ZeidData_Cisco_Detection_09_ransomware_staging_pre_encryption_secure_endpoint.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_09_ransomware_staging_pre_encryption_secure_endpoint.zip`
- `content/Cisco/Detections/ZeidData_Cisco_Detection_10_data_exfiltration_large_uploads_to_unsanctioned_cloud.zip` -> `content/vendors/cisco/Detections/ZeidData_Cisco_Detection_10_data_exfiltration_large_uploads_to_unsanctioned_cloud.zip`
- `content/Cisco/Detections/zeid_data_cisco-claude-firewall-endpoint-pack.zip` -> `content/vendors/cisco/Detections/zeid_data_cisco-claude-firewall-endpoint-pack.zip`
- `content/Cisco/PRE_REQ.md` -> `content/vendors/cisco/PRE_REQ.md`
- `content/Cisco/README.md` -> `content/vendors/cisco/README.md`
- `content/CrowdStrike/CrowdStrike Falcon AI Governance/HOWTO.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/HOWTO.md`
- `content/CrowdStrike/CrowdStrike Falcon AI Governance/LICENSE.txt` -> `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/LICENSE.txt`
- `content/CrowdStrike/CrowdStrike Falcon AI Governance/README.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/README.md`
- `content/CrowdStrike/CrowdStrike Falcon AI Governance/ZeidData_CrowdStrike_AI_Governance_Rules_Reports_Views_Filters_Package.zip` -> `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/ZeidData_CrowdStrike_AI_Governance_Rules_Reports_Views_Filters_Package.zip`
- `content/CrowdStrike/CrowdStrike Falcon AI Governance/manifest.yaml` -> `content/vendors/crowdstrike/CrowdStrike Falcon AI Governance/manifest.yaml`
- `content/CrowdStrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/HOWTO.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/HOWTO.md`
- `content/CrowdStrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/LICENSE.txt` -> `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/LICENSE.txt`
- `content/CrowdStrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/README.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/README.md`
- `content/CrowdStrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/Zeid_Data_Falcon_AuditEvidence_Noise_Reduction_Pack.zip` -> `content/vendors/crowdstrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/Zeid_Data_Falcon_AuditEvidence_Noise_Reduction_Pack.zip`
- `content/CrowdStrike/CrowdStrike Falcon Claude Bot Detection/HOWTO.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon Claude Bot Detection/HOWTO.md`
- `content/CrowdStrike/CrowdStrike Falcon Claude Bot Detection/README.md` -> `content/vendors/crowdstrike/CrowdStrike Falcon Claude Bot Detection/README.md`
- `content/CrowdStrike/CrowdStrike Falcon Claude Bot Detection/zeid_data_crowdstrike-claude-firewall-endpoint-pack.zip` -> `content/vendors/crowdstrike/CrowdStrike Falcon Claude Bot Detection/zeid_data_crowdstrike-claude-firewall-endpoint-pack.zip`
- `content/CrowdStrike/README.md` -> `content/vendors/crowdstrike/README.md`
- `content/Island/README.md` -> `content/vendors/island/README.md`
- `content/Island/zeid_data_elk_stack_connector/.env.example` -> `content/vendors/island/zeid_data_elk_stack_connector/.env.example`
- `content/Island/zeid_data_elk_stack_connector/HOWTO.md` -> `content/vendors/island/zeid_data_elk_stack_connector/HOWTO.md`
- `content/Island/zeid_data_elk_stack_connector/README.md` -> `content/vendors/island/zeid_data_elk_stack_connector/README.md`
- `content/Island/zeid_data_elk_stack_connector/docker-compose.yml` -> `content/vendors/island/zeid_data_elk_stack_connector/docker-compose.yml`
- `content/Island/zeid_data_elk_stack_connector/elastic/index-template-island.json` -> `content/vendors/island/zeid_data_elk_stack_connector/elastic/index-template-island.json`
- `content/Island/zeid_data_elk_stack_connector/examples/island_event_sample.json` -> `content/vendors/island/zeid_data_elk_stack_connector/examples/island_event_sample.json`
- `content/Island/zeid_data_elk_stack_connector/logstash/config/logstash.yml` -> `content/vendors/island/zeid_data_elk_stack_connector/logstash/config/logstash.yml`
- `content/Island/zeid_data_elk_stack_connector/logstash/pipeline/island-http.conf` -> `content/vendors/island/zeid_data_elk_stack_connector/logstash/pipeline/island-http.conf`
- `content/Island/zeid_data_elk_stack_connector/scripts/apply_index_template.sh` -> `content/vendors/island/zeid_data_elk_stack_connector/scripts/apply_index_template.sh`
- `content/Island/zeid_data_elk_stack_connector/scripts/generate_test_event.py` -> `content/vendors/island/zeid_data_elk_stack_connector/scripts/generate_test_event.py`
- `content/Island/zeid_data_elk_stack_connector/scripts/post_test_event.sh` -> `content/vendors/island/zeid_data_elk_stack_connector/scripts/post_test_event.sh`
- `content/Island/zeid_data_elk_stack_connector/training/KQL_QUERIES.md` -> `content/vendors/island/zeid_data_elk_stack_connector/training/KQL_QUERIES.md`
- `content/Island/zeid_data_elk_stack_connector/training/SCENARIOS.md` -> `content/vendors/island/zeid_data_elk_stack_connector/training/SCENARIOS.md`
- `content/Island/zeid_data_elk_stack_connector/training/screenshots/01_island_siem_settings_mock.png` -> `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/01_island_siem_settings_mock.png`
- `content/Island/zeid_data_elk_stack_connector/training/screenshots/02_logstash_ingest_mock.png` -> `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/02_logstash_ingest_mock.png`
- `content/Island/zeid_data_elk_stack_connector/training/screenshots/03_kibana_discover_mock.png` -> `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/03_kibana_discover_mock.png`
- `content/Island/zeid_data_elk_stack_connector/training/screenshots/04_kibana_dashboard_mock.png` -> `content/vendors/island/zeid_data_elk_stack_connector/training/screenshots/04_kibana_dashboard_mock.png`
- `content/Island/zeid_data_evidence_bundle/HOWTO.md` -> `content/vendors/island/zeid_data_evidence_bundle/HOWTO.md`
- `content/Island/zeid_data_evidence_bundle/README.md` -> `content/vendors/island/zeid_data_evidence_bundle/README.md`
- `content/Island/zeid_data_evidence_bundle/zeid_data_bundle_schema.json` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_bundle_schema.json`
- `content/Island/zeid_data_evidence_bundle/zeid_data_collect.py` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_collect.py`
- `content/Island/zeid_data_evidence_bundle/zeid_data_config.example.yaml` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_config.example.yaml`
- `content/Island/zeid_data_evidence_bundle/zeid_data_env.example` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_env.example`
- `content/Island/zeid_data_evidence_bundle/zeid_data_evidence_bundle_spec.md` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_evidence_bundle_spec.md`
- `content/Island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_island_policies.jsonl` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_island_policies.jsonl`
- `content/Island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_island_users.jsonl` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_island_users.jsonl`
- `content/Island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_manifest.json` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_examples/zeid_data_example_manifest.json`
- `content/Island/zeid_data_evidence_bundle/zeid_data_gitignore` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_gitignore`
- `content/Island/zeid_data_evidence_bundle/zeid_data_island_client.py` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_island_client.py`
- `content/Island/zeid_data_evidence_bundle/zeid_data_make_bundle.py` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_data_make_bundle.py`
- `content/Island/zeid_data_evidence_bundle/zeid_datapip_requirements.txt` -> `content/vendors/island/zeid_data_evidence_bundle/zeid_datapip_requirements.txt`
- `content/SentinelOne/README.md` -> `content/vendors/sentinelone/README.md`
- `content/SentinelOne/SOC2_Content/HOWTO.md` -> `content/vendors/sentinelone/SOC2_Content/HOWTO.md`
- `content/SentinelOne/SOC2_Content/README.md` -> `content/vendors/sentinelone/SOC2_Content/README.md`
- `content/SentinelOne/SOC2_Content/Zeid Data_sentinel_soc2_workbook_multi_source.workbook` -> `content/vendors/sentinelone/SOC2_Content/Zeid Data_sentinel_soc2_workbook_multi_source.workbook`
- `content/SentinelOne/SOC2_Content/Zeid Data_sentinel_soc2_workbook_multi_source_arm.json` -> `content/vendors/sentinelone/SOC2_Content/Zeid Data_sentinel_soc2_workbook_multi_source_arm.json`
- `content/Snowflake/Base_AI_Queries` -> `content/vendors/snowflake/Base_AI_Queries`
- `content/Snowflake/HOWTO.md` -> `content/vendors/snowflake/HOWTO.md`
- `content/Snowflake/LICENSE` -> `content/vendors/snowflake/LICENSE`
- `content/Snowflake/README.md` -> `content/vendors/snowflake/README.md`
- `content/Snowflake/zeid_data_snowflake-ai-governance-compliance-pack.zip` -> `content/vendors/snowflake/zeid_data_snowflake-ai-governance-compliance-pack.zip`
- `content/Splunk/README.md` -> `content/vendors/README.md`
- `content/Splunk/SPL_Top 10 Threat Hunts (AD + ASA + CrowdStrike)` -> `content/vendors/SPL_Top 10 Threat Hunts (AD + ASA + CrowdStrike)`
- `content/Splunk/YAML.md` -> `content/vendors/YAML.md`
- `content/Splunk/Zeid Data Claude Bot Content/HOWTO.md` -> `content/vendors/Zeid Data Claude Bot Content/HOWTO.md`
- `content/Splunk/Zeid Data Claude Bot Content/README.md` -> `content/vendors/Zeid Data Claude Bot Content/README.md`
- `content/Splunk/Zeid Data Claude Bot Content/zeid_data_splunk-claude-firewall-endpoint-pack.zip` -> `content/vendors/Zeid Data Claude Bot Content/zeid_data_splunk-claude-firewall-endpoint-pack.zip`
- `content/Splunk/Zeid Data Splunk App - Exfil Watch/HOWTO.md` -> `content/vendors/Zeid Data Splunk App - Exfil Watch/HOWTO.md`
- `content/Splunk/Zeid Data Splunk App - Exfil Watch/README.md` -> `content/vendors/Zeid Data Splunk App - Exfil Watch/README.md`
- `content/Splunk/Zeid Data Splunk App - Exfil Watch/ZeidData_Splunk_Exfil_Monitor_App.zip` -> `content/vendors/Zeid Data Splunk App - Exfil Watch/ZeidData_Splunk_Exfil_Monitor_App.zip`
- `content/Splunk/savedsearches.conf` -> `content/vendors/savedsearches.conf`

### `detections/vendor-packs/`

- `detections/README.md` -> `detections/vendor-packs/README.md`
- `detections/claude_bot/README.md` -> `detections/vendor-packs/claude_bot/README.md`
- `detections/claude_bot/zeid_data_claude_detection` -> `detections/vendor-packs/claude_bot/zeid_data_claude_detection`
- `detections/cve-2025-20393/README.md` -> `detections/vendor-packs/cve-2025-20393/README.md`
- `detections/cve-2025-20393/zeid_data_cisco_cve-2025-20393-detection-package.zip` -> `detections/vendor-packs/cve-2025-20393/zeid_data_cisco_cve-2025-20393-detection-package.zip`
- `detections/cve-2025-40551/HOWTO.md` -> `detections/vendor-packs/cve-2025-40551/HOWTO.md`
- `detections/cve-2025-40551/LICENSE` -> `detections/vendor-packs/cve-2025-40551/LICENSE`
- `detections/cve-2025-40551/README.md` -> `detections/vendor-packs/cve-2025-40551/README.md`
- `detections/cve-2025-40551/test.txt` -> `detections/vendor-packs/cve-2025-40551/test.txt`
- `detections/cve-2025-40551/zeid_data_CVE-2025-40551.py` -> `detections/vendor-packs/cve-2025-40551/zeid_data_CVE-2025-40551.py`
- `detections/cve-2026-24423/HOWTO.md` -> `detections/vendor-packs/cve-2026-24423/HOWTO.md`
- `detections/cve-2026-24423/LICENSE` -> `detections/vendor-packs/cve-2026-24423/LICENSE`
- `detections/cve-2026-24423/README.md` -> `detections/vendor-packs/cve-2026-24423/README.md`
- `detections/cve-2026-24423/zeid_data_CVE-2026-24423.py` -> `detections/vendor-packs/cve-2026-24423/zeid_data_CVE-2026-24423.py`
- `detections/cve-2026-24858/HOWTO.md` -> `detections/vendor-packs/cve-2026-24858/HOWTO.md`
- `detections/cve-2026-24858/LICENSE` -> `detections/vendor-packs/cve-2026-24858/LICENSE`
- `detections/cve-2026-24858/README.md` -> `detections/vendor-packs/cve-2026-24858/README.md`
- `detections/cve-2026-24858/zeid_data_CVE-2026-24858.py` -> `detections/vendor-packs/cve-2026-24858/zeid_data_CVE-2026-24858.py`

### `docs/guides/`

- `docs/index.md` -> `docs/guides/index.md`
- `docs/profile-readme.md` -> `docs/guides/profile-readme.md`
- `docs/standards/evidence.md` -> `docs/guides/standards/evidence.md`
- `docs/standards/naming.md` -> `docs/guides/standards/naming.md`
- `docs/standards/repository-structure.md` -> `docs/guides/standards/repository-structure.md`
- `docs/taxonomy.md` -> `docs/guides/taxonomy.md`

### `projects/active/`

- `projects/zeid_data_ai_guard/HOWTO.md` -> `projects/active/zeid_data_ai_guard/HOWTO.md`
- `projects/zeid_data_ai_guard/LICENSE` -> `projects/active/zeid_data_ai_guard/LICENSE`
- `projects/zeid_data_ai_guard/README.md` -> `projects/active/zeid_data_ai_guard/README.md`
- `projects/zeid_data_ai_guard/SECURITY.md` -> `projects/active/zeid_data_ai_guard/SECURITY.md`
- `projects/zeid_data_ai_guard/Zeid Data GenAIGuard.zip` -> `projects/active/zeid_data_ai_guard/Zeid Data GenAIGuard.zip`
- `projects/zeid_data_ai_guard/pyproject.toml` -> `projects/active/zeid_data_ai_guard/pyproject.toml`
- `projects/zeid_data_bruteforce_ssh/README.md` -> `projects/active/zeid_data_bruteforce_ssh/README.md`
- `projects/zeid_data_bruteforce_ssh/ZD_SSH Brute Force` -> `projects/active/zeid_data_bruteforce_ssh/ZD_SSH Brute Force`
- `projects/zeid_data_cloak_check/HOWTO.md` -> `projects/active/zeid_data_cloak_check/HOWTO.md`
- `projects/zeid_data_cloak_check/LICENSE.txt` -> `projects/active/zeid_data_cloak_check/LICENSE.txt`
- `projects/zeid_data_cloak_check/README.md` -> `projects/active/zeid_data_cloak_check/README.md`
- `projects/zeid_data_cloak_check/checklists/zeid_data_cloakcheck_scorecard.md` -> `projects/active/zeid_data_cloak_check/checklists/zeid_data_cloakcheck_scorecard.md`
- `projects/zeid_data_cloak_check/checklists/zeid_data_evidence_bundle_template.md` -> `projects/active/zeid_data_cloak_check/checklists/zeid_data_evidence_bundle_template.md`
- `projects/zeid_data_cloak_check/data/zeid_data_sample_proxy_logs.csv` -> `projects/active/zeid_data_cloak_check/data/zeid_data_sample_proxy_logs.csv`
- `projects/zeid_data_cloak_check/data/zeid_data_sample_redirect_telemetry.jsonl` -> `projects/active/zeid_data_cloak_check/data/zeid_data_sample_redirect_telemetry.jsonl`
- `projects/zeid_data_cloak_check/detections/zeid_data_elastic_esql_cloakcheck.esql` -> `projects/active/zeid_data_cloak_check/detections/zeid_data_elastic_esql_cloakcheck.esql`
- `projects/zeid_data_cloak_check/detections/zeid_data_elastic_kql_cloakcheck.txt` -> `projects/active/zeid_data_cloak_check/detections/zeid_data_elastic_kql_cloakcheck.txt`
- `projects/zeid_data_cloak_check/detections/zeid_data_sentinel_cloakcheck.kql` -> `projects/active/zeid_data_cloak_check/detections/zeid_data_sentinel_cloakcheck.kql`
- `projects/zeid_data_cloak_check/detections/zeid_data_sigma_cloaked_phishing.yml` -> `projects/active/zeid_data_cloak_check/detections/zeid_data_sigma_cloaked_phishing.yml`
- `projects/zeid_data_cloak_check/detections/zeid_data_splunk_cloakcheck.spl` -> `projects/active/zeid_data_cloak_check/detections/zeid_data_splunk_cloakcheck.spl`
- `projects/zeid_data_cloak_check/requirements.txt` -> `projects/active/zeid_data_cloak_check/requirements.txt`
- `projects/zeid_data_cloak_check/scripts/zeid_data_compare_runs.py` -> `projects/active/zeid_data_cloak_check/scripts/zeid_data_compare_runs.py`
- `projects/zeid_data_cloak_check/scripts/zeid_data_differential_fetch.py` -> `projects/active/zeid_data_cloak_check/scripts/zeid_data_differential_fetch.py`
- `projects/zeid_data_cloak_check/scripts/zeid_data_urls_sample.txt` -> `projects/active/zeid_data_cloak_check/scripts/zeid_data_urls_sample.txt`
- `projects/zeid_data_cloak_check/templates/zeid_data_ioc_schema.csv` -> `projects/active/zeid_data_cloak_check/templates/zeid_data_ioc_schema.csv`
- `projects/zeid_data_cloak_check/templates/zeid_data_ioc_schema.json` -> `projects/active/zeid_data_cloak_check/templates/zeid_data_ioc_schema.json`
- `projects/zeid_data_cloak_check/templates/zeid_data_stix_bundle_example.json` -> `projects/active/zeid_data_cloak_check/templates/zeid_data_stix_bundle_example.json`
- `projects/zeid_data_cloak_check/zeid_data_cloak_checking_email.md` -> `projects/active/zeid_data_cloak_check/zeid_data_cloak_checking_email.md`
- `projects/zeid_data_forensics_tools/README.md` -> `projects/active/zeid_data_forensics_tools/README.md`
- `projects/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/INSTRUCTOR_GUIDE.md` -> `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/INSTRUCTOR_GUIDE.md`
- `projects/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/README.md` -> `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/README.md`
- `projects/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/SECURITY.md` -> `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/SECURITY.md`
- `projects/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/run_tests.sh` -> `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/run_tests.sh`
- `projects/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/zeid_data_drt.zip` -> `projects/active/zeid_data_forensics_tools/Zeid Data DFIR Work Flow Trainer/zeid_data_drt.zip`
- `projects/zeid_data_gap_check/HOWTO.md` -> `projects/active/zeid_data_gap_check/HOWTO.md`
- `projects/zeid_data_gap_check/LICENSE` -> `projects/active/zeid_data_gap_check/LICENSE`
- `projects/zeid_data_gap_check/README.md` -> `projects/active/zeid_data_gap_check/README.md`
- `projects/zeid_data_gap_check/Zeid_Data_GapCheck.zip` -> `projects/active/zeid_data_gap_check/Zeid_Data_GapCheck.zip`
- `projects/zeid_data_gap_check/gapcheck.py` -> `projects/active/zeid_data_gap_check/gapcheck.py`
- `projects/zeid_data_gap_check/policy.sample.json` -> `projects/active/zeid_data_gap_check/policy.sample.json`
- `projects/zeid_data_gap_check/requirements.txt` -> `projects/active/zeid_data_gap_check/requirements.txt`
- `projects/zeid_data_net_ledger/README.md` -> `projects/active/zeid_data_net_ledger/README.md`
- `projects/zeid_data_net_ledger/Zeid Data NetLedger` -> `projects/active/zeid_data_net_ledger/Zeid Data NetLedger`
- `projects/zeid_data_nist_gen_ai_evidence_pack/.gitignore` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/.gitignore`
- `projects/zeid_data_nist_gen_ai_evidence_pack/HOWTO.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/HOWTO.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/LICENSE` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/LICENSE`
- `projects/zeid_data_nist_gen_ai_evidence_pack/README.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/README.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_control_matrix.csv` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_control_matrix.csv`
- `projects/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_control_matrix.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_control_matrix.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_model_system_card_template.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_model_system_card_template.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_risk_register_template.csv` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_risk_register_template.csv`
- `projects/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_vendor_questionnaire.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/controls/zeid_data_vendor_questionnaire.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/diagrams/zeid_data_ai_governance_architecture.mmd` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/diagrams/zeid_data_ai_governance_architecture.mmd`
- `projects/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_ai_event_schema.json` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_ai_event_schema.json`
- `projects/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_ai_event_schema.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_ai_event_schema.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_elastic_ingest_pipeline.json` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_elastic_ingest_pipeline.json`
- `projects/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_splunk_props.conf` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_splunk_props.conf`
- `projects/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_splunk_transforms.conf` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/logging/zeid_data_splunk_transforms.conf`
- `projects/zeid_data_nist_gen_ai_evidence_pack/policies/zeid_data_ai_policy_minimum.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/policies/zeid_data_ai_policy_minimum.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/requirements.txt` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/requirements.txt`
- `projects/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_ai_events.jsonl` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_ai_events.jsonl`
- `projects/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_risk_register.csv` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_risk_register.csv`
- `projects/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_system_card.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/sample_data/sample_system_card.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/scripts/bundle_evidence.py` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/scripts/bundle_evidence.py`
- `projects/zeid_data_nist_gen_ai_evidence_pack/scripts/generate_coverage_report.py` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/scripts/generate_coverage_report.py`
- `projects/zeid_data_nist_gen_ai_evidence_pack/scripts/validate_events.py` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/scripts/validate_events.py`
- `projects/zeid_data_nist_gen_ai_evidence_pack/zeid_data_ai_governance.md` -> `projects/active/zeid_data_nist_gen_ai_evidence_pack/zeid_data_ai_governance.md`
- `projects/zeid_data_qilin_ransomware_detection/HOWTO.md` -> `projects/active/zeid_data_qilin_ransomware_detection/HOWTO.md`
- `projects/zeid_data_qilin_ransomware_detection/README.md` -> `projects/active/zeid_data_qilin_ransomware_detection/README.md`
- `projects/zeid_data_qilin_ransomware_detection/qilin_ransomware_scanner` -> `projects/active/zeid_data_qilin_ransomware_detection/qilin_ransomware_scanner`
- `projects/zeid_data_regex_security/HOWTO.md` -> `projects/active/zeid_data_regex_security/HOWTO.md`
- `projects/zeid_data_regex_security/LICENSE.md` -> `projects/active/zeid_data_regex_security/LICENSE.md`
- `projects/zeid_data_regex_security/README.md` -> `projects/active/zeid_data_regex_security/README.md`
- `projects/zeid_data_regex_security/zeid_data_broken_vs_safe_regex_examples.md` -> `projects/active/zeid_data_regex_security/zeid_data_broken_vs_safe_regex_examples.md`
- `projects/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_auth_anchor_grouping_bypass_samples.jsonl` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_auth_anchor_grouping_bypass_samples.jsonl`
- `projects/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_filename_extension_bypass_samples.jsonl` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_filename_extension_bypass_samples.jsonl`
- `projects/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_ip_literal_unescaped_dot_samples.log` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_ip_literal_unescaped_dot_samples.log`
- `projects/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_kv_greedy_overcapture_samples.log` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_kv_greedy_overcapture_samples.log`
- `projects/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_payload_samples.log` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_payload_samples.log`
- `projects/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_proxy_url_allowlist_trap_samples.csv` -> `projects/active/zeid_data_regex_security/zeid_data_exploitable_log_samples/zeid_data_proxy_url_allowlist_trap_samples.csv`
- ... 8 more

### `research/malware/`

- `malware/README.md` -> `research/malware/README.md`
- `malware/claude/HOWTO.md` -> `research/malware/claude/HOWTO.md`
- `malware/claude/LICENSE` -> `research/malware/claude/LICENSE`
- `malware/claude/MANIFEST_SHA256.txt` -> `research/malware/claude/MANIFEST_SHA256.txt`
- `malware/claude/README.md` -> `research/malware/claude/README.md`
- `malware/claude/detections/sigma/zeid_data_claude_code_baseurl_env_override.yml` -> `research/malware/claude/detections/sigma/zeid_data_claude_code_baseurl_env_override.yml`
- `malware/claude/detections/sigma/zeid_data_claude_code_shell_spawn.yml` -> `research/malware/claude/detections/sigma/zeid_data_claude_code_shell_spawn.yml`
- `malware/claude/detections/sigma/zeid_data_claude_code_suspicious_config_change.yml` -> `research/malware/claude/detections/sigma/zeid_data_claude_code_suspicious_config_change.yml`
- `malware/claude/detections/yara/zeid_data_claude_code_config_risky_strings.yar` -> `research/malware/claude/detections/yara/zeid_data_claude_code_config_risky_strings.yar`
- `malware/claude/queries/sentinel/zeid_data_mde_file_events_claude_config.kql` -> `research/malware/claude/queries/sentinel/zeid_data_mde_file_events_claude_config.kql`
- `malware/claude/queries/sentinel/zeid_data_mde_network_unexpected_from_claude.kql` -> `research/malware/claude/queries/sentinel/zeid_data_mde_network_unexpected_from_claude.kql`
- `malware/claude/queries/sentinel/zeid_data_mde_process_shell_from_claude.kql` -> `research/malware/claude/queries/sentinel/zeid_data_mde_process_shell_from_claude.kql`
- `malware/claude/queries/splunk/zeid_data_file_change_claude_config.spl` -> `research/malware/claude/queries/splunk/zeid_data_file_change_claude_config.spl`
- `malware/claude/queries/splunk/zeid_data_network_unexpected_from_claude.spl` -> `research/malware/claude/queries/splunk/zeid_data_network_unexpected_from_claude.spl`
- `malware/claude/queries/splunk/zeid_data_process_shell_from_claude.spl` -> `research/malware/claude/queries/splunk/zeid_data_process_shell_from_claude.spl`
- `malware/claude/scripts/zeid_data_ci_block_risky_claude_config.ps1` -> `research/malware/claude/scripts/zeid_data_ci_block_risky_claude_config.ps1`
- `malware/claude/scripts/zeid_data_ci_block_risky_claude_config.sh` -> `research/malware/claude/scripts/zeid_data_ci_block_risky_claude_config.sh`
- `malware/promptflux_fruitshell/HOWTO.md` -> `research/malware/promptflux_fruitshell/HOWTO.md`
- `malware/promptflux_fruitshell/LICENSE.md` -> `research/malware/promptflux_fruitshell/LICENSE.md`
- `malware/promptflux_fruitshell/README.md` -> `research/malware/promptflux_fruitshell/README.md`
- `malware/promptflux_fruitshell/zeid_data_crowdstrike_deployment_steps.md` -> `research/malware/promptflux_fruitshell/zeid_data_crowdstrike_deployment_steps.md`
- `malware/promptflux_fruitshell/zeid_data_crowdstrike_detections.md` -> `research/malware/promptflux_fruitshell/zeid_data_crowdstrike_detections.md`
- `malware/promptflux_fruitshell/zeid_data_crowdstrike_overview.md` -> `research/malware/promptflux_fruitshell/zeid_data_crowdstrike_overview.md`
- `malware/promptflux_fruitshell/zeid_data_crowdstrike_queries.txt` -> `research/malware/promptflux_fruitshell/zeid_data_crowdstrike_queries.txt`
- `malware/promptflux_fruitshell/zeid_data_crowdstrike_tuning_guidance.md` -> `research/malware/promptflux_fruitshell/zeid_data_crowdstrike_tuning_guidance.md`
- `malware/promptflux_fruitshell/zeid_data_detection_strategy.md` -> `research/malware/promptflux_fruitshell/zeid_data_detection_strategy.md`
- `malware/promptflux_fruitshell/zeid_data_executive_summary.md` -> `research/malware/promptflux_fruitshell/zeid_data_executive_summary.md`
- `malware/promptflux_fruitshell/zeid_data_false_positive_guidance.md` -> `research/malware/promptflux_fruitshell/zeid_data_false_positive_guidance.md`
- `malware/promptflux_fruitshell/zeid_data_iocs.csv` -> `research/malware/promptflux_fruitshell/zeid_data_iocs.csv`
- `malware/promptflux_fruitshell/zeid_data_microsoft_deployment_steps.md` -> `research/malware/promptflux_fruitshell/zeid_data_microsoft_deployment_steps.md`
- `malware/promptflux_fruitshell/zeid_data_microsoft_detections.md` -> `research/malware/promptflux_fruitshell/zeid_data_microsoft_detections.md`
- `malware/promptflux_fruitshell/zeid_data_microsoft_overview.md` -> `research/malware/promptflux_fruitshell/zeid_data_microsoft_overview.md`
- `malware/promptflux_fruitshell/zeid_data_microsoft_queries.txt` -> `research/malware/promptflux_fruitshell/zeid_data_microsoft_queries.txt`
- `malware/promptflux_fruitshell/zeid_data_microsoft_tuning_guidance.md` -> `research/malware/promptflux_fruitshell/zeid_data_microsoft_tuning_guidance.md`
- `malware/promptflux_fruitshell/zeid_data_mitre_mapping.md` -> `research/malware/promptflux_fruitshell/zeid_data_mitre_mapping.md`
- `malware/promptflux_fruitshell/zeid_data_references.md` -> `research/malware/promptflux_fruitshell/zeid_data_references.md`
- `malware/promptflux_fruitshell/zeid_data_splunk_deployment_steps.md` -> `research/malware/promptflux_fruitshell/zeid_data_splunk_deployment_steps.md`
- `malware/promptflux_fruitshell/zeid_data_splunk_detections.md` -> `research/malware/promptflux_fruitshell/zeid_data_splunk_detections.md`
- `malware/promptflux_fruitshell/zeid_data_splunk_overview.md` -> `research/malware/promptflux_fruitshell/zeid_data_splunk_overview.md`
- `malware/promptflux_fruitshell/zeid_data_splunk_queries.txt` -> `research/malware/promptflux_fruitshell/zeid_data_splunk_queries.txt`
- `malware/promptflux_fruitshell/zeid_data_splunk_tuning_guidance.md` -> `research/malware/promptflux_fruitshell/zeid_data_splunk_tuning_guidance.md`
- `malware/promptflux_fruitshell/zeid_data_threat_overview.md` -> `research/malware/promptflux_fruitshell/zeid_data_threat_overview.md`
- `malware/promptflux_fruitshell/zeid_data_triage_checklist.md` -> `research/malware/promptflux_fruitshell/zeid_data_triage_checklist.md`
- `malware/qilin/Qilin_Ransomware Scanner.py` -> `research/malware/qilin/Qilin_Ransomware Scanner.py`

### `research/white-papers/`

- `white_papers/README.md` -> `research/white-papers/README.md`
- `white_papers/SECURITY.md` -> `research/white-papers/SECURITY.md`
- `white_papers/controls/zeid_data_ai_governance.md` -> `research/white-papers/controls/zeid_data_ai_governance.md`
- `white_papers/controls/zeid_data_broken_vs_safe_regex_examples.md` -> `research/white-papers/controls/zeid_data_broken_vs_safe_regex_examples.md`
- `white_papers/controls/zeid_data_regex_security.md` -> `research/white-papers/controls/zeid_data_regex_security.md`
- `white_papers/detections/zeid_data_akira_ransomware_detection_report.md` -> `research/white-papers/detections/zeid_data_akira_ransomware_detection_report.md`
- `white_papers/detections/zeid_data_black_basta_detection_report.md` -> `research/white-papers/detections/zeid_data_black_basta_detection_report.md`
- `white_papers/detections/zeid_data_cl0p_data_extortion_detection_report.md` -> `research/white-papers/detections/zeid_data_cl0p_data_extortion_detection_report.md`
- `white_papers/detections/zeid_data_cve_2025_22225_vmware_esxi_detection_report.md` -> `research/white-papers/detections/zeid_data_cve_2025_22225_vmware_esxi_detection_report.md`
- `white_papers/detections/zeid_data_cve_2025_34026_versa_concerto_auth_bypass_detection_report.md` -> `research/white-papers/detections/zeid_data_cve_2025_34026_versa_concerto_auth_bypass_detection_report.md`
- `white_papers/detections/zeid_data_cve_2025_68645_zimbra_rfi_detection_report.md` -> `research/white-papers/detections/zeid_data_cve_2025_68645_zimbra_rfi_detection_report.md`
- `white_papers/detections/zeid_data_cve_2025_8110_gogs_rce_detection_report.md` -> `research/white-papers/detections/zeid_data_cve_2025_8110_gogs_rce_detection_report.md`
- `white_papers/detections/zeid_data_cve_2026_21509_office_bypass_detection_report.md` -> `research/white-papers/detections/zeid_data_cve_2026_21509_office_bypass_detection_report.md`
- `white_papers/detections/zeid_data_qilin_extortion_detection_report.md` -> `research/white-papers/detections/zeid_data_qilin_extortion_detection_report.md`
- `white_papers/detections/zeid_data_safepay_ransomware_detection_report.md` -> `research/white-papers/detections/zeid_data_safepay_ransomware_detection_report.md`

### `tools/scripts/`

- `scripts/README.md` -> `tools/scripts/README.md`
- `scripts/audit_dashboard_sources.py` -> `tools/scripts/audit_dashboard_sources.py`
- `scripts/automation/README.md` -> `tools/scripts/automation/README.md`
- `scripts/automation/zeid_data_backup_verify/HOWTO.md` -> `tools/scripts/automation/zeid_data_backup_verify/HOWTO.md`
- `scripts/automation/zeid_data_backup_verify/README.md` -> `tools/scripts/automation/zeid_data_backup_verify/README.md`
- `scripts/automation/zeid_data_backup_verify/zeid_data_backup_verify.py` -> `tools/scripts/automation/zeid_data_backup_verify/zeid_data_backup_verify.py`
- `scripts/automation/zeid_data_dns_audit/HOWTO.md` -> `tools/scripts/automation/zeid_data_dns_audit/HOWTO.md`
- `scripts/automation/zeid_data_dns_audit/README.md` -> `tools/scripts/automation/zeid_data_dns_audit/README.md`
- `scripts/automation/zeid_data_dns_audit/zeid_data_dns_audit.py` -> `tools/scripts/automation/zeid_data_dns_audit/zeid_data_dns_audit.py`
- `scripts/automation/zeid_data_eventlog_export/HOWTO.md` -> `tools/scripts/automation/zeid_data_eventlog_export/HOWTO.md`
- `scripts/automation/zeid_data_eventlog_export/README.md` -> `tools/scripts/automation/zeid_data_eventlog_export/README.md`
- `scripts/automation/zeid_data_eventlog_export/zeid_data_eventlog_export.ps1` -> `tools/scripts/automation/zeid_data_eventlog_export/zeid_data_eventlog_export.ps1`
- `scripts/automation/zeid_data_host_reachability/HOWTO.md` -> `tools/scripts/automation/zeid_data_host_reachability/HOWTO.md`
- `scripts/automation/zeid_data_host_reachability/README.md` -> `tools/scripts/automation/zeid_data_host_reachability/README.md`
- `scripts/automation/zeid_data_host_reachability/zeid_data_host_reachability.py` -> `tools/scripts/automation/zeid_data_host_reachability/zeid_data_host_reachability.py`
- `scripts/automation/zeid_data_local_admin_audit/HOWTO.md` -> `tools/scripts/automation/zeid_data_local_admin_audit/HOWTO.md`
- `scripts/automation/zeid_data_local_admin_audit/README.md` -> `tools/scripts/automation/zeid_data_local_admin_audit/README.md`
- `scripts/automation/zeid_data_local_admin_audit/zeid_data_local_admin_audit.ps1` -> `tools/scripts/automation/zeid_data_local_admin_audit/zeid_data_local_admin_audit.ps1`
- `scripts/automation/zeid_data_log_summarizer_cpp/HOWTO.md` -> `tools/scripts/automation/zeid_data_log_summarizer_cpp/HOWTO.md`
- `scripts/automation/zeid_data_log_summarizer_cpp/README.md` -> `tools/scripts/automation/zeid_data_log_summarizer_cpp/README.md`
- `scripts/automation/zeid_data_log_summarizer_cpp/zeid_data_log_summarizer.cpp` -> `tools/scripts/automation/zeid_data_log_summarizer_cpp/zeid_data_log_summarizer.cpp`
- `scripts/automation/zeid_data_route_snapshot/HOWTO.md` -> `tools/scripts/automation/zeid_data_route_snapshot/HOWTO.md`
- `scripts/automation/zeid_data_route_snapshot/README.md` -> `tools/scripts/automation/zeid_data_route_snapshot/README.md`
- `scripts/automation/zeid_data_route_snapshot/zeid_data_route_snapshot.py` -> `tools/scripts/automation/zeid_data_route_snapshot/zeid_data_route_snapshot.py`
- `scripts/automation/zeid_data_service_health/HOWTO.md` -> `tools/scripts/automation/zeid_data_service_health/HOWTO.md`
- `scripts/automation/zeid_data_service_health/README.md` -> `tools/scripts/automation/zeid_data_service_health/README.md`
- `scripts/automation/zeid_data_service_health/zeid_data_service_health.ps1` -> `tools/scripts/automation/zeid_data_service_health/zeid_data_service_health.ps1`
- `scripts/automation/zeid_data_sha256_manifest_cpp/HOWTO.md` -> `tools/scripts/automation/zeid_data_sha256_manifest_cpp/HOWTO.md`
- `scripts/automation/zeid_data_sha256_manifest_cpp/README.md` -> `tools/scripts/automation/zeid_data_sha256_manifest_cpp/README.md`
- `scripts/automation/zeid_data_sha256_manifest_cpp/zeid_data_sha256_manifest.cpp` -> `tools/scripts/automation/zeid_data_sha256_manifest_cpp/zeid_data_sha256_manifest.cpp`
- `scripts/automation/zeid_data_tls_cert_expiry/HOWTO.md` -> `tools/scripts/automation/zeid_data_tls_cert_expiry/HOWTO.md`
- `scripts/automation/zeid_data_tls_cert_expiry/README.md` -> `tools/scripts/automation/zeid_data_tls_cert_expiry/README.md`
- `scripts/automation/zeid_data_tls_cert_expiry/zeid_data_tls_cert_expiry.py` -> `tools/scripts/automation/zeid_data_tls_cert_expiry/zeid_data_tls_cert_expiry.py`
- `scripts/detection/zeid_data_Hunt-NewScheduledTasks.ps1` -> `tools/scripts/detection/zeid_data_Hunt-NewScheduledTasks.ps1`
- `scripts/detection/zeid_data_Hunt-RansomwarePreEncryptCommands.ps1` -> `tools/scripts/detection/zeid_data_Hunt-RansomwarePreEncryptCommands.ps1`
- `scripts/detection/zeid_data_Hunt-linux-staging.sh` -> `tools/scripts/detection/zeid_data_Hunt-linux-staging.sh`
- `scripts/detection/zeid_data_README.md` -> `tools/scripts/detection/zeid_data_README.md`
- `scripts/detection/zeid_data_detection_scripts.zip` -> `tools/scripts/detection/zeid_data_detection_scripts.zip`
- `scripts/detection/zeid_data_hunt_ransomware_fileshare.py` -> `tools/scripts/detection/zeid_data_hunt_ransomware_fileshare.py`
- `scripts/detection/zeid_data_sentinel_infostealer_browser_chain.kql` -> `tools/scripts/detection/zeid_data_sentinel_infostealer_browser_chain.kql`
- `scripts/detection/zeid_data_sentinel_ransomware_prep.kql` -> `tools/scripts/detection/zeid_data_sentinel_ransomware_prep.kql`
- `scripts/detection/zeid_data_sigma_ransomware_prep.yml` -> `tools/scripts/detection/zeid_data_sigma_ransomware_prep.yml`
- `scripts/detection/zeid_data_splunk_exfil_tools.spl` -> `tools/scripts/detection/zeid_data_splunk_exfil_tools.spl`
- `scripts/detection/zeid_data_yara_infostealer_browsercred_access.yar` -> `tools/scripts/detection/zeid_data_yara_infostealer_browsercred_access.yar`
- `scripts/detection/zeid_data_zeek_firstseen_largepost.zeek` -> `tools/scripts/detection/zeid_data_zeek_firstseen_largepost.zeek`
- `scripts/inventory/README.md` -> `tools/scripts/inventory/README.md`
- `scripts/inventory/zeid_data_inventory_bash.sh` -> `tools/scripts/inventory/zeid_data_inventory_bash.sh`
- `scripts/inventory/zeid_data_inventory_csharp.cs` -> `tools/scripts/inventory/zeid_data_inventory_csharp.cs`
- `scripts/inventory/zeid_data_inventory_go.go` -> `tools/scripts/inventory/zeid_data_inventory_go.go`
- `scripts/inventory/zeid_data_inventory_java.java` -> `tools/scripts/inventory/zeid_data_inventory_java.java`
- `scripts/inventory/zeid_data_inventory_node.js` -> `tools/scripts/inventory/zeid_data_inventory_node.js`
- `scripts/inventory/zeid_data_inventory_perl.pl` -> `tools/scripts/inventory/zeid_data_inventory_perl.pl`
- `scripts/inventory/zeid_data_inventory_powershell.ps1` -> `tools/scripts/inventory/zeid_data_inventory_powershell.ps1`
- `scripts/inventory/zeid_data_inventory_python.py` -> `tools/scripts/inventory/zeid_data_inventory_python.py`
- `scripts/inventory/zeid_data_inventory_ruby.rb` -> `tools/scripts/inventory/zeid_data_inventory_ruby.rb`
- `scripts/inventory/zeid_data_inventory_rust.rs` -> `tools/scripts/inventory/zeid_data_inventory_rust.rs`
- `scripts/inventory/zeid_data_network_inventory_scripts.zip` -> `tools/scripts/inventory/zeid_data_network_inventory_scripts.zip`
- `scripts/weekly_top_malware_detections_scripted/README.md` -> `tools/scripts/weekly_top_malware_detections_scripted/README.md`
- `scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-NewScheduledTasks.ps1` -> `tools/scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-NewScheduledTasks.ps1`
- `scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-RansomwarePreEncryptCommands.ps1` -> `tools/scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-RansomwarePreEncryptCommands.ps1`
- `scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-linux-staging.sh` -> `tools/scripts/weekly_top_malware_detections_scripted/zeid_data_Hunt-linux-staging.sh`
- `scripts/weekly_top_malware_detections_scripted/zeid_data_hunt_ransomware_fileshare.py` -> `tools/scripts/weekly_top_malware_detections_scripted/zeid_data_hunt_ransomware_fileshare.py`
- `scripts/weekly_top_malware_detections_scripted/zeid_data_sentinel_infostealer_browser_chain.kql` -> `tools/scripts/weekly_top_malware_detections_scripted/zeid_data_sentinel_infostealer_browser_chain.kql`
- `scripts/weekly_top_malware_detections_scripted/zeid_data_sentinel_ransomware_prep.kql` -> `tools/scripts/weekly_top_malware_detections_scripted/zeid_data_sentinel_ransomware_prep.kql`
- `scripts/weekly_top_malware_detections_scripted/zeid_data_sigma_ransomware_prep.yml` -> `tools/scripts/weekly_top_malware_detections_scripted/zeid_data_sigma_ransomware_prep.yml`
- `scripts/weekly_top_malware_detections_scripted/zeid_data_splunk_exfil_tools.spl` -> `tools/scripts/weekly_top_malware_detections_scripted/zeid_data_splunk_exfil_tools.spl`
- `scripts/weekly_top_malware_detections_scripted/zeid_data_yara_infostealer_browsercred_access.yar` -> `tools/scripts/weekly_top_malware_detections_scripted/zeid_data_yara_infostealer_browsercred_access.yar`
- `scripts/weekly_top_malware_detections_scripted/zeid_data_zeek_firstseen_largepost.zeek` -> `tools/scripts/weekly_top_malware_detections_scripted/zeid_data_zeek_firstseen_largepost.zeek`

### `tools/validators/`

- `scripts/automation/zeid_data_regex_safety_tester.py` -> `tools/validators/automation/zeid_data_regex_safety_tester.py`

### `workbooks/dashboards/`

- `workbooks/README.md` -> `workbooks/dashboards/README.md`
- `workbooks/Security Operations Playbooks/AWS/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB01_suspicious_authentication.md`
- `workbooks/Security Operations Playbooks/AWS/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/Security Operations Playbooks/AWS/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB03_privileged_change_or_admin_grant.md`
- `workbooks/Security Operations Playbooks/AWS/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB04_malicious_process_or_edr_detection.md`
- `workbooks/Security Operations Playbooks/AWS/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/Security Operations Playbooks/AWS/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB06_command_and_control_beaconing.md`
- `workbooks/Security Operations Playbooks/AWS/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB07_lateral_movement.md`
- `workbooks/Security Operations Playbooks/AWS/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB08_ransomware_or_destructive_activity.md`
- `workbooks/Security Operations Playbooks/AWS/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/Security Operations Playbooks/AWS/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/PB10_oauth_token_api_key_misuse.md`
- `workbooks/Security Operations Playbooks/AWS/README.md` -> `workbooks/dashboards/Security Operations Playbooks/AWS/README.md`
- `workbooks/Security Operations Playbooks/Cisco/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB01_suspicious_authentication.md`
- `workbooks/Security Operations Playbooks/Cisco/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/Security Operations Playbooks/Cisco/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB03_privileged_change_or_admin_grant.md`
- `workbooks/Security Operations Playbooks/Cisco/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB04_malicious_process_or_edr_detection.md`
- `workbooks/Security Operations Playbooks/Cisco/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/Security Operations Playbooks/Cisco/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB06_command_and_control_beaconing.md`
- `workbooks/Security Operations Playbooks/Cisco/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB07_lateral_movement.md`
- `workbooks/Security Operations Playbooks/Cisco/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB08_ransomware_or_destructive_activity.md`
- `workbooks/Security Operations Playbooks/Cisco/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/Security Operations Playbooks/Cisco/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/PB10_oauth_token_api_key_misuse.md`
- `workbooks/Security Operations Playbooks/Cisco/README.md` -> `workbooks/dashboards/Security Operations Playbooks/Cisco/README.md`
- `workbooks/Security Operations Playbooks/CrowdStrike/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB01_suspicious_authentication.md`
- `workbooks/Security Operations Playbooks/CrowdStrike/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/Security Operations Playbooks/CrowdStrike/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB03_privileged_change_or_admin_grant.md`
- `workbooks/Security Operations Playbooks/CrowdStrike/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB08_ransomware_or_destructive_activity.md`
- `workbooks/Security Operations Playbooks/CrowdStrike/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/Security Operations Playbooks/CrowdStrike/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/PB10_oauth_token_api_key_misuse.md`
- `workbooks/Security Operations Playbooks/CrowdStrike/README.md` -> `workbooks/dashboards/Security Operations Playbooks/CrowdStrike/README.md`
- `workbooks/Security Operations Playbooks/Databricks/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB01_suspicious_authentication.md`
- `workbooks/Security Operations Playbooks/Databricks/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/Security Operations Playbooks/Databricks/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB03_privileged_change_or_admin_grant.md`
- `workbooks/Security Operations Playbooks/Databricks/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB04_malicious_process_or_edr_detection.md`
- `workbooks/Security Operations Playbooks/Databricks/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/Security Operations Playbooks/Databricks/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB06_command_and_control_beaconing.md`
- `workbooks/Security Operations Playbooks/Databricks/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB07_lateral_movement.md`
- `workbooks/Security Operations Playbooks/Databricks/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB08_ransomware_or_destructive_activity.md`
- `workbooks/Security Operations Playbooks/Databricks/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/Security Operations Playbooks/Databricks/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/PB10_oauth_token_api_key_misuse.md`
- `workbooks/Security Operations Playbooks/Databricks/README.md` -> `workbooks/dashboards/Security Operations Playbooks/Databricks/README.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB01_suspicious_authentication.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB03_privileged_change_or_admin_grant.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB04_malicious_process_or_edr_detection.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB06_command_and_control_beaconing.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB07_lateral_movement.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB08_ransomware_or_destructive_activity.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/PB10_oauth_token_api_key_misuse.md`
- `workbooks/Security Operations Playbooks/Google_Workspace/README.md` -> `workbooks/dashboards/Security Operations Playbooks/Google_Workspace/README.md`
- `workbooks/Security Operations Playbooks/Microsoft/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB01_suspicious_authentication.md`
- `workbooks/Security Operations Playbooks/Microsoft/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/Security Operations Playbooks/Microsoft/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB03_privileged_change_or_admin_grant.md`
- `workbooks/Security Operations Playbooks/Microsoft/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB04_malicious_process_or_edr_detection.md`
- `workbooks/Security Operations Playbooks/Microsoft/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/Security Operations Playbooks/Microsoft/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB06_command_and_control_beaconing.md`
- `workbooks/Security Operations Playbooks/Microsoft/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB07_lateral_movement.md`
- `workbooks/Security Operations Playbooks/Microsoft/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB08_ransomware_or_destructive_activity.md`
- `workbooks/Security Operations Playbooks/Microsoft/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/Security Operations Playbooks/Microsoft/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/PB10_oauth_token_api_key_misuse.md`
- `workbooks/Security Operations Playbooks/Microsoft/README.md` -> `workbooks/dashboards/Security Operations Playbooks/Microsoft/README.md`
- `workbooks/Security Operations Playbooks/Okta/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB01_suspicious_authentication.md`
- `workbooks/Security Operations Playbooks/Okta/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/Security Operations Playbooks/Okta/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB03_privileged_change_or_admin_grant.md`
- `workbooks/Security Operations Playbooks/Okta/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB04_malicious_process_or_edr_detection.md`
- `workbooks/Security Operations Playbooks/Okta/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB05_data_exfiltration_and_large_transfers.md`
- `workbooks/Security Operations Playbooks/Okta/PB06_command_and_control_beaconing.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB06_command_and_control_beaconing.md`
- `workbooks/Security Operations Playbooks/Okta/PB07_lateral_movement.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB07_lateral_movement.md`
- `workbooks/Security Operations Playbooks/Okta/PB08_ransomware_or_destructive_activity.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB08_ransomware_or_destructive_activity.md`
- `workbooks/Security Operations Playbooks/Okta/PB09_insider_risk_and_sensitive_access.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB09_insider_risk_and_sensitive_access.md`
- `workbooks/Security Operations Playbooks/Okta/PB10_oauth_token_api_key_misuse.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/PB10_oauth_token_api_key_misuse.md`
- `workbooks/Security Operations Playbooks/Okta/README.md` -> `workbooks/dashboards/Security Operations Playbooks/Okta/README.md`
- `workbooks/Security Operations Playbooks/PLAYBOOK_TEMPLATE.md` -> `workbooks/dashboards/Security Operations Playbooks/PLAYBOOK_TEMPLATE.md`
- `workbooks/Security Operations Playbooks/Palo_Alto_Networks/PB01_suspicious_authentication.md` -> `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB01_suspicious_authentication.md`
- `workbooks/Security Operations Playbooks/Palo_Alto_Networks/PB02_mfa_abuse_and_push_fatigue.md` -> `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB02_mfa_abuse_and_push_fatigue.md`
- `workbooks/Security Operations Playbooks/Palo_Alto_Networks/PB03_privileged_change_or_admin_grant.md` -> `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB03_privileged_change_or_admin_grant.md`
- `workbooks/Security Operations Playbooks/Palo_Alto_Networks/PB04_malicious_process_or_edr_detection.md` -> `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB04_malicious_process_or_edr_detection.md`
- `workbooks/Security Operations Playbooks/Palo_Alto_Networks/PB05_data_exfiltration_and_large_transfers.md` -> `workbooks/dashboards/Security Operations Playbooks/Palo_Alto_Networks/PB05_data_exfiltration_and_large_transfers.md`
- ... 30 more

## Reference risk

### `content/`
- `README.md`
- `content/CrowdStrike/README.md`
- `docs/standards/repository-structure.md`
- `white_papers/detections/zeid_data_cl0p_data_extortion_detection_report.md`

### `detections/`
- `README.md`
- `content/SentinelOne/README.md`
- `content/SentinelOne/SOC2_Content/HOWTO.md`
- `content/SentinelOne/SOC2_Content/Zeid Data_sentinel_soc2_workbook_multi_source_arm.json`
- `detections/README.md`
- `docs/index.md`
- `docs/standards/naming.md`
- `docs/standards/repository-structure.md`
- `docs/taxonomy.md`
- `malware/README.md`
- `malware/claude/HOWTO.md`
- `malware/claude/MANIFEST_SHA256.txt`
- `malware/claude/README.md`
- `projects/zeid_data_cloak_check/HOWTO.md`
- `projects/zeid_data_cloak_check/README.md`
- `projects/zeid_data_cloak_check/zeid_data_cloak_checking_email.md`
- `white_papers/README.md`

### `malware/`
- `README.md`
- `docs/standards/naming.md`
- `docs/standards/repository-structure.md`
- `docs/taxonomy.md`
- `malware/README.md`
- `white_papers/README.md`

### `media/`
- `README.md`
- `content/Cisco/README.md`
- `content/CrowdStrike/CrowdStrike Falcon AI Governance/README.md`
- `content/CrowdStrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/README.md`
- `content/CrowdStrike/CrowdStrike Falcon Claude Bot Detection/README.md`
- `content/CrowdStrike/README.md`
- `content/Island/README.md`
- `content/Island/zeid_data_elk_stack_connector/README.md`
- `content/Island/zeid_data_evidence_bundle/README.md`
- `content/README.md`
- `content/SentinelOne/README.md`
- `content/SentinelOne/SOC2_Content/README.md`
- `content/Snowflake/README.md`
- `content/Splunk/README.md`
- `content/Splunk/Zeid Data Claude Bot Content/README.md`
- `content/Splunk/Zeid Data Splunk App - Exfil Watch/README.md`
- `detections/README.md`
- `detections/claude_bot/README.md`
- `detections/cve-2025-20393/README.md`
- `detections/cve-2025-40551/README.md`
- `detections/cve-2026-24423/README.md`
- `detections/cve-2026-24858/README.md`
- `docs/index.md`
- `docs/profile-readme.md`
- `docs/standards/repository-structure.md`
- ... 44 more

### `projects/`
- `README.md`
- `detections/README.md`
- `docs/index.md`
- `docs/standards/naming.md`
- `docs/standards/repository-structure.md`
- `docs/taxonomy.md`
- `white_papers/README.md`

### `scripts/`
- `README.md`
- `content/CrowdStrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/HOWTO.md`
- `content/CrowdStrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/README.md`
- `content/Island/zeid_data_elk_stack_connector/HOWTO.md`
- `content/Island/zeid_data_elk_stack_connector/README.md`
- `docs/index.md`
- `docs/standards/repository-structure.md`
- `docs/taxonomy.md`
- `malware/README.md`
- `malware/claude/HOWTO.md`
- `malware/claude/MANIFEST_SHA256.txt`
- `malware/claude/README.md`
- `malware/claude/scripts/zeid_data_ci_block_risky_claude_config.ps1`
- `malware/claude/scripts/zeid_data_ci_block_risky_claude_config.sh`
- `projects/zeid_data_cloak_check/HOWTO.md`
- `projects/zeid_data_cloak_check/README.md`
- `projects/zeid_data_cloak_check/zeid_data_cloak_checking_email.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/HOWTO.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/README.md`
- `projects/zeid_data_nist_gen_ai_evidence_pack/scripts/bundle_evidence.py`
- `projects/zeid_data_nist_gen_ai_evidence_pack/scripts/generate_coverage_report.py`
- `projects/zeid_data_nist_gen_ai_evidence_pack/scripts/validate_events.py`
- `scripts/README.md`
- `scripts/automation/README.md`
- `white_papers/README.md`

### `templates/`
- `README.md`
- `content/CrowdStrike/CrowdStrike Falcon Audit Evidence & Noise Reduction/HOWTO.md`
- `content/Island/README.md`
- `content/SentinelOne/README.md`
- `docs/index.md`
- `docs/standards/evidence.md`
- `docs/standards/repository-structure.md`
- `docs/taxonomy.md`
- `projects/zeid_data_cloak_check/README.md`
- `projects/zeid_data_cloak_check/checklists/zeid_data_evidence_bundle_template.md`
- `projects/zeid_data_cloak_check/zeid_data_cloak_checking_email.md`
- `white_papers/README.md`

### `white_papers/`
- `README.md`
- `docs/standards/repository-structure.md`

### `workbooks/`
- `README.md`
- `docs/index.md`
- `docs/standards/naming.md`
- `docs/standards/repository-structure.md`
- `docs/taxonomy.md`
- `malware/README.md`
- `white_papers/README.md`

## Recommended execution path

1. Review `docs/repo/restructure-map.json`.
2. Move files on a dedicated branch.
3. Rewrite Markdown links and known path references.
4. Run tests, link checks, and README image checks.
5. Commit as one restructure commit.
6. Keep old path compatibility notes in the root README if needed.
