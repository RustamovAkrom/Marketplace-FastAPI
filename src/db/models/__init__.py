import importlib
import pkgutil
from pathlib import Path

__all__ = []


def load_all_models():
    package_dir = Path(__file__).resolve().parent

    for module_info in pkgutil.walk_packages(
        path=[str(package_dir)], prefix="db.models."
    ):
        module = importlib.import_module(module_info.name)

        # Если в модуле есть __all__, импортируем классы в namespace пакета
        if hasattr(module, "__all__"):
            for attr_name in module.__all__:
                globals()[attr_name] = getattr(module, attr_name)
                __all__.append(attr_name)


# Загружаем модели сразу при импорте пакета
load_all_models()
