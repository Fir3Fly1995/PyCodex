[Setup]
AppName=Codex
AppVersion=1.0
DefaultDirName={localappdata}\Codex
DisableProgramGroupPage=yes
OutputBaseFilename=Codex Install

[Files]
Source: "E:\CodexPython\PyCodex\dist\CodexLauncher.exe"; DestDir: "{localappdata}\Codex"; Flags: ignoreversion
Source: "E:\CodexPython\PyCodex\dist\codex.exe"; DestDir: "{localappdata}\Codex"; Flags: ignoreversion

[Icons]
Name: "{userdesktop}\Codex Launcher"; Filename: "{localappdata}\Codex\CodexLauncher.exe"

[Run]
Filename: "{localappdata}\Codex\CodexLauncher.exe"; Description: "Run Codex Launcher"; Flags: nowait postinstall skipifsilent