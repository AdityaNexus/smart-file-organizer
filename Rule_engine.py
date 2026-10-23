
import json
from pathlib import Path

from File_item import FileItem


class RuleEngine:
    def __init__(self, config_path: str | Path = "config.json"):
        self.config_path = Path(config_path)
        self.extension_rules = {}
        self.default_category = "Others"

        self.load_rules()

    def load_rules(self):
        with self.config_path.open("r", encoding="utf-8") as file:
            config = json.load(file)

        categories = config.get("categories", {})
        default_category = config.get("default_category", "Others")

        if not isinstance(categories, dict):
            raise ValueError("'categories' must be a dictionary.")

        if not isinstance(default_category, str) or not default_category:
            raise ValueError("'default_category' must be a non-empty string.")

        extension_rules = {}

        for category, extensions in categories.items():
            if not isinstance(category, str) or not category:
                raise ValueError("Category names must be non-empty strings.")

            if not isinstance(extensions, list):
                raise ValueError(
                    f"Extensions for '{category}' must be a list."
                )

            for extension in extensions:
                if not isinstance(extension, str) or not extension.startswith("."):
                    raise ValueError(
                        f"Invalid extension {extension!r} in '{category}'."
                    )

                extension = extension.lower()

                if extension in extension_rules:
                    raise ValueError(
                        f"Extension {extension} is assigned to multiple categories."
                    )

                extension_rules[extension] = category

        self.extension_rules = extension_rules
        self.default_category = default_category

    def get_category(self, file_item: FileItem) -> str:
        extension = file_item.get_extension().lower()

        return self.extension_rules.get(
            extension, self.default_category
        )

    def group_files(
        self, files: list[FileItem]
    ) -> dict[str, list[FileItem]]:
        categories = {}

        for file_item in files:
            category = self.get_category(file_item)
            categories.setdefault(category, []).append(file_item)

        return categories
