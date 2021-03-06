from unittest import mock
import pytest
import serial

# Package
from quartx_call_logger.plugins.siemens_hipath_serial import SiemensHipathSerial
from quartx_call_logger.record import Record
from quartx_call_logger import api, settings

mock_data = b"""
10.04.1923:19:06  2   104     00:00:0500441619251900                       2
10.04.1923:28:01  2      00:0100:00:000061393038625                        2
10.04.1923:28:01  2      00:0100:00:000061393038625                        2
10.04.1923:28:01  2      00:0100:00:000061393038625                        2
10.04.1923:19:06  2   104     00:00:0500441619251900                       2
11.04.1900:33:20  1   104     00:00:020857739075                           9
11.04.1900:34:13  2   104     00:00:060876153281                           2
11.04.1900:35:38  1   104             0876153281                           0
11.04.1900:35:38  1   103             0876153281                           0
11.04.1900:35:48  1   10400:0100:00:070876153281                           1
11.04.1900:36:28  2   104             79923                                0
11.04.1900:36:29  2   103             79923                                0
11.04.1900:36:34  2   10000:0500:00:0079923                                1
11.04.1900:49:13  1   104             0876153281                           0
11.04.1900:49:13  1   103             0876153281                           0
11.04.1900:49:22  2   104     00:00:030857739075                           2
11.04.1900:49:24  1   10000:1000:00:000876153281                           1
09.09.1821:04:01  1   100             0811111111                           009923
09.09.1820:16:50  1   10000:0100:00:060877629926                           1 9923
02.09.1814:07:40  1   10000:0900:00:000877629926                           2
22.02.1923:11:41  3   048             0248873711                           0 4416
22.02.1923:11:43  3   04800:4100:10:030248873711                           154416
22.02.1922:55:27  3   05800:0700:00:000922735086                           2
11.04.1914:58:19  1   103                                                  0
11.12.0008:23:23  4    16     00:05:2302317324856                       12 2                902725  841
11.12.0009:12:45  3    18     00:01:23834756                            34 212345678901                 2
11.12.0009:25:34  2    1100:34                                             1
11.12.0010:01:46  1    12     00:12:5383726639046287127384               5 2
11.12.0010:03:42  2    14     05:42:4338449434444495598376             245 2
11.12.0010:23:24  2    15     00:02:221234567890123412????              83 2
11.12.0011:12:45  3    18     00:01:23834756                            34 2
12.12.0012:23:34  3    1200:1500:03:12                                     1
12.12.0012:23:50  4    11     00:03:583844733399                         7 2
12.12.0013:23:54  3    17     00:02:233844733399                         8 5
12.12.0014:05:24  3    18     00:01:23834756                            31 2
12.12.0014:38:43  2    12     00:03:242374844                           63 2
12.12.0014:43:33  3    12     00:00:255345545556                         5 2
12.12.0014:44:12  2    12     00:12:122374844                           12 8
12.12.0014:44:12  3    12     00:12:125345545556                        10 8
12.12.0014:56:24  2    12     00:23:462374844                           84 2
13.12.0009:43:52  1     5     00:01:0539398989983                       76 4
14.12.0012:23:34  1     600:1400:02:3427348596872347569036                 3
15.12.0009:44:34  4    15     00:02:12189????                           23 2
15.12.0009:56:33  3    14     00:05:451283394495                        28 2
15.12.0012:20:26  1    12             0230298007766                        0
15.12.0012:23:34  1    1200:3400:02:340230298007766                        1
15.12.0013:43:25  3    15     00:05:2408972212345                          1
15.12.0013:43:25  4    15     00:05:24023147115432174                      9
15.12.0013:45:28  4    18             0230298007252                        0
15.12.0013:45:28  4    32             0230298007252                        0
15.12.0013:45:28  4    16             0230298007252                        0
15.12.0013:46:18  4    1600:50        0230298007252                        1
15.12.0013:49:28  4    16     00:00:0002317324856                          2
01.01.0000:00:00  8                                                     23 2
""".strip().split(b"\n")

settings.TIMEOUT = 0.01


@pytest.fixture
def mock_api():
    with mock.patch.object(api, "API") as mocker:
        mocker.return_value.running.return_value.is_set.return_value = True
        yield mocker


@pytest.fixture
def mock_serial():
    with mock.patch.object(serial, "Serial", spec=True) as mocker:
        def open_on_request():
            mocker.return_value.is_open = True
        mocker.return_value.open.side_effect = open_on_request
        mocker.return_value.is_open = False
        yield mocker


@pytest.fixture(params=mock_data)
def serial_params(request, mock_serial):
    mock_serial.return_value.readline.side_effect = [request.param, KeyboardInterrupt]
    return mock_serial


def test_call_logs(mock_api, serial_params):
    """Test the serial parser with different lines of call data."""
    def push(record):
        # Check if we have a Record class
        assert isinstance(record, Record)

        # The expected values for a given call type
        required_fields = ["number", "ext", "line"]
        if record.call_type == 2 or record.call_type == 1:
            required_fields.extend(["ring", "duration"])

        # Check if the required fields exists
        for val in required_fields:
            assert val in record

    mock_api.return_value.push.side_effect = push
    plugin = SiemensHipathSerial("/dev/ttyUSB0", 9600)
    plugin.start()


def test_failed_connection(mock_api, mock_serial):
    """Check that the SerialException is caught."""
    mock_serial.return_value.open.side_effect = [serial.SerialException, KeyboardInterrupt]
    plugin = SiemensHipathSerial("/dev/ttyUSB0", 9600)
    plugin.start()

    mock_serial.return_value.open.assert_called()


def test_read_handled_exception(mock_api, mock_serial):
    mock_serial.return_value.readline.side_effect = [serial.SerialException, KeyboardInterrupt]
    plugin = SiemensHipathSerial("/dev/ttyUSB0", 9600)
    plugin.start()

    mock_serial.return_value.readline.assert_called()


def test_read_unhandled_exception(mock_api, mock_serial):
    mock_serial.return_value.readline.side_effect = RuntimeError
    plugin = SiemensHipathSerial("/dev/ttyUSB0", 9600)
    with pytest.raises(RuntimeError):
        plugin.start()


def test_parse_error(mock_api, mock_serial):
    mock_serial.return_value.readline.side_effect = [b"dkdi", KeyboardInterrupt]
    plugin = SiemensHipathSerial("/dev/ttyUSB0", 9600)
    plugin.parse = mock.Mock(side_effect=RuntimeError)
    plugin.start()

    mock_serial.return_value.readline.assert_called()
