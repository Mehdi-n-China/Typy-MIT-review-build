"""zipfile facade: the .typyexp project archive format is a zip file."""
import zipfile
ZipFile: type = zipfile.ZipFile
BadZipFile: type = zipfile.BadZipFile
ZIP_DEFLATED: int = zipfile.ZIP_DEFLATED
