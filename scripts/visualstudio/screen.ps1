# Captures the code samples as Visual Studio draws them in each theme of a VSIX, for preview.py --visualstudio.
#
# Usage: screen.ps1 -Vsix <path> -Id <VSIX identity> -Themes <id>,<id>,... -Samples <folder> -Out <folder>
#
# It installs the VSIX into a Visual Studio instance of its own (/rootSuffix HeritagePreview), so the user's settings
# and extensions stay untouched, and starts that instance on the samples folder, passing its first-run dialog. It
# turns off CodeLens and error squiggles, which mark the samples' unresolved imports. For each theme, named by the ID
# that settings.json gives it, it switches the theme through settings.json and saves, per sample, the editor's margins
# and text as <Out>\<theme>\<sample>.png. It closes the instance at the end.
param([Parameter(Mandatory)][string]$Vsix, [Parameter(Mandatory)][string]$Id, [Parameter(Mandatory)][string]$Themes,
      [Parameter(Mandatory)][string]$Samples, [Parameter(Mandatory)][string]$Out)
$ErrorActionPreference = "Stop"
$suffix = "HeritagePreview"
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
$vs = & $vswhere -version "[18.0,19.0)" -latest -format json | ConvertFrom-Json | Select-Object -First 1
if (-not $vs) { throw "Visual Studio 2026 is not installed" }
$ide = Split-Path -Parent $vs.productPath
$hive = "$env:LOCALAPPDATA\Microsoft\VisualStudio\18.0_$($vs.instanceId)$suffix"
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes, System.Drawing
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.ComTypes;
public static class Native {
    [DllImport("ole32.dll")] static extern int GetRunningObjectTable(int reserved, out IRunningObjectTable table);
    [DllImport("ole32.dll")] static extern int CreateBindCtx(int reserved, out IBindCtx context);
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr window, IntPtr dc, uint flags);
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr window, out RECT rect);
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
    // The DTE of the Visual Studio process with this ID, from the running object table, or null.
    public static object Dte(int process) {
        IRunningObjectTable table;
        GetRunningObjectTable(0, out table);
        IEnumMoniker monikers;
        table.EnumRunning(out monikers);
        var moniker = new IMoniker[1];
        while (monikers.Next(1, moniker, IntPtr.Zero) == 0) {
            IBindCtx context;
            CreateBindCtx(0, out context);
            string name;
            moniker[0].GetDisplayName(context, null, out name);
            if (name.StartsWith("!VisualStudio.DTE.") && name.EndsWith(":" + process)) {
                object dte;
                table.GetObject(moniker[0], out dte);
                return dte;
            }
        }
        return null;
    }
}
"@
Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @"
using System.Drawing;
public static class Trim {
    // The part of an editor capture that holds code: up to the last column and row with a pixel that differs from its
    // row's background, the colour at the row's right end, which is the caret row's on the caret's line; with a margin.
    public static Bitmap Code(Bitmap image, int margin) {
        int right = 0, bottom = 0;
        for (int y = 0; y < image.Height; y++) {
            Color background = image.GetPixel(image.Width - 1, y);
            for (int x = 0; x < image.Width; x++)
                if (image.GetPixel(x, y) != background) { if (x > right) right = x; if (y > bottom) bottom = y; }
        }
        var area = new Rectangle(0, 0, System.Math.Min(image.Width, right + margin), System.Math.Min(image.Height, bottom + margin));
        return image.Clone(area, image.PixelFormat);
    }
}
"@
[Native]::SetProcessDPIAware() | Out-Null

function Close-Instance {
    $running = Get-CimInstance Win32_Process -Filter "Name='devenv.exe'" | Where-Object { $_.CommandLine -like "*/rootSuffix $suffix*" }
    foreach ($r in $running) {
        $p = Get-Process -Id $r.ProcessId -ErrorAction SilentlyContinue
        if ($p) { $p.CloseMainWindow() | Out-Null; if (-not $p.WaitForExit(60000)) { throw "Visual Studio $($r.ProcessId) did not close" } }
    }
}
function Write-Settings([hashtable]$values) {
    $path = "$hive\settings.json"
    $text = if (Test-Path $path) { [IO.File]::ReadAllText($path) } else { "{`n}" }
    foreach ($key in $values.Keys) {
        $value = $values[$key] | ConvertTo-Json
        $pattern = '"' + [regex]::Escape($key) + '"\s*:\s*[^,\r\n}]+'
        if ($text -match $pattern) { $text = [regex]::Replace($text, $pattern, "`"$key`": $value") }
        else { $text = ([regex]'\{').Replace($text, "{`n  `"$key`": $value,", 1) }
    }
    $text = [regex]::Replace($text, ',(\s*})', '$1')
    [IO.File]::WriteAllText($path, $text)
}
function Find([System.Windows.Automation.AutomationElement]$root, [string]$property, [string]$value) {
    $id = [System.Windows.Automation.AutomationElement]::"${property}Property"
    $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, (New-Object System.Windows.Automation.PropertyCondition $id, $value))
}
function Show-Document([string]$path) {
    # Brings the document to the front with the caret at its start. Visual Studio can take a moment after a theme
    # change before the document is the active one.
    for ($i = 0; $i -lt 20; $i++) {
        $window = $dte.ItemOperations.OpenFile($path)
        if ($window) { $window.Activate() }
        $active = $dte.ActiveDocument
        if ($active -and $active.FullName -ieq $path) { $active.Selection.StartOfDocument(); return }
        Start-Sleep -Milliseconds 500
    }
    throw "Visual Studio does not show $path"
}
function Invoke-Control([System.Windows.Automation.AutomationElement]$element) {
    $pattern = $null
    if ($element.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$pattern)) { $pattern.Invoke() }
}

