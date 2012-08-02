from obspy.core import UTCDateTime
from obspy.core.event import Catalog, Event, Origin, \
    Magnitude, StationMagnitude, Comment, Pick, WaveformStreamID, \
    OriginQuality
from obspy.core.util.xmlwrapper import XMLParser


def isSeishubEventFile(filename):
    """
    Checks whether a file is a Seishub Event file.

    This is a very rough test as the format is not very well defined and has no
    unique features.

    :type filename: str
    :param filename: Name of the Seishub event file to be checked.
    :rtype: bool
    :return: ``True`` if Seishub event file.

    .. rubric:: Example
    """
    try:
        parser = XMLParser(filename)
    except:
        return False
    # Simply check to paths that should always exist.
    if parser.xpath('event_id/value') and parser.xpath('event_type/value'):
        return True
    return False


def __toValueQuantity(parser, element, name, quantity_type=None):
    try:
        el = parser.xpath(name, element)[0]
    except:
        return None, None

    value = parser.xpath2obj('value', el, quantity_type)
    errors = {}
    uncertainty = parser.xpath2obj('uncertainty', el, float)
    if uncertainty:
        errors['uncertainty'] = uncertainty
    return value, errors


def __toFloatQuantity(parser, element, name):
    return __toValueQuantity(parser, element, name, float)


def __toTimeQuantity(parser, element, name):
    return __toValueQuantity(parser, element, name, UTCDateTime)


def __toOrigin(parser, origin_el):
    """
    Parses a given origin etree element.

    :type parser: :class:`~obspy.core.util.xmlwrapper.XMLParser`
    :param parser: Open XMLParser object.
    :type origin_el: etree.element
    :param origin_el: origin element to be parsed.
    :return: A ObsPy :class:`~obspy.core.event.Origin` object.
    """
    origin = Origin()

    # I guess setting the program used as the method id is fine.
    origin.method_id = parser.xpath2obj('program', origin_el)

    # Standard parameters.
    origin.time, origin.time_errors = \
        __toTimeQuantity(parser, origin_el, "time")
    origin.latitude, origin.latitude_errors = \
        __toFloatQuantity(parser, origin_el, "latitude")
    origin.longitude, origin.longitude_errors = \
        __toFloatQuantity(parser, origin_el, "longitude")
    origin.depth, origin.depth_errors = \
        __toFloatQuantity(parser, origin_el, "depth")

    # Figure out the depth type.
    depth_type = parser.xpath2obj("depth_type", origin_el, str)
    # Map Seishub specific depth type to the QuakeML depth type.
    if depth_type == "from location program":
        depth_type == "from location"
    origin.depth_type = "from location"

    # Earth model.
    origin.earth_model_id = parser.xpath2obj("earth_mod", origin_el, str)

    # Parse th origin uncertainty. Rather verbose but should cover all cases.
    pref_desc = parser.xpath2obj("originUncertainty/preferredDescription",
                                 origin_el, str)
    hor_uncert = parser.xpath2obj("originUncertainty/horizontalUncertainty",
                                  origin_el, float)
    min_hor_uncert = parser.xpath2obj(\
        "originUncertainty/minHorizontalUncertainty", origin_el, float)
    max_hor_uncert = parser.xpath2obj(\
        "originUncertainty/maxHorizontalUncertainty", origin_el, float)
    azi_max_hor_uncert = parser.xpath2obj(\
        "originUncertainty/azimuthMaxHorizontalUncertainty", origin_el, float)
    origin_uncert = {}
    if pref_desc:
        origin_uncert["preferred_description"] = pref_desc
    if hor_uncert:
        origin_uncert["horizontal_uncertainty"] = hor_uncert
    if min_hor_uncert:
        origin_uncert["min_horizontal_uncertainty"] = min_hor_uncert
    if max_hor_uncert:
        origin_uncert["max_horizontal_uncertainty"] = max_hor_uncert
    if azi_max_hor_uncert:
        origin_uncert["azimuth_max_horizontal_uncertainty"] = \
        azi_max_hor_uncert

    if origin_uncert:
        origin.origin_uncertainty = origin_uncert

    # Parse the OriginQuality if applicable.
    if not origin_el.xpath("originQuality"):
        return origin

    origin_quality_el = origin_el.xpath("originQuality")[0]
    origin.quality = OriginQuality()
    origin.quality.associated_phase_count = \
        parser.xpath2obj("associatedPhaseCount", origin_quality_el, int)
    # QuakeML does apparently not distinguish between P and S wave phase
    # count. Some Seishub event files do.
    p_phase_count = parser.xpath2obj("P_usedPhaseCount", origin_quality_el,
                                     int)
    s_phase_count = parser.xpath2obj("S_usedPhaseCount", origin_quality_el,
                                     int)
    # Use both in case they are set.
    if p_phase_count and s_phase_count:
        phase_count = p_phase_count + s_phase_count
        # Also add two Seishub element file specific elements.
        origin.quality.p_used_phase_count = p_phase_count
        origin.quality.s_used_phase_count = s_phase_count
    # Otherwise the total usedPhaseCount should be specified.
    else:
        phase_count = parser.xpath2obj("usedPhaseCount",
                                       origin_quality_el, int)
    origin.quality.used_phase_count = phase_count

    origin.quality.associated_station_count = \
        parser.xpath2obj("associatedStationCount", origin_quality_el, int)
    origin.quality.used_station_count = \
        parser.xpath2obj("usedStationCount", origin_quality_el, int)
    origin.quality.depth_phase_count = \
        parser.xpath2obj("depthPhaseCount", origin_quality_el, int)
    origin.quality.standard_error = \
        parser.xpath2obj("standardError", origin_quality_el, float)
    origin.quality.azimuthal_gap = \
        parser.xpath2obj("azimuthalGap", origin_quality_el, float)
    origin.quality.secondary_azimuthal_gap = \
        parser.xpath2obj("secondaryAzimuthalGap", origin_quality_el, float)
    origin.quality.ground_truth_level = \
        parser.xpath2obj("groundTruthLevel", origin_quality_el, float)
    origin.quality.minimum_distance = \
        parser.xpath2obj("minimumDistance", origin_quality_el, float)
    origin.quality.maximum_distance = \
        parser.xpath2obj("maximumDistance", origin_quality_el, float)
    origin.quality.median_distance = \
        parser.xpath2obj("medianDistance", origin_quality_el, float)

    return origin


