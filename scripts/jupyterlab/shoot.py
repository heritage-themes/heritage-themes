"""Screenshots JupyterLab showing a notebook, a text editor, a menu and a dialog with each Heritage theme.

Usage: python3 shoot.py REQUEST.json

Runs in the virtual environment that preview.py creates in scripts/jupyterlab/.venv, where JupyterLab, ipykernel and the
extension's wheel are installed. REQUEST.json holds {"themes": [{"stem", "label"}], "samples": {file name: text},
"fonts": folder of JetBrains Mono's web fonts, "out": folder, "chrome": the browser's command, "workers": number}.
Each worker runs a JupyterLab server of its own, with a home folder, settings and workspaces in a temporary folder, so
nothing of the user's JupyterLab is read or changed, and a headless Chrome that it drives over the DevTools protocol.
The theme is chosen in the settings, as a user chooses it in Settings | Theme, and the PNGs go to
out/<stem>/<screen>.png. Prints {"failures": [...]}.
"""
import asyncio, base64, concurrent.futures, json, os, shutil, socket, subprocess, sys, tempfile, time
import urllib.request

import tornado.websocket

WIDTH, HEIGHT, EDITOR_HEIGHT = 1440, 1040, 560
FONT = "JetBrains Mono"
FONT_FILES = (("Regular", 400, "normal"), ("Italic", 400, "italic"), ("Bold", 700, "normal"),
              ("BoldItalic", 700, "italic"))
READY_SECONDS = 90
# The screens, in the order they are taken: the notebook, a menu and a dialog on its page, then the editor.
SCREENS = ("Notebook", "Settings menu", "Delete dialog", "Editor")
EDITOR_FILE = "orders.py"
NOTEBOOK_FILE = "analysis.ipynb"

# An error as a kernel prints it with the 16 ANSI colours; the 256-colour codes that IPython highlights code with are
# drawn in fixed colours that no theme sets.
TRACEBACK = [
    "\x1b[0;31m---------------------------------------------------------------------------\x1b[0m",
    "\x1b[0;31mZeroDivisionError\x1b[0m                         Traceback (most recent call last)",
    "Cell \x1b[0;32mIn[4], line 2\x1b[0m\n\x1b[1;32m      1\x1b[0m def mean(values):\n"
    "\x1b[0;32m----> 2\x1b[0m     return sum(values) / len(values)\n",
    "\x1b[0;31mZeroDivisionError\x1b[0m: division by zero",
]


