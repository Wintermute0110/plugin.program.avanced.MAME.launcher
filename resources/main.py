# -*- coding: utf-8 -*-
#
# Advanced MAME Launcher main script file
#

# Copyright (c) 2016-2017 Wintermute0110 <wintermute0110@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# --- Python standard library ---
from __future__ import unicode_literals
import os
import urlparse
import subprocess

# --- Kodi stuff ---
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

# --- Modules/packages in this plugin ---
from utils import *
from utils_kodi import *
from disk_IO import *

# --- Addon object (used to access settings) ---
__addon_obj__     = xbmcaddon.Addon()
__addon_id__      = __addon_obj__.getAddonInfo('id').decode('utf-8')
__addon_name__    = __addon_obj__.getAddonInfo('name').decode('utf-8')
__addon_version__ = __addon_obj__.getAddonInfo('version').decode('utf-8')
__addon_author__  = __addon_obj__.getAddonInfo('author').decode('utf-8')
__addon_profile__ = __addon_obj__.getAddonInfo('profile').decode('utf-8')
__addon_type__    = __addon_obj__.getAddonInfo('type').decode('utf-8')

# --- Addon paths and constant definition ---
# _PATH is a filename | _DIR is a directory
ADDONS_DATA_DIR = FileName('special://profile/addon_data')
PLUGIN_DATA_DIR = ADDONS_DATA_DIR.pjoin(__addon_id__)
BASE_DIR        = FileName('special://profile')
HOME_DIR        = FileName('special://home')
KODI_FAV_PATH   = FileName('special://profile/favourites.xml')
ADDONS_DIR      = HOME_DIR.pjoin('addons')
AML_ADDON_DIR   = ADDONS_DIR.pjoin(__addon_id__)
ICON_IMG_PATH   = AML_ADDON_DIR.pjoin('icon.png')
FANART_IMG_PATH = AML_ADDON_DIR.pjoin('fanart.jpg')

LOCATION_STANDARD  = 'STANDARD'
LOCATION_MAME_FAVS = 'MAME_FAVS'
LOCATION_SL_FAVS   = 'MAME_FAVS'

# --- Plugin database indices ---
class AML_Paths:
    def __init__(self):
        # >> MAME XML, main database and main PClone list
        self.MAME_XML_PATH               = PLUGIN_DATA_DIR.pjoin('MAME.xml')
        self.MAME_STDOUT_PATH            = PLUGIN_DATA_DIR.pjoin('MAME_stdout.log')
        self.MAME_STDERR_PATH            = PLUGIN_DATA_DIR.pjoin('MAME_stderr.log')
        self.MAME_OUTPUT_PATH            = PLUGIN_DATA_DIR.pjoin('MAME_output.log')
        self.MAIN_DB_PATH                = PLUGIN_DATA_DIR.pjoin('MAME_main_db.json')
        self.MAIN_PCLONE_DIC_PATH        = PLUGIN_DATA_DIR.pjoin('MAME_pclone_dic.json')
        self.MAIN_CONTROL_PATH           = PLUGIN_DATA_DIR.pjoin('MAME_control_dic.json')
        self.MAIN_ASSETS_DB_PATH         = PLUGIN_DATA_DIR.pjoin('MAME_assets_db.json')
        self.MAIN_PROPERTIES_PATH        = PLUGIN_DATA_DIR.pjoin('MAME_properties.json')

        # >> Catalogs
        self.CATALOG_NONE_PARENT_PATH    = PLUGIN_DATA_DIR.pjoin('catalog_none_parents.json')
        self.CATALOG_NONE_ALL_PATH       = PLUGIN_DATA_DIR.pjoin('catalog_none_all.json')
        self.CATALOG_CATVER_PARENT_PATH  = PLUGIN_DATA_DIR.pjoin('catalog_catver_parents.json')
        self.CATALOG_CATVER_ALL_PATH     = PLUGIN_DATA_DIR.pjoin('catalog_catver_all.json')

        self.CATALOG_CATLIST_PATH        = PLUGIN_DATA_DIR.pjoin('catalog_catlist.json')
        self.CATALOG_GENRE_PATH          = PLUGIN_DATA_DIR.pjoin('catalog_genre.json')
        self.CATALOG_NPLAYERS_PATH       = PLUGIN_DATA_DIR.pjoin('catalog_nplayers.json')
        self.CATALOG_MANUFACTURER_PATH   = PLUGIN_DATA_DIR.pjoin('catalog_manufacturer.json')
        self.CATALOG_YEAR_PATH           = PLUGIN_DATA_DIR.pjoin('catalog_year.json')
        self.CATALOG_DRIVER_PATH         = PLUGIN_DATA_DIR.pjoin('catalog_driver.json')
        self.CATALOG_CONTROL_PATH        = PLUGIN_DATA_DIR.pjoin('catalog_control.json')
        self.CATALOG_DISPLAY_TAG_PATH    = PLUGIN_DATA_DIR.pjoin('catalog_display_tag.json')
        self.CATALOG_DISPLAY_TYPE_PATH   = PLUGIN_DATA_DIR.pjoin('catalog_display_type.json')
        self.CATALOG_DISPLAY_ROTATE_PATH = PLUGIN_DATA_DIR.pjoin('catalog_display_rotate.json')
        self.CATALOG_DEVICE_LIST_PATH    = PLUGIN_DATA_DIR.pjoin('catalog_device_list.json')
        self.CATALOG_SL_PATH             = PLUGIN_DATA_DIR.pjoin('catalog_SL.json')

        # >> Software Lists
        self.SL_DB_DIR                   = PLUGIN_DATA_DIR.pjoin('db_SoftwareLists')
        self.SL_INDEX_PATH               = PLUGIN_DATA_DIR.pjoin('SoftwareLists_index.json')
        self.SL_MACHINES_PATH            = PLUGIN_DATA_DIR.pjoin('SoftwareLists_machines.json')
        self.SL_PCLONE_DIC_PATH          = PLUGIN_DATA_DIR.pjoin('SoftwareLists_pclone_dic.json')
        self.SL_MACHINES_PROP_PATH       = PLUGIN_DATA_DIR.pjoin('SoftwareLists_properties.json')

        # >> Favourites
        self.FAV_MACHINES_PATH           = PLUGIN_DATA_DIR.pjoin('Favourite_Machines.json')
        self.FAV_SL_ROMS_PATH            = PLUGIN_DATA_DIR.pjoin('Favourite_SL_ROMs.json')

        # >> Reports
        self.REPORT_MAME_SCAN_ROMS_PATH  = PLUGIN_DATA_DIR.pjoin('Report_ROM_scanner.txt')
        self.REPORT_MAME_SCAN_CHDS_PATH  = PLUGIN_DATA_DIR.pjoin('Report_CHD_scanner.txt')
        self.REPORT_MAME_SCAN_SAMP_PATH  = PLUGIN_DATA_DIR.pjoin('Report_Samples_scanner.txt')
        self.REPORT_SL_SCAN_ROMS_PATH    = PLUGIN_DATA_DIR.pjoin('Report_SL_ROM_scanner.txt')
        self.REPORT_SL_SCAN_CHDS_PATH    = PLUGIN_DATA_DIR.pjoin('Report_SL_CHD_scanner.txt')
PATHS = AML_Paths()

