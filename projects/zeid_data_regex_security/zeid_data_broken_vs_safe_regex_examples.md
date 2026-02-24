# Broken vs Safe Regex Examples (Defensive Toy Cases)

## 1) Catastrophic Backtracking / ReDoS

### Vulnerable regex
```regex
^(a+)+$
```

### Why risky
Nested quantifiers can create heavy backtracking on near-match failures in backtracking engines.

### Toy input that demonstrates the issue
```text
aaaaaaaaaaaaaaaaaaaa!
```

### Safer regex
```regex
^a+$
```

### Practical mitigation tip
Enforce input length limits before regex matching and benchmark suspicious patterns with toy adversarial inputs.

---

## 2) Validation Bypass from Bad Anchors / Grouping

### Vulnerable regex
```regex
^admin|root$
```

### Why risky
The anchors do not apply to the whole alternation. It matches strings that merely start with `admin` or end with `root`.

### Toy examples (unexpected matches)
- `admin123`
- `notroot`

### Safer regex
```regex
^(?:admin|root)$
```

### Practical mitigation tip
When using alternation (`|`) with anchors, group the alternatives and test near misses.

---

## 3) Trusted Domain / Allowlist Matching Mistake

### Vulnerable regex
```regex
^https://.*trusted\.com
```

### Why risky
Can match hostnames that only contain `trusted.com` as a substring, not as the actual registered hostname ending.

### Toy examples (should not be trusted)
- `https://trusted.com.evil.example/path`
- `https://login.trusted.com.attacker.tld`

### Safer regex
```regex
^https://(?:[a-z0-9-]+\.)*trusted\.com(?:[:/]|$)
```

### Practical mitigation tip
Use a URL parser, normalize the hostname, and compare exact host or dot-boundary suffix in code.

---

## Extra Notes

- Regex is good for **shape checks**
- Parsers are better for **semantic trust checks**
- Always test:
  - expected valid input
  - obvious invalid input
  - weird near misses
  - long input
