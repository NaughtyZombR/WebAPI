from sqladmin import ModelView

from app.modules import models


class UserAdmin(ModelView, model=models.users_models.User):
    column_list = "__all__"
    # column_labels = {models.users_models.User.added_artworks: "объекты пользователя"}

    category = "Аккаунт"

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BoardAdmin(ModelView, model=models.boards_models.Board):
    column_list = "__all__"

    category = "Доски"

    name = "Доска"
    name_plural = "Доски"


class BoardColumnAdmin(ModelView, model=models.boards_models.BoardColumn):
    column_list = "__all__"

    category = "Доски"

    name = "Колонна доски"
    name_plural = "Колонны досок"


class TaskAdmin(ModelView, model=models.tasks_models.Task):
    column_list = "__all__"

    category = "Задачи"

    name = "Задача"
    name_plural = "Задачи"


class TaskHistoryAdmin(ModelView, model=models.tasks_models.TaskHistory):
    column_list = "__all__"

    category = "Задачи"

    name = "История задачи"
    name_plural = "Истории задач"


# class ArtworkAdmin(ModelView, model=Artwork):
#     column_list = "__all__"
#
#     category = "Арт-объект"
#
#     # form_columns = [Artwork.title]
#     # Определяем форматтер для отображения значения связного поля
#     column_formatters = {
#         Artwork.added_by_user: lambda model, a: f"{model.added_by_user.username} (ID: {model.added_by_user.id})",
#         Artwork.artist: lambda model, a: f"{model.artist.username} (ID: {model.artist.id})",
#         Artwork.location: lambda model, a: f"lat: {model.location.latitude}\nlng: {model.location.longitude}",
#         Artwork.images: lambda model, a: f"{len(model.images)}",
#         Artwork.moderation: lambda model, a: f"Status: {model.moderation.status.name}",
#     }
#     # column_formatters = {
#     #     'added_by_user': lambda v, c: f"{v.added_by_user.username} (ID: {v.added_by_user.id})"
#     # }
#
#
# class ArtworkImageAdmin(ModelView, model=ArtworkImage):
#     column_list = "__all__"
#     category = "Арт-объект"
#
#
# class ArtworkLocationAdmin(ModelView, model=ArtworkLocation):
#     column_list = "__all__"
#     category = "Арт-объект"
#
#
# class ArtworkModerationAdmin(ModelView, model=ArtworkModeration):
#     column_list = "__all__"
#     category = "Арт-объект"
