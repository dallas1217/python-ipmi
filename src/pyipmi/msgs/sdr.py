import array

import constants
from . import register_message_class
from . import Message
from . import ByteArray
from . import UnsignedInt
from . import Timestamp
from . import Bitfield
from . import CompletionCode
from . import Conditional
from pyipmi.utils import ByteBuffer
from pyipmi.errors import DecodingError, EncodingError


@register_message_class
class GetSDRRepositoryInfoReq(Message):
    __cmdid__ = constants.CMDID_GET_SDR_REPOSITORY_INFO
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0
    __fields__ = ()


@register_message_class
class GetSDRRepositoryInfoRsp(Message):
    __cmdid__ = constants.CMDID_GET_SDR_REPOSITORY_INFO
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0
    __fields__ = (
            CompletionCode(),
            UnsignedInt('sdr_version', 1),
            UnsignedInt('record_count', 2),
            UnsignedInt('free_space', 2),
            Timestamp('most_recent_addtion'),
            Timestamp('most_recent_erase'),
            Bitfield('operation_support', 1,
                Bitfield.Bit('get_sdr_repository_allocation_command', 1),
                Bitfield.Bit('reverse_sdr_repository_command', 1),
                Bitfield.Bit('partial_add_sdr_command', 1),
                Bitfield.Bit('delete_sdr_command', 1),
                Bitfield.ReservedBit(1, 0),
                Bitfield.Bit('sdr_repository_update_type', 2),
                Bitfield.Bit('overflow_flag', 1)
            ),
    )


@register_message_class
class GetDeviceSdrInfoReq(Message):
    __cmdid__ = constants.CMDID_GET_DEVICE_SDR_INFO
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0
    __fields__ = ()


@register_message_class
class GetDeviceSdrInfoRsp(Message):
    __cmdid__ = constants.CMDID_GET_DEVICE_SDR_INFO
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0
    __fields__ = (
            CompletionCode(),
            UnsignedInt('number_of_sensors', 1),
            Bitfield('flags', 1,
                Bitfield.Bit('lun0_has_sensors', 1),
                Bitfield.Bit('lun1_has_sensors', 1),
                Bitfield.Bit('lun2_has_sensors', 1),
                Bitfield.Bit('lun3_has_sensors', 1),
                Bitfield.ReservedBit(3, 0),
                Bitfield.Bit('dynamic_population', 1)
            ),
            Timestamp('sensor_population_change'),
    )


@register_message_class
class GetDeviceSdrReq(Message):
    __cmdid__ = constants.CMDID_GET_DEVICE_SDR
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0
    __fields__ = (
            UnsignedInt('reservation_id', 2, 0x0000),
            UnsignedInt('record_id', 2),
            UnsignedInt('offset', 1),
            UnsignedInt('length', 1),
    )


@register_message_class
class GetDeviceSdrRsp(Message):
    __cmdid__ = constants.CMDID_GET_DEVICE_SDR
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0

    def _encode(self):
        data = ByteBuffer()
        data.push_unsigned_int(self.completion_code, 1)
        if (self.completion_code == constants.CC_OK):
            data.push_unsigned_int(self.next_record_id, 2)
            data.extend(self.record_data)
        return data.to_string()

    def _decode(self, data):
        data = ByteBuffer(data)
        self.completion_code = data.pop_unsigned_int(1)
        if (self.completion_code != constants.CC_OK):
            return
        self.next_record_id = data.pop_unsigned_int(2)
        self.record_data = data[:]


@register_message_class
class ReserveDeviceSdrRepositoryReq(Message):
    __cmdid__ = constants.CMDID_RESERVE_DEVICE_SDR_REPOSITORY
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0
    __fields__ = ()


@register_message_class
class ReserveDeviceSdrRepositoryRsp(Message):
    __cmdid__ = constants.CMDID_RESERVE_DEVICE_SDR_REPOSITORY
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0
    __fields__ = (
            CompletionCode(),
            UnsignedInt('reservation_id', 2)
    )


