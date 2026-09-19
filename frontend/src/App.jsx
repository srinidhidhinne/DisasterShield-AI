import { useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Circle,
  Popup,
  useMapEvents
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import L from "leaflet";

import "./App.css";


// ==================================================
// LEAFLET ICON
// ==================================================

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",

  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",

  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png"
});


// ==================================================
// MAP CLICK
// ==================================================

function MapClickHandler({
  setLatitude,
  setLongitude
}) {

  useMapEvents({

    click(event) {

      setLatitude(
        event.latlng.lat.toFixed(6)
      );

      setLongitude(
        event.latlng.lng.toFixed(6)
      );

    }

  });

  return null;
}


// ==================================================
// RISK CIRCLE
// ==================================================

function RiskCircle({
  latitude,
  longitude,
  result
}) {

  if (!result) {
    return null;
  }

  const score =
    result.overall_risk.score;

  let color = "#4bd6a2";

  if (score >= 75) {
    color = "#e45d5d";
  }

  else if (score >= 40) {
    color = "#d5aa4b";
  }

  const radius =
    15000 + (score * 700);

  return (

    <Circle
      center={[
        Number(latitude),
        Number(longitude)
      ]}
      radius={radius}
      pathOptions={{
        color: color,
        fillColor: color,
        fillOpacity: 0.16,
        weight: 2
      }}
    />

  );
}


// ==================================================
// APP
// ==================================================

