# Exploitable Regex - Education Only ✅

No live target testing. No exploitation walkthroughs. No chaos engineering by accident.
Just practical examples, safer patterns, and a reminder that regex is both useful and emotionally expensive.

---

## Why Regex Can Hurt You 🤓

A regex engine tries to match input text against a pattern.

Some engines are **backtracking engines** (think PCRE style engines, many language runtimes, and other NFA/backtracking implementations). When a pattern is ambiguous, the engine may explore **a lot** of possible match paths before it decides whether the input matches.

If the pattern is poorly designed, an attacker or just a random ugly payload can trigger:

* **slow requests** 🐌
* **high CPU** 🔥
* **timeouts** ⏳
* **queue pileups** 📦
* and eventually your incident channel starts glowing like a Christmas tree 🚨

Also, not every regex problem is about performance. A regex can be **logically wrong** and quietly accept values you absolutely did not mean to allow. Which is fun, if your hobby is debugging production auth bypasses.

---

## Example 1: Catastrophic Backtracking (ReDoS) 💥

### Vulnerable regex

```regex
^(a+)+$
```

### Why it is risky

This pattern contains a **nested quantifier**: `(a+)+`.

In a backtracking engine, an input that almost matches but fails near the end can trigger a large number of retry paths. The engine keeps repartitioning the same characters, trying different ways to satisfy the nested repetition.

### Toy input example

```text
aaaaaaaaaaaaaaaaaaaa!
```

The trailing `!` causes failure, but only after the engine spends time exploring many partitions of the `a` sequence.

In other words, the regex does not just fail. It fails *dramatically*.

### Safer version

```regex
^a+$
```

If your intent is “one or more `a` characters,” say exactly that ✅

No nested repetition. Less ambiguity. Far less backtracking risk.

### Technical note

If your engine supports them, **atomic groups** or **possessive quantifiers** can reduce backtracking in some patterns.

That said, the best fix is usually simpler:

**Do not write a regex that needs a rescue mission.**

### Practical mitigation tips 🧯

* Enforce input length limits before regex evaluation (reject or truncate unexpected payload sizes)
* Prefer regex engines with linear time guarantees (for example, RE2 family designs) for untrusted, high volume input
* Benchmark suspicious patterns with toy adversarial inputs in CI

---

## Example 2: Validation Bypass from Bad Anchors and Grouping 🎯❌

### Vulnerable regex

```regex
^admin|root$
```

### Why it is risky

This looks like it means:

> Match exactly `admin` or `root`

It does **not**.

Because alternation (`|`) splits the expression, this behaves like:

* `^admin` **OR**
* `root$`

So these may match unexpectedly:

* `admin123` ✅ (starts with `admin`)
* `notroot` ✅ (ends with `root`)
* `admin...` ✅ (prefix branch still matches)

That is not strict validation. That is wishful thinking with a regex literal.

### Safer version

```regex
^(?:admin|root)$
```

### Why this works ✅

* `^` anchors the start of the string
* `$` anchors the end of the string
* `(?: ... )` groups the alternatives without capturing
* Only exact matches of `admin` or `root` succeed ✅

### Practical mitigation tips 🔍

When using alternation with anchors, group it:

```regex
^(?:option1|option2|option3)$
```

Add tests for near misses, not just happy paths:

* `admin123`
* `xroot`
* `rootx`

Because production traffic has a weird talent for finding the branch you forgot to test.

---

## Example 3: Trusted Domain / Allowlist Matching Mistakes 🌐⚠️

### Vulnerable regex

```regex
^https://.*trusted\.com
```

### Why it is risky

This can match strings like:

* `https://trusted.com.evil.example`
* `https://login.trusted.com.attacker.tld`

Why? Because `.*` is greedy, and there is no hostname boundary proving that `trusted.com` is the actual hostname ending or a valid subdomain target.

If this regex is used for:

* trusted redirect logic
* SSO callback allowlists
* URL filtering
* webhook source checks

...you may have a security control bypass.

Which is a very expensive way to learn that URL parsing is not “basically just string matching.”

### Safer regex (format check approach)

```regex
^https://(?:[a-z0-9-]+\.)*trusted\.com(?:[:/]|$)
```

### Why this is better ✅

It:

* requires `https://`
* allows optional subdomains
* requires `trusted.com` as the hostname suffix
* enforces a boundary after the hostname (`:`, `/`, or end of string)

### Important caveat (technical and very real) 🧠

Regex can be okay for **basic format checks**.

Regex is often the wrong tool for **trust decisions**.

URLs are tricky because of:

* IDNs / Unicode / Punycode (IDNA)
* trailing dots
* default ports
* userinfo segments
* normalization edge cases

### Even safer approach (recommended) ✅🛡️

Parse the URL first, then compare the normalized hostname in code:

1. Lowercase the hostname
2. Strip a trailing dot (if present)
3. Convert IDNs safely (IDNA / Punycode handling as appropriate)
4. Check for either:

   * exact match: `trusted.com`
   * dot boundary suffix: `.trusted.com`

Use a parser for structure. Use regex for syntax. Keep trust decisions explicit.

### Practical mitigation tip

For allowlists, prefer structured parsers (`URL`, `urllib.parse`, etc.) plus explicit hostname comparison instead of one giant regex monster 👹

---

## Broken vs Safe Quick Reference 📌

| Risk                              | Vulnerable Regex                                              | Safer Regex                                  |     |
| --------------------------------- | ------------------------------------------------------------- | -------------------------------------------- | --- |
| ReDoS / catastrophic backtracking | `^(a+)+$`                                                     | `^a+$`                                       |     |
| Anchor / grouping bypass          | `^admin\|root$` *(conceptually broken alternation anchoring)* | `^(?:admin\|root)$`                          |     |
| Trusted domain matching mistake   | `^https://.*trusted\.com`                                     | `^https://(?:[a-z0-9-]+.)*trusted.com(?:[:/] | $)` |

> Note: In the anchor example, the actual broken pattern is `^admin|root$` (without escaping `|`). The table escapes `|` for readability in markdown code contexts.

---

## Short Checklist for Secure Regex Design ✅

* Keep patterns as simple as possible
* Avoid nested quantifiers unless you can prove performance behavior
* Group alternations with `(?: ... )` when anchors are involved
* Add input length limits before regex matching
* Test bad, near miss, and adversarial inputs (not just valid ones)
* Prefer parsers over regex for URLs, emails, and other structured trust decisions
* Benchmark suspicious patterns on toy inputs in CI
* Log validation failures and timeouts so trends show up before incidents do 📈

Because if you do not measure it, you are just waiting to meet it in production.

---

## Call to Action 🔧

During code review this week, find one regex in your environment and ask:

* What is this actually enforcing?
* Can it backtrack badly?
* Are the anchors and groups correct?
* Should this be a parser instead?

Add tests. Add timing checks. Add logs.

Because “it’s just regex” is how tiny mistakes get promoted into incident tickets 🚨

