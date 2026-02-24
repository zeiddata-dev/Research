# Poorly Written Regex Can Become a Security Problem

Regex is one of those tools that feels tiny until it takes down a service, lets bad input through, or silently approves a "trusted" domain that absolutely is not trusted.

Used well, regular expressions are great for **parsing, filtering, and validation**. Used carelessly, they become:
- a **CPU heater** (ReDoS / catastrophic backtracking),
- a **false sense of validation** (bad anchors / grouping),
- or an **access control mistake in disguise** (bad allowlist/domain matching).

This post is for security engineers, IT admins, developers, and SOC analysts who have all seen this movie before:
> "It was just a validation regex"  
and then the dashboard went sideways at 2:14 AM.

## Plain English First

A regex engine tries to match text against a pattern.

Some regex engines (backtracking engines) will try many different paths when the pattern is ambiguous. If the pattern is poorly designed, a specially crafted input can force the engine to do a lot of useless work.

That means:
- **slow requests**
- **high CPU**
- **timeouts**
- **queue pileups**
- and eventually, your incident channel starts lighting up

And not every regex problem is about performance. A regex can also be logically wrong and accidentally match things you meant to reject.

Below are safe toy examples only. No live target testing, no exploitation walkthroughs, no chaos. Just defensive education.

---

## Example 1: Catastrophic Backtracking (ReDoS)

### Vulnerable regex
```regex
^(a+)+$
```

### Why it is risky
This pattern nests a repeating group (`(a+)+`). In a backtracking regex engine, inputs that almost match but fail near the end can trigger a huge number of retry paths.

Toy input example:
```text
aaaaaaaaaaaaaaaaaaaa!
```

The engine keeps trying different ways to partition the `a`s before realizing the trailing `!` makes the whole match fail.

### Safer version
```regex
^a+$
```

If your intent is "one or more `a` characters", say exactly that. No nested repetition.

If your engine supports them, atomic groups / possessive quantifiers can also reduce backtracking risk in some cases, but the best fix is usually to **simplify the pattern**.

### Practical mitigation tip
- Put **length limits** on untrusted input *before* regex evaluation (for example, reject or truncate unexpectedly long payloads).
- Prefer regex engines with **linear-time guarantees** (such as RE2 family style engines) for untrusted, high-volume input.

---

## Example 2: Validation Bypass from Bad Anchors / Grouping

### Vulnerable regex
```regex
^admin|root$
```

### Why it is risky
This looks like it means "match exactly `admin` or `root`", but it does **not**.

It actually means:
- `^admin` **OR**
- `root$`

So these may match unexpectedly:
- `admin123`  ✅ (starts with admin)
- `notroot`   ✅ (ends with root)
- `admin...`  ✅ (still matches prefix branch)

That is not validation. That is wishful thinking in production.

### Safer version
```regex
^(?:admin|root)$
```

Now the anchors apply to the **entire alternation**.

### Practical mitigation tip
- When using `|` (alternation), almost always group it:
  - `^(?:option1|option2|option3)$`
- Add unit tests for **near misses** (`admin123`, `xroot`, `rootx`) rather than only happy-path values.

---

## Example 3: Allowlist / Trusted Domain Matching Mistakes

### Vulnerable regex
```regex
^https://.*trusted\.com
```

### Why it is risky
This pattern can match strings like:
- `https://trusted.com.evil.example`
- `https://login.trusted.com.attacker.tld`

Because `.*` is greedy and there is no boundary that guarantees `trusted.com` is the actual hostname ending.

If this regex is used for "trusted redirect" logic, "SSO callback allowlist", or "URL filtering", it can create a security control bypass.

### Safer version (regex approach)
```regex
^https://(?:[a-z0-9-]+\.)*trusted\.com(?:[:/]|$)
```

This is better because it:
- requires `https://`
- allows optional subdomains
- requires `trusted.com` as the actual hostname suffix with a boundary (`:`, `/`, or end)

### Even safer approach (recommended)
Parse the URL first, then compare the **normalized hostname** in code:
1. Lowercase it
2. Strip a trailing dot if present
3. Convert IDNs safely if applicable (Punycode/IDNA)
4. Check exact match (`trusted.com`) or dot-boundary suffix (`.trusted.com`)

Regex is okay for *format checks*. It is often the wrong tool for *trust decisions*.

### Practical mitigation tip
- For allowlists, prefer structured parsers (`URL`, `urllib.parse`, etc.) plus explicit hostname comparison instead of one giant regex.

---

## Broken vs Safe Quick Reference

| Risk | Vulnerable Regex | Safer Regex |
|---|---|---|
| ReDoS / catastrophic backtracking | `^(a+)+$` | `^a+$` |
| Anchor / grouping bypass | `^admin|root$` | `^(?:admin|root)$` |
| Trusted domain matching mistake | `^https://.*trusted\.com` | `^https://(?:[a-z0-9-]+\.)*trusted\.com(?:[:/]|$)` |

---

## Short Checklist for Secure Regex Design

- Keep patterns **as simple as possible**
- Avoid **nested quantifiers** unless you can prove behavior and performance
- Group alternations with `(?: ... )` when anchors are involved
- Add **input length limits** before regex matching
- Test **bad / near-miss / adversarial** inputs, not just good inputs
- Prefer **parsers over regex** for URLs, emails, and structured data trust decisions
- Benchmark suspicious patterns on toy inputs in CI
- Log validation failures and timeouts so you can see trends before they become incidents

---

## Call to Action

During code review this week, find one regex in your environment and ask:
- What is this actually enforcing?
- Can it backtrack badly?
- Are the anchors and groups correct?
- Should this be a parser instead?

Add tests. Add timing checks. Add logs.

Because "it’s just regex" is how small mistakes graduate into incident tickets.