def __toMagnitude(parser, magnitude_el):
    """
    Parses a given magnitude etree element.

    :type parser: :class:`~obspy.core.util.xmlwrapper.XMLParser`
    :param parser: Open XMLParser object.
    :type magnitude_el: etree.element
    :param magnitude_el: magnitude element to be parsed.
    :return: A ObsPy :class:`~obspy.core.event.Magnitude` object.
    """
    mag = Magnitude()
    mag.mag, mag.mag_errors = __toFloatQuantity(parser, magnitude_el, "mag")
    mag.magnitude_type = parser.xpath2obj("type", magnitude_el)
    mag.station_count = parser.xpath2obj("stationCount", magnitude_el, int)
    mag.method_id = parser.xpath2obj("program", magnitude_el)

    return mag


def __toStationMagnitude(parser, stat_mag_el):
    """
    Parses a given station magnitude etree element.

    :type parser: :class:`~obspy.core.util.xmlwrapper.XMLParser`
    :param parser: Open XMLParser object.
    :type stat_mag_el: etree.element
    :param stat_mag_el: station magnitude element to be parsed.
    :return: A ObsPy :class:`~obspy.core.event.StationMagnitude` object.
    """
    mag = StationMagnitude()
    mag.mag, mag.mag_errors = __toFloatQuantity(parser, stat_mag_el, "mag")
    # Use the waveform id to store station and channel(s) in the form
    # station.[channel_1, channel_2] or station.channel in the case only one
    # channel has been used.
    # XXX: This might be a violation of how this field is used within QuakeML
    channels = parser.xpath2obj('channels', stat_mag_el).split(',')
    channels = ','.join([_i.strip() for _i in channels])
    if len(channels) > 1:
        channels = '%s' % channels
    station = parser.xpath2obj('station', stat_mag_el)
    mag.waveform_id = WaveformStreamID()
    mag.waveform_id.station_code = station
    mag.waveform_id.channel_code = channels
    weight_comment = Comment(
        text="Weight from the SeisHub event file: %.3f" % \
        parser.xpath2obj("weight", stat_mag_el, float))
    mag.comments.append(weight_comment)
    return mag


