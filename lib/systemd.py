import dbus


SYSTEM_DBUS = dbus.SystemBus()


SYSTEMD_DBUS_NAME = 'org.freedesktop.systemd1'
SYSTEMD_DBUS_PATH = '/org/freedesktop/systemd1'
SYSTEMD_DBUS_MANAGER_INTERFACE = 'org.freedesktop.systemd1.Manager'


proxy = SYSTEM_DBUS.get_object(SYSTEMD_DBUS_NAME, SYSTEMD_DBUS_PATH)
manager = dbus.Interface(proxy, dbus_interface=SYSTEMD_DBUS_MANAGER_INTERFACE)


SYSTEMD_MANAGER_UNIT_KEYS = [
    'Name',
    'Description',
    
    'LoadState',
    'ActiveState',
    'SubState',
    
    'Following',
    
    'DbusPath',
    
    'JobQueued',
    'JobType',
    'JobDbusPath'
]


def unit(path):
    return SYSTEM_DBUS.get_object(SYSTEMD_DBUS_NAME, path)


SYSTEMD_DBUS_UNIT_INTERFACE = 'org.freedesktop.systemd1.Unit'
def unit_interface(proxy):
    return dbus.Interface(proxy, SYSTEMD_DBUS_UNIT_INTERFACE)


def units():
    return [dict(zip(SYSTEMD_MANAGER_UNIT_KEYS, unit)) for unit in manager.ListUnits()]
