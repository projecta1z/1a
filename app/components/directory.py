import reflex as rx
from app.states.directory import DirectoryState


def brand_bar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.icon("library", class_name="h-5 w-5 text-[#365748]"),
                rx.el.span(
                    "The Username Index",
                    class_name="font-semibold tracking-tight",
                ),
                href="/",
                class_name="flex items-center gap-3",
            ),
            rx.el.span(
                "A LITTLE ORDER. A WORLD OF NAMES.",
                class_name="hidden sm:block text-[10px] tracking-[0.18em] text-[#73796f]",
            ),
            class_name="mx-auto max-w-7xl px-6 lg:px-12 h-18 flex items-center justify-between gap-6",
        ),
        class_name="border-b border-[#d6d5c9] bg-[#faf9f3]",
    )


def hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.p(
                "THE DIRECTORY  /  VOL. 001",
                class_name="text-[11px] font-medium tracking-[0.2em] text-[#526651] mb-5",
            ),
            rx.el.h1(
                "Every name.",
                rx.el.br(),
                rx.el.span("In its place.", class_name="italic text-[#365748]"),
                class_name="font-['Libre_Baskerville'] text-5xl sm:text-6xl lg:text-[72px] leading-[1.14] tracking-[-0.055em]",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.p(
                "Good things are easy to find.",
                class_name="font-['Libre_Baskerville'] text-xl mb-3",
            ),
            rx.el.p(
                "An alphabetically arranged collection of usernames. Search for a familiar name, or let a letter lead the way.",
                class_name="text-sm leading-7 text-[#6a706c] max-w-md mb-7",
            ),
            rx.el.div(
                rx.icon("search", class_name="h-5 w-5 shrink-0 text-[#526651]"),
                rx.el.input(
                    placeholder="Find a username…",
                    aria_label="Search usernames",
                    default_value=DirectoryState.search,
                    on_change=DirectoryState.search_changed.debounce(350),
                    class_name="w-full min-w-0 bg-transparent text-base text-[#202f37] outline-hidden placeholder:text-[#91958b] py-5",
                ),
                rx.cond(
                    DirectoryState.search != "",
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4"),
                        aria_label="Clear search",
                        on_click=DirectoryState.search_changed(""),
                        class_name="p-2 text-[#526651] hover:bg-[#e9e9df]",
                    ),
                ),
                class_name="flex items-center gap-3 border-b border-[#526651] focus-within:border-[#202f37]",
            ),
            class_name="w-full lg:w-5/12 lg:pb-2",
        ),
        class_name="flex flex-col lg:flex-row lg:items-end gap-12 lg:gap-20 pt-16 pb-16 lg:pt-24 lg:pb-20",
    )


def letter_cell(letter: str) -> rx.Component:
    return rx.el.button(
        letter,
        on_click=DirectoryState.select_initial(letter),
        aria_label=f"Browse {letter}",
        aria_pressed=DirectoryState.initial == letter,
        class_name=rx.cond(
            DirectoryState.initial == letter,
            "flex h-12 min-w-10 items-center justify-center border border-[#365748] bg-[#365748] text-[#faf9f3] font-['Libre_Baskerville'] text-lg transition-colors focus-visible:outline-2",
            "flex h-12 min-w-10 items-center justify-center border border-[#d6d5c9] bg-transparent text-[#365748] font-['Libre_Baskerville'] text-lg hover:bg-[#e9e9df] transition-colors focus-visible:outline-2",
        ),
    )


def alphabet_index() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Browse the alphabet",
                class_name="font-['Libre_Baskerville'] text-xl",
            ),
            rx.el.span(
                "A–Z, AND EVERYTHING IN BETWEEN.",
                class_name="text-[10px] tracking-[0.15em] text-[#73796f]",
            ),
            class_name="flex flex-wrap items-center justify-between gap-3 mb-6",
        ),
        rx.el.div(
            letter_cell("All"),
            rx.foreach(DirectoryState.letters, letter_cell),
            class_name="grid grid-cols-7 sm:grid-cols-9 lg:grid-cols-[repeat(27,minmax(0,1fr))] gap-1",
        ),
        class_name="pb-10 border-b border-[#d6d5c9]",
    )


def metric(value: rx.Var, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            value,
            class_name="font-['Libre_Baskerville'] text-2xl text-[#365748]",
        ),
        rx.el.span(
            label,
            class_name="text-[10px] uppercase tracking-[0.15em] text-[#73796f]",
        ),
        class_name="flex items-baseline gap-3",
    )


def result_row(row: dict[str, str]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            row["number"],
            class_name="px-5 sm:px-7 py-5 text-xs tabular-nums text-[#73796f] w-20",
        ),
        rx.el.td(
            rx.el.span(
                row["initial"],
                class_name="font-['Libre_Baskerville'] text-lg text-[#365748]",
            ),
            class_name="px-5 py-5 w-24",
        ),
        rx.el.td(
            row["username"],
            class_name="px-5 sm:px-7 py-5 font-['Libre_Baskerville'] text-lg text-[#202f37]",
        ),
        key=row["number"],
        class_name="border-t border-[#d9dacf] even:bg-[#f5f4ed] hover:bg-[#eeeee4] transition-colors",
    )