def __toPick(parser, pick_el, evaluation_mode):
    """
    """
    pick = Pick()
    waveform = pick_el.xpath("waveform")[0]
    pick.waveform_id = WaveformStreamID(\
                                network_code=waveform.get("networkCode"),
                                station_code=waveform.get("stationCode"),
                                channel_code=waveform.get("channelCode"),
                                location_code=waveform.get("locationCode"))
    pick.time, pick.time_errors = __toTimeQuantity(parser, pick_el, "time")
    pick.phase_hint = parser.xpath2obj('phaseHint', pick_el)
    onset = parser.xpath2obj('onset', pick_el)
    if onset and onset.lower() in ["emergent", "impulsive", "questionable"]:
        pick.onset = onset.lower()
    # Evaluation mode of a pick is global in the SeisHub Event file format.
    pick.evaluation_mode = evaluation_mode
    # The polarity needs to be mapped.
    polarity = parser.xpath2obj('polarity', pick_el)
    pol_map_dict = {'up': 'positive', 'positive': 'positive',
                    'down': 'negative', 'negative': 'negative',
                    'undecidable': 'undecidable'}
    if polarity and polarity.lower() in pol_map_dict:
        pick.polarity = pol_map_dict[polarity.lower()]
    # Convert azimuth to backazmith
    azimuth = __toFloatQuantity(parser, pick_el, "azimuth")
    if len(azimuth) == 2 and azimuth[0] and azimuth[1]:
        # Convert to backazimuth
        pick.backazimuth = (azimuth[0] + 180.0) % 360.0
        pick.backzimuth_errors = azimuth[1]
    return pick


def readSeishubEventFile(filename):
    """
    Reads a Seishub event file and returns a ObsPy Catalog object.

    .. warning::
        This function should NOT be called directly, it registers via the
        ObsPy :func:`~obspy.core.event.readEvents` function, call this instead.

    :type filename: str
    :param filename: Seishub event file to be read.
    :rtype: :class:`~obspy.core.event.Catalog`
    :return: A ObsPy Catalog object.

    .. rubric:: Example
    """
    # Just init the parser, the SeisHub event file format has no namespaces.
    parser = XMLParser(filename)
    # A Seishub event just specifies a single event so Catalog information is
    # not really given.
    catalog = Catalog()

    # Create new Event object.
    public_id = parser.xpath('event_id/value')[0].text

    # Read the event_type tag.
    pick_method = parser.xpath2obj('event_type/account', parser, str)
    user = parser.xpath2obj('event_type/user', parser, str)
    global_evaluation_mode = parser.xpath2obj('event_type/value', parser, str)
    # The author will be stored in the CreationInfo object. This will be the
    # creation info of the event as well as on all picks.
    creation_info = {"author": user}

    # Create the event object.
    event = Event(resource_id=public_id, creation_info=creation_info)

    # Parse the origins.
    for origin_el in parser.xpath("origin"):
        origin = __toOrigin(parser, origin_el)
        event.origins.append(origin)
    # There should always be only one origin.
    assert(len(event.origins) == 1)
    # Parse the magnitudes.
    for magnitude_el in parser.xpath("magnitude"):
        magnitude = __toMagnitude(parser, magnitude_el)
        event.magnitudes.append(magnitude)
    # Parse the station magnitudes.
    for stat_magnitude_el in parser.xpath("stationMagnitude"):
        stat_magnitude = __toStationMagnitude(parser, stat_magnitude_el)
        event.station_magnitudes.append(stat_magnitude)
    # Parse the picks. Pass the global evaluation mode (automatic, manual)
    for pick_el in parser.xpath("pick"):
        pick = __toPick(parser, pick_el, global_evaluation_mode)
        event.picks.append(pick)
    # Append the creation info to all picks. And also add the pick_method, e.g.
    # the event_type/account value as the method_id to the picks.
    for pick in event.picks:
        pick.creation_info = creation_info
        pick.method_id = pick_method

    # In QuakeML a StationMagnitude object has to be associated with an Origin.
    # This in turn means that the origin needs to have a resource_id.
    event.origins[0].resource_id = "smi:local/origins/%s" % \
        event.resource_id.resource_id
    for mag in event.station_magnitudes:
        mag.origin_id = event.origins[0].resource_id

    # Add the event to the catalog
    catalog.append(event)

    return catalog
