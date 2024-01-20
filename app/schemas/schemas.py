from pydantic import UUID4, BaseModel, Field, computed_field, field_validator


class DishIn(BaseModel):
    title: str
    description: str
    price: float


class DishOut(DishIn):
    id: UUID4

    @field_validator('price')
    def round_price(cls, v: float):
        return f'{v:.2f}'


class SubmenuIn(BaseModel):
    title: str
    description: str


class SubmenuOut(SubmenuIn):
    id: UUID4
    dishes: list[DishIn] = Field(..., exclude=True)

    @computed_field(return_type=int)
    def dishes_count(self):
        return len(self.dishes)


class MenuIn(BaseModel):
    title: str
    description: str


class MenuOut(MenuIn):
    id: UUID4
    submenus: list[SubmenuOut] = Field(..., exclude=True)

    @computed_field(return_type=int)
    def submenus_count(self):
        return len(self.submenus)

    @computed_field(return_type=int)
    def dishes_count(self):
        return sum(len(submenu.dishes) for submenu in self.submenus)
