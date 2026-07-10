[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [string]$CodexHome = $(
        if ($env:CODEX_HOME) { $env:CODEX_HOME }
        else { Join-Path $HOME '.codex' }
    ),
    [ValidateSet('User', 'Project')]
    [string]$Scope = 'User',
    [string]$ProjectRoot = (Get-Location).Path,
    [switch]$Force,
    [switch]$RunDoctor
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Resolve-SkillTarget {
    if ($Scope -eq 'Project') {
        return Join-Path $ProjectRoot '.agents\skills\godogen'
    }

    return Join-Path $CodexHome 'skills\godogen'
}

function Test-SafeTarget {
    param([Parameter(Mandatory)][string]$Path)

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    $root = [System.IO.Path]::GetPathRoot($fullPath)
    if ($fullPath -eq $root -or $fullPath.Length -lt ($root.Length + 6)) {
        throw "Refusing unsafe target path: $fullPath"
    }

    if ((Split-Path $fullPath -Leaf) -ne 'godogen') {
        throw "Target must end in a godogen directory: $fullPath"
    }
}

$source = Join-Path $SourceRoot '.agents\skills\godogen'
if (-not (Test-Path (Join-Path $source 'SKILL.md') -PathType Leaf)) {
    throw "Native skill source was not found at $source"
}

$target = Resolve-SkillTarget
Test-SafeTarget -Path $target

$backup = $null
if (Test-Path $target) {
    if (-not $Force) {
        throw "GodoGen is already installed at $target. Re-run with -Force to replace it safely."
    }

    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $backup = "$target.backup-$stamp"
    if ($PSCmdlet.ShouldProcess($target, "Back up existing installation to $backup")) {
        Move-Item -LiteralPath $target -Destination $backup
    }
}

$parent = Split-Path $target -Parent
if ($PSCmdlet.ShouldProcess($target, 'Install native GodoGen Codex skill')) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $target -Recurse
}

$installedSkill = Join-Path $target 'SKILL.md'
$installedMetadata = Join-Path $target 'agents\openai.yaml'
if (-not (Test-Path $installedSkill -PathType Leaf)) {
    throw "Installation verification failed: missing $installedSkill"
}
if (-not (Test-Path $installedMetadata -PathType Leaf)) {
    throw "Installation verification failed: missing $installedMetadata"
}

Write-Host "GodoGen installed at: $target"
if ($backup) {
    Write-Host "Previous installation backed up at: $backup"
}

if ($RunDoctor) {
    $doctor = Join-Path $target 'scripts\doctor.py'
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        $python = Get-Command py -ErrorAction SilentlyContinue
    }
    if (-not $python) {
        throw 'Python was not found. Installation succeeded, but the doctor could not run.'
    }

    $artifact = Join-Path $ProjectRoot 'artifacts\godogen\doctor.json'
    & $python.Source $doctor --project $ProjectRoot --json $artifact
    if ($LASTEXITCODE -ne 0) {
        throw "Environment doctor failed with exit code $LASTEXITCODE"
    }
}
