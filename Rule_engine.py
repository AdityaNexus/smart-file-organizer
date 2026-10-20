from File_item import FileItem

class RuleEngine:
    def __init__(self):
          self.extension_rules = {
            ".pdf": "Documents",
            ".docx": "Documents",
            ".txt": "Documents",
            ".png": "Images",
            ".jpg": "Images",
            ".jpeg": "Images",
            ".py": "Code",
            ".java": "Code",
        }

    def get_category(self , file_item : FileItem)->str:
         extension = file_item.get_extension().lower()
         return self.extension_rules.get(extension,"Others")

    def group_files(self, files: list[FileItem])->dict[str,list[FileItem]]:
        category = {}
        for file in files:
              belong = self.get_category(file)
              category.setdefault(belong,[]).append(file)
        return category