from django.db import models

from users.models import CustomUser


class Note(models.Model):
    """
    Модель для хранения заметок пользователей.
    Связана через fk с моделями User и Group.
    """
    text = models.TextField(
        verbose_name="текст",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="дата создания",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="aвтор",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "заметка"
        verbose_name_plural = "заметки"

    def __str__(self):
        return self.text[:30]
