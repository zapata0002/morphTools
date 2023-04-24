import maya.cmds as cmds
from functools import partial


class RenamerWindow:
    def __init__(self):
        self.name = 'renamer_zapata_v01'
        self.window_width = 320
        self.window_height = 355
        # If the window already exists, delete and create a new one
        if cmds.window(self.name, exists=True):
            cmds.deleteUI(self.name)
        cmds.window(self.name, sizeable=False)
        # Window title based on window name
        window_title = '{} {} {}'.format(self.name.split('_')[0].capitalize(), self.name.split('_')[1].capitalize(),
                                         self.name.split('_')[2])
        cmds.window(self.name, edit=True, width=self.window_width, height=self.window_height, title=window_title)
        main_column = cmds.columnLayout('main_column', width=self.window_width, height=self.window_height)
        # Search and replace layout
        cmds.separator(width=315, height=10, style='in')
        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 260)])
        cmds.text(label='Search: ', align='right')
        search_field = cmds.textField()
        cmds.setParent(main_column)
        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 260)])
        cmds.text(label='Replace: ', align='right')
        replace_field = cmds.textField()
        cmds.setParent(main_column)
        cmds.separator(width=325, height=8, style='none')
        cmds.button(label='Search And Replace', width=325, command=partial(search_and_replace, search_field,
                                                                           replace_field))
        # Prefix Layout
        cmds.separator(width=315, height=10, style='in')
        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 260)])
        cmds.text(label='Prefix: ', align='right')
        prefix_field = cmds.textField()
        cmds.setParent(main_column)
        cmds.separator(width=325, height=8, style='none')
        cmds.button(label='Add Prefix', width=325, command=partial(add_prefix, prefix_field))
        # Suffix Layout
        cmds.separator(width=315, height=10, style='in')
        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 260)])
        cmds.text(label='Suffix: ', align='right')
        suffix_field = cmds.textField()
        cmds.setParent(main_column)
        cmds.separator(width=325, height=8, style='none')
        cmds.button(label='Add Suffix', width=325, command=partial(add_suffix, suffix_field))
        # Rename And Number Layout
        cmds.separator(width=315, height=10, style='in')
        cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 50), (2, 170), (3, 8), (4, 50), (5, 30)],
                             rowSpacing=[(1, 5), (2, 5), (3, 5), (4, 5), (5, 5)])
        cmds.text(label='Rename: ', align='right')
        rename_field = cmds.textField()
        cmds.separator(style='none')
        cmds.text(label='Start #: ', align='right')
        start_number_field = cmds.intField(value=1, width=60, minValue=0)
        cmds.text(label='Prefix: ', align='right')
        rename_prefix_field = cmds.textField()
        cmds.separator(style='none')
        cmds.text(label='Padding: ', align='right')
        padding_field = cmds.intField(value=2, width=60, minValue=0)
        cmds.text(label='Suffix: ', align='right')
        rename_suffix_field = cmds.textField()
        cmds.setParent(main_column)
        cmds.separator(width=315, height=5, style='none')
        cmds.button(label='Rename And Number', width=315, align='center', command=partial(rename_and_number,
                                                                                          rename_field,
                                                                                          start_number_field,
                                                                                          padding_field,
                                                                                          rename_prefix_field,
                                                                                          rename_suffix_field))
        cmds.setParent(main_column)
        cmds.separator(width=315, height=5, style='none')
        cmds.button(label='Clear', width=315, align='center', command=partial(clear_text_filed, search_field,
                                                                              replace_field, prefix_field, suffix_field,
                                                                              rename_field, start_number_field,
                                                                              padding_field, rename_prefix_field,
                                                                              rename_suffix_field))
        cmds.separator(width=315, height=10, style='in')
        cmds.showWindow()


