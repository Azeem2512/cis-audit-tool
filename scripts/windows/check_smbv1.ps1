# check_smbv1.ps1 - Ensure SMBv1 protocol is disabled
try {
    $reg = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" -ErrorAction SilentlyContinue
    if ($reg.SMB1 -eq 0) {
        Write-Output "PASS: SMBv1 is disabled"
        exit 0
    } else {
        Write-Output "FAIL: SMBv1 is enabled"
        exit 2
    }
} catch {
    Write-Output "ERROR: $_"
    exit 3
}
