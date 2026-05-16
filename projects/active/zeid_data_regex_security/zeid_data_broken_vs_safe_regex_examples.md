````markdown
# Zeid Data Broken vs Safe Regex Examples 🛡️🧪
**Defensive toy cases for code review, CI checks, and “why is this matching that?” moments**

Regex is powerful, fast, and compact right up until it becomes:
- a CPU tax 💸
- a validation hallucination 🎭
- or a trust boundary bug disguised as “just a pattern” 😬

This guide uses **toy examples only** for defensive education.  
No exploitation walkthroughs. No live target testing. No chaos. Just safer patterns and practical review notes.

---

## 1) Catastrophic Backtracking / ReDoS 💥

### Vulnerable regex
```regex
^(a+)+$
```

### Why risky
This contains a **nested quantifier** (`(a+)+`), which can trigger heavy backtracking in backtracking engines when the input almost matches and then fails near the end.

### Toy input that demonstrates the issue
```text
aaaaaaaaaaaaaaaaaaaa!
```

### What happens (conceptually)
The engine keeps trying different ways to partition the `a` characters before finally admitting the trailing `!` breaks the match.

### Safer regex
```regex
^a+$
```

### More toy near misses to test
- `aaaaaaaab`
- `aaaaaaaaaaaaaaaaaaaaaaaaX`
- very long strings that end with one invalid character

### Practical mitigation tip
Enforce **input length limits** before regex matching and benchmark suspicious patterns with toy adversarial inputs.

### Bonus technical note
If your engine supports them, **atomic groups** / **possessive quantifiers** may help in some patterns, but the best fix is usually **simpler regex design**.

---

## 2) Validation Bypass from Bad Anchors / Grouping 🎯❌

### Vulnerable regex
```regex
^admin|root$
```

### Why risky
The anchors do **not** apply to the whole alternation. This is effectively:

- `^admin` **OR**
- `root$`

So it matches strings that merely start with `admin` or end with `root`.

### Toy examples (unexpected matches)
- `admin123` ✅
- `notroot` ✅
- `admin-but-definitely-not-a-valid-username` ✅

### Safer regex
```regex
^(?:admin|root)$
```

### More toy tests you should include
**Should match**
- `admin`
- `root`

**Should fail**
- `Admin` (if case sensitive)
- `root1`
- `xroot`
- `admin `
- ` admin`

### Practical mitigation tip
When using alternation (`|`) with anchors, **group the alternatives** and test **near misses**, not just happy paths.

---

## 3) Trusted Domain / Allowlist Matching Mistake 🌐⚠️

### Vulnerable regex
```regex
^https://.*trusted\.com
```

### Why risky
This can match hostnames that only contain `trusted.com` as a substring instead of the actual hostname ending.

### Toy examples (should not be trusted)
- `https://trusted.com.evil.example/path`
- `https://login.trusted.com.attacker.tld`
- `https://totallyfine.example/?next=trusted.com`

### Safer regex (format check only)
```regex
^https://(?:[a-z0-9-]+\.)*trusted\.com(?:[:/]|$)
```

### Why safer
- requires `https://`
- allows optional subdomains
- requires `trusted.com` as the hostname suffix
- enforces a hostname boundary (`:`, `/`, or end)

### Better than regex (recommended) ✅
Use a URL parser, normalize the hostname, and compare:
- exact host `trusted.com`
- or dot boundary suffix `.trusted.com`

### Practical mitigation tip
Regex is okay for **shape checks**. Use structured parsing for **trust decisions**.

---

## 4) “Dot Means Any Character” Mistake (Unescaped `.`) 🫠

### Vulnerable regex
```regex
^10.0.0.1$
```

### Why risky
In regex, `.` means **any character** (except newline in many modes), not a literal dot.

This pattern matches way more than the intended IP string.

### Toy examples (unexpected matches)
- `10x0x0x1` ✅
- `10-0-0-1` ✅
- `10A0B0C1` ✅

### Safer regex (exact literal string)
```regex
^10\.0\.0\.1$
```

### Better approach for real IP validation
Use an IP parsing library instead of regex where possible (especially for IPv6 and normalization rules).

### Practical mitigation tip
Escape literal dots in hostnames, IPs, and domains: `\.` not `.`

---

## 5) Character Class Range Trap: `[A-z]` 😵‍💫

### Vulnerable regex
```regex
^[A-z0-9_]+$
```

