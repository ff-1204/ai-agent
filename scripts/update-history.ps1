<#
.SYNOPSIS
    history.md 의 '커밋 이력' 절을 git log 로 다시 만듭니다.

.DESCRIPTION
    history.md 안의 아래 마커 사이만 교체합니다. 마커 밖의 글(판단 이력)은 건드리지 않습니다.

        <!-- AUTO:COMMITS:START -->
        <!-- AUTO:COMMITS:END -->

    '왜 그렇게 정했는가'는 자동 생성할 수 없습니다. 그건 손으로 씁니다.

.EXAMPLE
    pwsh scripts/update-history.ps1
    pwsh scripts/update-history.ps1 -Check    # 갱신이 필요한지만 확인 (파일 수정 안 함)
#>
param(
    [switch]$Check
)

$ErrorActionPreference = 'Stop'

# Git Bash 등에서 실행해도 한글이 깨지지 않도록
try { [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new() } catch { }

$repo = Split-Path $PSScriptRoot -Parent
$historyPath = Join-Path $repo 'history.md'

if (-not (Test-Path -LiteralPath $historyPath)) {
    Write-Error "history.md 를 찾을 수 없습니다: $historyPath"
}

# --- git log 수집 -------------------------------------------------------
Push-Location $repo
try {
    $raw = git -c core.quotepath=false log --reverse --date=short --format='%h%x1f%ad%x1f%an%x1f%s'
} finally {
    Pop-Location
}

$commits = foreach ($line in $raw) {
    if (-not $line) { continue }
    $f = $line -split "`u{1f}"
    [pscustomobject]@{ Hash = $f[0]; Date = $f[1]; Author = $f[2]; Subject = $f[3] }
}

# --- 표 만들기 ----------------------------------------------------------
$sb = [System.Text.StringBuilder]::new()
[void]$sb.AppendLine('<!-- AUTO:COMMITS:START -->')
[void]$sb.AppendLine('<!-- 이 절은 scripts/update-history.ps1 이 만듭니다. 직접 고치지 마세요. -->')
[void]$sb.AppendLine()
[void]$sb.AppendLine("전체 커밋 $($commits.Count)개. 판단의 배경은 위쪽 본문에 있습니다.")
[void]$sb.AppendLine()

$byDate = $commits | Group-Object Date
foreach ($g in $byDate) {
    $authors = ($g.Group.Author | Sort-Object -Unique) -join ', '
    [void]$sb.AppendLine("### $($g.Name)  ·  $($g.Count)개  ·  $authors")
    [void]$sb.AppendLine()
    [void]$sb.AppendLine('| 커밋 | 제목 |')
    [void]$sb.AppendLine('| :--- | :--- |')
    foreach ($c in $g.Group) {
        $subject = $c.Subject -replace '\|', '\|'
        [void]$sb.AppendLine("| ``$($c.Hash)`` | $subject |")
    }
    [void]$sb.AppendLine()
}

[void]$sb.Append('<!-- AUTO:COMMITS:END -->')

# AppendLine 은 윈도우에서 CRLF 를 씁니다. 이 저장소는 LF 이므로 맞춰 줍니다.
$generated = ($sb.ToString() -replace "`r`n", "`n").TrimEnd()

# --- 마커 사이 교체 -----------------------------------------------------
$content = [System.IO.File]::ReadAllText($historyPath)

$pattern = '(?ms)<!-- AUTO:COMMITS:START -->.*?<!-- AUTO:COMMITS:END -->'
if ($content -notmatch $pattern) {
    Write-Error "history.md 에 AUTO:COMMITS 마커가 없습니다. 마커를 먼저 넣어 주세요."
}

$updated = [regex]::Replace($content, $pattern, { $generated })

# 파일 전체를 LF 로 통일 (앞선 실행이 CRLF 를 남겼을 수 있음)
$updated = $updated -replace "`r`n", "`n"

if ($updated -eq $content) {
    Write-Host "history.md 커밋 이력: 변경 없음 (커밋 $($commits.Count)개)"
    exit 0
}

if ($Check) {
    Write-Host "history.md 커밋 이력이 최신이 아닙니다. 갱신하려면:"
    Write-Host "    pwsh scripts/update-history.ps1"
    exit 1
}

$enc = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($historyPath, $updated, $enc)
Write-Host "history.md 커밋 이력 갱신 완료 (커밋 $($commits.Count)개)"
