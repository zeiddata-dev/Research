rule INFOSTEALER_BrowserCred_Access_Heuristic
{
  meta:
    author = "Zeid Data (starter)"
    description = "Heuristic: binaries that reference common browser credential/cookie stores (tune to reduce FPs)."
    date = "2026-02-08"
    reference = "Hunting helper (not a definitive signature)."

  strings:
    $s1 = "Login Data" ascii wide
    $s2 = "Local State" ascii wide
    $s3 = "\\User Data\\Default\\Cookies" ascii wide
    $s4 = "\\User Data\\Default\\Web Data" ascii wide
    $s5 = "\\Google\\Chrome\\User Data" ascii wide
    $s6 = "\\Microsoft\\Edge\\User Data" ascii wide
    $s7 = "SELECT origin_url" ascii wide
    $s8 = "logins" ascii wide
    $s9 = "CryptUnprotectData" ascii wide

  condition:
    uint16(0) == 0x5A4D and
    4 of ($s*) and
    filesize < 20MB
}
