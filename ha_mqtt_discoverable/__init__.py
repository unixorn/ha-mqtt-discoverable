# Copyright 2022 Joe Block <jpb@unixorn.net>
#
# License: Apache 2.0 (see root of the repo)

import json
import logging
import ssl

import paho.mqtt.client as mqtt

__version__ = "0.4.2"

CONFIGURATION_KEY_NAMES = {
    "act_t": "action_topic",
    "act_tpl": "action_template",
    "action_template": "act_tpl",
    "action_topic": "act_t",
    "atype": "automation_type",
    "automation_type": "atype",
    "aux_cmd_t": "aux_command_topic",
    "aux_command_topic": "aux_cmd_t",
    "aux_stat_t": "aux_state_topic",
    "aux_stat_tpl": "aux_state_template",
    "aux_state_template": "aux_stat_tpl",
    "aux_state_topic": "aux_stat_t",
    "av_tones": "available_tones",
    "availability": "avty",
    "availability_mode": "avty_mode",
    "availability_template": "avty_tpl",
    "availability_topic": "avty_t",
    "available_tones": "av_tones",
    "avty": "availability",
    "avty_mode": "availability_mode",
    "avty_t": "availability_topic",
    "avty_tpl": "availability_template",
    "away_mode_cmd_t": "away_mode_command_topic",
    "away_mode_command_topic": "away_mode_cmd_t",
    "away_mode_stat_t": "away_mode_state_topic",
    "away_mode_stat_tpl": "away_mode_state_template",
    "away_mode_state_template": "away_mode_stat_tpl",
    "away_mode_state_topic": "away_mode_stat_t",
    "b_tpl": "blue_template",
    "bat_lev_t": "battery_level_topic",
    "bat_lev_tpl": "battery_level_template",
    "battery_level_template": "bat_lev_tpl",
    "battery_level_topic": "bat_lev_t",
    "blue_template": "b_tpl",
    "bri_cmd_t": "brightness_command_topic",
    "bri_cmd_tpl": "brightness_command_template",
    "bri_scl": "brightness_scale",
    "bri_stat_t": "brightness_state_topic",
    "bri_tpl": "brightness_template",
    "bri_val_tpl": "brightness_value_template",
    "brightness_command_template": "bri_cmd_tpl",
    "brightness_command_topic": "bri_cmd_t",
    "brightness_scale": "bri_scl",
    "brightness_state_topic": "bri_stat_t",
    "brightness_template": "bri_tpl",
    "brightness_value_template": "bri_val_tpl",
    "charging_template": "chrg_tpl",
    "charging_topic": "chrg_t",
    "chrg_t": "charging_topic",
    "chrg_tpl": "charging_template",
    "cleaning_template": "cln_tpl",
    "cleaning_topic": "cln_t",
    "cln_t": "cleaning_topic",
    "cln_tpl": "cleaning_template",
    "clr_temp_cmd_t": "color_temp_command_topic",
    "clr_temp_cmd_tpl": "color_temp_command_template",
    "clr_temp_stat_t": "color_temp_state_topic",
    "clr_temp_tpl": "color_temp_template",
    "clr_temp_val_tpl": "color_temp_value_template",
    "cmd_off_tpl": "command_off_template",
    "cmd_on_tpl": "command_on_template",
    "cmd_t": "command_topic",
    "cmd_tpl": "command_template",
    "cod_arm_req": "code_arm_required",
    "cod_dis_req": "code_disarm_required",
    "cod_trig_req": "code_trigger_required",
    "code_arm_required": "cod_arm_req",
    "code_disarm_required": "cod_dis_req",
    "code_trigger_required": "cod_trig_req",
    "color_temp_command_template": "clr_temp_cmd_tpl",
    "color_temp_command_topic": "clr_temp_cmd_t",
    "color_temp_state_topic": "clr_temp_stat_t",
    "color_temp_template": "clr_temp_tpl",
    "color_temp_value_template": "clr_temp_val_tpl",
    "command_off_template": "cmd_off_tpl",
    "command_on_template": "cmd_on_tpl",
    "command_template": "cmd_tpl",
    "command_topic": "cmd_t",
    "curr_temp_t": "current_temperature_topic",
    "curr_temp_tpl": "current_temperature_template",
    "current_temperature_template": "curr_temp_tpl",
    "current_temperature_topic": "curr_temp_t",
    "dev": "device",
    "dev_cla": "device_class",
    "device": "dev",
    "device_class": "dev_cla",
    "dock_t": "docked_topic",
    "dock_tpl": "docked_template",
    "docked_template": "dock_tpl",
    "docked_topic": "dock_t",
    "e": "encoding",
    "effect_command_template": "fx_cmd_tpl",
    "effect_command_topic": "fx_cmd_t",
    "effect_list": "fx_list",
    "effect_state_topic": "fx_stat_t",
    "effect_template": "fx_tpl",
    "effect_value_template": "fx_val_tpl",
    "encoding": "e",
    "ent_cat": "entity_category",
    "entity_category": "ent_cat",
    "err_t": "error_topic",
    "err_tpl": "error_template",
    "error_template": "err_tpl",
    "error_topic": "err_t",
    "exp_aft": "expire_after",
    "expire_after": "exp_aft",
    "fan_mode_cmd_t": "fan_mode_command_topic",
    "fan_mode_cmd_tpl": "fan_mode_command_template",
    "fan_mode_command_template": "fan_mode_cmd_tpl",
    "fan_mode_command_topic": "fan_mode_cmd_t",
    "fan_mode_stat_t": "fan_mode_state_topic",
    "fan_mode_stat_tpl": "fan_mode_state_template",
    "fan_mode_state_template": "fan_mode_stat_tpl",
    "fan_mode_state_topic": "fan_mode_stat_t",
    "fan_speed_list": "fanspd_lst",
    "fan_speed_template": "fanspd_tpl",
    "fan_speed_topic": "fanspd_t",
    "fanspd_lst": "fan_speed_list",
    "fanspd_t": "fan_speed_topic",
    "fanspd_tpl": "fan_speed_template",
    "flash_time_long": "flsh_tlng",
    "flash_time_short": "flsh_tsht",
    "flsh_tlng": "flash_time_long",
    "flsh_tsht": "flash_time_short",
    "force_update": "frc_upd",
    "frc_upd": "force_update",
    "fx_cmd_t": "effect_command_topic",
    "fx_cmd_tpl": "effect_command_template",
    "fx_list": "effect_list",
    "fx_stat_t": "effect_state_topic",
    "fx_tpl": "effect_template",
    "fx_val_tpl": "effect_value_template",
    "g_tpl": "green_template",
    "green_template": "g_tpl",
    "hold_cmd_t": "hold_command_topic",
    "hold_cmd_tpl": "hold_command_template",
    "hold_command_template": "hold_cmd_tpl",
    "hold_command_topic": "hold_cmd_t",
    "hold_stat_t": "hold_state_topic",
    "hold_stat_tpl": "hold_state_template",
    "hold_state_template": "hold_stat_tpl",
    "hold_state_topic": "hold_stat_t",
    "hs_cmd_t": "hs_command_topic",
    "hs_command_topic": "hs_cmd_t",
    "hs_stat_t": "hs_state_topic",
    "hs_state_topic": "hs_stat_t",
    "hs_val_tpl": "hs_value_template",
    "hs_value_template": "hs_val_tpl",
    "hum_cmd_t": "target_humidity_command_topic",
    "hum_cmd_tpl": "target_humidity_command_template",
    "hum_stat_t": "target_humidity_state_topic",
    "hum_stat_tpl": "target_humidity_state_template",
    "ic": "icon",
    "icon": "ic",
    "init": "initial",
    "initial": "init",
    "json_attr": "json_attributes",
    "json_attr_t": "json_attributes_topic",
    "json_attr_tpl": "json_attributes_template",
    "json_attributes": "json_attr",
    "json_attributes_template": "json_attr_tpl",
    "json_attributes_topic": "json_attr_t",
    "max_hum": "max_humidity",
    "max_humidity": "max_hum",
    "max_mireds": "max_mirs",
    "max_mirs": "max_mireds",
    "max_temp": "max_temp",
    "min_hum": "min_humidity",
    "min_humidity": "min_hum",
    "min_mireds": "min_mirs",
    "min_mirs": "min_mireds",
    "min_temp": "min_temp",
    "mode_cmd_t": "mode_command_topic",
    "mode_cmd_tpl": "mode_command_template",
    "mode_command_template": "mode_cmd_tpl",
    "mode_command_topic": "mode_cmd_t",
    "mode_stat_t": "mode_state_topic",
    "mode_stat_tpl": "mode_state_template",
    "mode_state_template": "mode_stat_tpl",
    "mode_state_topic": "mode_stat_t",
    "modes": "modes",
    "name": "name",
    "obj_id": "object_id",
    "object_id": "obj_id",
    "off_delay": "off_dly",
    "off_dly": "off_delay",
    "on_cmd_type": "on_command_type",
    "on_command_type": "on_cmd_type",
    "opt": "optimistic",
    "optimistic": "opt",
    "osc_cmd_t": "oscillation_command_topic",
    "osc_cmd_tpl": "oscillation_command_template",
    "osc_stat_t": "oscillation_state_topic",
    "osc_val_tpl": "oscillation_value_template",
    "oscillation_command_template": "osc_cmd_tpl",
    "oscillation_command_topic": "osc_cmd_t",
    "oscillation_state_topic": "osc_stat_t",
    "oscillation_value_template": "osc_val_tpl",
    "payload": "pl",
    "payload_arm_away": "pl_arm_away",
    "payload_arm_custom_bypass": "pl_arm_custom_b",
    "payload_arm_home": "pl_arm_home",
    "payload_arm_night": "pl_arm_nite",
    "payload_available": "pl_avail",
    "payload_clean_spot": "pl_cln_sp",
    "payload_close": "pl_cls",
    "payload_disarm": "pl_disarm",
    "payload_home": "pl_home",
    "payload_locate": "pl_loc",
    "payload_lock": "pl_lock",
    "payload_not_available": "pl_not_avail",
    "payload_not_home": "pl_not_home",
    "payload_off": "pl_off",
    "payload_on": "pl_on",
    "payload_open": "pl_open",
    "payload_oscillation_off": "pl_osc_off",
    "payload_oscillation_on": "pl_osc_on",
    "payload_pause": "pl_paus",
    "payload_reset_humidity": "pl_rst_hum",
    "payload_reset_mode": "pl_rst_mode",
    "payload_reset_percentage": "pl_rst_pct",
    "payload_reset_preset_mode": "pl_rst_pr_mode",
    "payload_return_to_base": "pl_ret",
    "payload_start": "pl_strt",
    "payload_start_pause": "pl_stpa",
    "payload_stop": "pl_stop",
    "payload_trigger": "pl_trig",
    "payload_turn_off": "pl_toff",
    "payload_turn_on": "pl_ton",
    "payload_unlock": "pl_unlk",
    "pct_cmd_t": "percentage_command_topic",
    "pct_cmd_tpl": "percentage_command_template",
    "pct_stat_t": "percentage_state_topic",
    "pct_val_tpl": "percentage_value_template",
    "percentage_command_template": "pct_cmd_tpl",
    "percentage_command_topic": "pct_cmd_t",
    "percentage_state_topic": "pct_stat_t",
    "percentage_value_template": "pct_val_tpl",
    "pl": "payload",
    "pl_arm_away": "payload_arm_away",
    "pl_arm_custom_b": "payload_arm_custom_bypass",
    "pl_arm_home": "payload_arm_home",
    "pl_arm_nite": "payload_arm_night",
    "pl_avail": "payload_available",
    "pl_cln_sp": "payload_clean_spot",
    "pl_cls": "payload_close",
    "pl_disarm": "payload_disarm",
    "pl_home": "payload_home",
    "pl_loc": "payload_locate",
    "pl_lock": "payload_lock",
    "pl_not_avail": "payload_not_available",
    "pl_not_home": "payload_not_home",
    "pl_off": "payload_off",
    "pl_on": "payload_on",
    "pl_open": "payload_open",
    "pl_osc_off": "payload_oscillation_off",
    "pl_osc_on": "payload_oscillation_on",
    "pl_paus": "payload_pause",
    "pl_ret": "payload_return_to_base",
    "pl_rst_hum": "payload_reset_humidity",
    "pl_rst_mode": "payload_reset_mode",
    "pl_rst_pct": "payload_reset_percentage",
    "pl_rst_pr_mode": "payload_reset_preset_mode",
    "pl_stop": "payload_stop",
    "pl_stpa": "payload_start_pause",
    "pl_strt": "payload_start",
    "pl_toff": "payload_turn_off",
    "pl_ton": "payload_turn_on",
    "pl_trig": "payload_trigger",
    "pl_unlk": "payload_unlock",
    "pos_clsd": "position_closed",
    "pos_open": "position_open",
    "pos_t": "position_topic",
    "pos_tpl": "position_template",
    "position_closed": "pos_clsd",
    "position_open": "pos_open",
    "position_template": "pos_tpl",
    "position_topic": "pos_t",
    "pow_cmd_t": "power_command_topic",
    "pow_stat_t": "power_state_topic",
    "pow_stat_tpl": "power_state_template",
    "power_command_topic": "pow_cmd_t",
    "power_state_template": "pow_stat_tpl",
    "power_state_topic": "pow_stat_t",
    "pr_mode_cmd_t": "preset_mode_command_topic",
    "pr_mode_cmd_tpl": "preset_mode_command_template",
    "pr_mode_stat_t": "preset_mode_state_topic",
    "pr_mode_val_tpl": "preset_mode_value_template",
    "pr_modes": "preset_modes",
    "preset_mode_command_template": "pr_mode_cmd_tpl",
    "preset_mode_command_topic": "pr_mode_cmd_t",
    "preset_mode_state_topic": "pr_mode_stat_t",
    "preset_mode_value_template": "pr_mode_val_tpl",
    "preset_modes": "pr_modes",
    "r_tpl": "red_template",
    "red_template": "r_tpl",
    "ret": "retain",
    "retain": "ret",
    "rgb_cmd_t": "rgb_command_topic",
    "rgb_cmd_tpl": "rgb_command_template",
    "rgb_command_template": "rgb_cmd_tpl",
    "rgb_command_topic": "rgb_cmd_t",
    "rgb_stat_t": "rgb_state_topic",
    "rgb_state_topic": "rgb_stat_t",
    "rgb_val_tpl": "rgb_value_template",
    "rgb_value_template": "rgb_val_tpl",
    "send_cmd_t": "send_command_topic",
    "send_command_topic": "send_cmd_t",
    "send_if_off": "send_if_off",
    "set_fan_spd_t": "set_fan_speed_topic",
    "set_fan_speed_topic": "set_fan_spd_t",
    "set_pos_t": "set_position_topic",
    "set_pos_tpl": "set_position_template",
    "set_position_template": "set_pos_tpl",
    "set_position_topic": "set_pos_t",
    "source_type": "src_type",
    "spd_rng_max": "speed_range_max",
    "spd_rng_min": "speed_range_min",
    "speed_range_max": "spd_rng_max",
    "speed_range_min": "spd_rng_min",
    "src_type": "source_type",
    "stat_cla": "state_class",
    "stat_closing": "state_closing",
    "stat_clsd": "state_closed",
    "stat_locked": "state_locked",
    "stat_off": "state_off",
    "stat_on": "state_on",
    "stat_open": "state_open",
    "stat_opening": "state_opening",
    "stat_stopped": "state_stopped",
    "stat_t": "state_topic",
    "stat_tpl": "state_template",
    "stat_unlocked": "state_unlocked",
    "stat_val_tpl": "state_value_template",
    "state_class": "stat_cla",
    "state_closed": "stat_clsd",
    "state_closing": "stat_closing",
    "state_locked": "stat_locked",
    "state_off": "stat_off",
    "state_on": "stat_on",
    "state_open": "stat_open",
    "state_opening": "stat_opening",
    "state_stopped": "stat_stopped",
    "state_template": "stat_tpl",
    "state_topic": "stat_t",
    "state_unlocked": "stat_unlocked",
    "state_value_template": "stat_val_tpl",
    "stype": "subtype",
    "subtype": "stype",
    "sup_duration": "support_duration",
    "sup_feat": "supported_features",
    "sup_off": "supported_turn_off",
    "sup_vol": "support_volume_set",
    "support_duration": "sup_duration",
    "support_volume_set": "sup_vol",
    "supported_features": "sup_feat",
    "supported_turn_off": "sup_off",
    "swing_mode_cmd_t": "swing_mode_command_topic",
    "swing_mode_cmd_tpl": "swing_mode_command_template",
    "swing_mode_command_template": "swing_mode_cmd_tpl",
    "swing_mode_command_topic": "swing_mode_cmd_t",
    "swing_mode_stat_t": "swing_mode_state_topic",
    "swing_mode_stat_tpl": "swing_mode_state_template",
    "swing_mode_state_template": "swing_mode_stat_tpl",
    "swing_mode_state_topic": "swing_mode_stat_t",
    "t": "topic",
    "target_humidity_command_template": "hum_cmd_tpl",
    "target_humidity_command_topic": "hum_cmd_t",
    "target_humidity_state_template": "hum_stat_tpl",
    "target_humidity_state_topic": "hum_stat_t",
    "temp_cmd_t": "temperature_command_topic",
    "temp_cmd_tpl": "temperature_command_template",
    "temp_hi_cmd_t": "temperature_high_command_topic",
    "temp_hi_cmd_tpl": "temperature_high_command_template",
    "temp_hi_stat_t": "temperature_high_state_topic",
    "temp_hi_stat_tpl": "temperature_high_state_template",
    "temp_lo_cmd_t": "temperature_low_command_topic",
    "temp_lo_cmd_tpl": "temperature_low_command_template",
    "temp_lo_stat_t": "temperature_low_state_topic",
    "temp_lo_stat_tpl": "temperature_low_state_template",
    "temp_stat_t": "temperature_state_topic",
    "temp_stat_tpl": "temperature_state_template",
    "temp_unit": "temperature_unit",
    "temperature_command_template": "temp_cmd_tpl",
    "temperature_command_topic": "temp_cmd_t",
    "temperature_high_command_template": "temp_hi_cmd_tpl",
    "temperature_high_command_topic": "temp_hi_cmd_t",
    "temperature_high_state_template": "temp_hi_stat_tpl",
    "temperature_high_state_topic": "temp_hi_stat_t",
    "temperature_low_command_template": "temp_lo_cmd_tpl",
    "temperature_low_command_topic": "temp_lo_cmd_t",
    "temperature_low_state_template": "temp_lo_stat_tpl",
    "temperature_low_state_topic": "temp_lo_stat_t",
    "temperature_state_template": "temp_stat_tpl",
    "temperature_state_topic": "temp_stat_t",
    "temperature_unit": "temp_unit",
    "tilt_closed_value": "tilt_clsd_val",
    "tilt_clsd_val": "tilt_closed_value",
    "tilt_cmd_t": "tilt_command_topic",
    "tilt_cmd_tpl": "tilt_command_template",
    "tilt_command_template": "tilt_cmd_tpl",
    "tilt_command_topic": "tilt_cmd_t",
    "tilt_inv_stat": "tilt_invert_state",
    "tilt_invert_state": "tilt_inv_stat",
    "tilt_max": "tilt_max",
    "tilt_min": "tilt_min",
    "tilt_opened_value": "tilt_opnd_val",
    "tilt_opnd_val": "tilt_opened_value",
    "tilt_opt": "tilt_optimistic",
    "tilt_optimistic": "tilt_opt",
    "tilt_status_t": "tilt_status_topic",
    "tilt_status_template": "tilt_status_tpl",
    "tilt_status_topic": "tilt_status_t",
    "tilt_status_tpl": "tilt_status_template",
    "topic": "t",
    "uniq_id": "unique_id",
    "unique_id": "uniq_id",
    "unit_of_meas": "unit_of_measurement",
    "unit_of_measurement": "unit_of_meas",
    "val_tpl": "value_template",
    "value_template": "val_tpl",
    "whit_val_cmd_t": "white_value_command_topic",
    "whit_val_scl": "white_value_scale",
    "whit_val_stat_t": "white_value_state_topic",
    "whit_val_tpl": "white_value_template",
    "white_value_command_topic": "whit_val_cmd_t",
    "white_value_scale": "whit_val_scl",
    "white_value_state_topic": "whit_val_stat_t",
    "white_value_template": "whit_val_tpl",
    "xy_cmd_t": "xy_command_topic",
    "xy_command_topic": "xy_cmd_t",
    "xy_stat_t": "xy_state_topic",
    "xy_state_topic": "xy_stat_t",
    "xy_val_tpl": "xy_value_template",
    "xy_value_template": "xy_val_tpl",
}


