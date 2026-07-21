#define MyAppName "USB Forensics Analyzer"
#define MyAppVersion "1.0"
#define MyAppPublisher "Joe"
#define MyAppExeName "USBForensicsAnalyzer.exe"

[Setup]
AppId={{USBForensicsAnalyzer}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\USB Forensics Analyzer

DefaultGroupName={#MyAppName}

OutputDir=installer_output

OutputBaseFilename=USBForensicsAnalyzer_Setup

Compression=lzma
SolidCompression=yes

WizardStyle=modern

SetupIconFile=assets\usb.ico


[Files]

Source: "dist\USBForensicsAnalyzer\*"; \
DestDir: "{app}"; \
Flags: recursesubdirs createallsubdirs


[Icons]

Name: "{group}\USB Forensics Analyzer"; \
Filename: "{app}\USBForensicsAnalyzer.exe"

Name: "{autodesktop}\USB Forensics Analyzer"; \
Filename: "{app}\USBForensicsAnalyzer.exe"


[Run]

Filename: "{app}\USBForensicsAnalyzer.exe"; \
Description: "Launch USB Forensics Analyzer"; \
Flags: nowait postinstall skipifsilent