@register_message_class
class GetSensorThresholdReq(Message):
    __cmdid__ = constants.CMDID_GET_SENSOR_THRESHOLD
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0
    __fields__ = (
        UnsignedInt('sensor_number', 1),
    )


@register_message_class
class GetSensorThresholdRsp(Message):
    __cmdid__ = constants.CMDID_GET_SENSOR_THRESHOLD
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0
    __fields__ = (
        CompletionCode(),
        Bitfield('readable_mask', 1,
                Bitfield.Bit('lnc', 1, default=0),
                Bitfield.Bit('lcr', 1, default=0),
                Bitfield.Bit('lnr', 1, default=0),
                Bitfield.Bit('unc', 1, default=0),
                Bitfield.Bit('ucr', 1, default=0),
                Bitfield.Bit('unr', 1, default=0),
                Bitfield.ReservedBit(2, 0),
            ),
        Bitfield('threshold', 6,
                Bitfield.Bit('lnc', 8, default=0),
                Bitfield.Bit('lcr', 8, default=0),
                Bitfield.Bit('lnr', 8, default=0),
                Bitfield.Bit('unc', 8, default=0),
                Bitfield.Bit('ucr', 8, default=0),
                Bitfield.Bit('unr', 8, default=0),
            ),
    )


@register_message_class
class SetSensorHysteresisReq(Message):
    __cmdid__ = constants.CMDID_SET_SENSOR_HYSTERESIS
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0
    __fields__ = (
            UnsignedInt('sensor_number', 1),
            UnsignedInt('reserved', 1, 0xff),
            UnsignedInt('positive_going_hysteresis', 1),
            UnsignedInt('negative_going_hysteresis', 1),
    )


@register_message_class
class SetSensorHysteresisRsp(Message):
    __cmdid__ = constants.CMDID_SET_SENSOR_HYSTERESIS
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0
    __fields__ = (
            CompletionCode(),
    )


@register_message_class
class GetSensorHysteresisReq(Message):
    __cmdid__ = constants.CMDID_GET_SENSOR_HYSTERESIS
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0
    __fields__ = (
            UnsignedInt('sensor_number', 1),
    )


@register_message_class
class GetSensorHysteresisRsp(Message):
    __cmdid__ = constants.CMDID_GET_SENSOR_HYSTERESIS
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0
    __fields__ = (
            CompletionCode(),
            UnsignedInt('positive_going_hysteresis', 1),
            UnsignedInt('negative_going_hysteresis', 1),
    )


@register_message_class
class SetSensorThresholdReq(Message):
    __cmdid__ = constants.CMDID_SET_SENSOR_THRESHOLD
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0
    __fields__ = (
        UnsignedInt('sensor_number', 1),
        Bitfield('set_mask', 1,
                Bitfield.Bit('lnc', 1, default=0),
                Bitfield.Bit('lcr', 1, default=0),
                Bitfield.Bit('lnr', 1, default=0),
                Bitfield.Bit('unc', 1, default=0),
                Bitfield.Bit('ucr', 1, default=0),
                Bitfield.Bit('unr', 1, default=0),
                Bitfield.ReservedBit(2, 0),
            ),
        Bitfield('threshold', 6,
                Bitfield.Bit('lnc', 8, default=0),
                Bitfield.Bit('lcr', 8, default=0),
                Bitfield.Bit('lnr', 8, default=0),
                Bitfield.Bit('unc', 8, default=0),
                Bitfield.Bit('ucr', 8, default=0),
                Bitfield.Bit('unr', 8, default=0),
            ),
    )


@register_message_class
class SetSensorThresholdRsp(Message):
    __cmdid__ = constants.CMDID_SET_SENSOR_THRESHOLD
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0
    __fields__ = (
        CompletionCode(),
    )


