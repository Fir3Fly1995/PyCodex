[Setup]
AppName=Codex
AppVersion=1.0
DefaultDirName={localappdata}\Codex
DisableProgramGroupPage=yes
OutputBaseFilename=Codex Install
SetupFinishedRunNoAuto=yes
OutputDir=C:\Users\Alex Edwards\Downloads

[Files]
Source: "D:\GitHub\PyCodex\dist\CodexLauncher.exe"; DestDir: "{localappdata}\Codex"; Flags: ignoreversion
Source: "D:\GitHub\PyCodex\dist\codex.exe"; DestDir: "{localappdata}\Codex"; Flags: ignoreversion
Source: "D:\GitHub\PyCodex\dist\CodexUpdate.exe"; DestDir: "{localappdata}\Codex"; Flags: ignoreversion

[Icons]
Name: "{userdesktop}\Codex Launcher"; Filename: "{localappdata}\Codex\CodexLauncher.exe"

[Run]
Filename: "{localappdata}\Codex\CodexLauncher.exe"; Description: "Run Codex Launcher"; Flags: nowait postinstall skipifsilent