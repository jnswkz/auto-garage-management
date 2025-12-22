#define MyAppName "Auto Garage Management"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Garage Co."
#define MyAppExeName "AutoGarage.exe"
#define MyAppId "{{E5E3FA4D-1C29-4A9D-9E9B-3FE8D2CC0E9C}}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\AutoGarageManagement
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=AutoGarageSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; Flags: unchecked

[Files]
Source: "..\\dist\\AutoGarage\\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs
Source: "mysql\\*"; DestDir: "{app}\\mysql"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon
