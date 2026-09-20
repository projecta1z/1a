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
                        rx.icon("x", class_name="w-4 h-4"),
                        on_click=DirectoryState.clear_filters,
                        aria_label="Clear search and filters",
                        class_name="p-2 text-[#526651] hover:bg-[#e9ecdf] rounded-sm",
                    ),
                ),
                class_name="flex items-center gap-3 px-5 bg-[#fffef9] border border-[#bdc3b5] rounded-sm focus-within:ring-2 focus-within:ring-[#365748]/20 focus-within:border-[#365748]",
            ),
            rx.el.p(
                "Search any part of a name. No exact match needed.",
                class_name="text-xs text-[#7c8177] mt-3",
            ),
            class_name="flex-1 lg:max-w-[460px] lg:pb-1",
        ),
        class_name="flex flex-col lg:flex-row gap-10 lg:gap-20 lg:items-end pt-14 pb-12 lg:pt-17 lg:pb-14",
    )


def letter_cell(letter: str) -> rx.Component:
    return rx.el.button(
        rx.el.span(
            letter, class_name="font-['Libre_Baskerville'] text-2xl sm:text-3xl"
        ),
        rx.el.span("↗", class_name="text-[10px] opacity-50"),
        on_click=DirectoryState.select_initial(letter),
        aria_label=f"Filter usernames starting with {letter}",
        aria_pressed=DirectoryState.initial == letter,
        class_name=rx.cond(
            DirectoryState.initial == letter,
            "flex flex-col items-center justify-center gap-2 h-22 sm:h-24 bg-[#365748] text-[#fffef6] border border-[#365748] rounded-sm transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#365748]",
            "flex flex-col items-center justify-center gap-2 h-22 sm:h-24 bg-[#faf9f2] text-[#28383d] border border-[#d9dacf] rounded-sm hover:bg-[#e8eddf] hover:border-[#81947a] transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#365748]",
        ),
    )


def alphabet_index() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.icon("list-filter", class_name="h-4 w-4"),
                rx.el.h2("Browse by initial", class_name="text-sm font-medium"),
                class_name="flex gap-2 items-center",
            ),
            rx.el.button(
                "All usernames",
                rx.icon("arrow-up-right", class_name="h-3 w-3"),
                on_click=DirectoryState.select_initial("All"),
                aria_pressed=DirectoryState.initial == "All",
                class_name=rx.cond(
                    DirectoryState.initial == "All",
                    "flex items-center gap-2 rounded-sm bg-[#365748] text-white px-4 py-2 text-xs",
                    "flex items-center gap-2 rounded-sm border border-[#bcc4b5] hover:bg-[#e9ecdf] text-[#365748] px-4 py-2 text-xs",
                ),
            ),
            class_name="flex items-center justify-between mb-5 gap-3",
        ),
        rx.el.div(
            rx.foreach(DirectoryState.letters, letter_cell),
            class_name="grid grid-cols-4 sm:grid-cols-7 lg:grid-cols-13 gap-2",
        ),
        rx.el.div(
            rx.el.span("26 LETTERS. ENDLESS POSSIBILITIES."),
            rx.el.span(
                "Select a letter to narrow your search.",
                class_name="normal-case tracking-normal",
            ),
            class_name="flex flex-wrap gap-2 justify-between mt-4 text-[10px] tracking-[0.13em] text-[#777e70]",
        ),
        class_name="border-t border-[#c8cdbf] pt-6 pb-8",
    )


def metric(value: rx.Var, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            rx.cond(DirectoryState.loading, "—", value),
            class_name="font-['Libre_Baskerville'] text-3xl",
        ),
        rx.el.span(label, class_name="text-xs text-[#71796d]"),
        class_name="flex flex-col sm:flex-row sm:items-baseline gap-2 sm:gap-3",
    )


