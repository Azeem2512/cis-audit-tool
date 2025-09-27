# fix_disable_guest.ps1 - disable the built-in Guest account
try {
    $guest = Get-LocalUser -Name "Guest" -ErrorAction SilentlyContinue
    if ($guest -and $guest.Enabled) {
        Disable-LocalUser -Name "Guest" -ErrorAction Stop
        Write-Output "OK: Guest account disabled."
        exit 0
    } else {
        Write-Output "OK: Guest account already disabled or not present."
        exit 0
    }
} catch {
    Write-Output "ERROR: $_"
    exit 1
}
