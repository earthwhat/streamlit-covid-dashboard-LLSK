# COVID-19 Hybrid Dashboard

## Project Overview
This project is a **Hybrid COVID-19 Dashboard** built with **Streamlit**. It visualizes COVID-19 data by combining real-time metrics with historical trend analysis. The application is designed to run in a Dockerized environment for consistent development and deployment across Windows and macOS.

**Key Features:**
*   **Hybrid Data Architecture:**
    *   **Real-time:** Fetches live data (cases, deaths, critical) via the [Disease.sh API](https://disease.sh/docs/).
    *   **Historical:** Downloads and processes time-series data from [OWID (Our World in Data)](https://github.com/owid/covid-19-data) for trend analysis (cached locally).
*   **Hynex Design System:** Implements a custom dark-mode design system ("Hynex") for a modern, semantic UI.
*   **Interactive Visualizations:** Uses Plotly for responsive charts (cases, deaths, vaccinations).
*   **Custom Sidebar:** Features a compact, CSS-styled navigation sidebar.

## Key Files
*   `app.py`: The main entry point for the Streamlit dashboard. Handles layout and primary visualization logic.
*   `data_manager.py`: Responsible for fetching data from APIs and managing local CSV cache for historical data.
*   `style.py`: Defines the "Hynex Design System," including color palettes and CSS styles.
*   `pages/design_guide.py`: A reference page demonstrating the available UI components and styles.
*   `docker-compose.yml` & `Dockerfile`: Configuration for containerizing the application.
*   `requirements.txt`: Python dependencies.

## Building and Running

The project is designed to be run using **Docker Compose**.

### Prerequisites
*   Docker Desktop installed and running.

### Run Application
To build the image and start the container:
```bash
docker-compose up --build
```
*   The dashboard will be available at: `http://localhost:8501`
*   **Note:** The first run may take a few minutes to download the OWID dataset.

### Development Mode
*   The project uses Docker volumes (`./:/app`) to map the local directory to the container.
*   Changes made to `app.py` or other source files will be reflected immediately (use the "Rerun" button in Streamlit).
*   **Dependency Changes:** If you modify `requirements.txt`, you must rebuild the container using `docker-compose up --build`.

## Development Conventions

*   **Design System:** All UI elements should adhere to the Hynex Design System defined in `style.py`.
    *   Import `style` and call `style.apply_hynex_style()` at the top of new pages.
    *   Use `style.get_chart_layout()` for consistent Plotly chart styling.
    *   Sidebars are implemented via HTML/CSS injection in the page and include responsive design for mobile (768px).
    *   Refer to `pages/design_guide.py` (accessible via sidebar) for component examples.
*   **Data Handling:**
    *   Historical data is large and stored in `data/`. This directory is gitignored.
    *   Use `data_manager.py` for all data retrieval logic to ensure proper caching.
*   **Containerization:** Ensure the application always runs correctly within the Docker container before committing.
