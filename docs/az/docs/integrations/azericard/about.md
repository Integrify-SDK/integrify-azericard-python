# AzeriCard

???+ danger
    Azericard inteqrasiyası tamamilə dokumentasiyaya uyğun yazılsa da, test mühiti olmadığından real testlər edilə bilinməyib. Ona görə istifadə edərkən, ehtiyatlı olun, göndərilən və alınan sorğuları bir daha yoxlamağınız tövsiyyə olunur. Əgər sizdə test mühiti varsa, və bizə yardımçı olmaq istəyirinizsə, əlaqə saxlamağınız xahiş olunur.

???+ warning
    Bu sorğulardan istifadə etmək üçün, bu dəyərləri "environment variable"-larına əlavə etməlisiniz: `AZERICARD_KEY_FILE_PATH`. Bu AzeriCard-dan alınmış açar faylıdır.

???+ note
    Bu sorğulardan rahat istifadə etmək üçün, qeyd olunan dəyərləri "environment variable"-larına əlavə etməyiniz məsləhət görülür: `AZERICARD_MERCHANT_ID` (Terminal ID), `AZERICARD_MERCHANT_NAME`, `AZERICARD_MERCHANT_URL`, `AZERICARD_CALLBACK_URL` (backref). Əks halda bu dəyərləri funksiyaları istifadə edərkən parametr kimi göndərməlisiniz.

???+ note
    AzeriCardClientClass interfeysinin dilini dəyişmək istəyirsinizsə, `AZERICARD_INTERFACE_LANG` "environment variable"-na dəyər verin, və ya hər sorğuda dil parametrini göndərin. Default olaraq, Azərbaycan dili olacaq.

## Rəsmi Dokumentasiya (v2024.11.6) { #official-documentation }

