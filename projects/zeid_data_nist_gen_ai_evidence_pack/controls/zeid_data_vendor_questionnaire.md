# AI Vendor Questionnaire (starter)

Goal: figure out if your vendor is running an AI platform, or a trust fall.

## Security
1) How do you authenticate and authorize access to the model API?
2) Do you support customer managed keys and tenant isolation?
3) How do you detect and respond to abuse (scraping, denial of wallet)?
4) Do you provide audit logs for admin actions and key events?

## Privacy and data use
5) Do you train on customer inputs by default? If not, show contract language.
6) How long are prompts and outputs retained? Can retention be configured?
7) What is your policy for subprocessors and third party services?

## Model updates and change control
8) How often do model versions change and how are customers notified?
9) Can we pin to a model version? What breaks when you update?
10) Do you provide release notes describing behavior changes?

## Safety controls
11) What guardrails are available (input, output, tool governance)?
12) How do you handle prompt injection and tool abuse scenarios?
13) Do you expose safety and policy decision logs?

## Evidence
14) Provide SOC reports, penetration test summaries, and incident reporting SLAs.
15) Provide documentation for logging fields and schemas.

If the answers are vague, treat that as an answer.