def search_and_replace(search_field, replace_field):
    cmds.undoInfo(openChunk=True)
    search_field = cmds.textField(search_field, query=True, text=True)
    replace_field = cmds.textField(replace_field, query=True, text=True)
    selected_list = cmds.ls(sl=True)
    if len(selected_list) == 0:
        cmds.warning("Select the node to replace")
    elif search_field == "":
        cmds.warning("Search entry field is empty")
    else:
        for sel in reversed(selected_list):
            split_name = sel.split('|')
            search_name_node = split_name[-1].replace(search_field, replace_field)
            cmds.rename(sel, search_name_node)
    cmds.undoInfo(closeChunk=True)


def add_prefix(prefix_field):
    cmds.undoInfo(openChunk=True)
    prefix_field = cmds.textField(prefix_field, query=True, text=True)
    selected_list = cmds.ls(sl=True)
    if len(selected_list) == 0:
        cmds.warning("Select the node to add prefix")
    elif prefix_field == "":
        cmds.warning("Prefix entry field is empty")
    else:
        for sel in reversed(selected_list):
            split_name = sel.split('|')
            cmds.rename(sel, '{}{}'.format(prefix_field, split_name[-1]))
    cmds.undoInfo(closeChunk=True)


def add_suffix(suffix_field):
    cmds.undoInfo(openChunk=True)
    suffix_field = cmds.textField(suffix_field, query=True, text=True)
    selected_list = cmds.ls(sl=True)
    if len(selected_list) == 0:
        cmds.warning("Select the node to add suffix")
    elif suffix_field == "":
        cmds.warning("Suffix entry field is empty")
    else:
        for sel in reversed(selected_list):
            split_name = sel.split('|')
            cmds.rename(sel, '{}{}'.format(split_name[-1], suffix_field))
    cmds.undoInfo(closeChunk=True)


def rename_and_number(rename_field, start_number_field, padding_field, rename_prefix_field, rename_suffix_field):
    cmds.undoInfo(openChunk=True)
    rename_field = cmds.textField(rename_field, query=True, text=True)
    start_number_field = cmds.intField(start_number_field, query=True, value=True)
    padding_field = cmds.intField(padding_field, query=True, value=True)
    rename_prefix_field = cmds.textField(rename_prefix_field, query=True, text=True)
    rename_suffix_field = cmds.textField(rename_suffix_field, query=True, text=True)
    selected_list = cmds.ls(sl=True)
    if len(selected_list) == 0:
        cmds.warning("Select the node to rename")
    elif rename_field == "":
        cmds.warning("Rename entry field is empty")
    else:
        start_number = int(start_number_field)
        padding_int = int(padding_field)
        end_number = len(selected_list) + start_number - 1
        zero_padding = ''
        for sel in reversed(selected_list):
            end_number_len = len(str(end_number))
            if padding_int > end_number_len:
                zero_padding = '0' * (padding_int - end_number_len)
            rename_name = cmds.rename(sel, '{}{}{}'.format(rename_field, zero_padding, str(end_number)))
            end_number -= 1
            if rename_suffix_field:
                rename_name = cmds.rename(rename_name, '{}{}'.format(rename_name, rename_suffix_field))
                if rename_prefix_field:
                    cmds.rename(rename_name, '{}{}'.format(rename_prefix_field, rename_name))
            else:
                if rename_prefix_field:
                    cmds.rename(rename_name, '{}{}'.format(rename_prefix_field, rename_name))
        cmds.undoInfo(closeChunk=True)


def clear_text_filed(search_field, replace_field,
                     prefix_field, suffix_field,
                     rename_field, start_number_field, padding_field, rename_prefix_field, rename_suffix_field):
    cmds.textField(search_field, edit=True, text='')
    cmds.textField(replace_field, edit=True, text='')
    cmds.textField(prefix_field, edit=True, text='')
    cmds.textField(suffix_field, edit=True, text='')
    cmds.textField(rename_field, edit=True, text='')
    cmds.intField(start_number_field, edit=True, value=1)
    cmds.intField(padding_field, edit=True, value=2)
    cmds.textField(rename_prefix_field, edit=True, text='')
    cmds.textField(rename_suffix_field, edit=True, text='')
