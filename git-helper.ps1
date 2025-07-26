# git-helper.ps1

function Prompt-And-Run {
    param (
        [string]$PromptMessage,
        [scriptblock]$Action
    )

    $confirm = Read-Host "$PromptMessage (y/n)"
    if ($confirm -eq 'y') {
        & $Action
    } elseif ($confirm -eq 'n') {
        Write-Host "Operation cancelled. Exiting script." -ForegroundColor Yellow
        exit
    } else {
        Write-Host "Invalid input. Exiting script." -ForegroundColor Red
        exit
    }
}

# Step 1: Add all changes
Prompt-And-Run "Run 'git add .'" { git add . }

# Step 2: Git status
Prompt-And-Run "Run 'git status'" { git status }

# Step 3: Commit
Prompt-And-Run "Run 'git commit'" {
    $message = Read-Host "Enter commit message"
    git commit -m "$message"
}

# Step 4: Set branch to main (first time only)
Prompt-And-Run "Run 'git branch -M main'" { git branch -M main }

# Step 5: Push
Prompt-And-Run "Run 'git push -u origin main'" { git push -u origin main }