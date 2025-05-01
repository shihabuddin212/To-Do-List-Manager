#define MyAppName "Todo List Manager"
#define MyAppVersion "1.0"
#define MyAppPublisher "Your Name"
#define MyAppURL "https://www.example.com/"
#define MyAppExeName "todo_gui.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{6A78F0E2-69B6-4F47-8B1A-F5C248B29341}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=TodoListManager_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=todo_icon.ico
; Create output directory if it doesn't exist
OutputDir=Output

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\todo_gui.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "todo_icon.ico"; DestDir: "{app}"; Flags: ignoreversion
; Include tasks.json if it exists
Source: "tasks.json"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists('tasks.json')

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\todo_icon.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\todo_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent 