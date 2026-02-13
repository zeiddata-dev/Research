# Training KQL Queries (Island in ELK)
These are quick pivots for analysts and incident responders who would rather do literally anything else.

## Basic
- All Island events:
  - `event.module : "island"`
- Blocked actions:
  - `island.policy.decision : "blocked"`
- Downloads:
  - `island.action : "download"`

## User pivots
- By user (example):
  - `island.user : "caitlin@example.com"`
  - or `user.name : "caitlin@example.com"`

## URL pivots
- Anything touching a domain:
  - `island.url : "*example.com*"`
- “Why is this person downloading everything?”
  - `island.action : "download" and island.user : "caitlin@example.com"`

## Device posture pivots
- Unverified devices:
  - `island.device.posture : "unverified"`

## Policy pivots
- Policy name:
  - `island.policy.name : "DLP - Finance"`