function App() {

  // ==================================================
  // LOCATION
  // ==================================================

  const [latitude, setLatitude] =
    useState(17.3850);

  const [longitude, setLongitude] =
    useState(78.4867);


  // ==================================================
  // ENVIRONMENT
  // ==================================================

  const [rainfall, setRainfall] =
    useState(0);

  // Real CWC flood-model features
  const [rainfall3h, setRainfall3h] =
    useState(0);

  const [rainfall6h, setRainfall6h] =
    useState(0);

  const [rainfall24h, setRainfall24h] =
    useState(0);

  const [previousWaterLevel, setPreviousWaterLevel] =
    useState(30);

  // Kept for dashboard display / future data sources
  const [waterLevel, setWaterLevel] =
    useState(30);

  const [soilMoisture, setSoilMoisture] =
    useState(30);

  const [windSpeed, setWindSpeed] =
    useState(10);

  const [pressure, setPressure] =
    useState(1013);

  const [pressureDrop, setPressureDrop] =
    useState(0);

  const [slope, setSlope] =
    useState(10);


  // ==================================================
  // WEATHER
  // ==================================================

  const [temperature, setTemperature] =
    useState(null);


  // ==================================================
  // RESULT
  // ==================================================

  const [result, setResult] =
    useState(null);


  // ==================================================
  // STATE
  // ==================================================

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  // ==================================================
  // CWC DATA
  // ==================================================

  const [cwcStations, setCwcStations] =
    useState([]);

  const [cwcLoading, setCwcLoading] =
    useState(false);

  const [selectedCwcStation, setSelectedCwcStation] =
    useState(null);


  // ==================================================
  // CWC STATIONS
  // ==================================================

  async function loadCwcStations() {

    setCwcLoading(true);
    setError("");

    try {

      const response =
        await fetch(
          "http://127.0.0.1:8000/api/cwc"
        );

      if (!response.ok) {

        throw new Error(
          "Unable to load CWC station data."
        );

      }

      const data =
        await response.json();

      setCwcStations(
        data.stations || []
      );

      if (!data.stations || data.stations.length === 0) {

        setError(
          "No common CWC rainfall and river-level stations were found."
        );

      }

    }

    catch (err) {

      setError(
        err.message ||
        "Unable to load CWC data."
      );

    }

    finally {

      setCwcLoading(false);

    }

  }


  function selectCwcStation(station) {

    setSelectedCwcStation(
      station
    );

    setLatitude(
      station.latitude
    );

    setLongitude(
      station.longitude
    );

    setRainfall(
      station.rainfall
    );

    setWaterLevel(
      station.water_level
    );

  }


  // ==================================================
  // LIVE WEATHER
  // ==================================================

  async function loadLiveWeather() {

    setLoading(true);
    setError("");

    try {

      const response =
        await fetch(
          "http://127.0.0.1:8000/api/weather",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify({

              latitude:
                Number(latitude),

              longitude:
                Number(longitude)

            })
          }
        );


      if (!response.ok) {

        throw new Error(
          "Unable to fetch live weather."
        );

      }


      const weatherData =
        await response.json();

      const weather =
        weatherData.weather;


      const liveRainfall =
        weather.rain ?? 0;

      const liveWind =
        weather.wind_speed ?? 0;

      const livePressure =
        weather.pressure ?? 1013;

      const liveSoil =
        (weather.soil_moisture ?? 0) * 100;


      setRainfall(liveRainfall);

      setWindSpeed(liveWind);

      setPressure(livePressure);

      setSoilMoisture(liveSoil);

      setTemperature(
        weather.temperature
      );


      await analyzeData({

        latitude:
          Number(latitude),

        longitude:
          Number(longitude),

        rainfall:
          liveRainfall,

        rainfall_3h:
          Number(rainfall3h),

        rainfall_6h:
          Number(rainfall6h),

        rainfall_24h:
          Number(rainfall24h),

        previous_water_level:
          Number(previousWaterLevel),

        water_level:
          Number(waterLevel),

        soil_moisture:
          liveSoil,

        wind_speed:
          liveWind,

        pressure:
          livePressure,

        pressure_drop:
          Number(pressureDrop),

        slope:
          Number(slope)

      });

    }

    catch (err) {

      setError(
        err.message ||
        "Something went wrong."
      );

    }

    finally {

      setLoading(false);

    }

  }


  // ==================================================
  // MANUAL ANALYSIS
  // ==================================================

  async function analyzeManualValues() {

    setLoading(true);
    setError("");

    await analyzeData({

      latitude:
        Number(latitude),

      longitude:
        Number(longitude),

      rainfall:
        Number(rainfall),

      rainfall_3h:
        Number(rainfall3h),

      rainfall_6h:
        Number(rainfall6h),

      rainfall_24h:
        Number(rainfall24h),

      previous_water_level:
        Number(previousWaterLevel),

      water_level:
        Number(waterLevel),

      soil_moisture:
        Number(soilMoisture),

      wind_speed:
        Number(windSpeed),

      pressure:
        Number(pressure),

      pressure_drop:
        Number(pressureDrop),

      slope:
        Number(slope)

    });

    setLoading(false);

  }


  // ==================================================
  // ANALYZE
  // ==================================================

  async function analyzeData(data) {

    try {

      const response =
        await fetch(
          "http://127.0.0.1:8000/api/predict",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body:
              JSON.stringify(data)

          }
        );


      if (!response.ok) {

        const message =
          await response.text();

        throw new Error(
          message ||
          "Prediction failed."
        );

      }


      const prediction =
        await response.json();

      setResult(
        prediction
      );

    }

    catch (err) {

      setError(
        err.message ||
        "Prediction failed."
      );

    }

  }


  // ==================================================
  // RISK CARD
  // ==================================================

  function RiskCard({
    title,
    data
  }) {

    if (!data) {
      return null;
    }


    return (

      <div className="risk-card">

        <div className="risk-card-header">

          <h3>
            {title}
          </h3>

          <span
            className={
              `risk-level ${data.level.toLowerCase()}`
            }
          >
            {data.level}
          </span>

        </div>


        <div className="risk-score">

          {data.probability}%

        </div>


        <div className="progress-container">

          <div
            className="progress-bar"
            style={{
              width:
                `${Math.min(
                  data.probability,
                  100
                )}%`
            }}
          />

        </div>


        <p className="risk-description">
          Risk probability
        </p>

      </div>

    );

  }


  // ==================================================
  // UI
  // ==================================================

  return (

    <div className="app">


      {/* ==============================================
          HEADER
      ============================================== */}

      <header className="header">

        <div>

          <h1>
            DisasterShield AI
          </h1>

          <p>
            Multi-Hazard Early Warning & Risk Prediction
          </p>

        </div>


        <div className="status">

          <span className="status-dot"></span>

          System Online

        </div>

      </header>


      {/* ==============================================
          DASHBOARD
      ============================================== */}

      <main className="dashboard">


        {/* ============================================
            MAP
        ============================================ */}

        <section className="panel">

          <div className="panel-title">

            <div>

              <h2>
                Risk Monitoring Map
              </h2>

              <p>
                Select a location and visualize the predicted hazard zone.
              </p>

            </div>


            {result && (

              <span
                className={
                  `risk-level ${
                    result.overall_risk.level.toLowerCase()
                  }`
                }
              >
                {result.overall_risk.level} RISK
              </span>

            )}

          </div>


          <div className="coordinates">

            <div className="input-group">

              <label>
                Latitude
              </label>

              <input
                type="number"
                step="any"
                value={latitude}
                onChange={(e) =>
                  setLatitude(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Longitude
              </label>

              <input
                type="number"
                step="any"
                value={longitude}
                onChange={(e) =>
                  setLongitude(e.target.value)
                }
              />

            </div>

          </div>


          <div
            style={{
              display: "flex",
              gap: "10px",
              alignItems: "center",
              marginBottom: "14px",
              flexWrap: "wrap"
            }}
          >

            <button
              className="primary-button"
              onClick={loadCwcStations}
              disabled={cwcLoading}
            >
              {cwcLoading
                ? "Loading CWC Stations..."
                : "Load Real CWC Stations"}
            </button>

            {cwcStations.length > 0 && (

              <span>
                {cwcStations.length} CWC stations loaded
              </span>

            )}

          </div>


          {selectedCwcStation && (

            <div className="live-info">

              <span>
                CWC Station:
                {" "}
                <strong>
                  {selectedCwcStation.station}
                </strong>
              </span>

              <span>
                Rainfall:
                {" "}
                <strong>
                  {selectedCwcStation.rainfall} mm
                </strong>
              </span>

              <span>
                River Level:
                {" "}
                <strong>
                  {selectedCwcStation.water_level} m
                </strong>
              </span>

              <span>
                Observation:
                {" "}
                <strong>
                  {selectedCwcStation.time}
                </strong>
              </span>

            </div>

          )}


          <div className="map-container">

            <MapContainer
              center={[
                Number(latitude),
                Number(longitude)
              ]}
              zoom={6}
              style={{
                height: "400px",
                width: "100%"
              }}
            >

              <TileLayer
                attribution="&copy; OpenStreetMap contributors"
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />


              {cwcStations.map((station) => (

                <Marker
                  key={station.station}
                  position={[
                    Number(station.latitude),
                    Number(station.longitude)
                  ]}
                  eventHandlers={{
                    click: () =>
                      selectCwcStation(station)
                  }}
                >

                  <Popup>

                    <strong>
                      {station.station}
                    </strong>

                    <br />

                    Rainfall:
                    {" "}
                    {station.rainfall} mm

                    <br />

                    River level:
                    {" "}
                    {station.water_level} m

                    <br />

                    Observation:
                    {" "}
                    {station.time}

                    <br />
                    <br />

                    Click the station marker to load its values.

                  </Popup>

                </Marker>

              ))}


              <Marker
                position={[
                  Number(latitude),
                  Number(longitude)
                ]}
              />


              <RiskCircle
                latitude={latitude}
                longitude={longitude}
                result={result}
              />


              <MapClickHandler
                setLatitude={setLatitude}
                setLongitude={setLongitude}
              />

            </MapContainer>

          </div>


          {cwcStations.length > 0 && (

            <p
              style={{
                marginTop: "10px",
                fontSize: "13px",
                opacity: 0.75
              }}
            >
              CWC markers show stations with matching rainfall and
              river-level observations. Click a marker to load its
              latest values into the dashboard.
            </p>

          )}


          {result && (

            <div className="map-legend">

              <div>
                <span className="legend-dot low-dot"></span>
                Low
              </div>

              <div>
                <span className="legend-dot moderate-dot"></span>
                Moderate
              </div>

              <div>
                <span className="legend-dot high-dot"></span>
                High
              </div>

            </div>

          )}

        </section>


        {/* ============================================
            LIVE WEATHER
        ============================================ */}

        <section className="panel">

          <div className="panel-title">

            <div>

              <h2>
                Live Environmental Data
              </h2>

              <p>
                Fetch current weather conditions and run the ML models.
              </p>

            </div>

          </div>


          <button
            className="primary-button"
            onClick={loadLiveWeather}
            disabled={loading}
          >

            {loading
              ? "Analyzing..."
              : "Load Live Weather & Analyze"}

          </button>


          {temperature !== null && (

            <div className="live-info">

              <span>
                Temperature:
                {" "}
                <strong>
                  {temperature} °C
                </strong>
              </span>

              <span>
                Live weather loaded
              </span>

            </div>

          )}

        </section>


        {/* ============================================
            MANUAL PARAMETERS
        ============================================ */}

        <section className="panel">

          <div className="panel-title">

            <div>

              <h2>
                Environmental Parameters
              </h2>

              <p>
                Adjust values manually for model testing. CWC station
                selection fills the latest rainfall and river-level values.
              </p>

            </div>

          </div>


          <div className="input-grid">

            <div className="input-group">

              <label>
                Rainfall (mm)
              </label>

              <input
                type="number"
                value={rainfall}
                onChange={(e) =>
                  setRainfall(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Rainfall — 3h (mm)
              </label>

              <input
                type="number"
                value={rainfall3h}
                onChange={(e) =>
                  setRainfall3h(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Rainfall — 6h (mm)
              </label>

              <input
                type="number"
                value={rainfall6h}
                onChange={(e) =>
                  setRainfall6h(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Rainfall — 24h (mm)
              </label>

              <input
                type="number"
                value={rainfall24h}
                onChange={(e) =>
                  setRainfall24h(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Previous River Level (m)
              </label>

              <input
                type="number"
                step="any"
                value={previousWaterLevel}
                onChange={(e) =>
                  setPreviousWaterLevel(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Water Level (m)
              </label>

              <input
                type="number"
                step="any"
                value={waterLevel}
                onChange={(e) =>
                  setWaterLevel(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Soil Moisture (%)
              </label>

              <input
                type="number"
                value={soilMoisture}
                onChange={(e) =>
                  setSoilMoisture(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Wind Speed (km/h)
              </label>

              <input
                type="number"
                value={windSpeed}
                onChange={(e) =>
                  setWindSpeed(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Central Pressure (hPa)
              </label>

              <input
                type="number"
                value={pressure}
                onChange={(e) =>
                  setPressure(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Pressure Drop (hPa)
              </label>

              <input
                type="number"
                value={pressureDrop}
                onChange={(e) =>
                  setPressureDrop(e.target.value)
                }
              />

            </div>


            <div className="input-group">

              <label>
                Slope (degrees)
              </label>

              <input
                type="number"
                value={slope}
                onChange={(e) =>
                  setSlope(e.target.value)
                }
              />

            </div>

          </div>


          <button
            className="secondary-button"
            onClick={analyzeManualValues}
            disabled={loading}
          >

            Analyze Manual Values

          </button>

        </section>


        {/* ============================================
            ERROR
        ============================================ */}

        {error && (

          <div className="error-box">

            <strong>
              Error:
            </strong>

            <span>
              {error}
            </span>

          </div>

        )}


        {/* ============================================
            RESULTS
        ============================================ */}

        {result && (

          <>

            {/* OVERALL */}

            <section className="panel overall-panel">

              <div>

                <h2>
                  Overall Risk
                </h2>

                <p>
                  Highest predicted hazard probability
                </p>

              </div>


              <div className="overall-risk">

                <div className="overall-score">

                  {result.overall_risk.score}%

                </div>

                <span
                  className={
                    `risk-level ${
                      result.overall_risk.level.toLowerCase()
                    }`
                  }
                >
                  {result.overall_risk.level}
                </span>

              </div>

            </section>


            {/* SMART ALERT */}

            <section className="panel smart-alert-panel">

              <div className="panel-title">

                <div>

                  <h2>
                    🚨 Smart Alert
                  </h2>

                  <p>
                    Priority warning based on the highest predicted hazard.
                  </p>

                </div>

              </div>

              {(() => {

                const hazards = [
                  {
                    name: "Flood",
                    data: result.predictions.flood
                  },
                  {
                    name: "Landslide",
                    data: result.predictions.landslide
                  },
                  {
                    name: "Severe Storm",
                    data: result.predictions.storm
                  }
                ];

                const priority = {
                  LOW: 1,
                  MODERATE: 2,
                  HIGH: 3,
                  CRITICAL: 4
                };

                const highest = hazards.reduce((a, b) =>
                  priority[b.data.level] > priority[a.data.level] ? b : a
                );

                let message = "";
                let actions = [];

                if (highest.name === "Flood") {
                  message =
                    "Flood risk is currently the priority hazard.";
                  actions = [
                    "Avoid low-lying and flooded areas.",
                    "Do not attempt to cross flooded roads.",
                    "Monitor local emergency announcements."
                  ];
                } else if (highest.name === "Severe Storm") {
                  message =
                    "Severe storm risk is currently the priority hazard.";
                  actions = [
                    "Stay indoors and away from windows.",
                    "Avoid trees and open areas.",
                    "Secure loose outdoor objects."
                  ];
                } else {
                  message =
                    "Landslide risk is currently the priority hazard.";
                  actions = [
                    "Avoid steep or unstable slopes.",
                    "Watch for cracks or unusual ground movement.",
                    "Follow local evacuation instructions if issued."
                  ];
                }

                return (
                  <div className="smart-alert-content">

                    <div className="smart-alert-main">

                      <span
                        className={
                          `risk-level ${highest.data.level.toLowerCase()}`
                        }
                      >
                        {highest.data.level}
                      </span>

                      <h3>
                        {highest.name} — {highest.data.probability}%
                      </h3>

                      <p>
                        {message}
                      </p>

                    </div>

                    <div className="smart-alert-actions">

                      <h4>
                        Recommended Actions
                      </h4>

                      <ul>
                        {actions.map((action, index) => (
                          <li key={index}>
                            {action}
                          </li>
                        ))}
                      </ul>

                    </div>

                  </div>
                );

              })()}

            </section>


            {/* HAZARDS */}

            <section className="risk-grid">

              <RiskCard
                title="Flood"
                data={
                  result.predictions.flood
                }
              />

              <RiskCard
                title="Landslide"
                data={
                  result.predictions.landslide
                }
              />

              <RiskCard
                title="Severe Storm"
                data={
                  result.predictions.storm
                }
              />

            </section>


            {/* ENVIRONMENT */}

            <section className="panel">

              <div className="panel-title">

                <div>

                  <h2>
                    Current Environment
                  </h2>

                  <p>
                    Values used by the prediction engine.
                  </p>

                </div>

              </div>


              <div className="environment-grid">

                <div className="environment-item">

                  <span>
                    Rainfall
                  </span>

                  <strong>
                    {result.environment.rainfall}
                  </strong>

                  <small>
                    mm
                  </small>

                </div>


                <div className="environment-item">

                  <span>
                    Rainfall 3h
                  </span>

                  <strong>
                    {result.environment.rainfall_3h}
                  </strong>

                  <small>
                    mm
                  </small>

                </div>


                <div className="environment-item">

                  <span>
                    Rainfall 6h
                  </span>

                  <strong>
                    {result.environment.rainfall_6h}
                  </strong>

                  <small>
                    mm
                  </small>

                </div>


                <div className="environment-item">

                  <span>
                    Rainfall 24h
                  </span>

                  <strong>
                    {result.environment.rainfall_24h}
                  </strong>

                  <small>
                    mm
                  </small>

                </div>


                <div className="environment-item">

                  <span>
                    Previous River Level
                  </span>

                  <strong>
                    {result.environment.previous_water_level}
                  </strong>

                  <small>
                    m
                  </small>

                </div>


                <div className="environment-item">

                  <span>
                    Water Level
                  </span>

                  <strong>
                    {result.environment.water_level}
                  </strong>

                </div>


                <div className="environment-item">

                  <span>
                    Soil Moisture
                  </span>

                  <strong>
                    {result.environment.soil_moisture}
                  </strong>

                  <small>
                    %
                  </small>

                </div>


                <div className="environment-item">

                  <span>
                    Wind Speed
                  </span>

                  <strong>
                    {result.environment.wind_speed}
                  </strong>

                  <small>
                    km/h
                  </small>

                </div>


                <div className="environment-item">

                  <span>
                    Pressure
                  </span>

                  <strong>
                    {result.environment.pressure}
                  </strong>

                  <small>
                    hPa
                  </small>

                </div>


                <div className="environment-item">

                  <span>
                    Pressure Drop
                  </span>

                  <strong>
                    {result.environment.pressure_drop}
                  </strong>

                  <small>
                    hPa
                  </small>

                </div>


                <div className="environment-item">

                  <span>
                    Slope
                  </span>

                  <strong>
                    {result.environment.slope}
                  </strong>

                  <small>
                    degrees
                  </small>

                </div>

              </div>

            </section>


            {/* ALERTS */}

            <section className="panel">

              <div className="panel-title">

                <div>

                  <h2>
                    Alerts & Recommended Actions
                  </h2>

                  <p>
                    Safety actions based on predicted risk levels.
                  </p>

                </div>

              </div>


              <div className="alerts">

                {result.alerts.map(
                  (alert, index) => (

                    <div
                      className={
                        `alert-card ${
                          alert.level.toLowerCase()
                        }`
                      }
                      key={index}
                    >

                      <div className="alert-header">

                        <h3>
                          {alert.hazard}
                        </h3>

                        <span
                          className={
                            `risk-level ${
                              alert.level.toLowerCase()
                            }`
                          }
                        >
                          {alert.level}
                        </span>

                      </div>


                      <p>
                        {alert.message}
                      </p>


                      <div className="action">

                        <strong>
                          Recommended Action:
                        </strong>

                        <span>
                          {alert.action}
                        </span>

                      </div>

                    </div>

                  )
                )}

              </div>

            </section>

          </>

        )}

      </main>


      {/* ==============================================
          FOOTER
      ============================================== */}

      <footer>

        <p>
          DisasterShield AI • Multi-Hazard Risk Prediction Platform
        </p>

        <p>
          Prototype for early-warning and decision-support use
        </p>

      </footer>

    </div>

  );

}


export default App;