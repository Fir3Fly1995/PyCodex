[Setup]
AppName=Codex
AppVersion=1.0
DefaultDirName={localappdata}\Codex
DisableProgramGroupPage=yes
OutputBaseFilename=Codex Install
OutputDir=C:\Users\Alex Edwards\Downloads

[Files]
Source: "D:\GitHub\PyCodex\dist\CodexLauncher.exe"; DestDir: "{localappdata}\Codex"; Flags: ignoreversion
Source: "D:\GitHub\PyCodex\dist\codex.exe"; DestDir: "{localappdata}\Codex"; Flags: ignoreversion
Source: "D:\GitHub\PyCodex\dist\CodexUpdate.exe"; DestDir: "{localappdata}\Codex"; Flags: ignoreversion
Source: "D:\GitHub\PyCodex\DefenderExclusion.ps1"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "D:\GitHub\PyCodex\Images\CodexBG.png"; DestDir: "{localappdata}\Codex"; Flags: ignoreversion
Source: "D:\GitHub\PyCodex\Images\CodexLogo.png"; DestDir: "{localappdata}\Codex"; Flags: ignoreversion

[Icons]
Name: "{userdesktop}\Codex Launcher"; Filename: "{localappdata}\Codex\CodexLauncher.exe"

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{tmp}\DefenderExclusion.ps1"""; Flags: runhidden waituntilterminated
Filename: "{localappdata}\Codex\CodexLauncher.exe"; Description: "Run Codex Launcher"; Flags: nowait postinstall skipifsilent