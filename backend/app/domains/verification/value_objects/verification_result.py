from enum import Enum


class VerificationResult(str, Enum):
    SUITABLE = "SUITABLE"
    UNSUITABLE = "UNSUITABLE"