Close-Instance
& "$ide\VSIXInstaller.exe" /q "/rootSuffix:$suffix" "/instanceIds:$($vs.instanceId)" "/u:$Id" | Out-Null
$install = Start-Process -FilePath "$ide\VSIXInstaller.exe" -Wait -PassThru `
    -ArgumentList '/q', "/rootSuffix:$suffix", "/instanceIds:$($vs.instanceId)", "`"$Vsix`""
if ($install.ExitCode) { throw "VSIXInstaller failed with $($install.ExitCode); its log is in $env:TEMP" }
Start-Process -FilePath "$ide\devenv.exe" -ArgumentList '/rootSuffix', $suffix, '/updateConfiguration' -Wait | Out-Null

$process = Start-Process -FilePath "$ide\devenv.exe" -ArgumentList '/rootSuffix', $suffix, "`"$Samples`"" -PassThru
$dte = $null
for ($i = 0; $i -lt 120 -and -not $dte; $i++) {
    Start-Sleep -Seconds 2
    # A new instance first asks for an account and a theme.
    $windows = [System.Windows.Automation.AutomationElement]::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children,
        (New-Object System.Windows.Automation.PropertyCondition ([System.Windows.Automation.AutomationElement]::ProcessIdProperty), $process.Id))
    foreach ($w in $windows) { foreach ($id in "NotNowLink", "FinishButton") { foreach ($e in Find $w "AutomationId" $id) { Invoke-Control $e } } }
    $dte = [Native]::Dte($process.Id)
}
if (-not $dte) { throw "Visual Studio did not start" }
try {
    Write-Settings @{ "textEditor.codeLens.enabled" = $false; "textEditor.general.display.errorSquiggles" = $false }
    # Twice the default size, so that the page, drawn at twice its size, shows the captures sharp at half theirs.
    $dte.Properties("FontsAndColors", "TextEditor").Item("FontSize").Value = 20
    $files = Get-ChildItem $Samples -File | Sort-Object Name
    foreach ($f in $files) { $dte.ItemOperations.OpenFile($f.FullName) | Out-Null }
    $dte.ExecuteCommand("View.FullScreen")  # the editor alone, with room for every sample at that size
    Start-Sleep -Seconds 30  # the language services classify the open documents
    $window = $process.MainWindowHandle
    foreach ($theme in $Themes.Split(",")) {
        Write-Settings @{ "environment.visualExperience.colorTheme" = "dark" }
        Start-Sleep -Seconds 4
        Write-Settings @{ "environment.visualExperience.colorTheme" = $theme }
        Start-Sleep -Seconds 8
        New-Item -ItemType Directory -Force "$Out\$theme" | Out-Null
        foreach ($f in $files) {
            Show-Document $f.FullName
            Start-Sleep -Seconds 2
            $root = [System.Windows.Automation.AutomationElement]::FromHandle($window)
            $view = (Find $root "ClassName" "WpfTextView" | Where-Object { -not $_.Current.IsOffscreen } | Select-Object -First 1).Current.BoundingRectangle
            $margin = (Find $root "ClassName" "GlyphMarginGrid" | Where-Object { -not $_.Current.IsOffscreen } | Select-Object -First 1).Current.BoundingRectangle
            $rect = New-Object Native+RECT
            [Native]::GetWindowRect($window, [ref]$rect) | Out-Null
            $full = New-Object System.Drawing.Bitmap ($rect.Right - $rect.Left), ($rect.Bottom - $rect.Top)
            $g = [System.Drawing.Graphics]::FromImage($full)
            $dc = $g.GetHdc(); [Native]::PrintWindow($window, $dc, 2) | Out-Null; $g.ReleaseHdc($dc); $g.Dispose()
            $crop = New-Object System.Drawing.Rectangle ([int]$margin.Left - $rect.Left), ([int]$view.Top - $rect.Top), `
                ([int]($view.Right - $margin.Left)), ([int]$view.Height)
            $editor = $full.Clone($crop, $full.PixelFormat)
            $code = [Trim]::Code($editor, 24)
            $code.Save("$Out\$theme\$($f.Name).png", [System.Drawing.Imaging.ImageFormat]::Png)
            $code.Dispose(); $editor.Dispose(); $full.Dispose()
        }
    }
} finally {
    $dte.Quit()
    if (-not $process.WaitForExit(120000)) { throw "Visual Studio did not close" }
}
