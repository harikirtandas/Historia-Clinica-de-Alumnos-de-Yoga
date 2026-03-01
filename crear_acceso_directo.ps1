$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$batPath = Join-Path $repoRoot "iniciar_app_oculto.vbs"
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "HCA Yoga.lnk"

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $batPath
$shortcut.WorkingDirectory = $repoRoot
$shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll, 1"
$shortcut.Save()

Write-Host "Acceso directo creado en el escritorio: $shortcutPath"
