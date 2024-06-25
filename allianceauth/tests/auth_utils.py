from typing import List

from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import m2m_changed, pre_save, post_save
from django.test import TestCase

from esi.models import Token

from allianceauth.authentication.models import (
    UserProfile, State, get_guest_state
)
from allianceauth.eveonline.models import EveCharacter
from allianceauth.authentication.signals import (
    state_member_alliances_changed,
    state_member_characters_changed,
    state_member_corporations_changed,
    state_saved,
    reassess_on_profile_save,
    assign_state_on_active_change,
    check_state_on_character_update
)
from allianceauth.services.signals import (
    m2m_changed_group_permissions,
    m2m_changed_user_permissions,
    m2m_changed_state_permissions,
    m2m_changed_user_groups, disable_services_on_inactive,
    process_main_character_change,
    process_main_character_update
)


class AuthUtils:
    """Utilities for making it easier to create tests for Alliance Auth"""

    @staticmethod
    def _create_user(username):
        return User.objects.create(username=username)

    @classmethod
    def create_user(cls, username, disconnect_signals=False):
        """create a new user

        username: Name of the user

        disconnect_signals: whether to run process without signals
        """
        if disconnect_signals:
            cls.disconnect_signals()
        user = cls._create_user(username)
        if disconnect_signals:
            cls.connect_signals()
        return user

    @staticmethod
    def _create_state(name, priority, member_characters=None, member_corporations=None, member_alliances=None, public=False):
        state = State.objects.create(name=name, priority=priority)
        if member_characters:
            state.member_characters.add(member_characters)
        if member_corporations:
            state.member_corporations.add(member_corporations)
        if member_alliances:
            state.member_alliances.add(member_alliances)
        return state

    @classmethod
    def create_state(cls, name, priority, member_characters=None, member_corporations=None, member_alliances=None, public=False, disconnect_signals=False):
        if disconnect_signals:
            cls.disconnect_signals()
        state = cls._create_state(name, priority, member_characters=member_characters, member_corporations=member_corporations, public=public, member_alliances=member_alliances)
        if disconnect_signals:
            cls.connect_signals()
        return state

    @classmethod
    def get_member_state(cls):
        try:
            return State.objects.get(name='Member')
        except State.DoesNotExist:
            return cls.create_state('Member', 100, disconnect_signals=True)

    @classmethod
    def get_guest_state(cls):
        cls.disconnect_signals()
        state = get_guest_state()
        cls.connect_signals()
        return state

    @classmethod
    def assign_state(cls, user, state, disconnect_signals=False):
        if disconnect_signals:
            cls.disconnect_signals()
        profile = user.profile
        profile.state = state
        profile.save()
        if disconnect_signals:
            cls.connect_signals()

    @classmethod
    def create_member(cls, username):
        user = cls.create_user(username, disconnect_signals=True)
        state = cls.get_member_state()
        cls.assign_state(user, state, disconnect_signals=True)
        cls.disconnect_signals()
        g = Group.objects.get_or_create(name='Member')[0]
        user.groups.add(g)
        cls.connect_signals()
        return user

    @classmethod
    def disconnect_signals(cls):
        m2m_changed.disconnect(m2m_changed_user_groups, sender=User.groups.through)
        m2m_changed.disconnect(m2m_changed_group_permissions, sender=Group.permissions.through)
        m2m_changed.disconnect(m2m_changed_user_permissions, sender=User.user_permissions.through)
        m2m_changed.disconnect(m2m_changed_state_permissions, sender=State.permissions.through)
        pre_save.disconnect(disable_services_on_inactive, sender=User)
        m2m_changed.disconnect(state_member_corporations_changed, sender=State.member_corporations.through)
        m2m_changed.disconnect(state_member_characters_changed, sender=State.member_characters.through)
        m2m_changed.disconnect(state_member_alliances_changed, sender=State.member_alliances.through)
        post_save.disconnect(state_saved, sender=State)
        post_save.disconnect(reassess_on_profile_save, sender=UserProfile)
        pre_save.disconnect(assign_state_on_active_change, sender=User)
        pre_save.disconnect(process_main_character_change, sender=UserProfile)
        pre_save.disconnect(process_main_character_update, sender=EveCharacter)
        post_save.disconnect(
            check_state_on_character_update, sender=EveCharacter
        )

    @classmethod
    def connect_signals(cls):
        m2m_changed.connect(m2m_changed_user_groups, sender=User.groups.through)
        m2m_changed.connect(m2m_changed_group_permissions, sender=Group.permissions.through)
        m2m_changed.connect(m2m_changed_user_permissions, sender=User.user_permissions.through)
        m2m_changed.connect(m2m_changed_state_permissions, sender=State.permissions.through)
        pre_save.connect(disable_services_on_inactive, sender=User)
        m2m_changed.connect(state_member_corporations_changed, sender=State.member_corporations.through)
        m2m_changed.connect(state_member_characters_changed, sender=State.member_characters.through)
        m2m_changed.connect(state_member_alliances_changed, sender=State.member_alliances.through)
        post_save.connect(state_saved, sender=State)
        post_save.connect(reassess_on_profile_save, sender=UserProfile)
        pre_save.connect(assign_state_on_active_change, sender=User)
        pre_save.connect(process_main_character_change, sender=UserProfile)
        pre_save.connect(process_main_character_update, sender=EveCharacter)
        post_save.connect(check_state_on_character_update, sender=EveCharacter)

    @classmethod
    def add_main_character(cls, user, name, character_id, corp_id=2345, corp_name='', corp_ticker='', alliance_id=None,
                            alliance_name='', faction_id=None, faction_name=''):
        if alliance_id:
            try:
                alliance_id = int(alliance_id)
            except Exception:
                alliance_id = None

        char = EveCharacter.objects.create(
            character_id=int(character_id),
            character_name=name,
            corporation_id=int(corp_id),
            corporation_name=corp_name,
            corporation_ticker=corp_ticker,
            alliance_id=alliance_id,
            alliance_name=alliance_name,
            faction_id=faction_id,
            faction_name=faction_name
        )
        UserProfile.objects.update_or_create(user=user, defaults={'main_character': char})

    @classmethod
    def add_main_character_2(
        cls,
        user,
        name,
        character_id,
        corp_id=2345,
        corp_name='',
        corp_ticker='',
        alliance_id=None,
        alliance_name='',
        disconnect_signals=False
    ) -> EveCharacter:
        """new version that works in all cases"""
        if disconnect_signals:
            cls.disconnect_signals()

        if alliance_id:
            try:
                alliance_id = int(alliance_id)
            except Exception:
                alliance_id = None

        char = EveCharacter.objects.create(
            character_id=int(character_id),
            character_name=name,
            corporation_id=int(corp_id),
            corporation_name=corp_name,
            corporation_ticker=corp_ticker,
            alliance_id=alliance_id,
            alliance_name=alliance_name,
        )
        user.profile.main_character = char
        user.profile.save()

        if disconnect_signals:
            cls.connect_signals()

        return char

    @classmethod
    def add_permissions_to_groups(cls, perms, groups, disconnect_signals=True):
        if disconnect_signals:
            cls.disconnect_signals()

        for group in groups:
            for perm in perms:
                group.permissions.add(perm)
            group = Group.objects.get(pk=group.pk)    # reload permission cache

        if disconnect_signals:
            cls.connect_signals()

    @classmethod
    def add_permissions_to_state(cls, perms, states, disconnect_signals=True):
        return cls.add_permissions_to_groups(
            perms, states, disconnect_signals=disconnect_signals
        )

    @classmethod
    def add_permissions_to_user(cls, perms, user, disconnect_signals=True) -> User:
        """add list of permissions to user

        perms: list of Permission objects

        user: user object

        disconnect_signals: whether to run process without signals
        """
        if disconnect_signals:
            cls.disconnect_signals()

        for perm in perms:
            user.user_permissions.add(perm)

        user = User.objects.get(pk=user.pk)     # reload permission cache
        if disconnect_signals:
            cls.connect_signals()

        return user

    @classmethod
    def add_permission_to_user_by_name(
        cls, perm, user, disconnect_signals=True
    ) -> User:
        """returns permission specified by qualified name

        perm: Permission name as 'app_label.codename'

        user: user object

        disconnect_signals: whether to run process without signals
        """
        p = cls.get_permission_by_name(perm)
        return cls.add_permissions_to_user([p], user, disconnect_signals)

    @classmethod
    def add_permissions_to_user_by_name(
        cls, perms: List[str], user: User, disconnect_signals: bool = True
    ) -> User:
        """Add permissions given by name to a user

        Args:
            perms: List of permission names as 'app_label.codename'
            user: user object
            disconnect_signals: whether to run process without signals

        Returns:
            Updated user object
        """
        permissions = [cls.get_permission_by_name(perm) for perm in perms]
        return cls.add_permissions_to_user(permissions, user, disconnect_signals)

    @staticmethod
    def get_permission_by_name(perm: str) -> Permission:
        """returns permission specified by qualified name

        perm: Permission name as 'app_label.codename'

        Returns: Permission object or throws exception if not found
        """
        perm_parts = perm.split('.')
        if len(perm_parts) != 2:
            raise ValueError('Invalid format for permission name')

        return Permission.objects.get(
            content_type__app_label=perm_parts[0], codename=perm_parts[1]
        )


class BaseViewTestCase(TestCase):
    def setUp(self):
        self.member = AuthUtils.create_member('auth_member')
        self.member.email = 'auth_member@example.com'
        self.member.save()
        AuthUtils.add_main_character(self.member, 'auth_member', '12345', corp_id='111', corp_name='Test Corporation',
                                    corp_ticker='TESTR')

    def login(self):
        token = Token.objects.create(character_id='12345', character_name='auth_member', character_owner_hash='1', user=self.member, access_token='1')
        self.client.login(token=token)
