from .browser_integration import *


class BrowserIntegrationJSCADCommand(sublime_plugin.TextCommand):
    plugin_name = "Execute jscad code"
    plugin_description = "Executes jscad code in the browser."

    @staticmethod
    def visible():
        return browser.connected()

    @require_browser
    @async
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                continue

            s = self.view.substr(region)
            #status("Executing `%s`" % s)
            result = browser.execute("gProcessor.setJsCad('" + s "')")
