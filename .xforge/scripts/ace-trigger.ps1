$ErrorActionPreference = "SilentlyContinue"

# ACE Auto-Trigger (B-090)
# This script is called after each command execution to capture feedback.
# It reads the last command from session log and creates a feedback entry.

$SessionDir = Join-Path $env:USERPROFILE ".xforge/memory/sessions"
$FeedbackLog = Join-Path $env:USERPROFILE ".xforge/learning/feedback-log.jsonl"
$FeedbackStats = Join-Path $env:USERPROFILE ".xforge/learning/feedback-stats.json"

# Ensure directories exist
$feedbackDir = Split-Path $FeedbackLog -Parent
if (-not (Test-Path $feedbackDir)) {
    New-Item -ItemType Directory -Path $feedbackDir -Force | Out-Null
}

# Get the last executed command from XForge session
$lastCommand = $env:XFORGE_LAST_COMMAND
$lastResult = $env:XFORGE_LAST_RESULT
$lastDuration = $env:XFORGE_LAST_DURATION_MS

if ([string]::IsNullOrEmpty($lastCommand)) {
    # No command to capture feedback for
    exit 0
}

# Generate feedback entry
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
$feedbackId = "FB-" + (Get-Date -Format "yyyyMMdd") + "-" + (Get-Random -Minimum 1000 -Maximum 9999).ToString()

# Determine result
$result = "SUCCESS"
if ($LASTEXITCODE -ne 0) {
    $result = "FAIL"
} elseif (-not [string]::IsNullOrEmpty($lastResult)) {
    if ($lastResult -match "error|fail|exception") {
        $result = "PARTIAL"
    }
}

$entry = @{
    feedbackId = $feedbackId
    timestamp = $timestamp
    taskId = "AUTO-" + $feedbackId
    taskTitle = $lastCommand
    taskType = "command"
    complexity = "S"
    result = $result
    error = if ($result -ne "SUCCESS") { @{ message = "Command exited with code $LASTEXITCODE"; type = "runtime"; stackTrace = "" } } else { $null }
    solution = @{ applied = ($result -eq "SUCCESS"); description = if ($result -eq "SUCCESS") { "No action needed" } else { "Pending analysis" }; resolved = ($result -eq "SUCCESS") }
    context = @{
        provider = $env:XFORGE_PROVIDER
        model = $env:XFORGE_MODEL
        attemptNumber = 1
        durationMs = if ($lastDuration) { [int]$lastDuration } else { 0 }
    }
    tags = @("auto", "command")
    recurring = $false
    previousOccurrences = 0
}

# Append to feedback log (JSON Lines)
$entry | ConvertTo-Json -Compress | Add-Content $FeedbackLog -Encoding UTF8

# Update stats
$stats = @{
    version = "1.0.0"
    lastUpdated = $timestamp
    totalFeedbacks = 0
    byResult = @{ SUCCESS = 0; FAIL = 0; PARTIAL = 0 }
    byType = @{}
    byComplexity = @{ S = 0; M = 0; L = 0; CRITICA = 0 }
    recurringErrors = @()
    topErrors = @()
}

if (Test-Path $FeedbackStats) {
    try {
        $stats = Get-Content $FeedbackStats -Raw | ConvertFrom-Json
    } catch {}
}

$stats.totalFeedbacks++
$stats.byResult[$result]++
$stats.byComplexity["S"]++

$stats | ConvertTo-Json -Depth 3 | Set-Content $FeedbackStats -Encoding UTF8

exit 0
