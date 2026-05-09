# GUI Module

This package contains the full Tkinter-based user interface of the application.

The GUI layer is intentionally separated from business logic and database access.  
It communicates with controllers and services only through explicit interfaces.

## Module Structure

```text
gui/
├── app.py
├── main_window.py
├── constants/
├── factories/
├── layout/
├── services/
├── theme/
├── utils/
└── views/
```

## Core Files

### `app.py`

GUI bootstrap module.

Responsibilities:

* create the GUI runtime objects;
* initialize application state;
* prepare controller access;
* create the main window;
* start the Tkinter event loop.

This is the GUI entry point used by the application startup flow.

### `main_window.py`

Main application window.

Responsibilities:

* create the root window;
* assemble all GUI layers;
* manage view switching;
* restore interface state;
* rebuild the interface when user settings change.

This is the main container for the complete UI.

## GUI Runtime Objects

### `AppState`

Stores mutable UI state.

Used for:

* active screen tracking;
* form field values;
* selected items;
* values that should survive widget rebuilds.

Because Tkinter widgets are not reactive, state must be stored explicitly.

### `UIBinder`

Connects widget values with `AppState`.

Responsibilities:

* read values from entry widgets and other controls;
* write values back to the state object;
* restore values when widgets are recreated.

This layer keeps the interface stable during rebuilds.

### `AppTheme`

Applies the global ttk theme.

Responsibilities:

* configure ttk styles;
* define theme-wide appearance;
* apply shared UI colors and widget rules.

### `UIFactory`

Factory for reusable GUI elements.

Currently responsible for:

* text buttons;
* icon buttons;
* buttons with tooltips.

This keeps widget creation consistent across the interface.

### `Translator`

Handles localized text lookup.

It loads the language-specific JSON files from `work/resources/i18n/` and returns translated interface strings.

### `UISettings`

Controls user-facing settings.

Responsibilities:

* load the current user interface settings;
* apply user changes;
* notify `MainWindow` when the GUI must be rebuilt;
* keep settings changes synchronized across the interface.

## Layout Package

The layout package builds the visible structure of the main window.

### `layout_manager.py`

Coordinates all layout layers.

Responsibilities:

* register layout sections;
* create grid structure;
* control visibility;
* apply row and column weights;
* apply separators and sticky rules;
* support adding new layers with minimal changes.

### `menu_bar.py`

Top-level menu layer.

Responsibilities:

* File and Help actions;
* settings access;
* window visibility controls;
* section-level global commands.

### `toolbar.py`

Second horizontal layer.

Responsibilities:

* main section buttons:

  * Data
  * Analysis
  * Reports

This layer acts as the top-level functional navigator.

### `context_panel.py`

Third horizontal layer.

Responsibilities:

* display contextual controls;
* change depending on the selected toolbar section;
* show section-specific actions and fields.

### `content_area.py`

Main content container.

Responsibilities:

* display tables;
* display forms;
* display charts;
* display reports;
* act as the primary workspace of the application.

## Views

View modules implement specific GUI screens and popups.

### `views/settings_menu.py`

Interface settings menu.

Supports:

* language switching;
* scale switching;
* font switching;
* theme switching;
* Tk theme switching;
* reset to defaults.

It may open additional confirmation or selection dialogs.

### `views/font_selector_popup.py`

Font selection popup.

Responsibilities:

* list available Tk fonts;
* preview the selected font;
* show a sample phrase adapted to the chosen language.

## GUI Constants

The constants package stores values that are reused across the GUI.

### `constants/i18n.py`

Supported language registry.

To add a new language:

1. add the translation file to `work/resources/i18n/`
2. add the language token and display name to this file

### `constants/scale.py`

UI scale registry.

Contains:

* scale token names;
* scale preset definitions;
* resolution helper for converting preset names into actual scale settings.

### `constants/window.py`

Window-related constants.

Contains:

* main window minimum size;
* font popup size;
* other size values used by the GUI.

## Theme Package

The theme package contains the styling system for the GUI.

### `theme/styles.py`

Defines named ttk styles used by custom widgets.

### `theme/themes.py`

Registers available theme names and theme presets.

### `theme/_themes/tokens.py`

Defines the token dataclass for theme values.

### `theme/_themes/light.py`

Light theme values.

### `theme/_themes/dark.py`

Dark theme values.

## Utility Modules

### `utils/tooltip.py`

Reusable tooltip implementation for buttons and other widgets.

### `utils/image_loader.py`

Utility for loading images and icons.

## Adding a New Screen

To add a new GUI screen:

1. Create the screen module in `views/`.
2. Register it in the layout or in the view-switching logic.
3. Add a controller method if the screen needs backend data.
4. Use `UIFactory` for standard widgets.
5. Store user-entered values in `AppState` through `UIBinder`.

Do not access the database directly from the view.

## Adding a New Theme

To add a new theme:

1. Add a new token file in `theme/_themes/`.
2. Register the new theme in `theme/themes.py`.
3. Update theme selection options in `views/settings_menu.py`.

## Adding a New Language

To add a new language:

1. Add the translation JSON file to `work/resources/i18n/`.
2. Add the language token to `constants/i18n.py`.
3. Make sure the translator can resolve all required keys.

## Adding a New Scale Preset

To add a new scale:

1. Define the preset in `constants/scale.py`.
2. Update the scale selection options in the settings menu.
3. Ensure the window dimensions remain valid for the minimum window size.

## UI Rebuild Flow

Some settings changes require rebuilding the visible interface.

Typical flow:

1. User changes a setting in the settings menu.
2. `UISettings` updates the active user configuration.
3. `MainWindow` receives the rebuild notification.
4. The window is reconstructed with the new settings.
5. `AppState` restores stored values into the new widgets.

This ensures that visible changes are applied immediately and consistently.

## Design Rules

When editing the GUI layer, follow these rules:

* keep all Tkinter code inside `scripts/gui/`;
* do not place business logic in views;
* do not call the database from GUI modules;
* use controllers for all user actions that affect data;
* keep all UI state in `AppState`;
* use `UIBinder` for form synchronization;
* use `UIFactory` for standard widgets;
* use `Translator` for all user-visible text.

## Summary

This package contains the complete user interface implementation of the application.

Its responsibilities are limited to:

* display;
* user interaction;
* state restoration;
* visual theming;
* localization;
* view composition.

All data access and business logic must remain outside this package.
