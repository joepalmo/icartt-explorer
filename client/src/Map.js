import './Map.css';
import mapboxgl from 'mapbox-gl'; 
import React, { useRef, useEffect, useState } from 'react';

// Set-up map
mapboxgl.accessToken = 'pk.eyJ1IjoianBhbG1vIiwiYSI6ImNsZGhzOG51dTFhNGczcG53eHRoZDZ3ZGEifQ.1jdyKokekh5tPbEth0zY6g';

const Map = () => {

const mapContainer = useRef(null);
const map = useRef(null);
const [lng, setLng] = useState(-70.9);
const [lat, setLat] = useState(42.35);
const [zoom, setZoom] = useState(9);

useEffect(() => {
  if (map.current) return; // initialize map only once
  map.current = new mapboxgl.Map({
  container: mapContainer.current,
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [lng, lat],
  zoom: zoom
  });
  map.current.on('move', () => {
    setLng(map.current.getCenter().lng.toFixed(4));
    setLat(map.current.getCenter().lat.toFixed(4));
    setZoom(map.current.getZoom().toFixed(2));
    });
  });

return (
  <div>
  <div className="sidebar">
  Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}
  </div>
  <div ref={mapContainer} className="map-container" />
  </div>
  );
}

export default Map;