def results() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            metric(DirectoryState.total, "Total names"),
            metric(DirectoryState.indexed, "Indexed letters"),
            rx.el.div(
                rx.cond(
                    DirectoryState.filtered,
                    rx.el.button(
                        "Clear filters",
                        rx.icon("x", class_name="h-3 w-3"),
                        on_click=DirectoryState.clear_filters,
                        class_name="flex items-center gap-2 text-xs text-[#365748] underline underline-offset-4",
                    ),
                    rx.el.span(
                        "ALL NAMES. IN ORDER.",
                        class_name="text-[10px] tracking-[0.15em] text-[#73796f]",
                    ),
                ),
                class_name="sm:ml-auto",
            ),
            class_name="flex flex-wrap items-center gap-6 sm:gap-10 py-8",
        ),
        rx.el.div(
            rx.el.h2(
                "The collection",
                class_name="font-['Libre_Baskerville'] text-2xl",
            ),
            rx.el.span(
                f"{DirectoryState.result_count} names",
                class_name="text-xs text-[#73796f]",
            ),
            class_name="flex items-center justify-between gap-4 mb-5 mt-5",
        ),
        rx.cond(
            DirectoryState.loading,
            rx.el.div(
                rx.icon(
                    "loader-circle",
                    class_name="h-5 w-5 animate-spin text-[#526651]",
                ),
                rx.el.p(
                    "Finding your place in the index…",
                    class_name="text-sm text-[#71796d]",
                ),
                class_name="flex items-center justify-center gap-3 py-20 bg-[#faf9f2] border border-[#d9dacf]",
                role="status",
            ),
            rx.cond(
                DirectoryState.error != "",
                rx.el.div(
                    rx.icon("circle-alert", class_name="h-6 w-6 text-red-500"),
                    rx.el.p(DirectoryState.error),
                    rx.el.button(
                        "Try again",
                        on_click=DirectoryState.load,
                        class_name="text-[#365748] underline py-2",
                    ),
                    class_name="flex flex-col items-center gap-3 py-14 text-sm",
                    role="alert",
                ),
                rx.cond(
                    DirectoryState.result_count == 0,
                    rx.el.div(
                        rx.icon(
                            "search-x", class_name="h-8 w-8 text-[#73856a]"
                        ),
                        rx.el.h3(
                            "No names on this shelf.",
                            class_name="font-['Libre_Baskerville'] text-xl",
                        ),
                        rx.el.p(
                            "Try a different search or browse all initials.",
                            class_name="text-sm text-[#777e70]",
                        ),
                        rx.el.button(
                            "Clear search & filters",
                            on_click=DirectoryState.clear_filters,
                            class_name="mt-2 bg-[#365748] text-white px-5 py-3 text-xs rounded-sm hover:bg-[#294436]",
                        ),
                        class_name="flex flex-col items-center gap-3 py-16 bg-[#faf9f2] border border-[#d9dacf]",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        rx.el.span(
                                            rx.icon(
                                                "hash", class_name="h-3 w-3"
                                            ),
                                            "No.",
                                            class_name="flex items-center gap-2",
                                        ),
                                        class_name="px-5 sm:px-7 py-4",
                                    ),
                                    rx.el.th(
                                        rx.el.span(
                                            rx.icon(
                                                "a-large-small",
                                                class_name="h-3 w-3",
                                            ),
                                            "Initial",
                                            class_name="flex items-center gap-2",
                                        ),
                                        class_name="px-5 py-4",
                                    ),
                                    rx.el.th(
                                        rx.el.span(
                                            rx.icon(
                                                "at-sign", class_name="h-3 w-3"
                                            ),
                                            "Username",
                                            class_name="flex items-center gap-2",
                                        ),
                                        class_name="px-5 sm:px-7 py-4",
                                    ),
                                    class_name="text-left text-[10px] uppercase tracking-[0.15em] text-[#73796f] bg-[#f0f0e7]",
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(DirectoryState.rows, result_row)
                            ),
                            class_name="table-auto w-full",
                        ),
                        class_name="overflow-hidden border border-[#d9dacf] bg-[#faf9f2]",
                    ),
                ),
            ),
        ),
        class_name="pb-16",
        aria_live="polite",
    )


def directory() -> rx.Component:
    return rx.el.div(
        brand_bar(),
        rx.el.main(
            hero(),
            alphabet_index(),
            results(),
            class_name="mx-auto w-full max-w-7xl px-6 lg:px-12",
        ),
        class_name="min-h-screen bg-[#faf9f3] text-[#202f37] font-['Inter']",
    )