def notebook():
    """A notebook with its outputs saved, so that it shows every output kind without running a cell: Markdown, code
    with comments, strings, numbers and classes, plain, coloured and HTML outputs, and an error."""
    def code(source, outputs, count):
        return {"cell_type": "code", "execution_count": count, "metadata": {}, "source": source, "outputs": outputs}
    def stream(text):
        return {"output_type": "stream", "name": "stdout", "text": text}
    table = ("<table border=\"1\" class=\"dataframe\"><thead><tr><th></th><th>region</th><th>orders</th><th>revenue"
             "</th></tr></thead><tbody><tr><th>0</th><td>Kerala</td><td>128</td><td>4210.50</td></tr><tr><th>1</th>"
             "<td>Gujarat</td><td>97</td><td>3188.25</td></tr><tr><th>2</th><td>Punjab</td><td>76</td><td>2904.00"
             "</td></tr></tbody></table>")
    return {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {"kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
                     "language_info": {"name": "python"}},
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "id": "a1",
             "source": ["# Order analysis\n", "\n", "Totals **per region**, with the *quarterly* trend and a "
                        "[link](https://example.com).\n", "\n", "- clean the data\n", "- group by region\n"]},
            {"cell_type": "code", "id": "a2", "execution_count": 1, "metadata": {}, "outputs": [stream("3 regions\n")],
             "source": ["import pandas as pd\n", "\n", "# Regions with their order counts\n",
                        "REGIONS = {\"Kerala\": 128, \"Gujarat\": 97, \"Punjab\": 76}\n",
                        "print(f\"{len(REGIONS)} regions\")"]},
            {"cell_type": "code", "id": "a3", "execution_count": 2, "metadata": {},
             "outputs": [{"output_type": "execute_result", "execution_count": 2, "metadata": {},
                          "data": {"text/html": table, "text/plain": "  region  orders  revenue"}}],
             "source": ["frame = pd.DataFrame({\"region\": list(REGIONS), \"orders\": list(REGIONS.values()),\n",
                        "                      \"revenue\": [4210.50, 3188.25, 2904.00]})\n", "frame"]},
            {"cell_type": "code", "id": "a4", "execution_count": 3, "metadata": {},
             "outputs": [stream("\x1b[1mbold\x1b[0m \x1b[31mred\x1b[0m \x1b[32mgreen\x1b[0m \x1b[33myellow\x1b[0m "
                                "\x1b[34mblue\x1b[0m \x1b[35mmagenta\x1b[0m \x1b[36mcyan\x1b[0m\n")],
             "source": ["class Order:\n", "    \"\"\"One order.\"\"\"\n", "\n",
                        "    def __init__(self, quantity: int = 0):\n", "        self.quantity = quantity\n"]},
            code(["def mean(values):\n", "    return sum(values) / len(values)\n", "\n", "mean([])"],
                 [{"output_type": "error", "ename": "ZeroDivisionError", "evalue": "division by zero",
                   "traceback": TRACEBACK}], 4),
        ],
    }


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def prepare(home, request):
    """The home folder of a worker: the settings that choose a theme, the font and no news prompt, and the files."""
    root = os.path.join(home, "files")
    os.makedirs(root)
    with open(os.path.join(root, NOTEBOOK_FILE), "w", encoding="utf-8") as f:
        json.dump(notebook(), f, indent=1)
    for name, text in request["samples"].items():
        with open(os.path.join(root, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    settings = os.path.join(home, "settings")

    def setting(plugin, values):
        path = os.path.join(settings, "@jupyterlab", plugin.replace(":", "/") + ".jupyterlab-settings")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(values, f)

    setting("apputils-extension:notification", {"fetchNews": "false"})
    setting("codemirror-extension:plugin", {"defaultConfig": {"fontFamily": FONT, "fontSize": 13}})
    return root, settings


def start_server(home, root, port):
    env = dict(os.environ, HOME=home, JUPYTER_CONFIG_DIR=os.path.join(home, "config"),
               JUPYTER_DATA_DIR=os.path.join(home, "data"), JUPYTER_RUNTIME_DIR=os.path.join(home, "runtime"),
               JUPYTERLAB_SETTINGS_DIR=os.path.join(home, "settings"),
               JUPYTERLAB_WORKSPACES_DIR=os.path.join(home, "workspaces"), JUPYTER_NO_CONFIG="1")
    log = open(os.path.join(home, "server.log"), "w")
    command = [os.path.join(os.path.dirname(sys.executable), "jupyter"), "lab", "--no-browser", "--ip=127.0.0.1",
               f"--port={port}", "--IdentityProvider.token=", f"--ServerApp.root_dir={root}", "--ServerApp.password=",
               "--LabApp.check_for_updates_class=jupyterlab.NeverCheckForUpdate"]
    server = subprocess.Popen(command, env=env, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(READY_SECONDS * 5):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/lab", timeout=2)
            return server
        except OSError:
            time.sleep(0.2)
    server.terminate()
    log.flush()
    with open(log.name, encoding="utf-8", errors="replace") as f:
        raise RuntimeError(f"JupyterLab did not start: {f.read()[-600:]}")


def font_script(fonts):
    """A script that Chrome runs on every page before its own: the font faces of JetBrains Mono, which the code and
    the outputs use, as data URLs so that no font has to be installed."""
    faces = []
    for name, weight, style in FONT_FILES:
        with open(os.path.join(fonts, f"JetBrainsMono-{name}.woff2"), "rb") as f:
            data = base64.b64encode(f.read()).decode()
        faces.append(f'@font-face{{font-family:"{FONT}";font-weight:{weight};font-style:{style};'
                     f'src:url(data:font/woff2;base64,{data}) format("woff2")}}')
    css = "".join(faces) + f':root{{--jp-code-font-family:"{FONT}",monospace}}'
    # JupyterLab asks before leaving a page with unsaved changes, which would stop the next screen from loading
    return ("window.addEventListener('beforeunload',e=>e.stopImmediatePropagation(),true);"
            "document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');"
            f"s.textContent={json.dumps(css)};document.head.appendChild(s)}});")


class Browser:
    """A headless Chrome driven over the DevTools protocol."""

    def __init__(self, chrome, home, fonts):
        self.port = free_port()
        self.process = subprocess.Popen(
            [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-color-profile=srgb",
             f"--user-data-dir={os.path.join(home, 'chrome')}", f"--remote-debugging-port={self.port}",
             f"--window-size={WIDTH},{HEIGHT}", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.fonts, self.counter, self.ws = fonts, 0, None

    async def open(self):
        for _ in range(100):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json"))
                target = next(t for t in tabs if t["type"] == "page")
                break
            except (OSError, StopIteration):
                await asyncio.sleep(0.2)
        else:
            raise RuntimeError("Chrome did not start")
        self.ws = await tornado.websocket.websocket_connect(target["webSocketDebuggerUrl"],
                                                            max_message_size=100_000_000)
        await self.call("Page.enable")
        await self.call("Emulation.setDeviceMetricsOverride", width=WIDTH, height=HEIGHT, deviceScaleFactor=1,
                        mobile=False)
        # a page that has no focus shows no kernel status in the status bar
        await self.call("Emulation.setFocusEmulationEnabled", enabled=True)
        await self.call("Page.addScriptToEvaluateOnNewDocument", source=self.fonts)

    async def call(self, method, **params):
        self.counter += 1
        await self.ws.write_message(json.dumps({"id": self.counter, "method": method, "params": params}))
        while True:
            message = json.loads(await self.ws.read_message())
            if message.get("id") == self.counter:
                if "error" in message:
                    raise RuntimeError(f"{method}: {message['error']}")
                return message.get("result", {})

    async def evaluate(self, expression):
        result = await self.call("Runtime.evaluate", expression=expression, returnByValue=True, awaitPromise=True)
        return result.get("result", {}).get("value")

    async def wait_for(self, expression, what, seconds=READY_SECONDS):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            if await self.evaluate(expression):
                return
            await asyncio.sleep(0.3)
        raise RuntimeError(f"timed out waiting for {what}")

    async def click(self, x, y):
        await self.call("Input.dispatchMouseEvent", type="mouseMoved", x=x, y=y)
        for kind in ("mousePressed", "mouseReleased"):
            await self.call("Input.dispatchMouseEvent", type=kind, x=x, y=y, button="left", clickCount=1)

    async def click_element(self, selector, text):
        """Clicks the centre of the first element that matches selector and contains text."""
        box = await self.evaluate(
            "(() => {for (const e of document.querySelectorAll(%s)) {if (e.textContent.includes(%s)) {"
            "const r = e.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2];}}})()"
            % (json.dumps(selector), json.dumps(text)))
        if not box:
            raise RuntimeError(f"no {selector} containing {text!r}")
        await self.click(*box)

    async def key(self, name, code, virtual):
        for kind in ("rawKeyDown", "keyUp"):
            await self.call("Input.dispatchKeyEvent", type=kind, key=name, code=code, windowsVirtualKeyCode=virtual)

    async def shot(self, path):
        data = (await self.call("Page.captureScreenshot", format="png"))["data"]
        with open(path, "wb") as f:
            f.write(base64.b64decode(data))

    def close(self):
        self.process.terminate()
        self.process.wait()


async def load(browser, port, path, label, ready):
    """Opens path in a fresh workspace and waits until JupyterLab has drawn it in the theme called label."""
    await browser.call("Page.navigate", url=f"http://127.0.0.1:{port}/lab/tree/{path}?reset")
    await browser.wait_for(f"document.body.dataset.jpThemeName === {json.dumps(label)}", f"the theme {label}")
    await browser.wait_for(ready, f"{path} to open")
    await asyncio.sleep(2)  # fonts, icons and the kernel's status settle


async def shoot_theme(browser, port, theme, out):
    folder = os.path.join(out, theme["stem"])
    os.makedirs(folder, exist_ok=True)
    await load(browser, port, NOTEBOOK_FILE, theme["label"],
               "document.querySelectorAll('.jp-Notebook .jp-Cell').length >= 5 && "
               "/Idle/.test(document.getElementById('jp-main-statusbar').textContent)")
    await browser.shot(os.path.join(folder, f"{SCREENS[0]}.png"))
    await browser.click_element(".lm-MenuBar-itemLabel", "Settings")
    await asyncio.sleep(1.2)
    await browser.shot(os.path.join(folder, f"{SCREENS[1]}.png"))
    await browser.key("Escape", "Escape", 27)
    await asyncio.sleep(0.6)
    await browser.click_element(".jp-DirListing-itemText", EDITOR_FILE)
    await asyncio.sleep(0.4)
    await browser.key("Delete", "Delete", 46)
    await browser.wait_for("!!document.querySelector('.jp-Dialog')", "the dialog")
    await asyncio.sleep(1)
    await browser.shot(os.path.join(folder, f"{SCREENS[2]}.png"))
    await load(browser, port, EDITOR_FILE, theme["label"], "!!document.querySelector('.jp-FileEditor .cm-content')")
    # a short file needs less window than a notebook
    await browser.call("Emulation.setDeviceMetricsOverride", width=WIDTH, height=EDITOR_HEIGHT, deviceScaleFactor=1,
                       mobile=False)
    await asyncio.sleep(1)
    await browser.shot(os.path.join(folder, f"{SCREENS[3]}.png"))
    await browser.call("Emulation.setDeviceMetricsOverride", width=WIDTH, height=HEIGHT, deviceScaleFactor=1,
                       mobile=False)


def worker(request, themes, index):
    """Shoots themes with a server and a browser of the worker's own; returns the failures."""
    failures = []
    home = tempfile.mkdtemp(prefix="heritage-jupyterlab-")
    server = browser = None
    try:
        root, settings = prepare(home, request)
        port = free_port()
        server = start_server(home, root, port)
        browser = Browser(request["chrome"], home, font_script(request["fonts"]))

        async def run():
            await browser.open()
            for theme in themes:
                path = os.path.join(settings, "@jupyterlab", "apputils-extension", "themes.jupyterlab-settings")
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump({"theme": theme["label"]}, f)
                try:
                    await shoot_theme(browser, port, theme, request["out"])
                except Exception as error:
                    failures.append(f"{theme['stem']}: {error}")
                    await browser.shot(os.path.join(request["out"], theme["stem"], "failure.png"))
        asyncio.run(run())
    except Exception as error:
        failures.append(f"worker {index}: {error}")
    finally:
        if browser:
            browser.close()
        if server:
            server.terminate()
            server.wait()
        shutil.rmtree(home, ignore_errors=True)
    return failures


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        request = json.load(f)
    workers = max(1, min(request["workers"], len(request["themes"])))
    chunks = [request["themes"][i::workers] for i in range(workers)]
    failures = []
    with concurrent.futures.ThreadPoolExecutor(workers) as pool:
        for result in pool.map(lambda args: worker(request, *args), [(c, i) for i, c in enumerate(chunks)]):
            failures += result
    print(json.dumps({"failures": failures}))


if __name__ == "__main__":
    main()
