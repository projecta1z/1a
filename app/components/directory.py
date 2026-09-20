import reflex as rx

from app.states.directory import DirectoryState


def brand_bar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.icon("book-open", class_name="h-5 w-5 text-[#526651]"),
                rx.el.span(
                    "The Username Index",
                    class_name="font-['Libre_Baskerville'] text-base sm:text-lg",
                ),
                href="/",
                class_name="flex items-center gap-3 text-[#202f37]",
            ),
            rx.el.span(
                "AN ALPHABETICAL COLLECTION",
                class_name="hidden sm:block text-[10px] tracking-[0.2em] text-[#73796f]",
            ),
            class_name="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-7 lg:px-12",
        ),
        class_name="border-b border-[#d9dacf]",
    )


def hero() -> rx.Component:
    return rx.el.section(
        rx.el.p(
            "A PLACE FOR EVERY NAME",
            class_name="mb-6 text-[10px] tracking-[0.22em] text-[#526651]",
        ),
        rx.el.h1(
            "The Username",
            rx.el.br(),
            rx.el.em("Index.", class_name="font-normal text-[#526651]"),
            class_name="font-['Libre_Baskerville'] text-5xl leading-[1.18] tracking-tight sm:text-7xl text-[#202f37]",
        ),
        rx.el.p(
            "An alphabetical collection of usernames. Find a name, or take your time and browse the A–Z index.",
            class_name="mt-6 max-w-lg text-sm sm:text-base leading-7 text-[#73796f]",
        ),
        rx.el.div(
            rx.icon("search", class_name="h-5 w-5 shrink-0 text-[#526651]"),
            rx.el.input(
                placeholder="Find a username…",
                aria_label="Find a username",
                default_value=DirectoryState.search,
                on_change=DirectoryState.search_changed.debounce(500),
                class_name="w-full min-w-0 bg-transparent text-base text-[#202f37] outline-hidden placeholder:text-[#91958b] py-5",
            ),
            rx.cond(
                DirectoryState.search != "",
                rx.el.button(
                    rx.icon("x", class_name="h-4 w-4"),
                    aria_label="Clear search and filters",
                    on_click=DirectoryState.clear_filters,
                    class_name="p-2 text-[#526651] hover:bg-[#eeeee4] focus-visible:outline-2",
                ),
            ),
            class_name="mt-9 flex max-w-xl items-center gap-4 border-b border-[#87917e] focus-within:border-[#365748]",
        ),
        class_name="pt-14 pb-12 sm:pt-20 sm:pb-16",
    )


def letter_cell(letter: str) -> rx.Component:
    return rx.el.button(
        letter,
        on_click=DirectoryState.select_initial(letter),
        aria_label=f"Browse {letter}",
        aria_pressed=DirectoryState.initial == letter,
        class_name=rx.cond(
            DirectoryState.initial == letter,
            "flex h-12 min-w-10 items-center justify-center border border-[#365748] bg-[#365748] text-[#faf9f3] font-['Libre_Baskerville'] text-sm transition-colors focus-visible:outline-2 focus-visible:outline-offset-2",
            "flex h-12 min-w-10 items-center justify-center border border-[#d9dacf] bg-[#faf9f2] text-[#526651] font-['Libre_Baskerville'] text-sm hover:bg-[#eeeee4] hover:border-[#87917e] transition-colors focus-visible:outline-2 focus-visible:outline-offset-2",
        ),
    )


def alphabet_index() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Browse the index",
                class_name="text-[10px] uppercase tracking-[0.18em] text-[#73796f]",
            ),
            rx.el.span(
                "A — Z",
                class_name="text-[10px] tracking-[0.18em] text-[#73796f]",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.div(
            letter_cell("All"),
            rx.foreach(DirectoryState.letters, letter_cell),
            class_name="grid grid-cols-7 sm:grid-cols-9 lg:grid-cols-[repeat(27,minmax(0,1fr))] gap-1",
        ),
        aria_label="Alphabetical index",
        class_name="border-b border-[#d9dacf] pb-8",
    )


def metric(value: rx.Var, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            value,
            class_name="font-['Libre_Baskerville'] text-2xl text-[#202f37]",
        ),
        rx.el.span(label, class_name="text-xs text-[#73796f]"),
        class_name="flex items-baseline gap-3",
    )


def result_row(row: dict[str, str]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            row["number"],
            class_name="w-24 px-5 sm:px-7 py-5 text-xs tabular-nums text-[#8a8f80]",
        ),
        rx.el.td(
            rx.el.span(
                row["initial"],
                class_name="flex h-8 w-8 items-center justify-center bg-[#eeeee4] text-[#526651] font-['Libre_Baskerville'] text-sm",
            ),
            class_name="w-28 px-5 py-5",
        ),
        rx.el.td(
            row["username"],
            class_name="px-5 sm:px-7 py-5 font-['Libre_Baskerville'] text-lg text-[#202f37]",
        ),
        key=row["number"],
        class_name="border-t border-[#d9dacf] even:bg-[#f5f4ed] hover:bg-[#eeeee4] transition-colors",
    )


def table_heading(icon: str, label: str) -> rx.Component:
    return rx.el.th(
        rx.el.span(
            rx.icon(icon, class_name="h-3 w-3"),
            label,
            class_name="flex items-center gap-2",
        ),
        scope="col",
        class_name="px-5 sm:px-7 py-4 font-medium",
    )


def results_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    table_heading("hash", "No."),
                    table_heading("a-large-small", "Initial"),
                    table_heading("at-sign", "Username"),
                    class_name="text-left text-[10px] uppercase tracking-[0.15em] text-[#73796f] bg-[#f0f0e7]",
                )
            ),
            rx.el.tbody(rx.foreach(DirectoryState.rows, result_row)),
            aria_label="Username collection",
            class_name="table-auto w-full",
        ),
        class_name="overflow-hidden border border-[#d9dacf] bg-[#faf9f2]",
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
                        class_name="flex items-center gap-2 text-xs text-[#365748] underline underline-offset-4 hover:text-[#202f37]",
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
                class_name="font-['Libre_Baskerville'] text-2xl text-[#202f37]",
            ),
            rx.el.span(
                rx.cond(
                    DirectoryState.loading,
                    "Loading…",
                    f"{DirectoryState.result_count} names",
                ),
                class_name="text-xs text-[#73796f]",
            ),
            class_name="flex items-center justify-between gap-4 mb-5 mt-5",
        ),
        rx.match(
            DirectoryState.display_state,
            (
                "loading",
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
            ),
            (
                "error",
                rx.el.div(
                    rx.icon("circle-alert", class_name="h-6 w-6 text-red-500"),
                    rx.el.p(DirectoryState.error),
                    rx.el.button(
                        "Try again",
                        on_click=DirectoryState.load,
                        class_name="text-[#365748] underline py-2",
                    ),
                    class_name="flex flex-col items-center gap-3 py-14 text-sm text-[#202f37]",
                    role="alert",
                ),
            ),
            (
                "empty",
                rx.el.div(
                    rx.icon("search-x", class_name="h-8 w-8 text-[#73856a]"),
                    rx.el.h3(
                        "No names on this shelf.",
                        class_name="font-['Libre_Baskerville'] text-xl text-[#202f37]",
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
                    class_name="flex flex-col items-center gap-3 py-16 px-4 text-center bg-[#faf9f2] border border-[#d9dacf]",
                ),
            ),
            results_table(),
        ),
        class_name="pb-16",
        aria_live="polite",
        aria_busy=DirectoryState.loading,
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
