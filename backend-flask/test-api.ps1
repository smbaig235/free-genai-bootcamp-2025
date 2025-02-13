# Create request body
$body = @{
    group_id = 1
    study_activity_id = 1
} | ConvertTo-Json

# Show what we're sending
Write-Host "Request body: $body"

# Make the request with verbose output
try {
    $response = Invoke-RestMethod `
        -Method POST `
        -Uri "http://localhost:5000/api/study-sessions" `
        -ContentType "application/json" `
        -Body $body `
        -Verbose

    Write-Host "`nSuccess! Response:"
    $response | ConvertTo-Json
} catch {
    Write-Host "`nError Response:"
    Write-Host "Status Code:" $_.Exception.Response.StatusCode.value__
    Write-Host "Error Message:" $_.ErrorDetails.Message
} 