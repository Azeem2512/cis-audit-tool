# check_defender.ps1 - returns 'PASS' or 'FAIL' and a short message
try {
    if (Get-Command Get-MpComputerStatus -ErrorAction SilentlyContinue) {
        $s = Get-MpComputerStatus
        if ($s.AntispywareEnabled -and $s.AntivirusEnabled) {
            Write-Output "PASS: Defender enabled"
            exit 0
        } else {
            Write-Output "FAIL: Defender disabled or not fully enabled"
            exit 2
        }
    } else {
        # Fallback - check service
        $svc = Get-Service -Name WinDefend -ErrorAction SilentlyContinue
        if ($svc -and $svc.Status -eq 'Running') {
            Write-Output "PASS: WinDefend running"
            exit 0
        } else {
            Write-Output "FAIL: WinDefend not running"
            exit 2
        }
    }
} catch {
    Write-Output "ERROR: $_"
    exit 3
}
