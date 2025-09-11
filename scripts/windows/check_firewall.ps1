# check_firewall.ps1 - Ensure Windows Firewall is enabled for all profiles
try {
    $profiles = Get-NetFirewallProfile
    $allEnabled = $true
    foreach ($p in $profiles) {
        if (-not $p.Enabled) {
            $allEnabled = $false
            Write-Output "FAIL: Firewall disabled for profile $($p.Name)"
        }
    }
    if ($allEnabled) {
        Write-Output "PASS: Firewall enabled on all profiles"
        exit 0
    } else {
        exit 2
    }
} catch {
    Write-Output "ERROR: $_"
    exit 3
}
