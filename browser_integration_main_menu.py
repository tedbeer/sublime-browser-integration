from .browser_integration import *

from .browser_integration_launch import *
from .browser_integration_reload import *
from .browser_integration_navigate import *
from .browser_integration_execute import *
from .browser_integration_jscad import *
from .browser_integration_stylesheets import *
from .browser_integration_select import *
from .browser_integration_selectint import *
from .browser_integration_source import *
from .browser_integration_click import *
from .browser_integration_type import *
from .browser_integration_class import *
from .browser_integration_record import *
from .browser_integration_stop import *
from .browser_integration_play import *
from .browser_integration_localstorage import *
from .browser_integration_quit import *


class BrowserIntegrationMainMenuCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        main_menu_commands = [
            BrowserIntegrationLaunchCommand,
            BrowserIntegrationReloadCommand,
            BrowserIntegrationNavigateCommand,
            ("Execute", "Execute snippets of code in the browser.", [
                BrowserIntegrationExecuteCommand,
		BrowserIntegrationJSCADCommand,
            ]),
            ("View", "View and modify text data of current document", [
                BrowserIntegrationStylesheetsCommand,
                BrowserIntegrationSourceCommand,
                BrowserIntegrationLocalstorageCommand,
            ]),
            ("Interact", "Interact with the document elements.", [
                BrowserIntegrationSelectCommand,
                BrowserIntegrationSelectxpathCommand,
                BrowserIntegrationSelectintCommand,
                BrowserIntegrationClickCommand,
                BrowserIntegrationTypeCommand,
                BrowserIntegrationClassCommand,
            ]),
            ("Macro", "Record and replay browser interaction.", [
                BrowserIntegrationRecordCommand,
                BrowserIntegrationStopCommand,
                BrowserIntegrationPlayCommand,
                BrowserIntegrationPlaydelayCommand,
            ]),
            BrowserIntegrationQuitCommand
        ]

        def filter_visible(cmd):
            if not isinstance(cmd, tuple):
                if cmd.visible():
                    return cmd
                else:
                    return None

            name, desc, submenu = cmd
            submenu = [filter_visible(c) for c in submenu
                       if filter_visible(c)]

            if submenu:
                return name, desc, submenu

            return None

        main_menu_commands = [filter_visible(c) for c in main_menu_commands
                              if filter_visible(c)]

        def select_command_func(commands):
            def select_command(i):
                if i < 0:
                    return

                command = commands[i]

                if isinstance(command, tuple):
                    name, desc, l = command

                    @async
                    def quick_panel():
                        sublime.active_window().show_quick_panel([
                            [command_name(item)] +
                            command_description(item).split("\n")
                            for item in l
                        ], select_command_func(l))

                    quick_panel()

                else:
                    cmd = command_str(command)

                    if issubclass(command, sublime_plugin.ApplicationCommand):
                        sublime.run_command(cmd)
                    elif issubclass(command, sublime_plugin.WindowCommand):
                        sublime.active_window().run_command(cmd)
                    elif issubclass(command, sublime_plugin.TextCommand):
                        sublime.active_window().active_view().run_command(cmd)

            return select_command

        def command_str(cls):
            name = cls.__name__
            return "browser_integration_" + name[18:-7].lower()

        def command_name(cls):
            if isinstance(cls, tuple):
                name, desc, l = cls
                return name

            return cls.plugin_name

        def command_description(cls):
            if isinstance(cls, tuple):
                name, desc, l = cls
                return desc

            return cls.plugin_description

        sublime.active_window().show_quick_panel([
            [command_name(cls)] + command_description(cls).split("\n")
            for cls in main_menu_commands
        ], select_command_func(main_menu_commands))
