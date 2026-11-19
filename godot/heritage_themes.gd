@tool
extends EditorPlugin
## Heritage Themes for the Godot editor. Project > Tools > Heritage Themes... applies a theme
## to the editor: it copies the text editor themes into the editor's text_editor_themes folder,
## selects the theme's one for the script editor, and sets the base colour, accent colour and
## contrast that Godot draws the rest of the editor from. The settings are the editor's own, so
## the theme stays when the plugin is disabled or removed.

const MENU_ITEM := "Heritage Themes..."
const THEMES := "themes.cfg"
const INTERFACE := "interface/theme/"
const COLOR_THEME := "text_editor/theme/color_theme"
# Godot's own text editor themes, which a .tet file cannot replace.
const BUILT_IN_THEMES: PackedStringArray = ["Default", "Godot 2", "Custom"]
const RESTORE_ACTION := "restore"

var _themes := ConfigFile.new()
var _menu_added := false
var _dialog: ConfirmationDialog
var _list: ItemList


func _enter_tree() -> void:
	var error := _themes.load(_folder().path_join(THEMES))
	if error != OK:
		push_error("Heritage Themes: cannot read %s: %s" % [THEMES, error_string(error)])
		return
	add_tool_menu_item(MENU_ITEM, _open)
	_menu_added = true


func _exit_tree() -> void:
	if _menu_added:
		remove_tool_menu_item(MENU_ITEM)
		_menu_added = false
	if _dialog:
		_dialog.queue_free()
		_dialog = null


func _folder() -> String:
	return (get_script() as Script).resource_path.get_base_dir()


func _open() -> void:
	if not _dialog:
		_dialog = _create_dialog()
		EditorInterface.get_base_control().add_child(_dialog)
	var current: String = EditorInterface.get_editor_settings().get_setting(COLOR_THEME)
	_list.deselect_all()
	for index in _list.item_count:
		if _list.get_item_text(index) == current:
			_list.select(index)
			_list.ensure_current_is_visible()
	_dialog.get_ok_button().disabled = not _list.is_anything_selected()
	_dialog.popup_centered()


func _create_dialog() -> ConfirmationDialog:
	var dialog := ConfirmationDialog.new()
	dialog.title = "Heritage Themes"
	dialog.ok_button_text = "Apply"
	dialog.min_size = Vector2i(Vector2(440, 520) * EditorInterface.get_editor_scale())
	dialog.add_button("Restore Godot's Theme", true, RESTORE_ACTION)
	dialog.confirmed.connect(_apply_selected)
	dialog.custom_action.connect(_on_custom_action)

	var box := VBoxContainer.new()
	var label := Label.new()
	label.text = "Choose a theme for the editor and the script editor."
	box.add_child(label)
	_list = ItemList.new()
	_list.size_flags_vertical = Control.SIZE_EXPAND_FILL
	for theme_name in _themes.get_sections():
		_list.add_item(theme_name)
	_list.item_selected.connect(func(_index: int) -> void:
		dialog.get_ok_button().disabled = false)
	_list.item_activated.connect(func(_index: int) -> void:
		dialog.hide()
		_apply_selected())
	box.add_child(_list)
	dialog.add_child(box)
	return dialog


func _on_custom_action(action: StringName) -> void:
	if action == RESTORE_ACTION:
		_dialog.hide()
		_restore()


func _apply_selected() -> void:
	var selected := _list.get_selected_items()
	if not selected.is_empty():
		_apply(_list.get_item_text(selected[0]))


func _apply(theme_name: String) -> void:
	var folder := EditorInterface.get_editor_paths().get_config_dir().path_join(
			"text_editor_themes")
	var error := DirAccess.make_dir_recursive_absolute(folder)
	if error != OK:
		push_error("Heritage Themes: cannot create %s: %s" % [folder, error_string(error)])
		return
	for section in _themes.get_sections():
		var file := section + ".tet"
		var source := _folder().path_join("themes").path_join(file)
		error = DirAccess.copy_absolute(source, folder.path_join(file))
		if error != OK:
			push_error("Heritage Themes: cannot copy %s to %s: %s"
					% [file, folder, error_string(error)])
			return
	var settings := EditorInterface.get_editor_settings()
	_list_text_editor_themes(settings, folder)
	settings.set_setting(INTERFACE + "follow_system_theme", false)
	settings.set_setting(INTERFACE + "use_system_accent_color", false)
	settings.set_setting(INTERFACE + "color_preset", "Custom")
	for key in ["base_color", "accent_color"]:
		settings.set_setting(INTERFACE + key, Color.html(_themes.get_value(theme_name, key)))
	for key in ["contrast", "icon_and_font_color"]:
		settings.set_setting(INTERFACE + key, _themes.get_value(theme_name, key))
	settings.set_setting(COLOR_THEME, theme_name)


# Lists the .tet files of folder in the choices of text_editor/theme/color_theme, as Godot does
# when it starts, so that Editor Settings shows the theme by name.
func _list_text_editor_themes(settings: EditorSettings, folder: String) -> void:
	var names := PackedStringArray()
	for file in DirAccess.get_files_at(folder):
		var theme_name := file.get_basename()
		if file.get_extension() == "tet" and not _is_built_in(theme_name):
			names.append(theme_name)
	names.sort()
	settings.add_property_info({
		"name": COLOR_THEME,
		"type": TYPE_STRING,
		"hint": PROPERTY_HINT_ENUM,
		"hint_string": ",".join(BUILT_IN_THEMES + names),
	})


# Godot compares the names of its own themes without case.
func _is_built_in(theme_name: String) -> bool:
	for built_in in BUILT_IN_THEMES:
		if built_in.nocasecmp_to(theme_name) == 0:
			return true
	return false


func _restore() -> void:
	var settings := EditorInterface.get_editor_settings()
	settings.set_setting(INTERFACE + "color_preset", "Default")
	settings.set_setting(INTERFACE + "icon_and_font_color", 0)
	settings.set_setting(COLOR_THEME, "Default")