def result_row(row: dict[str, str]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.span("@", class_name="text-[#8d9786] text-sm"),
                rx.el.span(row["username"], class_name="font-medium"),
                class_name="flex items-center gap-3",
            ),
            class_name="py-4 px-4 sm:px-6",
        ),
        rx.el.td(
            rx.el.span(
                row["initial"],
                class_name="inline-flex justify-center items-center w-7 h-7 bg-[#edf0e5] border border-[#dce1d3] rounded-sm text-xs text-[#476044]",
            ),
            class_name="py-4 px-3",
        ),
        rx.el.td(
            f"No. {row['number']}",
            class_name="py-4 px-4 sm:px-6 text-right font-mono text-xs text-[#7b8177]",
        ),
        key=row["number"],
        class_name="border-b border-[#e4e5da] odd:bg-[#fffef9] even:bg-[#fafaf4] hover:bg-[#eef1e6] transition-colors text-sm",
    )


def results() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            metric(DirectoryState.total, "usernames in the collection"),
            metric(DirectoryState.indexed, "initials indexed"),
            metric(DirectoryState.result_count, "matching your search"),
            class_name="grid grid-cols-3 gap-5 py-7 border-y border-[#c8cdbf] mb-10",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    rx.cond(
                        DirectoryState.initial == "All",
                        "The collection",
                        f"Filed under {DirectoryState.initial}",
                    ),
                    class_name="font-['Libre_Baskerville'] text-2xl tracking-tight",
                ),
                rx.el.p(
                    rx.cond(
                        DirectoryState.loading,
                        "Consulting the catalogue…",
                        f"Showing {DirectoryState.result_count} of {DirectoryState.total} usernames",
                    ),
                    class_name="text-xs text-[#777e70] mt-2",
                    aria_live="polite",
                ),
            ),
            rx.el.div(
                rx.cond(
                    DirectoryState.filtered,
                    rx.el.button(
                        rx.icon("rotate-ccw", class_name="h-3 w-3"),
                        "Reset filters",
                        on_click=DirectoryState.clear_filters,
                        class_name="flex items-center gap-2 text-xs text-[#365748] hover:underline py-2",
                    ),
                ),
                rx.el.span(
                    rx.icon("arrow-down-a-z", class_name="h-4 w-4"),
                    "Alphabetical",
                    class_name="flex gap-2 items-center text-xs text-[#777e70]",
                ),
                class_name="flex flex-col sm:flex-row gap-3 sm:gap-6 items-end sm:items-center",
            ),
            class_name="flex justify-between items-center gap-4 mb-6",
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
                                                "at-sign", class_name="w-3 h-3"
                                            ),
                                            "USERNAME",
                                            class_name="flex items-center gap-2",
                                        ),
                                        class_name="px-4 sm:px-6 py-3 font-medium",
                                    ),
                                    rx.el.th(
                                        rx.el.span(
                                            rx.icon(
                                                "case-upper",
                                                class_name="w-3 h-3",
                                            ),
                                            "INITIAL",
                                            class_name="flex items-center gap-2",
                                        ),
                                        class_name="px-3 py-3 font-medium",
                                    ),
                                    rx.el.th(
                                        rx.el.span(
                                            rx.icon(
                                                "hash", class_name="w-3 h-3"
                                            ),
                                            "RECORD",
                                            class_name="flex justify-end items-center gap-2",
                                        ),
                                        class_name="px-4 sm:px-6 py-3 font-medium",
                                    ),
                                    class_name="text-left text-[10px] tracking-widest text-[#737d6d] bg-[#eeefe5] border-b border-[#d9dacf]",
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(DirectoryState.rows, result_row)
                            ),
                            class_name="table-auto w-full",
                        ),
                        class_name="overflow-hidden border border-[#d9dacf] rounded-sm",
                    ),
                ),
            ),
        ),
        class_name="pb-12",
    )


def directory() -> rx.Component:
    return rx.el.div(
        brand_bar(),
        rx.el.main(
            hero(),
            alphabet_index(),
            results(),
            class_name="w-full max-w-7xl mx-auto px-6 lg:px-12",
        ),
        rx.el.footer(
            rx.el.span(
                "The Username Index", class_name="font-['Libre_Baskerville']"
            ),
            rx.el.span("A–Z, and everything in between.", class_name="text-xs"),
            class_name="max-w-7xl mx-auto px-6 lg:px-12 py-7 border-t border-[#d6d5c9] flex flex-wrap gap-4 items-center justify-between text-[#777e70]",
        ),
        class_name="min-h-screen bg-[#f5f4ec] text-[#23323a] font-['Inter']",
    )
