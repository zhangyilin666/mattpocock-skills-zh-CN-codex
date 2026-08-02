# Human-in-the-loop reproduction loop for Windows PowerShell.
# Copy this file, edit the steps below, then run:
#   powershell -ExecutionPolicy Bypass -File .\hitl-loop.template.ps1

$ErrorActionPreference = "Stop"

function Invoke-Step {
    param([Parameter(Mandatory)][string]$Instruction)
    Write-Host "`n>>> $Instruction"
    [void](Read-Host "    [Press Enter when done]")
}

function Read-Capture {
    param([Parameter(Mandatory)][string]$Question)
    Write-Host "`n>>> $Question"
    return Read-Host "    >"
}

# --- edit below ---------------------------------------------------------

Invoke-Step "Open the app at http://localhost:3000 and sign in."
$errored = Read-Capture "Click the 'Export' button. Did it throw an error? (y/n)"
$errorMessage = Read-Capture "Paste the error message (or 'none'):"

# --- edit above ---------------------------------------------------------

Write-Host "`n--- Captured ---"
Write-Host "ERRORED=$errored"
Write-Host "ERROR_MSG=$errorMessage"