@register_message_class
class SetSensorEventEnableReq(Message):
    __cmdid__ = constants.CMDID_SET_SENSOR_EVENT_ENABLE
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0

    def _encode(self):
        data = ByteBuffer()
        data.push_unsigned_int(self.sensor_number, 1)
        tmp = 0
        tmp |= (self.cfg & 0x3) << 4
        tmp |= (self.event_enable & 0x1) << 6
        tmp |= (self.scanning_enable & 0x1) << 7
        data.push_unsigned_int(tmp, 1)
        if hasattr(self, 'byte3'):
            data.push_unsigned_int(self.byte3, 1)
        if hasattr(self, 'byte4'):
            data.push_unsigned_int(self.byte4, 1)
        if hasattr(self, 'byte5'):
            data.push_unsigned_int(self.byte5, 1)
        if hasattr(self, 'byte6'):
            data.push_unsigned_int(self.byte6, 1)
        return data.to_string()


@register_message_class
class SetSensorEventEnableRsp(Message):
    __cmdid__ = constants.CMDID_SET_SENSOR_EVENT_ENABLE
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0
    __fields__ = (
            CompletionCode(),
    )


@register_message_class
class GetSensorEventEnableReq(Message):
    __cmdid__ = constants.CMDID_GET_SENSOR_EVENT_ENABLE
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0
    __fields__ = (
        UnsignedInt('sensor_number', 1),
    )


@register_message_class
class GetSensorEventEnableRsp(Message):
    __cmdid__ = constants.CMDID_GET_SENSOR_EVENT_ENABLE
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0
    __fields__ = (
        UnsignedInt('sensor_number', 1),
    )

    def _decode(self, data):
        data = ByteBuffer(data)
        self.completion_code = data.pop_unsigned_int(1)
        if (self.completion_code != constants.CC_OK):
            return

        tmp = data.pop_unsigned_int(1)
        self.event_enabled = (tmp & 0x80) >> 7
        self.scanning_enabled = (tmp & 0x40) >> 6

        if len(data):
            self.byte3 = data.pop_unsigned_int(1)
        if len(data):
            self.byte4 = data.pop_unsigned_int(1)
        if len(data):
            self.byte5 = data.pop_unsigned_int(1)
        if len(data):
            self.byte6 = data.pop_unsigned_int(1)


@register_message_class
class GetSensorReadingReq(Message):
    __cmdid__ = constants.CMDID_GET_SENSOR_READING
    __netfn__ = constants.NETFN_SENSOR_EVENT
    __default_lun__ = 0
    __fields__ = (
        UnsignedInt('sensor_number', 1),
    )


@register_message_class
class GetSensorReadingRsp(Message):
    __cmdid__ = constants.CMDID_GET_SENSOR_READING
    __netfn__ = constants.NETFN_SENSOR_EVENT | 1
    __default_lun__ = 0

    def _encode(self):
        data = ByteBuffer()
        data.push_unsigned_int(self.completion_code, 1)
        if (self.completion_code == constants.CC_OK):
            data.push_unsigned_int(self.sensor_reading, 1)
            tmp = (self.event_disabled & 0x1 << 5
                    | self.scanning_disabled & 0x1 << 6
                    | self.update_in_progress & 0x1 << 7)
            data.push_unsigned_int(tmp, 1)
            if self.states1:
                data.push_unsigned_int(self.states1, 1)
            if self.states2:
                data.push_unsigned_int(self.states2, 1)
        return data.to_string()

    def _decode(self, data):
        data = ByteBuffer(data)
        self.completion_code = data.pop_unsigned_int(1)
        if (self.completion_code != constants.CC_OK):
            return
        self.sensor_reading = data.pop_unsigned_int(1)

        tmp = data.pop_unsigned_int(1)
        self.event_disabled = (tmp & 0x80) >> 7
        self.scanning_disabled = (tmp & 0x40) >> 6
        self.update_in_progress = (tmp & 0x20) >> 5

        if len(data):
            self.states1 = data.pop_unsigned_int(1)
        if len(data):
            self.states2 = data.pop_unsigned_int(1)
