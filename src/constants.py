from types import SimpleNamespace

from src.utils.keyboards import create_keyboard

keys = SimpleNamespace(
    random_connect=':bust_in_silhouette: Random Connect',
    settings=':gear: Settings',
)

keyboards = SimpleNamespace(
    main=create_keyboard(keys.random_connect, keys.settings),
)
