// Accompanying Javascript that mainly handles displaying the events on a
// google map. Some function are called from Qt, other JS methods call Qt
// methods.

// Upon page load simple display a full screen map.
var map;
$(document).ready(function(){
    // Init global array that stores all events.
    window.events = new Array();

    map = new GMaps({
        div: '#map',
        lat: 47.723333,
        lng: 12.828333,
        zoom: 11,
        streetViewControl: false,
        mapType: "Terrain",
        // Inform the PyQt application that the bounds have changed.
        bounds_changed: function(e) {
           pyObj.set_lat_long_bounds(this.getBounds());
        }
        });
})

// Remove all events from the global events array and the map.
function clearEvents() {
    // Loop over array and remove all markers from the map.
    for (var i=0; i < window.events.length; i++) {
        window.events[i].marker.setMap(null);
    }
    // Clear the actual array.
    window.events.length = 0;
}


// Add a single event to the glob events array and also add a marker to the
// map.
function addEvent(lat, lng, depth, magnitude, magnitude_type, datetime,
        event_id, misc_info, server) {
    event = {
        lat: lat,
        lng: lng,
        depth: depth,
        magnitude: magnitude,
        magnitude_type: magnitude_type,
        datetime: datetime,
        event_id: event_id,
        misc_info: misc_info,
        server: server,
    };
    addMarker(event);
    window.events.push(event);
};


// Add a marker for the given event object to the map.
function addMarker(event) {
    // Parse the misc_info attribute of the event and create a HTML
    // list off it.
    var info_list = "<li>Server Type: {0}</li>".format(event.server);
    infos = event.misc_info.split(";");
    for (var i=0; i < infos.length; i++) {
        var cur_string = trim(infos[i]);
        info_list += "<li>" + cur_string + "</li>";
    }

    // Add a marker to the map.
    event.marker = map.addMarker({
        lat: event.lat,
        lng: event.lng,
        title: event.event_id,
        // Inform the PyQt application that the event marker has been clicked
        // (selected).
        click: function(e) {
            pyObj.event_selected(event.event_id);
        },
        // Choose iceon. Clamp and convert magnitude to integer for the
        // filename.
        icon : "icon_magnitude_{0}.png".format(
            Math.floor(Math.min(Math.max(event.magnitude, -1), 9))),
        infoWindow: {
            content: '<div class="infoWindow"> \
                <h1 id="event_header">{0}</h1> \
                <ul class="fancy"> \
                   <li class="fancy_label">Lat</li> \
                   <li>{1}</li> \
                   <li class="fancy_label">Long</li> \
                   <li>{2}</li> \
                   <li class="fancy_label">Depth</li> \
                   <li>{3}</li> \
                </ul> \
                <ul class="fancy"> \
                   <li class="fancy_label">Origin time</li> \
                   <li>{4}</li> \
                </ul> \
                <ul class="fancy"> \
                   <li class="fancy_label">Magnitude</li> \
                   <li>{5} {6}</li> \
                </ul> \
                <ul id="info_list">{7}</ul> \
                </div>'.format(event.event_id, event.lat,
                    event.lng, event.depth, event.datetime,
                    event.magnitude, event.magnitude_type,
                    info_list)
        }
    });
};


// Add a format method to JS Strings.
String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match;
    });
};


// Remove multiple, leading or trailing spaces from a string.
function trim(s) {
    s = s.replace(/(^\s*)|(\s*$)/gi,"");
    s = s.replace(/[ ]{2,}/gi," ");
    s = s.replace(/\n /,"\n");
    return s;
}