class Main:
    # --- Object variables ---
    settings = {}

    # ---------------------------------------------------------------------------------------------
    # This is the plugin entry point.
    # ---------------------------------------------------------------------------------------------
    def run_plugin(self):
        # --- Initialise log system ---
        # >> Force DEBUG log level for development.
        # >> Place it before setting loading so settings can be dumped during debugging.
        set_log_level(LOG_DEBUG)

        # --- Fill in settings dictionary using addon_obj.getSetting() ---
        self._get_settings()
        # set_log_level(self.settings['log_level'])

        # --- Some debug stuff for development ---
        log_debug('---------- Called AML Main::run_plugin() constructor ----------')
        log_debug('sys.platform   {0}'.format(sys.platform))
        log_debug('Python version ' + sys.version.replace('\n', ''))
        log_debug('__addon_version__ {0}'.format(__addon_version__))
        for i in range(len(sys.argv)): log_debug('sys.argv[{0}] = "{1}"'.format(i, sys.argv[i]))

        # --- Addon data paths creation ---
        if not PLUGIN_DATA_DIR.exists(): PLUGIN_DATA_DIR.makedirs()
        if not PATHS.SL_DB_DIR.exists(): PATHS.SL_DB_DIR.makedirs()

        # --- Process URL ---
        self.base_url     = sys.argv[0]
        self.addon_handle = int(sys.argv[1])
        args              = urlparse.parse_qs(sys.argv[2][1:])
        log_debug('args = {0}'.format(args))
        # Interestingly, if plugin is called as type executable then args is empty.
        # However, if plugin is called as type video then Kodi adds the following
        # even for the first call: 'content_type': ['video']
        self.content_type = args['content_type'] if 'content_type' in args else None
        log_debug('content_type = {0}'.format(self.content_type))

        # --- URL routing -------------------------------------------------------------------------
        args_size = len(args)
        if args_size == 0:
            self._render_root_list()
            log_debug('Advanced MAME Launcher exit (addon root)')
            return

        if 'catalog' in args and not 'command' in args:
            catalog_name = args['catalog'][0]
            # --- Software list is a special case ---
            if catalog_name == 'SL':
                SL_name     = args['SL'][0] if 'SL' in args else ''
                parent_name = args['parent'][0] if 'parent' in args else ''
                if category_name and parent_name:
                    self._render_SL_list_clone_list(SL_name, parent_name)
                elif category_name and not parent_name:
                    self._render_SL_list_parent_list(SL_name)
                else:
                    self._render_SL_list()
            else:
                category_name = args['category'][0] if 'category' in args else ''
                parent_name   = args['parent'][0] if 'parent' in args else ''
                if category_name and parent_name:
                    self._render_catalog_clone_list(catalog_name, category_name, parent_name)
                elif category_name and not parent_name:
                    self._render_catalog_parent_list(catalog_name, category_name)
                else:
                    self._render_catalog_list(catalog_name)

        elif 'command' in args:
            command = args['command'][0]
            if command == 'LAUNCH':
                machine  = args['machine'][0]
                location = args['location'][0] if 'location' in args else ''
                log_info('Launching MAME machine "{0}"'.format(machine, location))
                self._run_machine(machine, location)
            elif command == 'LAUNCH_SL':
                SL_name  = args['SL'][0]
                ROM_name = args['ROM'][0]
                log_info('Launching SL machine "{0}" (ROM "{1}")'.format(SL_name, ROM_name))
                self._run_SL_machine(SL_name, ROM_name)
            elif command == 'SETUP_PLUGIN':
                self._command_setup_plugin()
            elif command == 'VIEW':
                machine  = args['machine'][0]  if 'machine'  in args else ''
                SL       = args['SL'][0]       if 'SL'       in args else ''
                ROM      = args['ROM'][0]      if 'ROM'      in args else ''
                location = args['location'][0] if 'location' in args else LOCATION_STANDARD
                self._command_view(machine, SL, ROM, location)
            elif command == 'DISPLAY_SETTINGS':
                clist   = args['clist'][0]   if 'clist' in args else ''
                catalog = args['catalog'][0] if 'catalog' in args else ''
                machine = args['machine'][0] if 'machine' in args else ''
                self._command_display_settings(clist, catalog, machine)

            # >> MAME Favourites
            elif command == 'ADD_MAME_FAV':
                self._command_add_mame_fav(args['machine'][0])
            elif command == 'DELETE_MAME_FAV':
                self._command_delete_mame_fav(args['machine'][0])
            elif command == 'SHOW_MAME_FAVS':
                self._command_show_mame_fav()
            elif command == 'MANAGE_MAME_FAV':
                self._command_manage_mame_fav(args['machine'][0])

            # >> SL Favourites
            elif command == 'ADD_SL_FAV':
                self._command_add_sl_fav(args['SL'][0], args['ROM'][0])
            elif command == 'DELETE_SL_FAV':
                self._command_delete_sl_fav(args['SL'][0], args['ROM'][0])
            elif command == 'SHOW_SL_FAVS':
                self._command_show_sl_fav()
            elif command == 'MANAGE_SL_FAV':
                self._command_manage_sl_fav(args['SL'][0], args['ROM'][0])
            elif command == 'DISPLAY_SETTINGS_SL':
                self._command_display_settings_SL(args['SL'][0])

            else:
                log_error('Unknown command "{0}"'.format(command))

        else:
            log_error('Error in URL routing')

        # --- So Long, and Thanks for All the Fish ---
        log_debug('Advanced MAME Launcher exit')

    #
    # Get Addon Settings
    #
    def _get_settings(self):
        # --- Paths ---
        self.settings['mame_prog']     = __addon_obj__.getSetting('mame_prog').decode('utf-8')
        self.settings['rom_path']      = __addon_obj__.getSetting('rom_path').decode('utf-8')

        self.settings['assets_path']   = __addon_obj__.getSetting('assets_path').decode('utf-8')
        self.settings['chd_path']      = __addon_obj__.getSetting('chd_path').decode('utf-8')        
        self.settings['SL_hash_path']  = __addon_obj__.getSetting('SL_hash_path').decode('utf-8')
        self.settings['SL_rom_path']   = __addon_obj__.getSetting('SL_rom_path').decode('utf-8')
        self.settings['SL_chd_path']   = __addon_obj__.getSetting('SL_chd_path').decode('utf-8')
        self.settings['samples_path']  = __addon_obj__.getSetting('samples_path').decode('utf-8')
        self.settings['catver_path']   = __addon_obj__.getSetting('catver_path').decode('utf-8')
        self.settings['catlist_path']  = __addon_obj__.getSetting('catlist_path').decode('utf-8')
        self.settings['genre_path']    = __addon_obj__.getSetting('genre_path').decode('utf-8')
        self.settings['nplayers_path'] = __addon_obj__.getSetting('nplayers_path').decode('utf-8')

        # --- Display ---
        self.settings['display_hide_nonworking'] = True if __addon_obj__.getSetting('display_hide_nonworking') == 'true' else False
        self.settings['display_hide_imperfect']  = True if __addon_obj__.getSetting('display_hide_imperfect') == 'true' else False
        self.settings['display_available_only']  = True if __addon_obj__.getSetting('display_available_only') == 'true' else False

        # --- Advanced ---
        self.settings['log_level']               = int(__addon_obj__.getSetting('log_level'))

        # --- Dump settings for DEBUG ---
        # log_debug('Settings dump BEGIN')
        # for key in sorted(self.settings):
        #     log_debug('{0} --> {1:10s} {2}'.format(key.rjust(21), str(self.settings[key]), type(self.settings[key])))
        # log_debug('Settings dump END')

    # ---------------------------------------------------------------------------------------------
    # Root menu rendering
    # ---------------------------------------------------------------------------------------------
    # NOTE Devices are excluded from main PClone list.
    def _render_root_list(self):
        # >> Code Machines/Manufacturer/SF first. Rest are variations of those three.
        self._render_root_list_row('Machines (with coin slot)',       self._misc_url_2_arg('catalog', 'None', 'category', 'Machines'))
        self._render_root_list_row('Machines (no coin slot)',         self._misc_url_2_arg('catalog', 'None', 'category', 'NoCoin'))
        self._render_root_list_row('Machines (mechanical)',           self._misc_url_2_arg('catalog', 'None', 'category', 'Mechanical'))
        self._render_root_list_row('Machines (dead)',                 self._misc_url_2_arg('catalog', 'None', 'category', 'Dead'))
        self._render_root_list_row('Machines [with no ROMs]',         self._misc_url_2_arg('catalog', 'None', 'category', 'NoROM'))
        self._render_root_list_row('Machines [with CHDs]',            self._misc_url_2_arg('catalog', 'None', 'category', 'CHD'))
        self._render_root_list_row('Machines [with Samples]',         self._misc_url_2_arg('catalog', 'None', 'category', 'Samples'))
        self._render_root_list_row('Machines [BIOS]',                 self._misc_url_2_arg('catalog', 'None', 'category', 'BIOS'))
        # self._render_root_list_row('Machines [Devices]',              self._misc_url_2_arg('catalog', 'None', 'category', 'Devices'))
        self._render_root_list_row('Machines by Category (Catver)',   self._misc_url_1_arg('catalog', 'Catver'))
        self._render_root_list_row('Machines by Category (Catlist)',  self._misc_url_1_arg('catalog', 'Catlist'))
        self._render_root_list_row('Machines by Category (Genre)',    self._misc_url_1_arg('catalog', 'Genre'))
        self._render_root_list_row('Machines by Number of players',   self._misc_url_1_arg('catalog', 'NPlayers'))
        self._render_root_list_row('Machines by Manufacturer',        self._misc_url_1_arg('catalog', 'Manufacturer'))
        self._render_root_list_row('Machines by Year',                self._misc_url_1_arg('catalog', 'Year'))
        self._render_root_list_row('Machines by Driver',              self._misc_url_1_arg('catalog', 'Driver'))
        self._render_root_list_row('Machines by Control Type',        self._misc_url_1_arg('catalog', 'Controls'))
        self._render_root_list_row('Machines by Display Tag',         self._misc_url_1_arg('catalog', 'Display_Tag'))
        self._render_root_list_row('Machines by Display Type',        self._misc_url_1_arg('catalog', 'Display_Type'))
        self._render_root_list_row('Machines by Display Rotation',    self._misc_url_1_arg('catalog', 'Display_Rotate'))
        self._render_root_list_row('Machines by Device',              self._misc_url_1_arg('catalog', 'Devices'))
        self._render_root_list_row('Machines by Software List',       self._misc_url_1_arg('catalog', 'BySL'))
        self._render_root_list_row('Software Lists',                  self._misc_url_1_arg('catalog', 'SL'))
        self._render_root_list_row('<Favourite MAME machines>',       self._misc_url_1_arg('command', 'SHOW_MAME_FAVS'))
        self._render_root_list_row('<Favourite Software Lists ROMs>', self._misc_url_1_arg('command', 'SHOW_SL_FAVS'))
        xbmcplugin.endOfDirectory(handle = self.addon_handle, succeeded = True, cacheToDisc = False)

    def _render_root_list_row(self, root_name, root_URL):
        # --- Create listitem row ---
        icon = 'DefaultFolder.png'
        ICON_OVERLAY = 6
        listitem = xbmcgui.ListItem(root_name, iconImage = icon)

        # listitem.setProperty('fanart_image', category_dic['fanart'])
        listitem.setInfo('video', {'title' : root_name, 'overlay' : ICON_OVERLAY } )

        # --- Create context menu ---
        commands = []
        commands.append(('View', self._misc_url_1_arg_RunPlugin('command', 'VIEW'), ))
        commands.append(('Setup plugin', self._misc_url_1_arg_RunPlugin('command', 'SETUP_PLUGIN'), ))
        commands.append(('Kodi File Manager', 'ActivateWindow(filemanager)', ))
        commands.append(('Add-on Settings', 'Addon.OpenSettings({0})'.format(__addon_id__), ))
        listitem.addContextMenuItems(commands, replaceItems = True)

        # --- Add row ---
        xbmcplugin.addDirectoryItem(handle = self.addon_handle, url = root_URL, listitem = listitem, isFolder = True)

    #----------------------------------------------------------------------------------------------
    # Cataloged machines
    #----------------------------------------------------------------------------------------------
    def _render_catalog_list(self, catalog_name):
        log_error('_render_catalog_list() Starting ...')
        # >> Load catalog index
        catalog_name = self._get_catalog_name(clist_name)
        catalog_dic = self._get_cataloged_dic(clist_name)

        # >> Render categories in catalog index
        self._set_Kodi_all_sorting_methods_and_size()
        for catalog_key, catalog_value in catalog_dic.iteritems():
            self._render_indexed_list_row(clist_name, catalog_name, catalog_key, catalog_value['num_machines'])
        xbmcplugin.endOfDirectory(handle = self.addon_handle, succeeded = True, cacheToDisc = False)

    #
    # Renders a Parent list knowing the catalog name and the category.
    # Display mode: a) parents only b) all machines
    #
    def _render_catalog_parent_list(self, catalog_name, category_name):
        log_debug('_render_catalog_parent_list() catalog_name  = {0}'.format(catalog_name))
        log_debug('_render_catalog_parent_list() category_name = {0}'.format(category_name))
        display_hide_nonworking = self.settings['display_hide_nonworking']
        display_hide_imperfect  = self.settings['display_hide_imperfect']

        # >> Load ListItem properties
        prop_key = '{0} - {1}'.format(catalog_name, category_name)
        log_debug('_render_catalog_parent_list() Loading props with key "{0}"'.format(prop_key))
        mame_properties_dic = fs_load_JSON_file(PATHS.MAIN_PROPERTIES_PATH.getPath())
        prop_dic = mame_properties_dic[prop_key]

        # >> Load main MAME info DB
        loading_ticks_start = time.time()
        MAME_db_dic         = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
        MAME_assets_dic     = fs_load_JSON_file(PATHS.MAIN_ASSETS_DB_PATH.getPath())
        main_pclone_dic     = fs_load_JSON_file(PATHS.MAIN_PCLONE_DIC_PATH.getPath())
        # >> Load catalog index
        if prop_dic['vm'] == VIEW_MODE_NORMAL:
            catalog_dic = fs_get_cataloged_dic_parents(PATHS, catalog_name)
        elif prop_dic['vm'] == VIEW_MODE_PCLONE:
            catalog_dic = fs_get_cataloged_dic_all(PATHS, catalog_name)
        else:
            kodi_dialog_OK('Wrong vm = "{0}". This is a bug, please report it.'.format(prop_dic['vm']))
            return
        loading_ticks_end = time.time()

        # >> Render parent main list
        self._set_Kodi_all_sorting_methods()
        rendering_ticks_start = time.time()
        if prop_dic['vm'] == VIEW_MODE_NORMAL:
            # >> Normal mode render parents only
            machine_list = catalog_dic[category_name]['parents']
            for machine_name in machine_list:
                machine = MAME_db_dic[machine_name]
                if display_hide_nonworking and machine['driver_status'] == 'preliminary': continue
                if display_hide_imperfect and machine['driver_status'] == 'imperfect': continue
                assets  = MAME_assets_dic[machine_name]
                num_clones = len(main_pclone_dic[machine_name])
                self._render_catalog_machine_row(machine_name, machine, assets, True, catalog_name, category_name, num_clones)
        else:
            # >> Render all machines
            machine_list = catalog_dic[category_name]['machines']
            for machine_name in machine_list:
                machine = MAME_db_dic[machine_name]
                if display_hide_nonworking and machine['driver_status'] == 'preliminary': continue
                if display_hide_imperfect and machine['driver_status'] == 'imperfect': continue
                assets  = MAME_assets_dic[machine_name]
                self._render_catalog_machine_row(machine_name, machine, assets, False, catalog_name, category_name)
        xbmcplugin.endOfDirectory(handle = self.addon_handle, succeeded = True, cacheToDisc = False)
        rendering_ticks_end = time.time()

        # --- DEBUG Data loading/rendering statistics ---
        log_debug('Loading seconds   {0}'.format(loading_ticks_end - loading_ticks_start))
        log_debug('Rendering seconds {0}'.format(rendering_ticks_end - rendering_ticks_start))

    def _render_catalog_clone_list(self, catalog_name, category_name, parent_name):
        log_error('_render_catalog_clone_list() Starting ...')
        display_hide_nonworking = self.settings['display_hide_nonworking']
        display_hide_imperfect  = self.settings['display_hide_imperfect']

        # >> Load main MAME info DB
        MAME_db_dic     = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
        MAME_assets_dic = fs_load_JSON_file(PATHS.MAIN_ASSETS_DB_PATH.getPath())
        main_pclone_dic = fs_load_JSON_file(PATHS.MAIN_PCLONE_DIC_PATH.getPath())

        # >> Get catalog name
        catalog_name = self._get_catalog_name(clist_name)

        # >> Render parent first
        self._set_Kodi_all_sorting_methods()
        machine = MAME_db_dic[parent_name]
        assets  = MAME_assets_dic[parent_name]
        self._render_indexed_machine_row(parent_name, machine, assets, False, clist_name, catalog_name, catalog_item_name)

        # >> Render clones belonging to parent in this category
        for p_name in main_pclone_dic[parent_name]:
            machine = MAME_db_dic[p_name]
            assets  = MAME_assets_dic[p_name]
            if display_hide_nonworking and machine['driver_status'] == 'preliminary': continue
            if display_hide_imperfect and machine['driver_status'] == 'imperfect': continue
            self._render_indexed_machine_row(p_name, machine, assets, False, clist_name, catalog_name, catalog_item_name)
        xbmcplugin.endOfDirectory(handle = self.addon_handle, succeeded = True, cacheToDisc = False)

    def _render_catalog_list_row(self, clist_name, catalog_name, catalog_key, num_machines):
        # --- Create listitem row ---
        icon = 'DefaultFolder.png'
        ICON_OVERLAY = 6
        title_str = '{0} [COLOR orange]({1} machines)[/COLOR]'.format(catalog_key, num_machines)

        listitem = xbmcgui.ListItem(title_str, iconImage = icon)
        # listitem.setProperty('fanart_image', category_dic['fanart'])
        listitem.setInfo('video', {'Title'   : title_str, 'Overlay' : ICON_OVERLAY, 'size' : num_machines})

        # --- Create context menu ---
        commands = []
        URL_view = self._misc_url_1_arg_RunPlugin('command', 'VIEW')
        commands.append(('View', URL_view ))
        commands.append(('Kodi File Manager', 'ActivateWindow(filemanager)' ))
        commands.append(('Add-on Settings', 'Addon.OpenSettings({0})'.format(__addon_id__) ))
        listitem.addContextMenuItems(commands, replaceItems = True)

        # --- Add row ---
        URL = self._misc_url_2_arg('clist', clist_name, catalog_name, catalog_key)
        xbmcplugin.addDirectoryItem(handle = self.addon_handle, url = URL, listitem = listitem, isFolder = True)

    def _render_catalog_machine_row(self, machine_name, machine, machine_assets, flag_parent_list,
                                    catalog_name, category_name, num_clones = 0):
        display_name = machine['description']

        # --- Render a Parent only list ---
        if flag_parent_list and num_clones > 0:
            # >> Machine has clones
            display_name += ' [COLOR orange] ({0} clones)[/COLOR]'.format(num_clones)
        else:
            # >> Machine has no clones
            # --- Mark Status ---
            status = '{0}{1}{2}{3}{4}'.format(machine['status_ROM'], machine['status_CHD'],
                                              machine['status_SAM'], machine['status_SL'],
                                              machine['status_Device'])
            display_name += ' [COLOR skyblue]{0}[/COLOR]'.format(status)

            # --- Mark Devices, BIOS and clones ---
            if machine['isDevice']: display_name += ' [COLOR violet][Dev][/COLOR]'
            if machine['isBIOS']:   display_name += ' [COLOR cyan][BIOS][/COLOR]'
            if machine['cloneof']:  display_name += ' [COLOR orange][Clo][/COLOR]'

            # --- Mark driver status: Good (no mark), Imperfect, Preliminar ---
            if   machine['driver_status'] == 'imperfect':   display_name += ' [COLOR yellow][Imp][/COLOR]'
            elif machine['driver_status'] == 'preliminary': display_name += ' [COLOR red][Pre][/COLOR]'

        # --- Assets/artwork ---
        icon_path      = machine_assets['title'] if machine_assets['title'] else 'DefaultProgram.png'
        fanart_path    = machine_assets['snap']
        banner_path    = machine_assets['marquee']
        clearlogo_path = machine_assets['clearlogo']
        poster_path    = machine_assets['flyer']

        # --- Create listitem row ---
        ICON_OVERLAY = 6
        listitem = xbmcgui.ListItem(display_name)
        # >> Make all the infolabels compatible with Advanced Emulator Launcher
        listitem.setInfo('video', {'title'   : display_name,            'year'    : machine['year'],
                                   'genre'   : '',                      'plot'    : '',
                                   'studio'  : machine['manufacturer'], 'rating'  : '',
                                   'trailer' : '',                      'overlay' : ICON_OVERLAY})
        listitem.setProperty('platform', 'MAME')

        # --- Assets ---
        # >> AEL custom artwork fields
        listitem.setArt({'title'     : machine_assets['title'],   'snap'    : machine_assets['snap'],
                         'boxfront'  : machine_assets['cabinet'], 'boxback' : machine_assets['cpanel'],
                         'cartridge' : machine_assets['PCB'],     'flyer'   : machine_assets['flyer'] })

        # >> Kodi official artwork fields
        listitem.setArt({'icon'   : icon_path,   'fanart'    : fanart_path,
                         'banner' : banner_path, 'clearlogo' : clearlogo_path, 'poster' : poster_path })

        # --- Create context menu ---
        commands = []
        URL_view    = self._misc_url_2_arg_RunPlugin('command', 'VIEW', 'machine', machine_name)
        URL_display = self._misc_url_4_arg_RunPlugin('command', 'DISPLAY_SETTINGS', 
                                                     'catalog', catalog_name, 'category', category_name, 'machine', machine_name)
        URL_fav     = self._misc_url_2_arg_RunPlugin('command', 'ADD_MAME_FAV', 'machine', machine_name)
        commands.append(('View',  URL_view ))
        commands.append(('Display settings', URL_display ))
        commands.append(('Add machine to MAME Favourites', URL_fav ))
        commands.append(('Kodi File Manager', 'ActivateWindow(filemanager)' ))
        commands.append(('Add-on Settings', 'Addon.OpenSettings({0})'.format(__addon_id__) ))
        listitem.addContextMenuItems(commands, replaceItems = True)

        # --- Add row ---
        if flag_parent_list and num_clones > 0:
            URL = self._misc_url_3_arg('catalog', catalog_name, 'category', category_name, 'parent', machine_name)
            xbmcplugin.addDirectoryItem(handle = self.addon_handle, url = URL, listitem = listitem, isFolder = True)
        else:
            URL = self._misc_url_2_arg('command', 'LAUNCH', 'machine', machine_name)
            xbmcplugin.addDirectoryItem(handle = self.addon_handle, url = URL, listitem = listitem, isFolder = False)

    #----------------------------------------------------------------------------------------------
    # Software Lists
    #----------------------------------------------------------------------------------------------
    def _render_SL_machine_list(self):
        # >> Load Software List catalog
        SL_catalog_dic = fs_load_JSON_file(PATHS.SL_INDEX_PATH.getPath())

        self._set_Kodi_all_sorting_methods()
        for SL_name in SL_catalog_dic:
            SL = SL_catalog_dic[SL_name]
            self._render_SL_machine_row(SL_name, SL)
        xbmcplugin.endOfDirectory(handle = self.addon_handle, succeeded = True, cacheToDisc = False)

    def _render_SL_machine_ROM_list(self, SL_name):
        # >> Load Software List catalog
        SL_catalog_dic = fs_load_JSON_file(PATHS.SL_INDEX_PATH.getPath())

        # >> Load Software List ROMs
        file_name =  SL_catalog_dic[SL_name]['rom_DB_noext'] + '.json'
        SL_DB_FN = PATHS.SL_DB_DIR.pjoin(file_name)
        log_info('_render_SL_machine_ROM_list() ROMs JSON "{0}"'.format(SL_DB_FN.getPath()))
        SL_roms = fs_load_JSON_file(SL_DB_FN.getPath())

        assets_file_name =  SL_catalog_dic[SL_name]['rom_DB_noext'] + '_assets.json'
        SL_asset_DB_FN = PATHS.SL_DB_DIR.pjoin(assets_file_name)
        SL_asset_dic = fs_load_JSON_file(SL_asset_DB_FN.getPath())

        self._set_Kodi_all_sorting_methods()
        for rom_name in SL_roms:
            ROM    = SL_roms[rom_name]
            assets = SL_asset_dic[rom_name]
            self._render_SL_ROM_row(SL_name, rom_name, ROM, assets)
        xbmcplugin.endOfDirectory(handle = self.addon_handle, succeeded = True, cacheToDisc = False)

    def _render_SL_machine_row(self, SL_name, SL):
        if SL['chd_count'] == 0:
            if SL['rom_count'] == 1: display_name = '{0}  [COLOR orange]({1} ROM)[/COLOR]'.format(SL['display_name'], SL['rom_count'])
            else:                    display_name = '{0}  [COLOR orange]({1} ROMs)[/COLOR]'.format(SL['display_name'], SL['rom_count'])
        elif SL['rom_count'] == 0:
            if SL['chd_count'] == 1: display_name = '{0}  [COLOR orange]({1} CHD)[/COLOR]'.format(SL['display_name'], SL['chd_count'])
            else:                    display_name = '{0}  [COLOR orange]({1} CHDs)[/COLOR]'.format(SL['display_name'], SL['chd_count'])
        else:
            display_name = '{0}  [COLOR orange]({1} ROMs and {2} CHDs)[/COLOR]'.format(SL['display_name'], SL['rom_count'], SL['chd_count'])

        # --- Create listitem row ---
        icon = 'DefaultFolder.png'
        listitem = xbmcgui.ListItem(display_name, iconImage = icon)
        ICON_OVERLAY = 6
        # listitem.setProperty('fanart_image', category_dic['fanart'])
        listitem.setInfo('video', {'title' : display_name, 'overlay' : ICON_OVERLAY } )

        # --- Create context menu ---
        commands = []
        URL_view = self._misc_url_1_arg_RunPlugin('command', 'VIEW')
        commands.append(('View', URL_view ))
        commands.append(('Kodi File Manager', 'ActivateWindow(filemanager)' ))
        commands.append(('Add-on Settings', 'Addon.OpenSettings({0})'.format(__addon_id__) ))
        listitem.addContextMenuItems(commands, replaceItems = True)

        # --- Add row ---
        URL = self._misc_url_2_arg('clist', 'SL', 'SL', SL_name)
        xbmcplugin.addDirectoryItem(handle = self.addon_handle, url = URL, listitem = listitem, isFolder = True)

    def _render_SL_ROM_row(self, SL_name, rom_name, ROM, assets):
        display_name = ROM['description']

        # --- Mark Status and Clones ---
        status = '{0}{1}'.format(ROM['status_ROM'], ROM['status_CHD'])
        display_name += ' [COLOR skyblue]{0}[/COLOR]'.format(status)
        if ROM['cloneof']: display_name += ' [COLOR orange][Clo][/COLOR]'

        # --- Assets/artwork ---
        icon_path   = assets['title'] if assets['title'] else 'DefaultProgram.png'
        fanart_path = assets['snap']
        poster_path = assets['boxfront']

        # --- Create listitem row ---
        ICON_OVERLAY = 6
        listitem = xbmcgui.ListItem(display_name)
        # >> Make all the infolabels compatible with Advanced Emulator Launcher
        listitem.setInfo('video', {'title'   : display_name,     'year'    : ROM['year'],
                                   'studio'  : ROM['publisher'], 'overlay' : ICON_OVERLAY })
        listitem.setProperty('platform', 'MAME')

        # --- Assets ---
        # >> AEL custom artwork fields
        listitem.setArt({'title' : assets['title'], 'snap' : assets['snap'], 'boxfront' : assets['boxfront']})

        # >> Kodi official artwork fields
        listitem.setArt({'icon' : icon_path, 'fanart' : fanart_path, 'poster' : poster_path})

        # --- Create context menu ---
        commands = []
        URL_view = self._misc_url_3_arg_RunPlugin('command', 'VIEW', 'SL', SL_name, 'ROM', rom_name)
        URL_fav = self._misc_url_3_arg_RunPlugin('command', 'ADD_SL_FAV', 'SL', SL_name, 'ROM', rom_name)
        commands.append(('View', URL_view ))
        commands.append(('Add ROM to SL Favourites', URL_fav ))
        commands.append(('Kodi File Manager', 'ActivateWindow(filemanager)' ))
        commands.append(('Add-on Settings', 'Addon.OpenSettings({0})'.format(__addon_id__) ))
        listitem.addContextMenuItems(commands, replaceItems = True)

        # --- Add row ---
        URL = self._misc_url_3_arg('command', 'LAUNCH_SL', 'SL', SL_name, 'ROM', rom_name)
        xbmcplugin.addDirectoryItem(handle = self.addon_handle, url = URL, listitem = listitem, isFolder = False)

    # ---------------------------------------------------------------------------------------------
    # Information display
    # ---------------------------------------------------------------------------------------------
    def _command_view(self, machine_name, SL_name, SL_ROM, location):
        log_debug('_command_view() machine_name "{0}"'.format(machine_name))
        log_debug('_command_view() SL_name      "{0}"'.format(SL_name))
        log_debug('_command_view() SL_ROM       "{0}"'.format(SL_ROM))
        log_debug('_command_view() location     "{0}"'.format(location))
        MENU_SIMPLE    = 100
        MENU_MAME_DATA = 200
        MENU_SL_DATA   = 300
        menu_kind = 0
        size_output = 0
        if PATHS.MAME_OUTPUT_PATH.exists():
            stat_output = PATHS.MAME_OUTPUT_PATH.stat()
            size_output = stat_output.st_size
        dialog = xbmcgui.Dialog()
        if not machine_name and not SL_name:
            menu_kind = MENU_SIMPLE
            type = dialog.select('View ...',
                                 ['View database information',
                                  'View MAME ROM scanner report',
                                  'View MAME CHD scanner report',
                                  'View MAME Samples scanner report',
                                  'View Software Lists ROM scanner report',
                                  'View Software Lists CHD scanner report',
                                  'MAME last execution output ({0} bytes)'.format(size_output)])
        elif machine_name:
            menu_kind = MENU_MAME_DATA
            type = dialog.select('View ...',
                                 ['View MAME machine data',
                                  'View database information',
                                  'View MAME ROM scanner report',
                                  'View MAME CHD scanner report',
                                  'View MAME Samples scanner report',
                                  'View Software Lists ROM scanner report',
                                  'View Software Lists CHD scanner report',
                                  'MAME last execution output ({0} bytes)'.format(size_output)])
        elif SL_name:
            menu_kind = MENU_SL_DATA
            type = dialog.select('View ...',
                                 ['View Software List machine data',
                                  'View database information',
                                  'View MAME ROM scanner report',
                                  'View MAME CHD scanner report',
                                  'View MAME Samples scanner report',
                                  'View Software Lists ROM scanner report',
                                  'View Software Lists CHD scanner report',
                                  'MAME last execution output ({0} bytes)'.format(size_output)])
        else:
            kodi_dialog_OK('_command_view() runtime error. Report this bug')
            return
        if type < 0: return

        # --- View MAME Machine ---
        if menu_kind == MENU_MAME_DATA:
            type_nb = 0
            if type == 0:
                if location == LOCATION_STANDARD:
                    # >> Read MAME machine information
                    kodi_busydialog_ON()
                    MAME_db_dic     = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
                    MAME_assets_dic = fs_load_JSON_file(PATHS.MAIN_ASSETS_DB_PATH.getPath())
                    kodi_busydialog_OFF()
                    machine = MAME_db_dic[machine_name]
                    assets  = MAME_assets_dic[machine_name]
                    window_title = 'MAME Machine Information'
                elif location == LOCATION_MAME_FAVS:
                    machines = fs_load_JSON_file(PATHS.FAV_MACHINES_PATH.getPath())
                    machine = machines[machine_name]
                    assets = machine['assets']
                    window_title = 'Favourite MAME Machine Information'

                # --- Make information string ---
                info_text  = '[COLOR orange]Machine {0}[/COLOR]\n'.format(machine_name)
                info_text += "[COLOR skyblue]CHDs[/COLOR]: {0}\n".format(machine['CHDs'])
                info_text += "[COLOR skyblue]CHDs_merged[/COLOR]: {0}\n".format(machine['CHDs_merged'])
                info_text += "[COLOR skyblue]bios_desc[/COLOR]: {0}\n".format(machine['bios_desc'])
                info_text += "[COLOR skyblue]bios_name[/COLOR]: {0}\n".format(machine['bios_name'])
                info_text += "[COLOR violet]catlist[/COLOR]: '{0}'\n".format(machine['catlist'])
                info_text += "[COLOR violet]catver[/COLOR]: '{0}'\n".format(machine['catver'])
                info_text += "[COLOR violet]cloneof[/COLOR]: '{0}'\n".format(machine['cloneof'])
                info_text += "[COLOR skyblue]coins[/COLOR]: {0}\n".format(machine['coins'])
                info_text += "[COLOR skyblue]control_type[/COLOR]: {0}\n".format(machine['control_type'])
                info_text += "[COLOR violet]description[/COLOR]: '{0}'\n".format(machine['description'])
                info_text += "[COLOR skyblue]device_list[/COLOR]: {0}\n".format(machine['device_list'])
                # info_text += "[COLOR skyblue]device_tags[/COLOR]: {0}\n".format(machine['device_tags'])
                info_text += "[COLOR skyblue]display_rotate[/COLOR]: {0}\n".format(machine['display_rotate'])
                info_text += "[COLOR skyblue]display_tag[/COLOR]: {0}\n".format(machine['display_tag'])
                info_text += "[COLOR skyblue]display_type[/COLOR]: {0}\n".format(machine['display_type'])
                info_text += "[COLOR violet]driver_status[/COLOR]: '{0}'\n".format(machine['driver_status'])
                info_text += "[COLOR violet]genre[/COLOR]: '{0}'\n".format(machine['genre'])
                info_text += "[COLOR skyblue]hasCoin[/COLOR]: {0}\n".format(machine['hasCoin'])                
                info_text += "[COLOR skyblue]hasROMs[/COLOR]: {0}\n".format(machine['hasROMs'])
                info_text += "[COLOR skyblue]hasROMs_merged[/COLOR]: {0}\n".format(machine['hasROMs_merged'])                
                info_text += "[COLOR skyblue]isBIOS[/COLOR]: {0}\n".format(machine['isBIOS'])
                info_text += "[COLOR skyblue]isDead[/COLOR]: {0}\n".format(machine['isDead'])
                info_text += "[COLOR skyblue]isDevice[/COLOR]: {0}\n".format(machine['isDevice'])
                info_text += "[COLOR skyblue]isMechanical[/COLOR]: {0}\n".format(machine['isMechanical'])
                if location == LOCATION_MAME_FAVS:
                    info_text += "[COLOR slateblue]mame_version[/COLOR]: {0}\n".format(machine['mame_version'])
                info_text += "[COLOR violet]manufacturer[/COLOR]: '{0}'\n".format(machine['manufacturer'])
                info_text += "[COLOR violet]nplayers[/COLOR]: '{0}'\n".format(machine['nplayers'])
                info_text += "[COLOR violet]romof[/COLOR]: '{0}'\n".format(machine['romof'])
                info_text += "[COLOR violet]sampleof[/COLOR]: '{0}'\n".format(machine['sampleof'])
                info_text += "[COLOR skyblue]softwarelists[/COLOR]: {0}\n".format(machine['softwarelists'])
                info_text += "[COLOR violet]sourcefile[/COLOR]: '{0}'\n".format(machine['sourcefile'])
                info_text += "[COLOR violet]status_CHD[/COLOR]: '{0}'\n".format(machine['status_CHD'])
                info_text += "[COLOR violet]status_ROM[/COLOR]: '{0}'\n".format(machine['status_ROM'])
                info_text += "[COLOR violet]status_SAM[/COLOR]: '{0}'\n".format(machine['status_SAM'])
                info_text += "[COLOR violet]status_SL[/COLOR]: '{0}'\n".format(machine['status_SL'])
                info_text += "[COLOR violet]year[/COLOR]: '{0}'\n".format(machine['year'])

                info_text += '\n[COLOR orange]Asset/artwork information[/COLOR]\n'
                info_text += "[COLOR violet]cabinet[/COLOR]: '{0}'\n".format(assets['cabinet'])
                info_text += "[COLOR violet]cpanel[/COLOR]: '{0}'\n".format(assets['cpanel'])
                info_text += "[COLOR violet]flyer[/COLOR]: '{0}'\n".format(assets['flyer'])
                info_text += "[COLOR violet]marquee[/COLOR]: '{0}'\n".format(assets['marquee'])
                info_text += "[COLOR violet]PCB[/COLOR]: '{0}'\n".format(assets['PCB'])
                info_text += "[COLOR violet]snap[/COLOR]: '{0}'\n".format(assets['snap'])
                info_text += "[COLOR violet]title[/COLOR]: '{0}'\n".format(assets['title'])
                info_text += "[COLOR violet]clearlogo[/COLOR]: '{0}'\n".format(assets['clearlogo'])

                # --- Show information window ---
                try:
                    xbmc.executebuiltin('ActivateWindow(10147)')
                    window = xbmcgui.Window(10147)
                    xbmc.sleep(100)
                    window.getControl(1).setLabel(window_title)
                    window.getControl(5).setText(info_text)
                except:
                    log_error('_command_view_machine() Exception rendering INFO window')

        # --- View Software List Machine ---
        elif menu_kind == MENU_SL_DATA:
            type_nb = 0
            if type == type_nb:
                if location == LOCATION_STANDARD:
                    SL_DB_FN = PATHS.SL_DB_DIR.pjoin(SL_name + '.json')
                    kodi_busydialog_ON()
                    SL_catalog_dic = fs_load_JSON_file(PATHS.SL_INDEX_PATH.getPath())
                    SL_machines_dic = fs_load_JSON_file(PATHS.SL_MACHINES_PATH.getPath())
                    kodi_busydialog_OFF()
                    SL_dic = SL_catalog_dic[SL_name]
                    SL_machine_list = SL_machines_dic[SL_name]
                    roms = fs_load_JSON_file(SL_DB_FN.getPath())
                    rom = roms[SL_ROM]
                    window_title = 'Software List ROM Information'

                    # >> Build information string
                    info_text  = '[COLOR orange]ROM {0}[/COLOR]\n'.format(SL_ROM)
                    info_text += "[COLOR skyblue]CHDs[/COLOR]: {0}\n".format(rom['CHDs'])
                    info_text += "[COLOR violet]cloneof[/COLOR]: '{0}'\n".format(rom['cloneof'])
                    info_text += "[COLOR violet]description[/COLOR]: '{0}'\n".format(rom['description'])
                    info_text += "[COLOR skyblue]num_roms[/COLOR]: {0}\n".format(rom['num_roms'])
                    info_text += "[COLOR skyblue]part_interface[/COLOR]: {0}\n".format(rom['part_interface'])
                    info_text += "[COLOR skyblue]part_name[/COLOR]: {0}\n".format(rom['part_name'])
                    info_text += "[COLOR violet]publisher[/COLOR]: '{0}'\n".format(rom['publisher'])
                    info_text += "[COLOR violet]status_CHD[/COLOR]: '{0}'\n".format(rom['status_CHD'])
                    info_text += "[COLOR violet]status_ROM[/COLOR]: '{0}'\n".format(rom['status_ROM'])
                    info_text += "[COLOR violet]year[/COLOR]: '{0}'\n".format(rom['year'])

                    info_text += '\n[COLOR orange]Software List {0}[/COLOR]\n'.format(SL_name)
                    info_text += "[COLOR skyblue]chd_count[/COLOR]: {0}\n".format(SL_dic['chd_count'])
                    info_text += "[COLOR violet]display_name[/COLOR]: '{0}'\n".format(SL_dic['display_name'])
                    info_text += "[COLOR violet]rom_DB_noext[/COLOR]: '{0}'\n".format(SL_dic['rom_DB_noext'])
                    info_text += "[COLOR violet]rom_count[/COLOR]: '{0}'\n".format(SL_dic['rom_count'])

                    info_text += '\n[COLOR orange]Runnable by[/COLOR]\n'
                    for machine_dic in sorted(SL_machine_list):
                        t = "[COLOR violet]machine[/COLOR]: '{0}' [COLOR slateblue]({1})[/COLOR]\n"
                        info_text += t.format(machine_dic['description'], machine_dic['machine'])

                elif location == LOCATION_SL_FAVS:
                    fav_SL_roms = fs_load_JSON_file(PATHS.FAV_SL_ROMS_PATH.getPath())
                    fav_key = SL_name + '-' + SL_ROM
                    rom = fav_SL_roms[fav_key]
                    window_title = 'Favourite Software List ROM Information'

                    # >> Build information string
                    info_text  = '[COLOR orange]ROM {0}[/COLOR]\n'.format(fav_key)
                    info_text += "[COLOR skyblue]CHDs[/COLOR]: {0}\n".format(rom['CHDs'])
                    info_text += "[COLOR violet]ROM_name[/COLOR]: '{0}'\n".format(rom['ROM_name'])
                    info_text += "[COLOR violet]SL_name[/COLOR]: '{0}'\n".format(rom['SL_name'])
                    info_text += "[COLOR violet]cloneof[/COLOR]: '{0}'\n".format(rom['cloneof'])
                    info_text += "[COLOR violet]description[/COLOR]: '{0}'\n".format(rom['description'])
                    info_text += "[COLOR violet]mame_version[/COLOR]: '{0}'\n".format(rom['mame_version'])
                    info_text += "[COLOR skyblue]num_roms[/COLOR]: {0}\n".format(rom['num_roms'])
                    info_text += "[COLOR skyblue]part_interface[/COLOR]: {0}\n".format(rom['part_interface'])
                    info_text += "[COLOR skyblue]part_name[/COLOR]: {0}\n".format(rom['part_name'])
                    info_text += "[COLOR violet]publisher[/COLOR]: '{0}'\n".format(rom['publisher'])
                    info_text += "[COLOR violet]status_CHD[/COLOR]: '{0}'\n".format(rom['status_CHD'])
                    info_text += "[COLOR violet]status_ROM[/COLOR]: '{0}'\n".format(rom['status_ROM'])
                    info_text += "[COLOR violet]year[/COLOR]: '{0}'\n".format(rom['year'])

                # --- Show information window ---
                try:
                    xbmc.executebuiltin('ActivateWindow(10147)')
                    window = xbmcgui.Window(10147)
                    xbmc.sleep(100)
                    window.getControl(1).setLabel(window_title)
                    window.getControl(5).setText(info_text)
                except:
                    log_error('_command_view_machine() Exception rendering INFO window')
        else:
            type_nb = -1

        # --- View database information and statistics ---
        type_nb += 1
        if type == type_nb:
            # --- Load control dic ---
            control_dic = fs_load_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath())
            
            # --- Main stuff ---
            info_text  = '[COLOR orange]Main information[/COLOR]\n'
            info_text += "AML version: {0}\n".format(__addon_version__)
            info_text += "MAME version: {0}\n".format(control_dic['mame_version'])
            info_text += "Catver.ini version: {0}\n".format(control_dic['catver_version'])
            info_text += "Catlist.ini version: {0}\n".format(control_dic['catlist_version'])
            info_text += "Genre.ini version: {0}\n".format(control_dic['genre_version'])
            info_text += "nplayers.ini version: {0}\n".format(control_dic['nplayers_version'])

            info_text += '\n[COLOR orange]MAME machine count[/COLOR]\n'
            t = "Machines: {0} ({1} Parents / {2} Clones)\n"
            info_text += t.format(control_dic['processed_machines'], control_dic['parent_machines'],
                                  control_dic['clone_machines'])
            info_text += "Devices: {0}\n".format(control_dic['devices_machines'])
            info_text += "BIOS: {0}\n".format(control_dic['BIOS_machines'])
            info_text += "Coin: {0}\n".format(control_dic['coin_machines'])
            info_text += "Nocoin: {0}\n".format(control_dic['nocoin_machines'])
            info_text += "Mechanical: {0}\n".format(control_dic['mechanical_machines'])
            info_text += "Dead: {0}\n".format(control_dic['dead_machines'])
            t = "ROMs: {0} ({1} Merged ROMs / {2} ROMless)\n"
            info_text += t.format(control_dic['Own_ROM_machines'], control_dic['Merged_ROM_machines'], 
                                  control_dic['No_ROM_machines'])
            t = "CHDs: {0} ({1} Merged CHDs)\n"
            info_text += t.format(control_dic['Own_CHD_machines'], control_dic['Merged_CHD_machines'])
            info_text += "Samples: {0}\n".format(control_dic['samples_machines'])

            info_text += '\n[COLOR orange]Software Lists ROM count[/COLOR]\n'
            info_text += "Number of SL files: {0}\n".format(control_dic['num_SL_files'])
            info_text += "Total ROMs in all SLs: {0}\n".format(control_dic['num_SL_ROMs'])
            info_text += "Total CHDs in all SLs: {0}\n".format(control_dic['num_SL_CHDs'])

            info_text += '\n[COLOR orange]ROM audit information[/COLOR]\n'
            t = "You have {0} ROMs out of {1} ({2} missing)\n"
            info_text += t.format(control_dic['ROMs_have'], control_dic['ROMs_total'], control_dic['ROMs_missing'])
            t = "You have {0} CHDs out of {1} ({2} missing)\n"
            info_text += t.format(control_dic['CHDs_have'], control_dic['CHDs_total'], control_dic['CHDs_missing'])
            t = "You have {0} Samples out of {1} ({2} missing)\n"
            info_text += t.format(control_dic['Samples_have'], control_dic['Samples_total'], control_dic['Samples_missing'])
            t = "You have {0} SL ROMs out of {1} ({2} missing)\n"
            info_text += t.format(control_dic['SL_ROMs_have'], control_dic['SL_ROMs_total'], control_dic['SL_ROMs_missing'])
            t = "You have {0} SL CHDs out of {1} ({2} missing)\n"
            info_text += t.format(control_dic['SL_CHDs_have'], control_dic['SL_CHDs_total'], control_dic['SL_CHDs_missing'])

            # --- Show information window ---
            window_title = 'Database information and statistics'
            try:
                xbmc.executebuiltin('ActivateWindow(10147)')
                window = xbmcgui.Window(10147)
                xbmc.sleep(100)
                window.getControl(1).setLabel(window_title)
                window.getControl(5).setText(info_text)
            except:
                log_error('_command_view_machine() Exception rendering INFO window')

        # --- View MAME ROM scanner report ---
        type_nb += 1
        if type == type_nb:
            if not PATHS.REPORT_MAME_SCAN_ROMS_PATH.exists():
                kodi_dialog_OK('MAME ROM scanner report not found. Please scan MAME ROMs and try again.')
                return

            # --- Read stdout and put into a string ---
            info_text = ''
            with open(PATHS.REPORT_MAME_SCAN_ROMS_PATH.getPath(), "r") as myfile:
                info_text = myfile.read()

            # --- Show information window ---
            window_title = 'ROM scanner report'
            try:
                xbmc.executebuiltin('ActivateWindow(10147)')
                window = xbmcgui.Window(10147)
                xbmc.sleep(100)
                window.getControl(1).setLabel(window_title)
                window.getControl(5).setText(info_text)
            except:
                log_error('_command_view_machine() Exception rendering INFO window')

        # --- View MAME CHD scanner report ---
        type_nb += 1
        if type == type_nb:
            if not PATHS.REPORT_MAME_SCAN_CHDS_PATH.exists():
                kodi_dialog_OK('MAME CHD scanner report not found. Please scan MAME ROMs and try again.')
                return

            # --- Read stdout and put into a string ---
            info_text = ''
            with open(PATHS.REPORT_MAME_SCAN_CHDS_PATH.getPath(), "r") as myfile:
                info_text = myfile.read()

            # --- Show information window ---
            window_title = 'MAME CHD scanner report'
            try:
                xbmc.executebuiltin('ActivateWindow(10147)')
                window = xbmcgui.Window(10147)
                xbmc.sleep(100)
                window.getControl(1).setLabel(window_title)
                window.getControl(5).setText(info_text)
            except:
                log_error('_command_view_machine() Exception rendering INFO window')

        # --- View MAME Samples scanner report ---
        type_nb += 1
        if type == type_nb:
            if not PATHS.REPORT_MAME_SCAN_SAMP_PATH.exists():
                kodi_dialog_OK('MAME Samples scanner report not found. Please scan MAME ROMs and try again.')
                return

            # --- Read stdout and put into a string ---
            info_text = ''
            with open(PATHS.REPORT_MAME_SCAN_SAMP_PATH.getPath(), 'r') as myfile:
                info_text = myfile.read()

            # --- Show information window ---
            window_title = 'MAME samples scanner report'
            try:
                xbmc.executebuiltin('ActivateWindow(10147)')
                window = xbmcgui.Window(10147)
                xbmc.sleep(100)
                window.getControl(1).setLabel(window_title)
                window.getControl(5).setText(info_text)
            except:
                log_error('_command_view_machine() Exception rendering INFO window')

        # --- View Software Lists ROM scanner report ---
        type_nb += 1
        if type == type_nb:
            if not PATHS.REPORT_SL_SCAN_ROMS_PATH.exists():
                kodi_dialog_OK('SL ROM scanner report not found. Please scan MAME ROMs and try again.')
                return

            # --- Read stdout and put into a string ---
            info_text = ''
            with open(PATHS.REPORT_SL_SCAN_ROMS_PATH.getPath(), 'r') as myfile:
                info_text = myfile.read()

            # --- Show information window ---
            window_title = 'SL ROM scanner report'
            try:
                xbmc.executebuiltin('ActivateWindow(10147)')
                window = xbmcgui.Window(10147)
                xbmc.sleep(100)
                window.getControl(1).setLabel(window_title)
                window.getControl(5).setText(info_text)
            except:
                log_error('_command_view_machine() Exception rendering INFO window')

        # --- View Software Lists CHD scanner report ---
        type_nb += 1
        if type == type_nb:
            if not PATHS.REPORT_SL_SCAN_CHDS_PATH.exists():
                kodi_dialog_OK('SL CHD scanner report not found. Please scan MAME ROMs and try again.')
                return

            # --- Read stdout and put into a string ---
            info_text = ''
            with open(PATHS.REPORT_SL_SCAN_CHDS_PATH.getPath(), 'r') as myfile:
                info_text = myfile.read()

            # --- Show information window ---
            window_title = 'SL CHD scanner report'
            try:
                xbmc.executebuiltin('ActivateWindow(10147)')
                window = xbmcgui.Window(10147)
                xbmc.sleep(100)
                window.getControl(1).setLabel(window_title)
                window.getControl(5).setText(info_text)
            except:
                log_error('_command_view_machine() Exception rendering INFO window')

        # --- View MAME stdout/stderr ---
        type_nb += 1
        if type == type_nb:
            if not PATHS.MAME_OUTPUT_PATH.exists():
                kodi_dialog_OK('MAME output file not found. Execute MAME and try again.')
                return

            # --- Read stdout and put into a string ---
            info_text = ''
            with open(PATHS.MAME_OUTPUT_PATH.getPath(), 'r') as myfile:
                info_text = myfile.read()

            # --- Show information window ---
            window_title = 'MAME last execution output'
            try:
                xbmc.executebuiltin('ActivateWindow(10147)')
                window = xbmcgui.Window(10147)
                xbmc.sleep(100)
                window.getControl(1).setLabel(window_title)
                window.getControl(5).setText(info_text)
            except:
                log_error('_command_view_machine() Exception rendering INFO window')

    def _command_display_settings(self, clist, catalog, mname):
        log_debug('_command_display_settings() clist   "{0}"'.format(clist))
        log_debug('_command_display_settings() catalog "{0}"'.format(catalog))
        log_debug('_command_display_settings() mname   "{0}"'.format(mname))

        dialog = xbmcgui.Dialog()
        menu_item = dialog.select('Display settings',
                                 ['Display mode',
                                  'Default Icon',   'Default Fanart',
                                  'Default Banner', 'Default Poster',
                                  'Default Clearlogo'])
        if menu_item < 0: return
        kodi_dialog_OK('Not coded yet. Sorry')

    def _command_add_mame_fav(self, machine_name):
        log_debug('_command_add_mame_fav() Machine_name "{0}"'.format(machine_name))

        # >> Get Machine database entry
        kodi_busydialog_ON()
        MAME_db_dic     = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
        MAME_assets_dic = fs_load_JSON_file(PATHS.MAIN_ASSETS_DB_PATH.getPath())
        control_dic     = fs_load_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath())
        kodi_busydialog_OFF()
        machine = MAME_db_dic[machine_name]
        assets  = MAME_assets_dic[machine_name]

        # >> Open Favourite Machines dictionary
        fav_machines = fs_load_JSON_file(PATHS.FAV_MACHINES_PATH.getPath())
        
        # >> If machine already in Favourites ask user if overwrite.
        if machine_name in fav_machines:
            ret = kodi_dialog_yesno('Machine {0} ({1}) '.format(machine['description'], machine_name) +
                                    'already in MAME Favourites. Overwrite?')
            if ret < 1: return

        # >> Add machine. Add database version to Favourite.
        machine['assets'] = assets
        machine['mame_version'] = control_dic['mame_version']
        fav_machines[machine_name] = machine
        log_info('_command_add_mame_fav() Added machine "{0}"'.format(machine_name))

        # >> Save Favourites
        fs_write_JSON_file(PATHS.FAV_MACHINES_PATH.getPath(), fav_machines)
        kodi_notify('Machine {0} added to MAME Favourites'.format(machine_name))

    def _command_delete_mame_fav(self, machine_name):
        log_debug('_command_delete_mame_fav() Machine_name "{0}"'.format(machine_name))

        # >> Open Favourite Machines dictionary
        fav_machines = fs_load_JSON_file(PATHS.FAV_MACHINES_PATH.getPath())
        
        # >> Ask user for confirmation.
        ret = kodi_dialog_yesno('Delete Machine {0} ({1})?'.format(fav_machines[machine_name]['description'], machine_name))
        if ret < 1: return
        
        # >> Delete machine
        del fav_machines[machine_name]
        log_info('_command_delete_mame_fav() Deleted machine "{0}"'.format(machine_name))

        # >> Save Favourites
        fs_write_JSON_file(PATHS.FAV_MACHINES_PATH.getPath(), fav_machines)
        kodi_refresh_container()
        kodi_notify('Machine {0} deleted from MAME Favourites'.format(machine_name))

    def _command_show_mame_fav(self):
        log_debug('_command_show_mame_fav() Starting ...')

        # >> Open Favourite Machines dictionary
        fav_machines = fs_load_JSON_file(PATHS.FAV_MACHINES_PATH.getPath())

        # >> Render Favourites
        self._set_Kodi_all_sorting_methods()
        for m_name in fav_machines:
            machine = fav_machines[m_name]
            assets  = machine['assets']
            self._render_fav_machine_row(m_name, machine, assets)
        xbmcplugin.endOfDirectory(handle = self.addon_handle, succeeded = True, cacheToDisc = False)

    def _render_fav_machine_row(self, machine_name, machine, machine_assets):
        display_name = machine['description']

        # --- Mark Status ---
        status = '{0}{1}{2}{3}{4}'.format(machine['status_ROM'], machine['status_CHD'],
                                          machine['status_SAM'], machine['status_SL'],
                                          machine['status_Device'])
        display_name += ' [COLOR skyblue]{0}[/COLOR]'.format(status)

        # --- Mark Devices, BIOS and clones ---
        if machine['isDevice']: display_name += ' [COLOR violet][Dev][/COLOR]'
        if machine['isBIOS']:   display_name += ' [COLOR cyan][BIOS][/COLOR]'
        if machine['cloneof']:  display_name += ' [COLOR orange][Clo][/COLOR]'

        # --- Mark driver status: Good (no mark), Imperfect, Preliminar ---
        if   machine['driver_status'] == 'imperfect':   display_name += ' [COLOR yellow][Imp][/COLOR]'
        elif machine['driver_status'] == 'preliminary': display_name += ' [COLOR red][Pre][/COLOR]'

        # --- Assets/artwork ---
        thumb_path      = machine_assets['title']
        thumb_fanart    = machine_assets['snap']
        thumb_banner    = machine_assets['marquee']
        thumb_clearlogo = machine_assets['clearlogo']
        thumb_poster    = machine_assets['flyer']

        # --- Create listitem row ---
        default_icon = 'DefaultFolder.png'
        ICON_OVERLAY = 6
        listitem = xbmcgui.ListItem(display_name)

        # --- Metadata ---
        # >> Make all the infotables compatible with Advanced Emulator Launcher
        listitem.setInfo('video', {'title'   : display_name,            'year'    : machine['year'],
                                   'genre'   : '',                      'plot'    : '',
                                   'studio'  : machine['manufacturer'], 'rating'  : '',
                                   'trailer' : '',                      'overlay' : ICON_OVERLAY})
        listitem.setProperty('platform', 'MAME')

        # --- Assets ---
        # >> AEL custom artwork fields
        listitem.setArt({'title'     : machine_assets['title'],   'snap'    : machine_assets['snap'],
                         'boxfront'  : machine_assets['cabinet'], 'boxback' : machine_assets['cpanel'],
                         'cartridge' : machine_assets['PCB'],     'flyer'   : machine_assets['flyer'] })

        # >> Kodi official artwork fields
        listitem.setArt({'icon'   : thumb_path,   'fanart'    : thumb_fanart,
                         'banner' : thumb_banner, 'clearlogo' : thumb_clearlogo, 'poster' : thumb_poster })

        # --- Create context menu ---
        commands = []
        URL_view = self._misc_url_3_arg_RunPlugin('command', 'VIEW', 'machine', machine_name, 'location', LOCATION_MAME_FAVS)
        URL_manage = self._misc_url_2_arg_RunPlugin('command', 'MANAGE_MAME_FAV', 'machine', machine_name)
        URL_display = self._misc_url_2_arg_RunPlugin('command', 'DELETE_MAME_FAV', 'machine', machine_name)
        commands.append(('View',  URL_view ))
        commands.append(('Manage Favourite machines',  URL_manage ))
        commands.append(('Delete machine from Favourites', URL_display ))
        commands.append(('Kodi File Manager', 'ActivateWindow(filemanager)' ))
        commands.append(('Add-on Settings', 'Addon.OpenSettings({0})'.format(__addon_id__) ))
        listitem.addContextMenuItems(commands, replaceItems = True)

        # --- Add row ---
        URL = self._misc_url_3_arg('command', 'LAUNCH', 'machine', machine_name, 'location', 'MAME_FAV')
        xbmcplugin.addDirectoryItem(handle = self.addon_handle, url = URL, listitem = listitem, isFolder = False)

    def _command_manage_mame_fav(self, machine_name):
        dialog = xbmcgui.Dialog()
        idx = dialog.select('Manage MAME Favourites', 
                           ['Scan ROMs/CHDs/Samples',
                            'Scan assets/artwork',
                            'Check MAME Favourites'])
        if idx < 0: return

        # --- Scan ROMs/CHDs/Samples ---
        if idx == 0:
            # >> Check paths
            if not self.settings['rom_path']:
                kodi_dialog_OK('ROM directory not configured. Aborting.')
                return
            ROM_path_FN = FileName(self.settings['rom_path'])
            if not ROM_path_FN.isdir():
                kodi_dialog_OK('ROM directory does not exist. Aborting.')
                return

            scan_CHDs = False
            if self.settings['chd_path']:
                CHD_path_FN = FileName(self.settings['chd_path'])
                if not CHD_path_FN.isdir():
                    kodi_dialog_OK('CHD directory does not exist. CHD scanning disabled.')
                else:
                    scan_CHDs = True
            else:
                kodi_dialog_OK('CHD directory not configured. CHD scanning disabled.')
                CHD_path_FN = FileName('')

            scan_Samples = False
            if self.settings['samples_path']:
                Samples_path_FN = FileName(self.settings['samples_path'])
                if not Samples_path_FN.isdir():
                    kodi_dialog_OK('Samples directory does not exist. Samples scanning disabled.')
                else:
                    scan_Samples = True
            else:
                kodi_dialog_OK('Samples directory not configured. Samples scanning disabled.')
                Samples_path_FN = FileName('')

            # >> Load database
            # >> Create a fake control_dic for the FAV MAME ROMs
            fav_machines = fs_load_JSON_file(PATHS.FAV_MACHINES_PATH.getPath())
            control_dic = fs_new_control_dic()
            fs_scan_MAME_ROMs(PATHS, fav_machines, control_dic, ROM_path_FN, CHD_path_FN, Samples_path_FN, scan_CHDs, scan_Samples)

            # >> Save updated database
            fs_write_JSON_file(PATHS.FAV_MACHINES_PATH.getPath(), fav_machines)
            kodi_refresh_container()
            kodi_notify('Scanning of MAME Favourites finished')

        # --- Scan assets/artwork ---
        elif idx == 1:
            kodi_dialog_OK('Check this code. I think is wrong. Data must be in machine["assets"]')

            # >> Get assets directory. Abort if not configured/found.
            if not self.settings['assets_path']:
                kodi_dialog_OK('Asset directory not configured. Aborting.')
                return
            Asset_path_FN = FileName(self.settings['assets_path'])
            if not Asset_path_FN.isdir():
                kodi_dialog_OK('Asset directory does not exist. Aborting.')
                return

            fav_machines = fs_load_JSON_file(PATHS.FAV_MACHINES_PATH.getPath())
            pDialog = xbmcgui.DialogProgress()
            pDialog_canceled = False
            pDialog.create('Advanced MAME Launcher', 'Scanning MAME assets/artwork...')
            total_machines = len(fav_machines)
            processed_machines = 0
            assets_dic = {}
            for key in sorted(fav_machines):
                machine = fav_machines[key]
                for idx, asset_key in enumerate(ASSET_MAME_KEY_LIST):
                    asset_FN = Asset_path_FN.pjoin(ASSET_MAME_PATH_LIST[idx]).pjoin(key + '.png')
                    if asset_FN.exists(): machine[asset_key] = asset_FN.getOriginalPath()
                    else:                 machine[asset_key] = ''
                processed_machines = processed_machines + 1
                pDialog.update(100 * processed_machines / total_machines)
            pDialog.close()
            fs_write_JSON_file(PATHS.FAV_MACHINES_PATH.getPath(), fav_machines)
            kodi_notify('Scanning of MAME Favourite Assets finished')

        # --- Check Favourites ---
        # >> Check if Favourites can be found in current MAME main database. It may happen that
        # >> a machine is renamed between MAME version although I think this is very unlikely.
        # >> MAME Favs can not be relinked. If the machine is not found in current database it must
        # >> be deleted by the user and a new Favourite created.
        elif idx == 2:
            # >> Now just report if a machine is not found in main DB.
            kodi_busydialog_ON()
            machines     = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
            fav_machines = fs_load_JSON_file(PATHS.FAV_MACHINES_PATH.getPath())
            kodi_busydialog_OFF()
            for fav_key in sorted(fav_machines):
                log_debug('Checking Favourite "{0}"'.format(fav_key))
                if fav_key not in machines:
                    t = 'Favourite machine "{0}" not found in database'
                    kodi_dialog_OK(t.format(fav_key))
            kodi_notify('MAME Favourite checked')

    def _command_add_sl_fav(self, SL_name, ROM_name):
        log_debug('_command_add_sl_fav() SL_name  "{0}"'.format(SL_name))
        log_debug('_command_add_sl_fav() ROM_name "{0}"'.format(ROM_name))

        # >> Get Machine database entry
        kodi_busydialog_ON()
        control_dic = fs_load_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath())
        SL_catalog_dic = fs_load_JSON_file(PATHS.SL_INDEX_PATH.getPath())
        file_name =  SL_catalog_dic[SL_name]['rom_DB_noext'] + '.json'
        SL_DB_FN = PATHS.SL_DB_DIR.pjoin(file_name)
        SL_roms = fs_load_JSON_file(SL_DB_FN.getPath())
        kodi_busydialog_OFF()
        ROM = SL_roms[ROM_name]

        # >> Open Favourite Machines dictionary
        fav_SL_roms = fs_load_JSON_file(PATHS.FAV_SL_ROMS_PATH.getPath())
        SL_fav_key = SL_name + '-' + ROM_name
        log_debug('_command_add_sl_fav() SL_fav_key "{0}"'.format(SL_fav_key))
        
        # >> If machine already in Favourites ask user if overwrite.
        if SL_fav_key in fav_SL_roms:
            ret = kodi_dialog_yesno('Machine {0} ({1}) '.format(ROM_name, SL_name) +
                                    'already in SL Favourites. Overwrite?')
            if ret < 1: return

        # >> Add machine.
        ROM['ROM_name'] = ROM_name
        ROM['SL_name']  = SL_name
        ROM['mame_version'] = control_dic['mame_version']
        fav_SL_roms[SL_fav_key] = ROM
        log_info('_command_add_sl_fav() Added machine "{0}" ("{1}")'.format(ROM_name, SL_name))

        # >> Save Favourites
        fs_write_JSON_file(PATHS.FAV_SL_ROMS_PATH.getPath(), fav_SL_roms)
        kodi_notify('ROM {0} added to SL Favourite ROMs'.format(ROM_name))

    def _command_delete_sl_fav(self, SL_name, ROM_name):
        log_debug('_command_delete_sl_fav() SL_name  "{0}"'.format(SL_name))
        log_debug('_command_delete_sl_fav() ROM_name "{0}"'.format(ROM_name))

        # >> Get Machine database entry
        kodi_busydialog_ON()
        SL_catalog_dic = fs_load_JSON_file(PATHS.SL_INDEX_PATH.getPath())
        file_name =  SL_catalog_dic[SL_name]['rom_DB_noext'] + '.json'
        SL_DB_FN = PATHS.SL_DB_DIR.pjoin(file_name)
        SL_roms = fs_load_JSON_file(SL_DB_FN.getPath())
        kodi_busydialog_OFF()
        ROM = SL_roms[ROM_name]
        
        # >> Open Favourite Machines dictionary
        fav_SL_roms = fs_load_JSON_file(PATHS.FAV_SL_ROMS_PATH.getPath())
        SL_fav_key = SL_name + '-' + ROM_name
        log_debug('_command_delete_sl_fav() SL_fav_key "{0}"'.format(SL_fav_key))
        
        # >> Ask user for confirmation.
        ret = kodi_dialog_yesno('Delete Machine {0} ({1})?'.format(ROM_name, SL_name))
        if ret < 1: return

        # >> Delete machine
        del fav_SL_roms[SL_fav_key]
        log_info('_command_delete_sl_fav() Deleted machine {0} ({1})'.format(ROM_name, SL_name))

        # >> Save Favourites
        fs_write_JSON_file(PATHS.FAV_SL_ROMS_PATH.getPath(), fav_SL_roms)
        kodi_refresh_container()
        kodi_notify('ROM {0} deleted from SL Favourites'.format(ROM_name))

    def _command_show_sl_fav(self):
        log_debug('_command_show_sl_fav() Starting ...')

        # >> Open Favourite Machines dictionary
        fav_SL_roms = fs_load_JSON_file(PATHS.FAV_SL_ROMS_PATH.getPath())

        # >> Render Favourites
        self._set_Kodi_all_sorting_methods()
        for SL_fav_key in fav_SL_roms:
            SL_fav_ROM = fav_SL_roms[SL_fav_key]
            self._render_sl_fav_machine_row(SL_fav_key, SL_fav_ROM)
        xbmcplugin.endOfDirectory(handle = self.addon_handle, succeeded = True, cacheToDisc = False)

    def _render_sl_fav_machine_row(self, SL_fav_key, ROM):
        SL_name  = ROM['SL_name']
        ROM_name = ROM['ROM_name']
        display_name = ROM['description']

        # --- Mark Status and Clones ---
        status = '{0}{1}'.format(ROM['status_ROM'], ROM['status_CHD'])
        display_name += ' [COLOR skyblue]{0}[/COLOR]'.format(status)
        if ROM['cloneof']:  display_name += ' [COLOR orange][Clo][/COLOR]'

        # --- Create listitem row ---
        icon = 'DefaultFolder.png'
        listitem = xbmcgui.ListItem(display_name, iconImage = icon)
        ICON_OVERLAY = 6
        # listitem.setProperty('fanart_image', category_dic['fanart'])
        listitem.setInfo('video', {'title'   : display_name,     'year'    : ROM['year'],
                                   'studio'  : ROM['publisher'], 'overlay' : ICON_OVERLAY })

        # --- Create context menu ---
        commands = []
        URL_view    = self._misc_url_4_arg_RunPlugin('command', 'VIEW', 'SL', SL_name, 'ROM', ROM_name, 'location', LOCATION_SL_FAVS)
        URL_display = self._misc_url_2_arg_RunPlugin('command', 'DISPLAY_SETTINGS_SL', 'SL', SL_name)
        URL_manage  = self._misc_url_3_arg_RunPlugin('command', 'MANAGE_SL_FAV', 'SL', SL_name, 'ROM', ROM_name)
        URL_fav     = self._misc_url_3_arg_RunPlugin('command', 'DELETE_SL_FAV', 'SL', SL_name, 'ROM', ROM_name)
        commands.append(('View', URL_view ))
        commands.append(('Display settings', URL_display ))
        commands.append(('Manage SL Favourite machines',  URL_manage ))
        commands.append(('Delete ROM from SL Favourites', URL_fav ))
        commands.append(('Kodi File Manager', 'ActivateWindow(filemanager)' ))
        commands.append(('Add-on Settings', 'Addon.OpenSettings({0})'.format(__addon_id__) ))
        listitem.addContextMenuItems(commands, replaceItems = True)

        # --- Add row ---
        URL = self._misc_url_3_arg('command', 'LAUNCH_SL', 'SL', SL_name, 'ROM', ROM_name)
        xbmcplugin.addDirectoryItem(handle = self.addon_handle, url = URL, listitem = listitem, isFolder = False)

    def _command_manage_sl_fav(self, SL_name, ROM_name):
        dialog = xbmcgui.Dialog()
        idx = dialog.select('Manage Software Lists Favourites', 
                           ['Scan ROMs/CHDs',
                            'Scan assets/artwork',
                            'Check SL Favourites'])
        if idx < 0: return

        # --- Scan ROMs/CHDs ---
        # Reuse SL scanner for Favourites
        if idx == 0:
            kodi_dialog_OK('SL scanner not coded yet. Sorry.')

        # --- Scan assets/artwork ---
        # Reuse SL scanner for Favourites
        elif idx == 1:
            kodi_dialog_OK('SL asset scanner not coded yet. Sorry.')

        # --- Check SL Favourties ---
        elif idx == 2:
            kodi_dialog_OK('Check not coded yet. Sorry.')
            
    def _command_display_settings_SL(self, SL_name):
        log_debug('_command_display_settings_SL() SL_name "{0}"'.format(SL_name))

        # --- Load properties DB ---
        SL_properties_dic = fs_load_JSON_file(PATHS.SL_MACHINES_PROP_PATH.getPath())
        prop_dic = SL_properties_dic[SL_name]

        # --- Show menu ---
        view_mode_str = 'Normal' if prop_dic['view_mode'] == VIEW_MODE_NORMAL else 'PClone'
        dialog = xbmcgui.Dialog()
        menu_item = dialog.select('Display mode: {0}'.format(view_mode_str),
                                 ['Display mode', 'Default Icon', 'Default Fanart', 
                                  'Default Banner', 'Default Poster', 'Default Clearlogo'])
        if menu_item < 0: return

        # --- Change display mode ---
        if menu_item == 0:
            if prop_dic['view_mode'] == VIEW_MODE_NORMAL:
                item_list = ['Normal mode [Current]', 'PClone mode']
            else:
                item_list = ['Normal mode', 'PClone mode [Current]']
            # >> Use new Krypton feature to preselect current item on select dialog
            type_temp = dialog.select('Manage Items List', item_list)
            if type_temp < 0: return
            # SL_properties_dic is automatically updated because prop_dic references there.
            if type_temp == 0:
                prop_dic['view_mode'] = VIEW_MODE_NORMAL
                kodi_notify('SL display mode set to Normal')
            elif type_temp == 1:
                prop_dic['view_mode'] = VIEW_MODE_PCLONE
                kodi_notify('SL display mode set to PClone')

        # --- Change default icon ---
        elif menu_item == 1:
            kodi_dialog_OK('Not coded yet. Sorry')

        # --- Save display settings ---
        fs_write_JSON_file(PATHS.SL_MACHINES_PROP_PATH.getPath(), SL_properties_dic)

    # ---------------------------------------------------------------------------------------------
    # Setup plugin databases
    # ---------------------------------------------------------------------------------------------
    def _command_setup_plugin(self):
        dialog = xbmcgui.Dialog()
        menu_item = dialog.select('Setup plugin',
                                 ['Extract MAME.xml ...',
                                  'Build all databases ...',
                                  'Scan everything ...',
                                  'Build MAME database ...',
                                  'Build MAME catalogs ...',
                                  'Build Software Lists indices and catalogs ...',
                                  'Scan MAME ROMs/CHDs/Samples ...',
                                  'Scan MAME assets/artwork ...',
                                  'Scan Software Lists ROMs/CHDs ...',
                                  'Scan Software Lists assets/artwork ...' ])
        if menu_item < 0: return

        # --- Extract MAME.xml ---
        if menu_item == 0:
            if not self.settings['mame_prog']:
                kodi_dialog_OK('MAME executable is not set.')
                return
            mame_prog_FN = FileName(self.settings['mame_prog'])

            # --- Extract MAME XML ---
            (filesize, total_machines) = fs_extract_MAME_XML(PATHS, mame_prog_FN)
            kodi_dialog_OK('Extracted MAME XML database. '
                           'Size is {0} MB and there are {1} machines.'.format(filesize / 1000000, total_machines))

        # --- Build everything ---
        elif menu_item == 1:
            if not PATHS.MAME_XML_PATH.exists():
                kodi_dialog_OK('MAME XML not found. Execute "Extract MAME.xml" first.')
                return

            # --- Build all databases ---
            control_dic = fs_load_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath())
            fs_build_MAME_main_database(PATHS, self.settings, control_dic)
            kodi_busydialog_ON()
            machines        = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
            main_pclone_dic = fs_load_JSON_file(PATHS.MAIN_PCLONE_DIC_PATH.getPath())
            kodi_busydialog_OFF()
            fs_build_MAME_indices_and_catalogs(PATHS, machines, main_pclone_dic)
            fs_build_SoftwareLists_index(PATHS, self.settings, machines, main_pclone_dic, control_dic)
            kodi_notify('All databases built')

        # --- Scan everything ---
        elif menu_item == 2:
            log_info('_command_setup_plugin() Scanning everything ...')

            # --- MAME Machines -------------------------------------------------------------------
            # NOTE Here only check for abort conditions. Optinal conditions must be check
            #      inside the function.
            # >> Get paths and check they exist
            if not self.settings['rom_path']:
                kodi_dialog_OK('ROM directory not configured. Aborting.')
                return
            ROM_path_FN = FileName(self.settings['rom_path'])
            if not ROM_path_FN.isdir():
                kodi_dialog_OK('ROM directory does not exist. Aborting.')
                return

            scan_CHDs = False
            if self.settings['chd_path']:
                CHD_path_FN = FileName(self.settings['chd_path'])
                if not CHD_path_FN.isdir():
                    kodi_dialog_OK('CHD directory does not exist. CHD scanning disabled.')
                else:
                    scan_CHDs = True
            else:
                kodi_dialog_OK('CHD directory not configured. CHD scanning disabled.')
                CHD_path_FN = FileName('')

            scan_Samples = False
            if self.settings['samples_path']:
                Samples_path_FN = FileName(self.settings['samples_path'])
                if not Samples_path_FN.isdir():
                    kodi_dialog_OK('Samples directory does not exist. Samples scanning disabled.')
                else:
                    scan_Samples = True
            else:
                kodi_dialog_OK('Samples directory not configured. Samples scanning disabled.')
                Samples_path_FN = FileName('')

            # >> Load machine database and control_dic
            kodi_busydialog_ON()
            machines    = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
            control_dic = fs_load_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath())
            kodi_busydialog_OFF()
            fs_scan_MAME_ROMs(PATHS, machines, control_dic, ROM_path_FN, CHD_path_FN, Samples_path_FN, scan_CHDs, scan_Samples)

            # >> Get assets directory. Abort if not configured/found.
            do_MAME_asset_scan = True
            if not self.settings['assets_path']:
                kodi_dialog_OK('Asset directory not configured. Aborting.')
                do_MAME_asset_scan = False
            Asset_path_FN = FileName(self.settings['assets_path'])
            if not Asset_path_FN.isdir():
                kodi_dialog_OK('Asset directory does not exist. Aborting.')
                do_MAME_asset_scan = False

            if do_MAME_asset_scan: fs_scan_MAME_assets(PATHS, machines, Asset_path_FN)

            kodi_busydialog_ON()
            fs_write_JSON_file(PATHS.MAIN_DB_PATH.getPath(), machines)
            fs_write_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath(), control_dic)
            kodi_busydialog_OFF()

            # --- Software Lists ------------------------------------------------------------------
            # >> Abort if SL hash path not configured.
            do_SL_ROM_scan = True
            if not self.settings['SL_hash_path']:
                kodi_dialog_OK('Software Lists hash path not set. Scanning aborted.')
                do_SL_ROM_scan = False
            SL_hash_dir_FN = PATHS.SL_DB_DIR
            log_info('_command_setup_plugin() SL hash dir OP {0}'.format(SL_hash_dir_FN.getOriginalPath()))
            log_info('_command_setup_plugin() SL hash dir  P {0}'.format(SL_hash_dir_FN.getPath()))

            # >> Abort if SL ROM dir not configured.
            if not self.settings['SL_rom_path']:
                kodi_dialog_OK('Software Lists ROM path not set. Scanning aborted.')
                do_SL_ROM_scan = False
            SL_ROM_dir_FN = FileName(self.settings['SL_rom_path'])
            log_info('_command_setup_plugin() SL ROM dir OP {0}'.format(SL_ROM_dir_FN.getOriginalPath()))
            log_info('_command_setup_plugin() SL ROM dir  P {0}'.format(SL_ROM_dir_FN.getPath()))

            # >> Load SL catalog
            SL_catalog_dic = fs_load_JSON_file(PATHS.SL_INDEX_PATH.getPath())            
            control_dic    = fs_load_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath())
            if do_SL_ROM_scan: fs_scan_SL_ROMs(PATHS, SL_catalog_dic, control_dic, SL_hash_dir_FN, SL_ROM_dir_FN)

            # >> Get assets directory. Abort if not configured/found.
            do_SL_asset_scan = True
            if not self.settings['assets_path']:
                kodi_dialog_OK('Asset directory not configured. Aborting.')
                do_SL_asset_scan = False
            Asset_path_FN = FileName(self.settings['assets_path'])
            if not Asset_path_FN.isdir():
                kodi_dialog_OK('Asset directory does not exist. Aborting.')
                do_SL_asset_scan = False

            if do_SL_asset_scan: fs_scan_SL_assets(PATHS, SL_catalog_dic, Asset_path_FN)

            # --- All operations finished ---
            kodi_notify('All ROM/asset scanning finished')

        # --- Build main MAME database and PClone list ---
        elif menu_item == 3:
            # --- Error checks ---
            # >> Check that MAME_XML_PATH exists
            if not PATHS.MAME_XML_PATH.exists():
                kodi_dialog_OK('MAME XML not found. Execute "Extract MAME.xml" first.')
                return

            # --- Parse MAME XML and generate main database and PClone list ---
            control_dic = fs_load_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath())
            log_info('_command_setup_plugin() Generating MAME main database and PClone list...')
            fs_build_MAME_main_database(PATHS, self.settings, control_dic)
            kodi_notify('Main MAME database built')

        # --- Build MAME catalogs ---
        elif menu_item == 4:
            # --- Error checks ---
            # >> Check that main MAME database exists

            # --- Read main database and control dic ---
            kodi_busydialog_ON()
            machines        = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
            main_pclone_dic = fs_load_JSON_file(PATHS.MAIN_PCLONE_DIC_PATH.getPath())
            kodi_busydialog_OFF()
            fs_build_MAME_catalogs(PATHS, machines, main_pclone_dic)
            kodi_notify('Indices and catalogs built')

        # --- Build Software Lists indices/catalogs ---
        elif menu_item == 5:
            # --- Error checks ---
            if not self.settings['SL_hash_path']:
                kodi_dialog_OK('Software Lists hash path not set.')
                return

            # --- Read main database and control dic ---
            kodi_busydialog_ON()
            machines        = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
            main_pclone_dic = fs_load_JSON_file(PATHS.MAIN_PCLONE_DIC_PATH.getPath())
            control_dic     = fs_load_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath())
            kodi_busydialog_OFF()
            fs_build_SoftwareLists_index(PATHS, self.settings, machines, main_pclone_dic, control_dic)
            kodi_notify('Software Lists indices and catalogs built')

        # --- Scan ROMs/CHDs/Samples and updates ROM status ---
        elif menu_item == 6:
            log_info('_command_setup_plugin() Scanning MAME ROMs/CHDs/Samples ...')

            # >> Get paths and check they exist
            if not self.settings['rom_path']:
                kodi_dialog_OK('ROM directory not configured. Aborting.')
                return
            ROM_path_FN = FileName(self.settings['rom_path'])
            if not ROM_path_FN.isdir():
                kodi_dialog_OK('ROM directory does not exist. Aborting.')
                return

            scan_CHDs = False
            if self.settings['chd_path']:
                CHD_path_FN = FileName(self.settings['chd_path'])
                if not CHD_path_FN.isdir():
                    kodi_dialog_OK('CHD directory does not exist. CHD scanning disabled.')
                else:
                    scan_CHDs = True
            else:
                kodi_dialog_OK('CHD directory not configured. CHD scanning disabled.')
                CHD_path_FN = FileName('')

            scan_Samples = False
            if self.settings['samples_path']:
                Samples_path_FN = FileName(self.settings['samples_path'])
                if not Samples_path_FN.isdir():
                    kodi_dialog_OK('Samples directory does not exist. Samples scanning disabled.')
                else:
                    scan_Samples = True
            else:
                kodi_dialog_OK('Samples directory not configured. Samples scanning disabled.')
                Samples_path_FN = FileName('')

            # >> Load machine database and control_dic and scan
            kodi_busydialog_ON()
            machines    = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
            control_dic = fs_load_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath())
            kodi_busydialog_OFF()
            fs_scan_MAME_ROMs(PATHS, machines, control_dic, ROM_path_FN, CHD_path_FN, Samples_path_FN, scan_CHDs, scan_Samples)
            kodi_busydialog_ON()
            fs_write_JSON_file(PATHS.MAIN_DB_PATH.getPath(), machines)
            fs_write_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath(), control_dic)
            kodi_busydialog_OFF()
            kodi_notify('Scanning of ROMs, CHDs and Samples finished')

        # --- Scans MAME assets/artwork ---
        elif menu_item == 7:
            log_info('_command_setup_plugin() Scanning MAME assets/artwork ...')

            # >> Get assets directory. Abort if not configured/found.
            if not self.settings['assets_path']:
                kodi_dialog_OK('Asset directory not configured. Aborting.')
                return
            Asset_path_FN = FileName(self.settings['assets_path'])
            if not Asset_path_FN.isdir():
                kodi_dialog_OK('Asset directory does not exist. Aborting.')
                return

            # >> Load machine database and scan
            kodi_busydialog_ON()
            machines = fs_load_JSON_file(PATHS.MAIN_DB_PATH.getPath())
            kodi_busydialog_OFF()
            fs_scan_MAME_assets(PATHS, machines, Asset_path_FN)
            kodi_notify('Scanning of assets/artwork finished')

        # --- Scan SL ROMs ---
        elif menu_item == 8:
            log_info('_command_setup_plugin() Scanning SL ROMs/CHDs ...')

            # >> Abort if SL hash path not configured.
            if not self.settings['SL_hash_path']:
                kodi_dialog_OK('Software Lists hash path not set. Scanning aborted.')
                return
            SL_hash_dir_FN = PATHS.SL_DB_DIR
            log_info('_command_setup_plugin() SL hash dir OP {0}'.format(SL_hash_dir_FN.getOriginalPath()))
            log_info('_command_setup_plugin() SL hash dir  P {0}'.format(SL_hash_dir_FN.getPath()))

            # >> Abort if SL ROM dir not configured.
            if not self.settings['SL_rom_path']:
                kodi_dialog_OK('Software Lists ROM path not set. Scanning aborted.')
                return
            SL_ROM_dir_FN = FileName(self.settings['SL_rom_path'])
            log_info('_command_setup_plugin() SL ROM dir OP {0}'.format(SL_ROM_dir_FN.getOriginalPath()))
            log_info('_command_setup_plugin() SL ROM dir  P {0}'.format(SL_ROM_dir_FN.getPath()))

            # >> Load SL and scan
            SL_catalog_dic = fs_load_JSON_file(PATHS.SL_INDEX_PATH.getPath())            
            control_dic    = fs_load_JSON_file(PATHS.MAIN_CONTROL_PATH.getPath())
            fs_scan_SL_ROMs(PATHS, SL_catalog_dic, control_dic, SL_hash_dir_FN, SL_ROM_dir_FN)
            kodi_notify('Scanning of SL ROMs finished')

        # --- Scan SL assets/artwork ---
        # >> Database format: ADDON_DATA_DIR/db_SoftwareLists/32x_assets.json
        # >> { 'ROM_name' : {'asset1' : 'path', 'asset2' : 'path', ... }, ... }
        elif menu_item == 9:
            log_info('_command_setup_plugin() Scanning SL assets/artwork ...')

            # >> Get assets directory. Abort if not configured/found.
            if not self.settings['assets_path']:
                kodi_dialog_OK('Asset directory not configured. Aborting.')
                return
            Asset_path_FN = FileName(self.settings['assets_path'])
            if not Asset_path_FN.isdir():
                kodi_dialog_OK('Asset directory does not exist. Aborting.')
                return

            # >> Load SL database and scan
            kodi_busydialog_ON()
            SL_catalog_dic = fs_load_JSON_file(PATHS.SL_INDEX_PATH.getPath())
            kodi_busydialog_OFF()
            fs_scan_SL_assets(PATHS, SL_catalog_dic, Asset_path_FN)
            kodi_notify('Scanning of SL assets finished')

    #
    # Launch MAME machine. Syntax: $ mame <machine_name> [options]
    # Example: $ mame dino
    #
    def _run_machine(self, machine_name, location):
        log_info('_run_machine() Launching MAME machine  "{0}"'.format(machine_name))
        log_info('_run_machine() Launching MAME location "{0}"'.format(location))

        # >> If launching from Favourites read ROM from Fav database
        if location and location == 'MAME_FAV':
            fav_machines = fs_load_JSON_file(PATHS.FAV_MACHINES_PATH.getPath())
            machine = fav_machines[machine_name]
            assets  = machine['assets']

        # >> Get paths
        mame_prog_FN = FileName(self.settings['mame_prog'])

        # >> Check if ROM exist
        if not self.settings['rom_path']:
            kodi_dialog_OK('ROM directory not configured.')
            return
        ROM_path_FN = FileName(self.settings['rom_path'])
        if not ROM_path_FN.isdir():
            kodi_dialog_OK('ROM directory does not exist.')
            return
        ROM_FN = ROM_path_FN.pjoin(machine_name + '.zip')
        # if not ROM_FN.exists():
        #     kodi_dialog_OK('ROM "{0}" not found.'.format(ROM_FN.getBase()))
        #     return

        # >> Choose BIOS (only available for Favourite Machines)
        if location and location == 'MAME_FAV' and len(machine['bios_name']) > 1:
            dialog = xbmcgui.Dialog()
            m_index = dialog.select('Select BIOS', machine['bios_desc'])
            if m_index < 0: return
            BIOS_name = machine['bios_name'][m_index]
        else:
            BIOS_name = ''

        # >> Launch machine using subprocess module
        (mame_dir, mame_exec) = os.path.split(mame_prog_FN.getPath())
        log_info('_run_machine() mame_prog_FN "{0}"'.format(mame_prog_FN.getPath()))    
        log_info('_run_machine() mame_dir     "{0}"'.format(mame_dir))
        log_info('_run_machine() mame_exec    "{0}"'.format(mame_exec))
        log_info('_run_machine() machine_name "{0}"'.format(machine_name))
        log_info('_run_machine() BIOS_name    "{0}"'.format(BIOS_name))

        # >> Prevent a console window to be shown in Windows. Not working yet!
        if sys.platform == 'win32':
            log_info('_run_machine() Platform is win32. Creating _info structure')
            _info = subprocess.STARTUPINFO()
            _info.dwFlags = subprocess.STARTF_USESHOWWINDOW
            # See https://msdn.microsoft.com/en-us/library/ms633548(v=vs.85).aspx
            # See https://docs.python.org/2/library/subprocess.html#subprocess.STARTUPINFO
            # >> SW_HIDE = 0
            # >> Does not work: MAME console window is not shown, graphical window not shonw either,
            # >> process run in background.
            # _info.wShowWindow = subprocess.SW_HIDE
            # >> SW_SHOWMINIMIZED = 2
            # >> Both MAME console and graphical window minimized.
            # _info.wShowWindow = 2
            # >> SW_SHOWNORMAL = 1
            # >> MAME console window is shown, MAME graphical window on top, Kodi on bottom.
            _info.wShowWindow = 1
        else:
            log_info('_run_machine() _info is None')
            _info = None

        # >> Launch MAME
        # arg_list = [mame_prog_FN.getPath(), '-window', machine_name]
        if BIOS_name: arg_list = [mame_prog_FN.getPath(), machine_name, '-bios', BIOS_name]
        else:         arg_list = [mame_prog_FN.getPath(), machine_name]
        log_info('arg_list = {0}'.format(arg_list))
        log_info('_run_machine() Calling subprocess.Popen()...')
        with open(PATHS.MAME_OUTPUT_PATH.getPath(), 'wb') as f:
            p = subprocess.Popen(arg_list, cwd = mame_dir, startupinfo = _info, stdout = f, stderr = subprocess.STDOUT)
        p.wait()
        log_info('_run_machine() Exiting function')

    #
    # Launch SL machine. See http://docs.mamedev.org/usingmame/usingmame.html
    # Syntax: $ mame <system> <software> [options]
    # Example: $ mame smspal sonic
    # Requirements:
    #   A) machine_name
    #   B) media_name
    #
    # Software list <part> tag has an interface attribute that tells how to virtually plug the
    # cartridge/cassete/disk/etc. There is not need to media type in MAME commandline.
    #
    def _run_SL_machine(self, SL_name, ROM_name):
        log_info('_run_SL_machine() Launching SL machine ...')

        # >> Get paths
        mame_prog_FN = FileName(self.settings['mame_prog'])

        # >> Get a list of machines that can launch this SL ROM. User chooses.
        SL_machines_dic = fs_load_JSON_file(PATHS.SL_MACHINES_PATH.getPath())
        SL_machine_list = SL_machines_dic[SL_name]
        SL_machine_names_list = []
        SL_machine_desc_list = []
        # SL_machine_device_props_list = []
        for SL_machine in SL_machine_list: 
            SL_machine_names_list.append(SL_machine['machine'])
            SL_machine_desc_list.append(SL_machine['description'])
            # SL_machine_device_props_list.append(SL_machine['device_props'])
        dialog = xbmcgui.Dialog()
        m_index = dialog.select('Select machine', SL_machine_desc_list)
        if m_index < 0: return
        machine_name = SL_machine_names_list[m_index]
        machine_desc = SL_machine_desc_list[m_index]

        # >> Select media if more than one device instance
        # >> Not necessary. MAME knows what media to plug the SL ROM into.
        # if len(SL_machine_device_props_list[m_index]) > 1:
        #     device_names_list = []
        #     for device in SL_machine_device_props_list[m_index]: device_names_list.append(device['name'])
        #     dialog = xbmcgui.Dialog()
        #     d_index = dialog.select('Select device', device_names_list)
        #     if d_index < 0: return
        #     media_name = SL_machine_device_props_list[m_index][d_index]['name']
        # else:
        #     media_name = SL_machine_device_props_list[m_index][0]['name']

        # >> Launch machine using subprocess module
        (mame_dir, mame_exec) = os.path.split(mame_prog_FN.getPath())
        log_info('_run_SL_machine() mame_prog_FN "{0}"'.format(mame_prog_FN.getPath()))    
        log_info('_run_SL_machine() mame_dir     "{0}"'.format(mame_dir))
        log_info('_run_SL_machine() mame_exec    "{0}"'.format(mame_exec))
        log_info('_run_SL_machine() machine_name "{0}"'.format(machine_name))
        log_info('_run_SL_machine() machine_desc "{0}"'.format(machine_desc))
        # log_info('_run_SL_machine() media_name   "{0}"'.format(media_name))
        log_info('_run_SL_machine() SL_name      "{0}"'.format(SL_name))
        log_info('_run_SL_machine() ROM_name     "{0}"'.format(ROM_name))

        # >> Prevent a console window to be shown in Windows. Not working yet!
        if sys.platform == 'win32':
            log_info('_run_SL_machine() Platform is win32. Creating _info structure')
            _info = subprocess.STARTUPINFO()
            _info.dwFlags = subprocess.STARTF_USESHOWWINDOW
            _info.wShowWindow = 1
        else:
            log_info('_run_SL_machine() _info is None')
            _info = None

        # >> Launch MAME
        # arg_list = [mame_prog_FN.getPath(), machine_name, '-{0}'.format(media_name), ROM_name]
        arg_list = [mame_prog_FN.getPath(), machine_name, ROM_name]
        log_info('arg_list = {0}'.format(arg_list))
        log_info('_run_SL_machine() Calling subprocess.Popen()...')
        with open(PATHS.MAME_OUTPUT_PATH.getPath(), 'wb') as f:
            p = subprocess.Popen(arg_list, cwd = mame_dir, startupinfo = _info, stdout = f, stderr = subprocess.STDOUT)
        p.wait()
        log_info('_run_SL_machine() Exiting function')

    # ---------------------------------------------------------------------------------------------
    # Misc functions
    # ---------------------------------------------------------------------------------------------
    # List of sorting methods here http://mirrors.xbmc.org/docs/python-docs/16.x-jarvis/xbmcplugin.html#-setSetting
    def _set_Kodi_all_sorting_methods(self):
        if self.addon_handle < 0: return
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_FOLDERS)
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_STUDIO)
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_GENRE)
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)

    def _set_Kodi_all_sorting_methods_and_size(self):
        if self.addon_handle < 0: return
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_FOLDERS)
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_STUDIO)
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_GENRE)
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_SIZE)
        xbmcplugin.addSortMethod(handle=self.addon_handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)

    # ---------------------------------------------------------------------------------------------
    # Misc URL building functions
    # ---------------------------------------------------------------------------------------------
    #
    # Used in xbmcplugin.addDirectoryItem()
    #
    def _misc_url_1_arg(self, arg_name, arg_value):
        arg_value_escaped = arg_value.replace('&', '%26')

        return '{0}?{1}={2}'.format(self.base_url, arg_name, arg_value_escaped)

    def _misc_url_2_arg(self, arg_name_1, arg_value_1, arg_name_2, arg_value_2):
        # >> Escape '&' in URLs
        arg_value_1_escaped = arg_value_1.replace('&', '%26')
        arg_value_2_escaped = arg_value_2.replace('&', '%26')

        return '{0}?{1}={2}&{3}={4}'.format(self.base_url, 
                                            arg_name_1, arg_value_1_escaped,
                                            arg_name_2, arg_value_2_escaped)

    def _misc_url_3_arg(self, arg_name_1, arg_value_1, arg_name_2, arg_value_2, arg_name_3, arg_value_3):
        arg_value_1_escaped = arg_value_1.replace('&', '%26')
        arg_value_2_escaped = arg_value_2.replace('&', '%26')
        arg_value_3_escaped = arg_value_3.replace('&', '%26')

        return '{0}?{1}={2}&{3}={4}&{5}={6}'.format(self.base_url,
                                                    arg_name_1, arg_value_1_escaped,
                                                    arg_name_2, arg_value_2_escaped,
                                                    arg_name_3, arg_value_3_escaped)

    #
    # Used in context menus
    #
    def _misc_url_1_arg_RunPlugin(self, arg_name_1, arg_value_1):
        return 'XBMC.RunPlugin({0}?{1}={2})'.format(self.base_url, 
                                                    arg_name_1, arg_value_1)

    def _misc_url_2_arg_RunPlugin(self, arg_name_1, arg_value_1, arg_name_2, arg_value_2):
        return 'XBMC.RunPlugin({0}?{1}={2}&{3}={4})'.format(self.base_url,
                                                            arg_name_1, arg_value_1,
                                                            arg_name_2, arg_value_2)

    def _misc_url_3_arg_RunPlugin(self, arg_name_1, arg_value_1, arg_name_2, arg_value_2, 
                                  arg_name_3, arg_value_3):
        return 'XBMC.RunPlugin({0}?{1}={2}&{3}={4}&{5}={6})'.format(self.base_url,
                                                                    arg_name_1, arg_value_1,
                                                                    arg_name_2, arg_value_2,
                                                                    arg_name_3, arg_value_3)

    def _misc_url_4_arg_RunPlugin(self, arg_name_1, arg_value_1, arg_name_2, arg_value_2, 
                                  arg_name_3, arg_value_3, arg_name_4, arg_value_4):
        return 'XBMC.RunPlugin({0}?{1}={2}&{3}={4}&{5}={6}&{7}={8})'.format(self.base_url,
                                                                            arg_name_1, arg_value_1,
                                                                            arg_name_2, arg_value_2,
                                                                            arg_name_3, arg_value_3, 
                                                                            arg_name_4, arg_value_4)
