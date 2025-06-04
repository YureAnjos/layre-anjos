import shutil
from pathlib import Path

class BackupManager:
  def __init__(self, path: Path):
    self.path = path
    self.path.mkdir(parents=True, exist_ok=True)

    self.backupDir = str(path)

  def saveBackup(self, originalPath, fileName):
    sourcePath = originalPath / fileName
    destPath = self.path / fileName
    try:
      shutil.copy2(sourcePath, destPath)
    except Exception as e:
      print(e)