# GUI Architecture

## Purpose

The GUI layer provides the user-facing interface for the application.  
It is responsible for displaying data, collecting user input, switching between screens, and forwarding user actions to the controller layer.

The GUI does not contain business logic and does not access the database directly.

## Architectural Role

The GUI layer is the top-level presentation layer of the application and follows the project flow:

GUI → Controller → Service → Repository → Database

This separation keeps the interface independent from data storage and analytical logic.

## Startup Flow

Application startup follows this sequence:

1. `work/scripts/main.py` creates `ConfigManager`.
2. `ConfigManager` loads application and user configuration.
3. `work/scripts/gui/app.py` creates GUI-related objects.
4. `AppState` is created to preserve UI state.
5. `UIBinder` connects GUI widgets with state values.
6. `AppTheme` initializes global ttk styling.
7. `UIFactory` provides reusable widget constructors.
8. `Translator` loads localized texts from `resources/i18n/`.
9. `UISettings` manages user-visible settings and rebuild requests.
10. `MainWindow` creates and assembles all GUI layers.

## Main GUI Components

### `AppState`
`AppState` stores the current UI state.  
It is used to preserve information across redraws and rebuilds, such as:
- current active screen;
- current selected values;
- form field values;
- other temporary interface data.

Tkinter is not reactive, so the state object is needed to restore values when widgets are recreated.

### `UIBinder`
`UIBinder` is the layer between widgets and `AppState`.  
It ensures that input values remain synchronized with the stored UI state.

Its role is to:
- read values from widgets;
- write values into `AppState`;
- restore values after rebuilding the interface.

### `AppTheme`
`AppTheme` defines global styling using `ttk.Style`.  
It is responsible for applying theme-wide appearance rules to standard Tk widgets.

Global theme configuration includes:
- default colors;
- ttk style setup;
- base widget styling;
- theme switching support.

### `UIFactory`
`UIFactory` is a reusable widget factory.  
It creates common GUI elements in a consistent way, such as:
- text buttons;
- icon buttons;
- buttons with tooltips.

The purpose of the factory is to keep widget creation uniform and avoid duplicated styling code.

### `Translator`
`Translator` handles language-dependent text rendering.

It reads translation files from:
- `resources/i18n/en.json`
- `resources/i18n/ru.json`
- `resources/i18n/pt.json`
- `resources/i18n/ky.json`

The translator selects the active language and returns the correct labels, messages, and interface text.

### `UISettings`
`UISettings` manages user-side appearance and behavior settings.

It is responsible for:
- reading current user configuration;
- applying changes to GUI-related components;
- notifying `MainWindow` when the interface must be rebuilt.

When a setting changes, the window is rebuilt so that the new parameters can be applied consistently.

### `MainWindow`
`MainWindow` is the central GUI container.  
It assembles all visible interface layers and controls layout switching.

Its responsibilities are:
- create the main window;
- manage all top-level layout blocks;
- switch between sections;
- hide and show interface layers;
- restore GUI state after rebuild;
- rebuild the interface when settings change.

## Layout System

The visible interface is assembled from several horizontal layers:

1. `menu_bar` — top navigation and global actions
2. `toolbar` — main functional groups such as Data, Analysis, Reports
3. `context_panel` — context-dependent controls
4. `content_area` — main working area for forms, data, charts, and reports

The `LayoutManager` is responsible for:
- registering layout layers;
- placing them into the grid;
- managing visibility;
- applying weights, sticky options, separators, and related layout rules.

This allows new layers to be added without rewriting the entire interface.

## Layout Modules

### `menu_bar.py`
Top application layer.

Responsibilities:
- provide File and Help actions;
- allow hiding of lower layers when needed;
- open settings menu;
- control global navigation actions.

When the settings button is activated, `_toggle_settings_menu()` opens `SettingsMenu`.

### `toolbar.py`
Second GUI layer.

Responsibilities:
- provide the main functional sections:
  - Data
  - Analysis
  - Reports

At the current stage, these buttons act as section selectors and placeholders for future functionality.

### `context_panel.py`
Third GUI layer.

Responsibilities:
- show controls and input fields depending on the selected toolbar section;
- dynamically adapt to the current application context.

### `content_area.py`
Fourth GUI layer.

Responsibilities:
- host the main application content;
- display data tables, forms, reports, charts, or database records;
- act as the primary working area.

At the current stage it may be a placeholder, but it is intended to become the main content container.

## View System

The GUI uses separate view modules for popups and settings-related screens.

### `settings_menu.py`
Settings menu for interface customization.

It supports:
- language switching;
- scale switching;
- font selection;
- theme switching;
- Tk theme switching;
- reset of all settings to defaults.

It also opens confirmation windows when needed.

### `font_selector_popup.py`
Popup window for font selection.

Responsibilities:
- show available Tkinter fonts;
- show live preview;
- display sample text appropriate for the selected language.

## Constants and Configuration Support

GUI-level constants are stored in `scripts/gui/constants/`.

### `i18n.py`
Contains supported language tokens and display names.

Example:
- `ru` → `Русский`
- `en` → `English`
- `pt` → `Português`
- `ky` → `Кыргызча`

To add a new language:
1. add the language JSON file in `work/resources/i18n/`
2. add the language token to `constants/i18n.py`

### `scale.py`
Contains GUI scale presets and scale resolution logic.

It defines:
- scale token names;
- dataclass describing scale fields;
- scale presets;
- `resolve_ui_scale()` helper.

### `window.py`
Contains window size constants such as:
- minimum main window size;
- font popup size.

## Theme System

Theme management is separated into dedicated modules.

### `theme/styles.py`
Contains reusable ttk style names for fine-grained widget styling.

### `theme/themes.py`
Contains available theme names and the theme registry.

### `theme/_themes/tokens.py`
Defines the theme token dataclass used by all built-in themes.

### `_themes/light.py` and `_themes/dark.py`
Contain the concrete visual token sets for light and dark appearance modes.

## UI Services

The GUI service layer contains small helpers that support the user interface.

### `translator.py`
Provides language-aware text lookup.

### `ui_binder.py`
Synchronizes widget values with `AppState`.

### `ui_settings.py`
Applies user configuration changes and triggers interface rebuilds when necessary.

## Resource Files

Translation resources are stored in:

```text
work/resources/i18n/
```

These files contain localized interface texts and allow the GUI to support multiple languages without changing code.

## Extension Rules

When adding a new GUI feature, follow these rules:

1. Add reusable widget code to `widgets/`.
2. Add screen-level code to `views/`.
3. Add popup dialogs to `views/` or a dedicated dialog module if the screen is modal.
4. Add GUI-specific logic to `services/`.
5. Do not place database logic inside GUI modules.
6. Do not place business logic inside Tkinter view code.
7. Keep GUI state in `AppState` and not inside individual widgets.

## Summary

The GUI layer is designed as a clean presentation layer with the following goals:

* keep UI logic separate from business logic;
* allow state restoration after rebuilds;
* support language and theme switching;
* centralize widget creation;
* provide a scalable structure for future screens and dialogs.
