# check_rdp_nla.ps1 - Ensure RDP requires Network Level Authentication
try {
    $value = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "UserAuthentication" -ErrorAction SilentlyContinue
    if ($value.UserAuthentication -eq 1) {
        Write-Output "PASS: RDP requires NLA"
        exit 0
    } else {
        Write-Output "FAIL: RDP does not require NLA"
        exit 2
    }
} catch {
    Write-Output "ERROR: $_"
    exit 3
}
