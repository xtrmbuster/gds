import logging

from celery import shared_task

from .models import EveAllianceInfo, EveCharacter, EveCorporationInfo
from . import providers


logger = logging.getLogger(__name__)

TASK_PRIORITY = 7
CHUNK_SIZE = 500


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@shared_task
def update_corp(corp_id):
    """Update given corporation from ESI"""
    EveCorporationInfo.objects.update_corporation(corp_id)


@shared_task
def update_alliance(alliance_id):
    """Update given alliance from ESI"""
    EveAllianceInfo.objects.update_alliance(alliance_id).populate_alliance()


@shared_task
def update_character(character_id: int) -> None:
    """Update given character from ESI."""
    EveCharacter.objects.update_character(character_id)


@shared_task
def run_model_update():
    """Update all alliances, corporations and characters from ESI"""

    #update existing corp models
    for corp in EveCorporationInfo.objects.all().values('corporation_id'):
        update_corp.apply_async(args=[corp['corporation_id']], priority=TASK_PRIORITY)

    # update existing alliance models
    for alliance in EveAllianceInfo.objects.all().values('alliance_id'):
        update_alliance.apply_async(args=[alliance['alliance_id']], priority=TASK_PRIORITY)

    # update existing character models
    character_ids = EveCharacter.objects.all().values_list('character_id', flat=True)
    for character_ids_chunk in chunks(character_ids, CHUNK_SIZE):
        update_character_chunk.apply_async(
            args=[character_ids_chunk], priority=TASK_PRIORITY
        )


@shared_task
def update_character_chunk(character_ids_chunk: list):
    """Update a list of character from ESI"""
    try:
        affiliations_raw = providers.provider.client.Character\
            .post_characters_affiliation(characters=character_ids_chunk).result()
        character_names = providers.provider.client.Universe\
            .post_universe_names(ids=character_ids_chunk).result()
    except OSError:
        logger.info("Failed to bulk update characters. Attempting single updates")
        for character_id in character_ids_chunk:
            update_character.apply_async(
                args=[character_id], priority=TASK_PRIORITY
            )
        return

    affiliations = {
        affiliation.get('character_id'): affiliation
        for affiliation in affiliations_raw
    }
    # add character names to affiliations
    for character in character_names:
        character_id = character.get('id')
        if character_id in affiliations:
            affiliations[character_id]['name'] = character.get('name')

    # fetch current characters
    characters = EveCharacter.objects.filter(character_id__in=character_ids_chunk)\
        .values('character_id', 'corporation_id', 'alliance_id', 'character_name')

    for character in characters:
        character_id = character.get('character_id')
        if character_id in affiliations:
            affiliation = affiliations[character_id]

            corp_changed = (
                character.get('corporation_id') != affiliation.get('corporation_id')
            )

            alliance_id = character.get('alliance_id')
            if not alliance_id:
                alliance_id = None
            alliance_changed = alliance_id != affiliation.get('alliance_id')

            name_changed = False
            fetched_name = affiliation.get('name', False)
            if fetched_name:
                name_changed = character.get('character_name') != fetched_name

            if corp_changed or alliance_changed or name_changed:
                update_character.apply_async(
                    args=[character.get('character_id')], priority=TASK_PRIORITY
                )
