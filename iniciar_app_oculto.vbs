Set WshShell = CreateObject("WScript.Shell")
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.Run Chr(34) & scriptDir & "\iniciar_app_windows.bat" & Chr(34), 0
Set WshShell = Nothing
