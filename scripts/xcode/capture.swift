// Window listing and editor cropping for scripts/xcode/screen.py, which compiles this file with swiftc.
//
// Usage: capture windows <pid>
//          prints, per on-screen window of the process at the normal level: id, width and height in points, and title,
//          separated by tabs
//        capture resize <pid> <title> <width>
//          sets the width in points of the process's window with that title, keeping its height
//        capture raise <pid> <title>
//          brings the process and its window with that title to the front, as the key window
//        capture crop <window.png> <editor.png> <window width> <background> <current line>
//          writes the editor of a window capture, converted to sRGB, and prints the scale of the capture (pixels per
//          point). The editor is the rows between the separator under the jump bar and the next one, over the status
//          bar or over the preview that Xcode shows under HTML in a narrow window: rows that are one colour, other than
//          the editor's background, from the window's left edge across its left third. It takes the window's width,
//          less its border, and is trimmed to the last row that holds code, with a margin. It fails when code reaches
//          the last points of the window, where Xcode cuts a line off. The window width is in points; the background
//          and the current line's colour are six-digit hex colours.
//
// resize and raise use the Accessibility API, which needs Accessibility permission for the terminal.
import AppKit
import ApplicationServices
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(("capture: " + message + "\n").data(using: .utf8)!)
    exit(1)
}

func windows(pid: Int32) {
    guard let list = CGWindowListCopyWindowInfo([.optionOnScreenOnly], kCGNullWindowID) as? [[String: Any]] else {
        fail("cannot list windows")
    }
    for window in list where window[kCGWindowOwnerPID as String] as? Int32 == pid
        && window[kCGWindowLayer as String] as? Int == 0 {
        let bounds = window[kCGWindowBounds as String] as? [String: CGFloat] ?? [:]
        let id = window[kCGWindowNumber as String] as? Int ?? 0
        let title = window[kCGWindowName as String] as? String ?? ""
        print("\(id)\t\(Int(bounds["Width"] ?? 0))\t\(Int(bounds["Height"] ?? 0))\t\(title)")
    }
}

/// The window of the process with that title, through the Accessibility API.
func window(pid: Int32, title: String) -> AXUIElement {
    var value: CFTypeRef?
    guard AXUIElementCopyAttributeValue(AXUIElementCreateApplication(pid), kAXWindowsAttribute as CFString, &value)
            == .success, let list = value as? [AXUIElement] else {
        fail("cannot list the windows of \(pid); the terminal needs Accessibility permission")
    }
    for window in list {
        var name: CFTypeRef?
        if AXUIElementCopyAttributeValue(window, kAXTitleAttribute as CFString, &name) == .success,
           name as? String == title {
            return window
        }
    }
    fail("\(pid) has no window \(title)")
}

func resize(pid: Int32, title: String, width: Int) {
    let window = window(pid: pid, title: title)
    var value: CFTypeRef?
    var size = CGSize.zero
    guard AXUIElementCopyAttributeValue(window, kAXSizeAttribute as CFString, &value) == .success,
          AXValueGetValue(value as! AXValue, .cgSize, &size) else { fail("cannot read the size of \(title)") }
    size.width = CGFloat(width)
    guard AXUIElementSetAttributeValue(window, kAXSizeAttribute as CFString, AXValueCreate(.cgSize, &size)!)
            == .success else { fail("cannot resize \(title)") }
}

func raise(pid: Int32, title: String) {
    let window = window(pid: pid, title: title)
    guard let app = NSRunningApplication(processIdentifier: pid), app.activate(),
          AXUIElementPerformAction(window, kAXRaiseAction as CFString) == .success,
          AXUIElementSetAttributeValue(window, kAXMainAttribute as CFString, kCFBooleanTrue) == .success else {
        fail("cannot bring \(title) to the front")
    }
}

/// The image's pixels as RGBA bytes in sRGB, with its width and height.
func pixels(_ path: String) -> ([UInt8], Int, Int) {
    guard let source = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil),
          let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else { fail("cannot read \(path)") }
    let width = image.width, height = image.height
    var data = [UInt8](repeating: 0, count: width * height * 4)
    let space = CGColorSpace(name: CGColorSpace.sRGB)!
    data.withUnsafeMutableBytes { buffer in
        let context = CGContext(data: buffer.baseAddress, width: width, height: height, bitsPerComponent: 8,
                                bytesPerRow: width * 4, space: space,
                                bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
        context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))
    }
    return (data, width, height)
}

