class OlmsMinioError(Exception):
    pass


class OlmsMinioConfigurationError(OlmsMinioError):
    pass


class OlmsMinioFileNotFoundError(OlmsMinioError):
    pass


class OlmsMinioUploadError(OlmsMinioError):
    pass


class OlmsMinioDownloadError(OlmsMinioError):
    pass


class OlmsMinioDeleteError(OlmsMinioError):
    pass