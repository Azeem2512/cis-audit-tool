# fix_enable_firewall.ps1 - enable Windows Firewall for all profiles
try {
    Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True -ErrorAction Stop
    Write-Output "OK: Windows Firewall enabled for Domain, Public and Private profiles."
    exit 0
} catch {
    Write-Output "ERROR: $_"
    exit 1
}