func crop(input: String, output: String, points: Int, background: UInt32, line: UInt32) {
    let (data, width, height) = pixels(input)
    func pixel(_ x: Int, _ y: Int) -> UInt32 {
        let i = (y * width + x) * 4
        return UInt32(data[i]) << 16 | UInt32(data[i + 1]) << 8 | UInt32(data[i + 2])
    }
    let scale = width / max(points, 1)
    // The window's rounded corners and border take a few points at each side.
    let inset = 12 * scale
    // A separator is a line across the window from its left edge: at most two points of rows of one colour, other
    // than the background, between rows of other colours, and next to any other such rows, as under the jump bar of
    // the key window. Empty rows of the toolbar are one colour too, but many; the rule that a MARK: comment draws
    // starts after the gutter. The window's rounded corners, at its top and bottom edges, are left out.
    func uniform(_ y: Int) -> Bool {
        let first = pixel(0, y)
        return first != background && (0..<(width / 3)).allSatisfy { pixel($0, y) == first }
    }
    var lines: [ClosedRange<Int>] = []
    var y = inset
    while y < height - inset {
        guard uniform(y) else { y += 1; continue }
        var end = y
        while end + 1 < height - inset && uniform(end + 1) && pixel(0, end + 1) == pixel(0, y) { end += 1 }
        if end - y < 2 * scale && pixel(0, y - 1) != pixel(0, y) && pixel(0, end + 1) != pixel(0, y) {
            if let previous = lines.last, previous.upperBound + 1 == y {
                lines[lines.count - 1] = previous.lowerBound...end
            } else {
                lines.append(y...end)
            }
        }
        y = end + 1
    }
    // The editor starts under the first line and ends over the next.
    guard lines.count >= 2, lines[1].lowerBound - lines[0].upperBound > 40 * scale else {
        fail("\(input): no jump bar and status bar separators")
    }
    let top = lines[0].upperBound, bottom = lines[1].lowerBound
    // Code ends at the last column and row with a pixel that is not a mix of the background and the current line's
    // colour, as the rounded ends of the current line are, outside rows of one colour across the editor, such as the
    // rule that a MARK: comment draws.
    func code(_ colour: UInt32) -> Bool {
        [16, 8, 0].contains { shift in
            let value = Int(colour >> shift & 0xFF), a = Int(background >> shift & 0xFF), b = Int(line >> shift & 0xFF)
            return value < min(a, b) - 2 || value > max(a, b) + 2
        }
    }
    let left = 2 * scale, edge = width - 2 * scale
    var right = 0, last = top
    for y in (top + 1)..<bottom where !(inset..<(width - inset)).allSatisfy({ pixel($0, y) == pixel(inset, y) }) {
        for x in inset..<(width - inset) where code(pixel(x, y)) {
            right = max(right, x)
            last = y
        }
    }
    if right == width - inset - 1 {
        fail("\(input): code reaches the window's edge, where Xcode cuts it off; the sample is wider than the editor")
    }
    let margin = 12 * scale
    let area = CGRect(x: left, y: top + 1, width: edge - left, height: min(bottom, last + margin) - top - 1)
    let space = CGColorSpace(name: CGColorSpace.sRGB)!
    var copy = data
    let image: CGImage = copy.withUnsafeMutableBytes { buffer in
        let context = CGContext(data: buffer.baseAddress, width: width, height: height, bitsPerComponent: 8,
                                bytesPerRow: width * 4, space: space,
                                bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
        return context.makeImage()!.cropping(to: area)!
    }
    guard let destination = CGImageDestinationCreateWithURL(URL(fileURLWithPath: output) as CFURL,
                                                            UTType.png.identifier as CFString, 1, nil) else {
        fail("cannot write \(output)")
    }
    CGImageDestinationAddImage(destination, image, nil)
    if !CGImageDestinationFinalize(destination) { fail("cannot write \(output)") }
    print(scale)
}

let arguments = CommandLine.arguments
switch (arguments.count, arguments.count > 1 ? arguments[1] : "") {
case (3, "windows"):
    windows(pid: Int32(arguments[2]) ?? 0)
case (5, "resize"):
    resize(pid: Int32(arguments[2]) ?? 0, title: arguments[3], width: Int(arguments[4]) ?? 0)
case (4, "raise"):
    raise(pid: Int32(arguments[2]) ?? 0, title: arguments[3])
case (7, "crop"):
    guard let background = UInt32(arguments[5], radix: 16), let line = UInt32(arguments[6], radix: 16) else {
        fail("\(arguments[5]) or \(arguments[6]) is not a hex colour")
    }
    crop(input: arguments[2], output: arguments[3], points: Int(arguments[4]) ?? 0, background: background,
         line: line)
default:
    fail("usage: capture windows <pid> | capture resize <pid> <title> <width> | capture raise <pid> <title> | "
         + "capture crop <window.png> <editor.png> <window width> <background> <current line>")
}
