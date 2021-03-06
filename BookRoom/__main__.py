import argparse
import logging

from BookRoom.requestlib import login, form_request, request_set_config_file
from BookRoom.datelib import get_unixdate, get_timecode, get_endtime_code
from BookRoom.roomlib import get_room_id, check_room_available, select_available_room
from BookRoom.paramlib import valid_date, valid_time, valid_config_file
from BookRoom.logger import logger

resource_id = 'a2d188b3-8349-4f4a-8d2d-549a691864c5'

####################################################################################
#
#
#
####################################################################################

parser = argparse.ArgumentParser(description='This program will book a specified study room at Sheridan college')
parser.add_argument('--room', '-r', help='The room you want to book.')
parser.add_argument('--date','-d', help="Pass the date of the room booking either as an absolute date 'YYYY/MM/DD' or relative date specified by python's dateparser package", type=valid_date, required=True)
parser.add_argument('--starttime', '-t', help='start time of room book. valid format is hh:mm[am,pm]', type=valid_time, required=True)
parser.add_argument('--duration', '-period', '-p', help='How long to reserve the room.', choices=[ '30', '60', '90', '120'], required=True)
parser.add_argument('--config', '-c', help='path to load conifiguration file. default is .config.yaml', default='config.yml', type=valid_config_file)
parser.add_argument("-l", "--log", dest="logLevel", help="Set the logging level" , choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO' )
args = parser.parse_args()

room_name = args.room
room_booking_date = args.date
room_booking_start_time = args.starttime
room_booking_duration = args.duration
config_file = args.config
room_id = None # this will be populated later

logger(args.logLevel)

logger = logging.getLogger(__name__)

logger.info('info message in main')
logger.debug('debug message in main')

request_set_config_file(config_file)

# Get available rooms
response = form_request(
    url = 'https://roombooking.sheridancollege.ca/Portal/Services/SelfServiceFindRoomList.php'
    ,payload = {
        'cboRequestType': resource_id,
        'startDate': get_unixdate(room_booking_date), # unix datestamp, date of request
        'isSelfService': '1',
        'startTime': get_timecode(room_booking_start_time),
        'duration': room_booking_duration,
        'endTime': get_endtime_code(room_booking_start_time, room_booking_duration),
        'originalRequestID': '00000000-0000-0000-0000-000000000000'
    }
)

if room_name is None: # check if a room has already been passed
    room_name = select_available_room(response)

check_room_available(response, room_name)
room_id = get_room_id(response, room_name)

# Make request to book room
form_request(
    url = "https://roombooking.sheridancollege.ca/index.php?p=ConfirmBooking"
    ,payload = {
        'txtOriginalRequestId': '00000000-0000-0000-0000-000000000000',
        'txtRequestTypeId': resource_id,
        'txtRoomId': resource_id,
        'txtRoomConfigId': resource_id,
        'txtStartDate': 'get_unixdate(room_booking_date)',  # unix datestamp, date of request
        'txtDuration': room_booking_duration,
        'AvailableRoomConfigIdentIDs': room_id,
        'dpStartDate3_stamp': get_unixdate(room_booking_date),
        'dpStartDate3': room_booking_date,
        'dpEndByDate_stamp': get_unixdate(room_booking_date),
        'dpEndByDate': room_booking_date,
        'numOccurrences': '10', 'radRecRange': '1', 'txtEndDate': '', 'txtStartTime': '', 'txtEndTime': '',
        'txtCapacity': '0', 'txtMinArea': '0', 'txtLocationId': '', 'RoomTypes': '', 'FloorLevels': '',
        'Pavilions': '', 'Characteristics': '', 'ConfigurationTypes': '', 'everyDay': '1', 'everyWeek': '1',
        'radMonthlyRankType': '1', 'everyMonthDay': '1', 'everyMonth': '1', 'monthlyRank': '0', 'monthlyDayOfWeek': '0',
        'everyMonthRank': '0', 'radYearlyRankType': '1', 'yearlyEveryMonth': '1', 'yearlyMonthDay': '1',
        'yearlyRank': '0', 'yearlyDayOfWeek': '0', 'yearlyMonth': '1',
    }
)

# Confirm Room Booking Request
form_request(
    url = "https://roombooking.sheridancollege.ca/Portal/Services/CreateBookingRequest.php"
    ,payload = {
        'selfService': '1',
        'txtRequestDisclaimer': 'Select OK to submit this request.',
        'txtRoomConfigId': room_id,
        'txtOriginalRequestId': '00000000-0000-0000-0000-000000000000',
        'cboRequestType': resource_id,
        'txtNumberOfAttendees': '',
        'dpStartDate_stamp': get_unixdate(room_booking_date),  # unix datestamp, date of request
        'cboStartTime': get_timecode(room_booking_start_time),
        'cboDuration': room_booking_duration,
        'txtNbOfPeople': '0',
        'txtMinArea': '0',
        'txtRoomId': resource_id,
        'cboRoomConfiguration': room_id,
        'btnConfirm': 'Confirm'
    }
)
