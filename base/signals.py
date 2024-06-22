from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import QuizAttempt, AnswerRecord, ScoreRecord


@receiver(post_save, sender=QuizAttempt)
def deleteAnswerRecord(sender, instance, created, **kwargs):
    if created:
        AnswerRecord.objects.filter(user=instance.user, question__quiz=instance.quiz).delete()


@receiver(post_delete, sender=QuizAttempt)
def deleteScoreRecord(sender, instance, **kwargs):
    ScoreRecord.objects.filter(user=instance.user, quiz=instance.quiz).delete()