class Discoverable:
    """
    Base class for making MQTT discoverable objects
    """

    def __init__(self, settings: dict = {}) -> None:
        """
        Validate the settings and setup the base discoverable object class

        Args:
            settings(dict): Settings for the sensor we want to create in Home Assistant.

            Mandatory Keys:
                mqtt_server
                mqtt_prefix - defaults to homeassistant
                mqtt_user
                mqtt_password
                device_id
                device_name
                device_class

            Optional Keys:
                payload_off
                payload_on
                unique_id
        """
        settings_error_base = "You must specify a server and a client_name"

        if "client_name" not in settings:
            raise RuntimeError(f"client_name is unset. {settings_error_base}")
        self.client_name = settings["client_name"]

        if "debug" not in settings:
            settings["debug"] = False
        self.debug = settings["debug"]

        if "mqtt_server" not in settings:
            raise RuntimeError(f"mqtt_server is unset. {settings_error_base}")
        self.mqtt_server = settings["mqtt_server"]

        if "mqtt_prefix" not in settings:
            raise RuntimeError("mqtt_prefix is unset.")
        self.mqtt_prefix = settings["mqtt_prefix"]

        if "mqtt_password" not in settings:
            raise RuntimeError("mqtt_password is unset.")
        self.mqtt_password = settings["mqtt_password"]

        if "mqtt_user" not in settings:
            raise RuntimeError(f"mqtt_user is unset. {settings_error_base}")
        self.mqtt_user = settings["mqtt_user"]

        if "device_id" not in settings:
            raise RuntimeError("device_id is unset.")
        self.device_id = settings["device_id"]

        if "device_name" not in settings:
            raise RuntimeError("device_name is unset.")
        self.device_name = settings["device_name"]

        if "device_class" not in settings:
            raise RuntimeError("device_class is unset.")
        self.device_class = settings["device_class"]

        if "icon" in settings:
            self.icon = settings["icon"]
        if "manufacturer" in settings:
            self.manufacturer = settings["manufacturer"]
        else:
            self.manufacturer = "Acme Products"

        if "model" in settings:
            self.model = settings["model"]
        if "unique_id" in settings:
            self.unique_id = settings["unique_id"]

        # SSL setup

        self.use_tls = False
        if "use_tls" in settings:
            if settings["use_tls"]:
                self.tls_ca_cert = settings["tls_ca_cert"]
                self.tls_certfile = settings["tls_certfile"]
                self.tls_key = settings["tls_key"]
                self.use_tls = settings["use_tls"]

        self.topic_prefix = f"{self.mqtt_prefix}/{self.device_class}/{self.device_name}"
        self.config_topic = f"{self.topic_prefix}/config"
        self.state_topic = f"{self.topic_prefix}/state"
        logging.info(f"topic_prefix: {self.topic_prefix}")
        logging.info(f"self.state_topic: {self.state_topic}")
        self.wrote_configuration = False

    def __str__(self) -> str:
        """
        Generate a string representation of the Discoverable object
        """
        dump = f"""
topic_prefix: {self.topic_prefix}
mqtt_prefix: {self.mqtt_prefix}
mqtt_server: {self.mqtt_server}
mqtt_user: {self.mqtt_user}
device_class: {self.device_class}
device_id: {self.device_id}
device_name: {self.device_name}
device_class: {self.device_class}
config_topic: {self.config_topic}
state_topic: {self.state_topic}
wrote_configuration: {self.wrote_configuration}
        """
        if self.icon:
            dump = f"""{dump}
            icon: {self.icon}"""
        return dump

    def _connect(self) -> None:
        if not hasattr(self, "mqtt_client"):
            logging.debug(
                f"Creating mqtt client({self.client_name}) for {self.mqtt_server}"
            )
            self.mqtt_client = mqtt.Client(self.client_name)
            if self.use_tls:
                logging.info(f"Connecting to {self.mqtt_server}...")
                logging.info("Configuring SSL")
                logging.debug(f"ca_certs=s{self.tls_ca_cert}")
                logging.debug(f"certfile={self.tls_certfile}")
                logging.debug(f"keyfile={self.tls_key}")
                self.mqtt_client.tls_set(
                    ca_certs=self.tls_ca_cert,
                    certfile=self.tls_certfile,
                    keyfile=self.tls_key,
                    cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=ssl.PROTOCOL_TLS,
                )
            else:
                logging.warning(f"Connecting to {self.mqtt_server} without SSL")
                self.mqtt_client.username_pw_set(
                    self.mqtt_user, password=self.mqtt_password
                )
            self.mqtt_client.connect(self.mqtt_server)
        else:
            logging.debug("Reusing existing mqtt_client...")

    def _state_helper(self, state: str = None, topic: str = None) -> None:
        """
        Write a state to our MQTT state topic
        """
        self._connect()
        if not self.wrote_configuration:
            logging.debug("Writing sensor configuration")
            self.write_config()
        if not topic:
            logging.debug(f"topic unset, using default of '{self.state_topic}'")
            topic = self.state_topic
        logging.debug(f"Writing '{state}' to {topic}")
        if self.debug:
            logging.warning(f"Debug is {self.debug}, skipping state write")
        else:
            logging.warning(self.mqtt_client.publish(topic, state, retain=True))

    def debug_mode(self, mode: bool):
        self.debug = mode
        logging.warning(f"Set debug mode to {self.debug}")

    def delete(self) -> None:
        """
        Delete a synthetic sensor from Home Assistant via MQTT message.

        Based on https://www.home-assistant.io/docs/mqtt/discovery/

        mosquitto_pub -r -h 127.0.0.1 -p 1883 \
            -t "homeassistant/binary_sensor/garden/config" \
            -m '{"name": "garden", "device_class": "motion", \
            "state_topic": "homeassistant/binary_sensor/garden/state"}'
        """

        config_message = ""
        self._connect()
        logging.info(
            f"Writing '{config_message}' to topic {self.config_topic} on {self.mqtt_server}"
        )
        self.mqtt_client.publish(self.config_topic, config_message, retain=True)

    def generate_config(self) -> dict:
        """
        Generate a dictionary that we'll grind into JSON and write to MQTT.

        Will be used with the MQTT discovery protocol to make Home Assistant
        automagically ingest the new sensor.
        """
        config = {
            "name": self.device_name,
            "device_class": self.device_class,
            "state_topic": self.state_topic,
            "availability_topic": self.state_topic,
        }
        if hasattr(self, "icon"):
            config["icon"] = self.icon
        return config

    def write_config(self) -> None:
        """
        mosquitto_pub -r -h 127.0.0.1 -p 1883 \
            -t "homeassistant/binary_sensor/garden/config" \
            -m '{"name": "garden", "device_class": "motion", \
                "state_topic": "homeassistant/binary_sensor/garden/state"}'
        """

        self._connect()
        config_message = json.dumps(self.generate_config())

        logging.debug(
            f"Writing '{config_message}' to topic {self.config_topic} on {self.mqtt_server}"
        )
        self.wrote_configuration = True
        self.config_message = config_message

        if self.debug:
            logging.warning(f"Debug is set to {self.debug}, skipping config write.")
        else:
            self.mqtt_client.publish(self.config_topic, config_message, retain=True)

    def update_state(self, state) -> None:
        """
        Update MQTT device state

        Override in subclasses
        """
        self._state_helper(state=state)
