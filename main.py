import subprocess

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


def list_profiles():
    try:
        result = subprocess.run(
            ['autorandr', '--list'],
            capture_output=True, text=True, timeout=5
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        return []


def load_profile(profile):
    subprocess.Popen(['autorandr', '--load', profile])


class AutorandrExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, QueryHandler())
        self.subscribe(ItemEnterEvent, ItemEnterHandler())


class QueryHandler(EventListener):
    def on_event(self, event, extension):
        profiles = list_profiles()
        query = (event.get_argument() or '').lower().strip()

        if not profiles:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='No autorandr profiles found',
                    description='Run: autorandr --save <profile-name>',
                    on_enter=HideWindowAction(),
                )
            ])

        matches = [p for p in profiles if query in p.lower()] if query else profiles

        if not matches:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=f'No profiles matching "{query}"',
                    description='Try a different search term',
                    on_enter=HideWindowAction(),
                )
            ])

        return RenderResultListAction([
            ExtensionResultItem(
                icon='images/icon.png',
                name=profile,
                description=f'Load display profile: {profile}',
                on_enter=ExtensionCustomAction(profile, keep_app_open=False),
            )
            for profile in matches
        ])


class ItemEnterHandler(EventListener):
    def on_event(self, event, extension):
        load_profile(event.get_data())
        return HideWindowAction()


if __name__ == '__main__':
    AutorandrExtension().run()
