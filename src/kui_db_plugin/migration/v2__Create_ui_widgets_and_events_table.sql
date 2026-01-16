
-- Add UI Widgets table.
CREATE TABLE IF NOT EXISTS ui_widgets (
    id                  VARCHAR NOT NULL,
    parent              VARCHAR,
    section             VARCHAR,
    type                VARCHAR NOT NULL,
    layout              VARCHAR,
    content             VARCHAR,
    tooltip             VARCHAR,
    controller          VARCHAR,
    args                TEXT,
    grid_columns        INTEGER,
    style_id            VARCHAR,
    alignment           VARCHAR,
    spacing             INTEGER,
    width               INTEGER,
    height              INTEGER,
    margin_left         INTEGER,
    margin_top          INTEGER,
    margin_right        INTEGER,
    margin_bottom       INTEGER,
    order_id            INTEGER,
    stylesheet          TEXT,

    PRIMARY KEY (id, section),
    FOREIGN KEY (section) REFERENCES ui_sections(section_id) ON DELETE CASCADE
);

-- Create table to store refresh events that should trigger refresh of widget.
CREATE TABLE IF NOT EXISTS ui_widget_events (
    widget_id           VARCHAR NOT NULL,
    section_id          VARCHAR,
    refresh_event_id    VARCHAR NOT NULL,
    refresh_children    INTEGER DEFAULT 0,

    PRIMARY KEY (widget_id, section_id, refresh_event_id),
    FOREIGN KEY (widget_id, section_id) REFERENCES ui_widgets(id, section) ON DELETE CASCADE
);
