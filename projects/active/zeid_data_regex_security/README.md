<!-- ZEID DATA README HERO START -->
<p align="center">
  <img src="../../../assets/banners/readme/projects.png" alt="Zeid Data projects banner" width="100%">
</p>

<p align="center">
  <a href="../../../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../content"><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../../../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../.."><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

# Zeid Data Regex Security Education Bundle 🧪🛡️

This package contains defensive education content and lightweight tooling to help teams understand and test regex related security risks.

Because apparently `just a little regex` keeps ending up in security critical paths. 😅

## What’s Included 📦

* `zeid_data_regex_education.md`
  Full cybersecurity education post in plain English with toy examples

* `zeid_data_regex_security_research.md`
  Research notes and defensive rationale

* `zeid_data_broken_vs_safe_regex_examples.md`
  Side by side examples with safer alternatives

* `HOWTO.md`
  Usage guide for the included script

* `LICENSE.md`
  License text (MIT)

* `zeid_data_regex_safety_tester.py`
  Toy benchmark and heuristic checks for regex review

## Purpose 🎯

This bundle is for defensive education and engineering hygiene. It helps teams:

* identify risky regex patterns
* improve validation correctness
* reduce ReDoS risk
* encourage parser first trust decisions for URLs and domains

In short: fewer regex surprises, fewer production regrets.

## Safety Notes 🚧

* No live target exploitation guidance
* No illegal activity instructions
* All examples are toy examples
* The script is a helper, not a formal proof of safety

It is meant to help you catch obvious problems early, not replace engineering judgment, code review, or reality.

## Suggested Workflow ✅

1. Read the education post
2. Review the broken vs safe examples
3. Run the script on patterns used in your codebase
4. Add tests and logs
5. Replace fragile regex trust checks with structured parsing where possible

Regex is powerful.
It is also extremely literal and has no interest in your intentions. 🤖
