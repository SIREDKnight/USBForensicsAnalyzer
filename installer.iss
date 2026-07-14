#define MyAppName "USB Forensics Analyzer"
#define MyAppVersion "1.0"
#define MyAppPublisher "USB Forensics Analyzer"
#define MyAppExeName "USBForensicsAnalyzer.exe"

[Setup]
AppId={{USBForensicsAnalyzer}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\USBForensicsAnalyzer

DefaultGroupName={#MyAppName}

OutputDir=installer_output
OutputBaseFilename=USBForensicsAnalyzer_Setup

Compression=lzma
SolidCompression=yes

SetupIconFile=assets/usb.ico

ArchitecturesInstallIn64BitMode=x64compatible


[Files]

Source: "dist\USBForensicsAnalyzer\*"; \
DestDir: "{app}"; \
Flags: recursesubdirs createallsubdirs


[Icons]

Name: "{autoprograms}\USB Forensics Analyzer"; \
Filename: "{app}\USBForensicsAnalyzer.exe"

Name: "{autodesktop}\USB Forensics Analyzer"; \
Filename: "{app}\USBForensicsAnalyzer.exe"


[Run]

Filename: "{app}\USBForensicsAnalyzer.exe"; \
Description: "Launch USB Forensics Analyzer"; \
Flags: nowait postinstall skipifsilent