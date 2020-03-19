from qgis.core import QgsProject

from csv_tools.file import filename_to_uri, read_csv_file
from csv_tools.filter import filter_id_date
from data_processing.heatmap_plugin import create_heatmap
from data_processing.lines import create_line_geometry, create_line_layer
from layer_stuff.basic import create_vector_layer_from_csv, add_layer_to_project
from layer_stuff.csv_layer_filtering import create_id_and_direction_filter, create_id_and_time_bracket_filter, \
    create_uri_filter_end
from layer_stuff.memory_layer_persistence import persistify_vector_layer

call_layer_filename = "/home/arne/Documents/git-repos/ubiquitous-systems/generated/cdr-converted/calls.csv"
call_layer_uri = filename_to_uri(call_layer_filename)
persistency_folder = "/home/arne/Documents/git-repos/ubiquitous-systems/generated/"


def __load_cell_tower_layer():
    cell_tower_uri = filename_to_uri(
        "/home/arne/Documents/git-repos/ubiquitous-systems/assets/cdr/cell_towers_porto.csv")
    cell_tower_layer = create_vector_layer_from_csv(cell_tower_uri, "Porto Cell Tower")
    add_layer_to_project(cell_tower_layer)


def __load_incoming_call_layer(user_id: str):
    uri_filter = create_id_and_direction_filter(user_id, "incoming")
    incoming_calls_layer = create_vector_layer_from_csv(call_layer_uri, "Calls to " + user_id, uri_filter)
    add_layer_to_project(incoming_calls_layer)


def __load_outgoing_call_layer(user_id: str):
    uri_filter = create_id_and_direction_filter(user_id, "outgoing")
    outgoing_calls_layer = create_vector_layer_from_csv(call_layer_uri, "Calls from " + user_id, uri_filter)
    add_layer_to_project(outgoing_calls_layer)


def __show_movement(user_id: str, date: str):
    csv_data = read_csv_file(call_layer_filename, delimiter=",")
    csv_data = filter_id_date(csv_data, user_id, date)
    geometry = create_line_geometry(csv_data)
    memory_line_layer = create_line_layer(geometry, "{} movement on {}".format(user_id, date))
    persistent_line_layer = persistify_vector_layer(persistency_folder, memory_line_layer)
    add_layer_to_project(persistent_line_layer)


def __show_heatmap(user_id: str, time_bracket: str):
    id_tb_filter = create_id_and_time_bracket_filter(user_id, time_bracket)
    temp_layer_name = "heatmap tmp layer {} {}".format(user_id, time_bracket)
    temp_layer = create_vector_layer_from_csv(call_layer_uri, temp_layer_name, id_tb_filter)

    heatmap_layer_name = "{} heatmap for {}".format(time_bracket.capitalize(), user_id)
    heatmap_layer = create_heatmap(temp_layer, persistency_folder, heatmap_layer_name)
    add_layer_to_project(heatmap_layer)


def execute(user_id: str, date: str):
    __load_cell_tower_layer()
    __load_incoming_call_layer(user_id)
    __load_outgoing_call_layer(user_id)
    __show_movement(user_id, date)

    time_brackets = ["morning", "midday", "night"]
    for time_bracket in time_brackets:
        __show_heatmap(user_id, time_bracket)
