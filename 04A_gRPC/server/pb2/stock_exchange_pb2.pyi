from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
EUR: Currency
GBP: Currency
JPY: Currency
USD: Currency

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Offer(_message.Message):
    __slots__ = ["price", "quantity"]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    price: float
    quantity: int
    def __init__(self, price: _Optional[float] = ..., quantity: _Optional[int] = ...) -> None: ...

class StockData(_message.Message):
    __slots__ = ["best_ask_offers", "best_bid_offers", "company_name", "currency", "pct_change", "price", "symbol", "timestamp", "volume"]
    BEST_ASK_OFFERS_FIELD_NUMBER: _ClassVar[int]
    BEST_BID_OFFERS_FIELD_NUMBER: _ClassVar[int]
    COMPANY_NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    PCT_CHANGE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    best_ask_offers: _containers.RepeatedCompositeFieldContainer[Offer]
    best_bid_offers: _containers.RepeatedCompositeFieldContainer[Offer]
    company_name: str
    currency: Currency
    pct_change: float
    price: float
    symbol: str
    timestamp: int
    volume: int
    def __init__(self, symbol: _Optional[str] = ..., company_name: _Optional[str] = ..., price: _Optional[float] = ..., volume: _Optional[int] = ..., timestamp: _Optional[int] = ..., best_bid_offers: _Optional[_Iterable[_Union[Offer, _Mapping]]] = ..., best_ask_offers: _Optional[_Iterable[_Union[Offer, _Mapping]]] = ..., currency: _Optional[_Union[Currency, str]] = ..., pct_change: _Optional[float] = ...) -> None: ...

class StockDataResponse(_message.Message):
    __slots__ = ["data"]
    class DataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: StockData
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[StockData, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.MessageMap[str, StockData]
    def __init__(self, data: _Optional[_Mapping[str, StockData]] = ...) -> None: ...

class SubPctChangeRequest(_message.Message):
    __slots__ = ["pct_change", "symbols"]
    PCT_CHANGE_FIELD_NUMBER: _ClassVar[int]
    SYMBOLS_FIELD_NUMBER: _ClassVar[int]
    pct_change: float
    symbols: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, symbols: _Optional[_Iterable[str]] = ..., pct_change: _Optional[float] = ...) -> None: ...

class SubRequest(_message.Message):
    __slots__ = ["symbols"]
    SYMBOLS_FIELD_NUMBER: _ClassVar[int]
    symbols: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, symbols: _Optional[_Iterable[str]] = ...) -> None: ...

class Currency(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
