"""
Font selector popup widget layout builder.

This module provides a standalone function for constructing the
widget tree of the FontSelectorPopup window, separated from the
window logic for maintainability.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple


def build_font_selector_widgets(
    popup: tk.Toplevel,
    fonts: List[str],
    current_font: str,
    example_text: str,
    apply_text: str,
    on_select: Callable,
    on_apply: Callable,
    on_filter: Callable,
    colors,
    get_font_fn: Callable[[], Tuple[str, int]],
) -> Tuple[tk.Listbox, tk.Text, tk.StringVar]:
    """
    Build and pack all widgets inside the font selector popup.

    Creates the search entry, scrollable font listbox, preview
    text area, and apply button. Binds selection and keyboard
    events. Populates the listbox with the provided font list and
    scrolls to the current font if it is present.

    Parameters
    ----------
    popup : tk.Toplevel
        The parent popup window that receives all widgets.

    fonts : List[str]
        Sorted list of available font family names.

    current_font : str
        Currently active font family (pre-selected in the list).

    example_text : str
        Text shown in the preview area.

    apply_text : str
        Label for the apply button.

    on_select : Callable
        Callback invoked when the listbox selection changes.

    on_apply : Callable
        Callback invoked when the apply button is pressed or a
        font entry is double-clicked / Enter is pressed.

    on_filter : Callable
        Callback invoked on each ``<KeyRelease>`` in the search
        entry to filter the font list.

    colors : object
        Theme color tokens with attributes: ``surface``, ``text``,
        ``accent``, ``button_text``.

    get_font_fn : Callable[[], Tuple[str, int]]
        Zero-argument callable that returns the current UI font
        tuple ``(family, size)``.

    Returns
    -------
    Tuple[tk.Listbox, tk.Text, tk.StringVar]
        A 3-tuple of ``(listbox, preview, search_var)`` references
        that the caller should store for later interaction.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    container = ttk.Frame(popup)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    search_var = tk.StringVar()

    search_entry = ttk.Entry(container, textvariable=search_var)
    search_entry.configure(font=get_font_fn())
    search_entry.pack(fill="x", pady=(0, 10))

    search_entry.bind(
        sequence="<KeyRelease>",
        func=on_filter,
    )

    list_frame = ttk.Frame(master=container)
    list_frame.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(master=list_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    listbox_font = ("Segoe UI", get_font_fn()[1])

    listbox = tk.Listbox(
        master=list_frame,
        yscrollcommand=scrollbar.set,
        exportselection=False,
    )
    listbox.configure(
        bg=colors.surface,
        fg=colors.text,
        selectbackground=colors.accent,
        selectforeground=colors.button_text,
        highlightthickness=0,
        font=listbox_font,
    )
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)  # type: ignore

    preview = tk.Text(master=container, height=4, wrap="word")
    preview.configure(
        bg=colors.surface,
        fg=colors.text,
        insertbackground=colors.text,
        highlightthickness=0,
    )
    preview.pack(fill="x", pady=10)
    preview.insert(index="1.0", chars=example_text)
    preview.config(state="disabled")

    ttk.Button(
        master=container,
        text=apply_text,
        command=on_apply,
    ).pack(fill="x")

    # Populate the listbox.
    for font_name in fonts:
        listbox.insert("end", font_name)

    if current_font in fonts:
        index = fonts.index(current_font)
        listbox.selection_set(first=index)
        listbox.see(index=index)

    listbox.bind(sequence="<<ListboxSelect>>", func=on_select)
    listbox.bind(sequence="<Double-Button-1>", func=on_apply)
    listbox.bind(sequence="<Return>", func=on_apply)

    return listbox, preview, search_var
