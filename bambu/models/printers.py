from sqlmodel import Field, SQLModel


class PrinterBase(SQLModel):
    name: str = Field(max_length=100)
    model: str = Field(max_length=100)
    ip: str = Field(max_length=100)
    serial: str = Field(max_length=100)
    access_code: str = Field(max_length=100)
    is_current: bool = Field(default=False)


class Printer(PrinterBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class PrinterCreate(PrinterBase):
    pass


class PrinterResponse(PrinterBase):
    id: int
    is_online: bool