### Why risky
`[A-z]` is a common mistake. In ASCII, the range from `A` to `z` includes extra punctuation characters between `Z` and `a` such as:

- `[`
- `\`
- `]`
- `^`
- `_`
- `` ` ``

So this may allow characters you did not intend.

### Toy examples (unexpected matches)
- `user[name]` ✅ (because `[` and `]` fall in `A-z`)
- `admin^ops` ✅
- ``dev`test`` ✅

### Safer regex
```regex
^[A-Za-z0-9_]+$
```

### Practical mitigation tip
Avoid broad ASCII ranges unless you are absolutely sure. Prefer explicit ranges:
- `A-Z`
- `a-z`
- `0-9`

---

## 6) File Extension Check Bypass from Missing End Anchor 📎⚠️

### Vulnerable regex
```regex
^.*\.(jpg|png)
```

### Why risky
There is no end anchor, so it can match strings that only *contain* a permitted extension and then continue with extra content.

### Toy examples (unexpected matches)
- `avatar.jpg.exe` ✅
- `report.png.bak` ✅
- `image.jpg/evil` ✅ (depends on context and engine use)

### Safer regex (basic shape check)
```regex
^[^/\\]+\.(?:jpg|png)$
```

### Better (if this is a real upload control)
Do not trust filename regex alone. Also validate:
- MIME type
- actual file signature / magic bytes
- storage handling and execution permissions

### Practical mitigation tip
If your regex is meant to validate a full filename, anchor it on both ends and define what characters are allowed before the extension.

---

## 7) Greedy Parsing in Delimited Logs (Over-capture) 📜🧲

### Vulnerable regex
```regex
^user=(.*);role=(.*)$
```

### Why risky
Greedy `.*` can over-capture when delimiters appear unexpectedly, leading to parsing errors, incorrect field extraction, or blind spots in normalization pipelines.

### Toy example (ambiguous parse)
```text
user=alice;meta=x;y;role=admin
```

Depending on parsing expectations, `user` may absorb too much content.

### Safer regex (delimiter-aware)
```regex
^user=([^;]*);role=([^;]*)$
```

### Why safer
It only captures characters up to the delimiter `;`, which reduces accidental over-capture.

### Practical mitigation tip
For structured logs, prefer real parsers (JSON, key-value parsers, CSV parsers) over regex whenever format is known.

---

## 8) Whitespace Validation That Accidentally Accepts Empty Strings 🫥

### Vulnerable regex
```regex
^\s*$
```

### Why risky
Sometimes this gets used where people meant “has text” or “safe whitespace handling.” It actually matches:
- empty string
- spaces only
- tabs only
- newline only (depending on input/mode)

That can turn “required field” validation into “sure, blank is fine.”

### Toy examples (unexpected matches)
- `` (empty string) ✅
- `   ` ✅
- `\t\t` ✅

### Safer regex (if intent is non-empty non-whitespace)
```regex
^\S(?:.*\S)?$
```

### Simpler alternative in code (usually better)
Trim the string and check length:
- `value.strip() != ""`

### Practical mitigation tip
Be explicit about intent:
- “optional field”
- “non-empty field”
- “non-whitespace field”
These are different rules and should have different validations.

---

## Quick Patterns to Review First in Real Environments 🔎

If you are doing a regex safety pass, start with patterns used in:

- auth / login / RBAC checks
- redirect and callback validation
- URL/domain allowlists
- WAF/SIEM content filtering
- parser/normalization pipelines
- filename/content upload rules
- high volume request validation paths

Those are the places where tiny regex mistakes become loud operational problems.

---

## Defensive Review Checklist ✅

When reviewing a regex, ask:

- What is this **intended** to enforce?
- What are the **counterexamples** that must fail?
- Can this pattern **backtrack badly**?
- Are anchors and alternation grouped correctly?
- Is regex the right tool, or should this be a **parser**?
- Is there an **input length limit** before matching?
- Are there tests for:
  - expected valid input
  - obvious invalid input
  - weird near misses
  - long input
  - delimiter edge cases
  - Unicode / case behavior (if relevant)

---

## Extra Notes (The Boring Stuff That Prevents Incidents) 🧠

- Regex is great for **shape checks**
- Parsers are better for **semantic trust checks**
- Keep patterns simple
- Benchmark suspicious patterns
- Log slow matches / timeouts when your engine supports it
- Treat validation regex in critical paths like code, not comments

Because production does not care that the bug was only 12 characters long. 😅
````
