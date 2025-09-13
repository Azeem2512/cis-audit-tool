# check_autorun.ps1
try {
    $reg = Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" -ErrorAction SilentlyContinue
    if ($reg.NoDriveTypeAutoRun -band 0xFF) {
        Write-Output "PASS: AutoRun is disabled"
        exit 0
    } else {
        Write-Output "FAIL: AutoRun is not properly disabled"
        exit 1
    }
} catch {
    Write-Output "FAIL: Unable to check AutoRun setting"
    exit 1
}
