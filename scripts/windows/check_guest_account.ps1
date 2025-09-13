# check_guest_account.ps1
try {
    $guest = Get-LocalUser -Name "Guest" -ErrorAction SilentlyContinue
    if ($guest -and $guest.Enabled -eq $true) {
        Write-Output "FAIL: Guest account is enabled"
        exit 1
    } else {
        Write-Output "PASS: Guest account is disabled"
        exit 0
    }
} catch {
    Write-Output "FAIL: Unable to verify Guest account"
    exit 1
}
