// Initialize and add the map
let map;

async function initMap() {
  // The location of Luke&Jakob
  //48.902669680777485, 11.651608603704362
  const position = { lat: 48.902669680777485, lng: 11.651608603704362 };
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

  // The map, centered at Luke&Jakob
  map = new Map(document.getElementById("map"), {
    zoom: 4,
    center: position,
    mapId: "CompanyLocation",
  });

  // The marker, positioned at the Luke&Jakob Company
  const marker = new AdvancedMarkerView({
    map: map,
    position: position,
    title: "Luke&Jakob",
  });
}


// initMap();