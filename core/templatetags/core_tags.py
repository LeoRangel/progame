from django import template
from django.core.serializers import serialize
from progame.models import Conquista

register = template.Library()


@register.filter
def translate_message_tag(tag):
    """Recebe uma message tag e retorna ela traduzida"""
    if tag == 'success':
        return 'Sucesso'
    elif tag == 'error':
        return 'Erro'
    elif tag == 'warning':
        return 'Aviso'
    else:
        return 'Informação'


@register.filter
def json(queryset):
    """Retorna queryset serializado"""
    return serialize('json', queryset)


@register.filter
def get_conquista(conquista_pk):
    try:
        return Conquista.objects.get(pk=conquista_pk)
    except Conquista.DoesNotExist:
        return None


@register.filter
def sectodur(value, arg=''):
    """Segundos para duração"""

    # Place seconds in to integer
    secs = int(value)

    # If seconds are greater than 0
    if secs > 0:

        # Import math library
        import math

        # Place durations of given units in to variables
        daySecs = 86400
        hourSecs = 3600
        minSecs = 60

        # If short string is enabled
        if arg != 'long':

            # Set short names
            dayUnitName = ' dia'
            hourUnitName = ' hr'
            minUnitName = ' min'
            secUnitName = ' seg'

            # Set short duration unit splitters
            lastDurSplitter = ' '
            nextDurSplitter = lastDurSplitter

        # If short string is not provided or any other value
        else:
            # Set long names
            dayUnitName = ' dia'
            hourUnitName = ' hora'
            minUnitName = ' minuto'
            secUnitName = ' segundo'

            # Set long duration unit splitters
            lastDurSplitter = ' e '
            nextDurSplitter = ', '

        # Create string to hold outout
        durationString = ''

        # Calculate number of days from seconds
        days = int(math.floor(secs / int(daySecs)))

        # Subtract days from seconds
        secs = secs - (days * int(daySecs))

        # Calculate number of hours from seconds (minus number of days)
        hours = int(math.floor(secs / int(hourSecs)))

        # Subtract hours from seconds
        secs = secs - (hours * int(hourSecs))

        # Calculate number of minutes from seconds (minus number of days and hours)
        minutes = int(math.floor(secs / int(minSecs)))

        # Subtract days from seconds
        secs = secs - (minutes * int(minSecs))

        # Calculate number of seconds (minus days, hours and minutes)
        seconds = secs

        # If number of days is greater than 0
        if days > 0:
            # Add multiple days to duration string
            durationString += ' ' + str(days) + dayUnitName + (days > 1 and 's' or '')

        # Determine if next string is to be shown
        if hours > 0:

            # If there are no more units after this
            if minutes <= 0 and seconds <= 0:

                # Set hour splitter to last
                hourSplitter = lastDurSplitter

            # If there are unit after this
            else:

                # Set hour splitter to next
                hourSplitter = (len(durationString) > 0 and nextDurSplitter or '')

        # If number of hours is greater than 0
        if hours > 0:
            # Add multiple days to duration string
            durationString += hourSplitter + ' ' + str(hours) + hourUnitName + (hours > 1 and 's' or '')

        # Determine if next string is to be shown
        if minutes > 0:

            # If there are no more units after this
            if seconds <= 0:

                # Set minute splitter to last
                minSplitter = lastDurSplitter

            # If there are unit after this
            else:

                # Set minute splitter to next
                minSplitter = (len(durationString) > 0 and nextDurSplitter or '')

        # If number of minutes is greater than 0
        if minutes > 0:
            # Add multiple days to duration string
            durationString += minSplitter + ' ' + str(minutes) + minUnitName + (minutes > 1 and 's' or '')

        # Determine if next string is last
        if seconds > 0:
            # Set second splitter
            secSplitter = (len(durationString) > 0 and lastDurSplitter or '')

        # If number of seconds is greater than 0
        if seconds > 0:
            # Add multiple days to duration string
            durationString += secSplitter + ' ' + str(seconds) + secUnitName + (seconds > 1 and 's' or '')

        # Return duration string
        return durationString.strip()

    # If seconds are not greater than 0
    else:
        # Provide 'No duration' message
        return 'Sem duração'
