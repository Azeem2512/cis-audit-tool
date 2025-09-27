# fix_smbv1.ps1 - Disable SMBv1 safely (works on different Windows versions)
try {
    $changed = $false

    # --- Method 1: Registry (covers older builds & compatibility layer) ---
    $regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters"
    if (Test-Path $regPath) {
        $current = (Get-ItemProperty -Path $regPath -Name SMB1 -ErrorAction SilentlyContinue).SMB1
        if ($null -eq $current -or $current -ne 0) {
            Set-ItemProperty -Path $regPath -Name SMB1 -Value 0 -Force
            Write-Output "OK: SMBv1 has been disabled via registry (SMB1=0). A restart may be required."
            $changed = $true
        } else {
            Write-Output "OK: SMBv1 already disabled in registry."
        }
    }

    # --- Method 2: Windows Optional Feature (Windows 10/11) ---
    $feature = Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -ErrorAction SilentlyContinue
    if ($feature -and $feature.State -ne "Disabled") {
        Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart -ErrorAction SilentlyContinue | Out-Null
        Write-Output "OK: SMBv1 feature disabled (no restart)."
        $changed = $true
    } elseif ($feature -and $feature.State -eq "Disabled") {
        Write-Output "OK: SMBv1 feature already disabled."
    }

    if (-not $changed) {
        Write-Output "INFO: No changes needed. SMBv1 already disabled."
    }

    exit 0
}
catch {
    Write-Output "ERROR: $_"
    exit 1
}
