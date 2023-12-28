from typing import TypeVar

from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter

ParentT = TypeVar("ParentT", APIRouter, FastAPI)


def remove_trailing_slashes_from_routes(parent: ParentT) -> ParentT:
    """Удаляет конечные слэши со всех маршрутов в данном маршрутизаторе"""

    for route in parent.routes:
        if isinstance(route, APIRoute):
            route.path = route.path.rstrip("/")

    return parent
