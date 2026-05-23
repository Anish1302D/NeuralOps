$delaySeconds = 10

Write-Host "Starting real-time GitHub continuous sync (every $delaySeconds seconds)..."
Write-Host "Close this terminal to stop syncing."

while ($true) {
    Start-Sleep -Seconds $delaySeconds
    
    # Check if there are any changes to track
    $status = git status --porcelain
    if (-not [string]::IsNullOrWhiteSpace($status)) {
        $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        Write-Host "Changes detected at $timestamp. Syncing to GitHub..."
        
        git add .
        git commit -m "Auto-update: $timestamp" | Out-Null
        git push | Out-Null
        
        Write-Host "Sync successful!"
    }
}
