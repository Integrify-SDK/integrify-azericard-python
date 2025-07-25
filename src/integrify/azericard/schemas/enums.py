from enum import Enum


class AuthorizationType(str, Enum):
    FREEZE = '0'
    """Məbləği bloklamaq"""

    DIRECT = '1'
    """Məbləği birbaşa çıxmaq"""

    def __str__(self):
        return self.value


class AuthorizationResponseType(str, Enum):
    ACCEPT_PAYMENT = '21'
    RETURN_PAYMENT = '22'
    CANCEL_PAYMENT = '24'

    def __str__(self):
        return self.value


class AuthorizationMiscType(str, Enum):
    REQUEST_STATUS = '90'

    def __str__(self):
        return self.value


class Action(int, Enum):
    TRANSACTION_SUCCESS = 0
    """Tranzaksiya uğurla tamamlandı"""

    TRANSACTION_DUPLICATE = 1
    """Duplikat əməliyyat aşkar edildi"""

    TRANSACTION_CANCELLED = 2
    """Tranzaksiya rədd edildi"""

    TRANSACTION_PROCESSING_ERROR = 3
    """Tranzaksiya emal xətası"""

    TRANSACTION_REPEAT_OF_CANCELLED = 6
    """İmtina edilmiş əməliyyatın təkrarlanması"""

    TRANSACTION_REPEAT_OF_UNAPPROVED = 7
    """Doğrulama xətası ilə əməliyyatın təkrarlanması"""

    TRANSACTION_REPEAT_OF_UNRESPONDED = 8
    """Cavab verilmədən dayandırılmış əməliyyatın təkrarlanması"""


class CardStatus(str, Enum):
    ACTIVE = 'our_active'
    """Kart AzeriCard database-indədir və aktiv statusa malikdir"""

    INACTIVE = 'our_inactive'
    """Kart AzeriCard database-indədir və və qeyri-aktiv statusa malikdir (bloklanmış/müddəti bitmiş və s.)"""  # noqa: E501

    MISSING = 'foreign'
    """Kart AzeriCard database-ində yoxdur"""


class TransferStatusCode(str, Enum):
    SUCCESS = 0
    """Uğurla tamamlandı"""

    DUPLICATE_TRANSACTION = 105
    """Tranzaksiya Gözləyən statusunda deyil. Onu rədd etmək və ya təsdiqləmək mümkün deyil.
    Əlavə məlumat üçün Azericard ilə əlaqə saxlayın"""

    SIGNATURE_ERROR = 106
    """Giriş məlumatları imzaya uyğun gəlmir"""

    TRANSACTION_NOT_FOUND = 112
    """Ödəniş arxa tərəfdə tapılmadı"""

    TRANSACTION_ACTIVE = 116
    """Tranzaksiya artıq təsdiqlənib, tamamlanması və ya yoxlanılmasını gözləməyə başlayıb."""

    def __str__(self):
        return str(self.value)