[Azərbaycanca](https://developer.azericard.com/az)

[İngliscə](https://developer.azericard.com/en)

## Sorğular listi { #list-of-requests }

| Sorğu metodu                                                                                       | Məqsəd                                               |                      Azericard API                       |
| :------------------------------------------------------------------------------------------------- | :--------------------------------------------------- | :------------------------------------------------------: |
| [`authorization`][integrify.azericard.client.AzeriCardClientClass.authorization]                   | Ödəniş/Bloklama                                      | `https://mpi.3dsecure.az/cgi-bin/cgi_link (TRTYPE='1')`  |
| [`auth_and_save_card`][integrify.azericard.client.AzeriCardClientClass.auth_and_save_card]         | Ödəniş/Bloklama və kartı yadda saxlamaq              | `https://mpi.3dsecure.az/cgi-bin/cgi_link (TRTYPE='1')`  |
| [`auth_with_saved_card`][integrify.azericard.client.AzeriCardClientClass.auth_with_saved_card]     | Saxlanılan kartla ödəniş/bloklama                    | `https://mpi.3dsecure.az/cgi-bin/cgi_link (TRTYPE='1')`  |
| [`finalize`][integrify.azericard.client.AzeriCardClientClass.finalize]                             | Blok olunmuş məbləği qəbul ETMƏMƏK (offline) sorğusu | `https://mpi.3dsecure.az/cgi-bin/cgi_link (TRTYPE='24')` |
| [`get_transaction_status`][integrify.azericard.client.AzeriCardClientClass.get_transaction_status] | Ödəniş statusunun yoxlanılması                       | `https://mpi.3dsecure.az/cgi-bin/cgi_link (TRTYPE='90')` |
| [`transfer_start`][integrify.azericard.client.AzeriCardClientClass.transfer_start]                 | Müştəriyə pul köçürülmə prosesinin başladılması      |         `https://mt.azericard.com/payment/view`          |
| [`transfer_confirm`][integrify.azericard.client.AzeriCardClientClass.transfer_confirm]             | Müştəriyə pul köçürülmə prosesini təsdiqləmə         |          `https://mt.azericard.com/api/confirm`          |
| [`transfer_decline`][integrify.azericard.client.AzeriCardClientClass.transfer_decline]             | Müştəriyə pul köçürülmə prosesini imtina etmə        |          `https://mt.azericard.com/api/decline`          |

### Sorğu göndərmək axını { #request-flow }

Nəzərə alsaq ki, Azericard form submission qəbul edərək, sizə redirectsiz səhifəni açır, form-u backend-dən submit etmık mümkün deyil, məhz front tərəfdən olmalıdır. Ona görə, başqa inteqrasiyalardan fərqli olaraq, Azericard-da kitabxana sorğu atmır, form-da göndərilməli olan data-nı qaytarır. Format JSON olsa da, köməkçi funksiyadan istifadə edərək, HTML formu alın, front-a response kimi göndərə bilərsiniz:

```python
from integrify.azericard.client import AzericardClient
from integrify.azericard.helpers import json_to_html_form

req = AzericardClient.pay(
    amount=1,
    currency='AZN',
    order='12345678',
    desc='test',
    country='AZ',
)

form = json_to_html_form(req)
print(form)  # <form action="https://testmpi.3dsecure.az/cgi-bin/cgi_link" method="POST">
             #   <input type="hidden" name="ORDER" value="12345678"> ...
```

## Callback Sorğusu { #callback-request }

Bəzi sorğular müştəri məlumat daxil etdikdən və arxa fonda bank işləmləri bitdikdən sonra, tranzaksiya haqqında məlumat sizin mühit dəyişənində (və ya sorğuda) qeyd etdiyiniz callback URL-ə POST sorğusu göndərilir. Hər datada PSIGN field-i vardır ki, sizin server tərəfindən scamming-in qarşısını almaq üçün düzgün olub-olmadığını yoxlamalısınız.

> **Qeyd**
>
> FastAPI istifadəçiləri kiçik "shortcut"-dan istifadə edə bilərlər:
>
> ```python
> from fastapi import Fastapi, APIRouter, Depends
> from integrify.azericard.schemas.callback import AuthCallbackWithCardDataSchema
>
> router = APIRouter()
>
> @router.post('/azericard/callback')
> async def azericard_callback(data: AuthCallbackWithCardDataSchema):
>    ...
> ```

---

## Callback Data formatı { #callback-data-format }

Nə sorğu göndərməyinizdən asılı olaraq, callback-ə gələn data biraz fərqlənə bilər. [`AuthCallbackWithCardDataSchema`][integrify.azericard.schemas.callback.AuthCallbackWithCardDataSchema] bütün bu dataları özündə cəmləsə də, hansı fieldlərin gəlməyəcəyini (yəni, decode-dan sonra `None` olacağını) bilmək yaxşı olar. Ümumilikdə, mümkün olacaq datalar bunlardır:

| Dəyişən adı | İzahı                                                                                                                                          |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `terminal`  | Sorğudan əks etdirilməsi Terminal ID                                                                                                           |
| `trtype`    | Sorğudan əks etdirilməsi Transaction Type                                                                                                      |
| `order`     | Sorğudan əks etdirilməsi order id                                                                                                              |
| `amount`    | İcazə verilən məbləğ. Adətən, orijinal məbləğə və alıcının haqqına bərabər olacaq.                                                             |
| `currency`  | Sorğudan əks etdirilməsi ödəniş məzənnəsi                                                                                                      |
| `action`    | EGateway fəaliyyət kodu                                                                                                                        |
| `rc`        | Əməliyyat cavab kodu (ISO-8583 Sahə 39)                                                                                                        |
| `approval`  | Müştəri bankının təsdiq kodu (ISO-8583 Sahə 38). Kart idarəetmə sistemi tərəfindən təmin edilmədikdə boş ola bilər.                            |
| `rrn`       | Müştəri bankının axtarış istinad nömrəsi (ISO-8583 Sahə 37)                                                                                    |
| `int_ref`   | Elektron ticarət şlüzünün daxili istinad nömrəsi                                                                                               |
| `timestamp` | GMT-də e-ticarət şlüzünün vaxt damğası:: YYYYMMDDHHMMSS                                                                                        |
| `nonce`     | E-Commerce Gateway qeyri-dəyərlidir. Hexadecimal formatda 8-32 gözlənilməz təsadüfi baytla doldurulacaq. MAC istifadə edildikdə mövcud olacaq. |
| `card`      | 123456******1234 formatında əks edilən kart maskası                                                                                            |
| `token`     | Saxlanılacaq kartın TOKEN parametri                                                                                                            |
| `p_sign`    | Onaltılıq formada E-Commerce Gateway MAC (Message Authentication Code). MAC istifadə edildikdə mövcud olacaq.                                  |

Sorğudan asılı olaraq, bu data-lar callback-də **GƏLMİR** (yəni, avtomatik `None` dəyəri alır):

| Sorğu metodu                                                                                   | `None` field-lər |
| :--------------------------------------------------------------------------------------------- | :--------------- |
| [`authorization`][integrify.azericard.client.AzeriCardClientClass.authorization]               | `card`, `token`  |
| [`auth_and_save_card`][integrify.azericard.client.AzeriCardClientClass.auth_and_save_card]     | -                |
| [`auth_with_saved_card`][integrify.azericard.client.AzeriCardClientClass.auth_with_saved_card] | -                |
| [`finalize`][integrify.azericard.client.AzeriCardClientClass.finalize]                         | `card`, `token`  |

> **Qeyd**
>
> Qalan bütün data-lar sorğu success olduqda gəlir, əks halda, onlar da `None` dəyəri alır.
