import logging

from django.contrib.auth.models import User, Permission
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo, EveAllianceInfo, EveFactionInfo
from allianceauth.notifications import notify
from django.conf import settings

from .managers import CharacterOwnershipManager, StateManager

logger = logging.getLogger(__name__)


class State(models.Model):
    name = models.CharField(max_length=32, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    priority = models.IntegerField(unique=True, help_text="Users get assigned the state with the highest priority available to them.")

    member_characters = models.ManyToManyField(EveCharacter, blank=True,
                                                help_text="Characters to which this state is available.")
    member_corporations = models.ManyToManyField(EveCorporationInfo, blank=True,
                                                help_text="Corporations to whose members this state is available.")
    member_alliances = models.ManyToManyField(EveAllianceInfo, blank=True,
                                            help_text="Alliances to whose members this state is available.")
    member_factions = models.ManyToManyField(EveFactionInfo, blank=True,
                                            help_text="Factions to whose members this state is available.")
    public = models.BooleanField(default=False, help_text="Make this state available to any character.")

    objects = StateManager()

    class Meta:
        ordering = ['-priority']

    def __str__(self):
        return self.name

    def available_to_character(self, character):
        return self in State.objects.available_to_character(character)

    def available_to_user(self, user):
        return self in State.objects.available_to_user(user)

    def delete(self, **kwargs):
        with transaction.atomic():
            for profile in self.userprofile_set.all():
                profile.assign_state(state=State.objects.exclude(pk=self.pk).get_for_user(profile.user))
        super().delete(**kwargs)


def get_guest_state():
    try:
        return State.objects.get(name='Guest')
    except State.DoesNotExist:
        return State.objects.create(name='Guest', priority=0, public=True)


def get_guest_state_pk():
    return get_guest_state().pk


class UserProfile(models.Model):
    class Meta:
        default_permissions = ('change',)

    class Language(models.TextChoices):
        """
        Choices for UserProfile.language
        """

        ENGLISH = 'en', _('English')
        GERMAN = 'de', _('German')
        SPANISH = 'es', _('Spanish')
        CHINESE = 'zh-hans', _('Chinese Simplified')
        RUSSIAN = 'ru', _('Russian')
        KOREAN = 'ko', _('Korean')
        FRENCH = 'fr', _('French')
        JAPANESE = 'ja', _('Japanese')
        ITALIAN = 'it', _('Italian')
        UKRAINIAN = 'uk', _('Ukrainian')
        POLISH = 'pl', _("Polish")

    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE)
    main_character = models.OneToOneField(
        EveCharacter,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    state = models.ForeignKey(
        State,
        on_delete=models.SET_DEFAULT,
        default=get_guest_state_pk)
    language = models.CharField(
        _("Language"), max_length=10,
        choices=Language.choices,
        blank=True,
        default='')
    night_mode = models.BooleanField(
        _("Night Mode"),
        blank=True,
        null=True)
    theme = models.CharField(
        _("Theme"),
        max_length=200,
        blank=True,
        null=True,
        help_text="Bootstrap 5 Themes from https://bootswatch.com/ or Community Apps"
    )

    def assign_state(self, state=None, commit=True):
        if not state:
            state = State.objects.get_for_user(self.user)
        if self.state != state:
            self.state = state
            if commit:
                logger.info(f'Updating {self.user} state to {self.state}')
                self.save(update_fields=['state'])
                notify(
                    self.user,
                    _('State changed to: %s' % state),
                    _('Your user\'s state is now: %(state)s')
                    % ({'state': state}),
                    'info'
                )
                from allianceauth.authentication.signals import state_changed

                # We need to ensure we get up to date perms here as they will have just changed.
                # Clear all attribute caches and reload the model that will get passed to the signals!
                self.refresh_from_db()

                state_changed.send(
                    sender=self.__class__, user=self.user, state=self.state
                )

    def __str__(self):
        return str(self.user)
class CharacterOwnership(models.Model):
    class Meta:
        default_permissions = ('change', 'delete')
        ordering = ['user', 'character__character_name']

    character = models.OneToOneField(EveCharacter, on_delete=models.CASCADE, related_name='character_ownership')
    owner_hash = models.CharField(max_length=28, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='character_ownerships')

    objects = CharacterOwnershipManager()

    def __str__(self):
        return f"{self.user}: {self.character}"


class OwnershipRecord(models.Model):
    character = models.ForeignKey(EveCharacter, on_delete=models.CASCADE, related_name='ownership_records')
    owner_hash = models.CharField(max_length=28, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ownership_records')
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.user}: {self.character} on {self.created}"
