# check_windows_update.ps1
try {
    $service = Get-Service -Name wuauserv -ErrorAction SilentlyContinue
    if ($service.Status -eq "Running") {
        Write-Output "PASS: Windows Update service is running"
        exit 0
    } else {
        Write-Output "FAIL: Windows Update service is not running"
        exit 1
    }
} catch {
    Write-Output "FAIL: Unable to check Windows Update service"
    exit 1
}
