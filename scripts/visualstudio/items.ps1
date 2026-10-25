# Prints the default colours of the editor's display items in a running Visual Studio, under its Dark and Light themes,
# for scripts/visualstudio/tokens.py.
#
# Usage: items.ps1 -Categories <GUID>,<GUID>,...
#
# It connects to the Visual Studio that runs alone, reads the names of the Text Editor's display items through its
# automation model, switches the theme by writing environment.visualExperience.colorTheme to the settings.json of the
# instance, which Visual Studio applies as it changes, and reads each item of each category from the font and colour
# storage with the theme's defaults. It restores the theme before it exits. Each line is tab-separated: theme, category
# GUID, item name, foreground and background as RRGGBB, or "-" for a colour the item does not set.
param([Parameter(Mandatory)][string]$Categories)
$ErrorActionPreference = "Stop"
$ide = Split-Path -Parent ((Get-Process devenv | Select-Object -First 1).Path)
$assemblies = "OLE.Interop", "Interop", "Shell.Interop" | ForEach-Object { "$ide\PublicAssemblies\Microsoft.VisualStudio.$_.dll" }
foreach ($a in $assemblies) { [System.Reflection.Assembly]::LoadFrom($a) | Out-Null }
Add-Type -ReferencedAssemblies $assemblies -TypeDefinition @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using Microsoft.VisualStudio.Shell.Interop;
public static class FontAndColorDefaults {
    const uint ReadOnlyDefaults = 0x1 | 0x2;  // FCSF_READONLY | FCSF_LOADDEFAULTS: the theme's colours, not the user's
    static object Storage(object dte) {
        Guid iid = new Guid("6D5140C1-7436-11CE-8034-00AA006009FA");  // the OLE IServiceProvider that DTE implements
        IntPtr provider;
        Marshal.ThrowExceptionForHR(Marshal.QueryInterface(Marshal.GetIUnknownForObject(dte), ref iid, out provider));
        var services = (Microsoft.VisualStudio.OLE.Interop.IServiceProvider)Marshal.GetTypedObjectForIUnknown(
            provider, typeof(Microsoft.VisualStudio.OLE.Interop.IServiceProvider));
        Guid service = typeof(SVsFontAndColorStorage).GUID, storage = typeof(IVsFontAndColorStorage).GUID;
        IntPtr pointer;
        Marshal.ThrowExceptionForHR(services.QueryService(ref service, ref storage, out pointer));
        return Marshal.GetObjectForIUnknown(pointer);
    }
    // A stored colour as RRGGBB, "automatic" for the editor's own text or background colour, or "-" when not set. The
    // storage encodes indexed, system and Visual Studio colours in the COLORREF; the utilities decode them.
    static string Colour(IVsFontAndColorUtilities utilities, Guid category, int valid, uint encoded) {
        if (valid == 0) return "-";
        int type;
        Marshal.ThrowExceptionForHR(utilities.GetColorType(encoded, out type));
        if (type == (int)__VSCOLORTYPE.CT_AUTOMATIC) return "automatic";
        if (type == (int)__VSCOLORTYPE.CT_INVALID) return "-";
        uint rgb;
        Marshal.ThrowExceptionForHR(utilities.GetRGBOfEncodedColor(encoded, 0, ref category, out rgb));
        return string.Format("{0:X2}{1:X2}{2:X2}", rgb & 0xFF, rgb >> 8 & 0xFF, rgb >> 16 & 0xFF);
    }
    public static string[] Items(object dte, string category, string[] names) {
        object service = Storage(dte);
        var storage = (IVsFontAndColorStorage)service;
        var utilities = (IVsFontAndColorUtilities)service;
        Guid guid = new Guid(category);
        Marshal.ThrowExceptionForHR(storage.OpenCategory(ref guid, ReadOnlyDefaults));
        var lines = new List<string>();
        try {
            foreach (var name in names) {
                var info = new ColorableItemInfo[1];
                if (storage.GetItem(name, info) == 0) {
                    lines.Add(name + "\t" + Colour(utilities, guid, info[0].bForegroundValid, info[0].crForeground)
                              + "\t" + Colour(utilities, guid, info[0].bBackgroundValid, info[0].crBackground));
                }
            }
        } finally {
            storage.CloseCategory();
        }
        return lines.ToArray();
    }
}
"@
$dte = [System.Runtime.InteropServices.Marshal]::GetActiveObject("VisualStudio.DTE.18.0")
$names = @($dte.Properties("FontsAndColors", "TextEditor").Item("FontsAndColorsItems").Object | ForEach-Object { $_.Name })
# DTE.RegistryRoot is Software\Microsoft\VisualStudio\<instance>, the instance's folder in LocalAppData.
$settings = Join-Path "$env:LOCALAPPDATA\Microsoft\VisualStudio" (Split-Path -Leaf $dte.RegistryRoot) | Join-Path -ChildPath "settings.json"
$original = [IO.File]::ReadAllText($settings)
$key = '"environment.visualExperience.colorTheme"'
function Set-Theme([string]$theme) {
    $text = [IO.File]::ReadAllText($settings)
    if ($text -match [regex]::Escape($key)) {
        $text = [regex]::Replace($text, [regex]::Escape($key) + '\s*:\s*"[^"]*"', "$key`: `"$theme`"")
    } else {
        $text = ([regex]'\{').Replace($text, "{`n  $key`: `"$theme`",", 1)
    }
    [IO.File]::WriteAllText($settings, $text)
    Start-Sleep -Seconds 8  # Visual Studio reloads settings.json and repaints with the theme
}
try {
    foreach ($theme in "dark", "light") {
        Set-Theme $theme
        foreach ($category in $Categories.Split(",")) {
            foreach ($line in [FontAndColorDefaults]::Items($dte, $category, $names)) { "$theme`t$category`t$line" }
        }
    }
} finally {
    [IO.File]::WriteAllText($settings, $original)
}
