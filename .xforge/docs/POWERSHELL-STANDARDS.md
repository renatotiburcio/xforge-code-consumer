# PowerShell Standards

## Encoding

- **Always** use `-Encoding utf8` with `Out-File` / `Set-Content`
- **Never** use `Out-File` without `-Encoding`
- **Never** use `[System.Text.Encoding]::UTF8` directly — prefer `-Encoding utf8`

### Rationale

PowerShell 5.1 defaults to UTF-16LE (big-endian) when `-Encoding` is omitted.
Using `-Encoding utf8` ensures cross-platform compatibility and avoids file bloat.

### Acceptable

```powershell
Out-File -FilePath "out.json" -Encoding utf8
Set-Content -Path "out.json" -Encoding utf8
```

### Avoid

```powershell
Out-File -FilePath "out.json"                       # UTF-16LE
[System.IO.File]::WriteAllText("out.json", $data)   # .NET default, not explicit
```

## Directory Changes

- Use `Push-Location` / `Pop-Location` instead of bare `Set-Location`
- Wrap directory-dependent code in `try { ... } finally { Pop-Location }`

### Acceptable

```powershell
Push-Location $Root
try {
    # directory-dependent work
}
finally {
    Pop-Location
}
```

### Avoid

```powershell
Set-Location $Root
# no restoration
```
