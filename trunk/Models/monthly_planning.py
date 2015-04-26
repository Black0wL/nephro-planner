__author__ = "Christophe"
# -*- coding: utf-8 -*-

from Enums.timeslot import TimeSlot
from Enums.constraint_strategy import ConstraintStrategy
from Models.daily_planning import DailyPlanning
import sqlite3
from Utils.parameters import Parameters
from Utils.constants import Constants
from Utils.database import Database
from datetime import timedelta, date, datetime
from collections import Counter
from Enums.activity import Activity
import calendar


def singleton(cls):
    instances = dict()

    def __new__(_year, _month):
        if _year not in instances:
            instances[_year] = dict()
        if _month not in instances[_year]:
            instances[_year][_month] = cls(_year, _month)
        return instances[_year][_month]
    return __new__


@singleton
class MonthlyPlanning():
    def __init__(self, _year, _month):
        self.year = _year
        self.month = _month
        self.daily_plannings = dict()
        self.human_readable_days = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi", "Dimanche"]
        self.human_readable_months = ["Janvier","Février","Mars","Avril","Mai","Juin", "Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
        self.human_readable_activities = {
            Activity.NEPHROLOGY: "NEPH",
            Activity.DIALYSIS: "DIAL",
            Activity.CONSULTATION: "CP",
            Activity.OTHERS: "AA",
            Activity.OBLIGATION: "ASTR",
            Activity.OBLIGATION_HOLIDAY: "ASTR",
            Activity.OBLIGATION_WEEKEND: "ASTR"
        }

        for _date in [date(_year, _month, day) for day in range(1, calendar.monthrange(_year, _month)[1] + 1)]:
            self.daily_plannings[_date] = DailyPlanning(_date)

        # adding to the month's days the potentially additional overflowing days
        first_date, last_date = self.__first_last_key_dates__()

        _index = self.daily_plannings[last_date].weekday  # getting last key date's weekday index
        if _index in [4, 5, 6]:  # if last month's day is friday, saturday or sunday (unusual day)
            for _day in range(1, 6-_index+1):
                _date = last_date + timedelta(days=_day)
                self.daily_plannings[_date] = DailyPlanning(_date)

        """
        with Parameters() as params, sqlite3.connect(params.data[Constants.DATABASE_FILENAME_KEY]) as connection:
            cursor = connection.cursor()

            data_set = cursor.execute('''
                SELECT
                    date_pk,
                    time_slot_type_pk,
                    activity_type,
                    id_nephrologist_fk
                FROM {}
                WHERE
                    date_pk >= '{}'
                    AND date_pk <= '{}'
            '''.format(
                Database.DATABASE_TABLE_MONTHLY_PLANNINGS,
                date(_year, _month, 1).isoformat(),  # first month's day
                date(_year, _month, calendar.monthrange(_year, _month)[1]).isoformat()  # last month's day
            ))

        self.daily_plannings = dict()
        if data_set.rowcount > 0:  # load an resource-allocated image of the specific days
            for row in data_set.fetchmany():
                _date = datetime.strptime(row[0], "%Y-%m-%d").date()
                self.daily_plannings[_date] = DailyPlanning(_date).__allocate__(
                    row[1],
                    row[2],
                    row[3]
                )
        """

    def __first_last_key_dates__(self):
        return sorted(self.daily_plannings.keys())[::len(self.daily_plannings)-1]  # takes first and last of keys

    def iterate(self):
        from itertools import chain, repeat, islice
        from math import floor

        def pad_infinite(iterable, padding=None):
           return chain(iterable, repeat(padding))

        def pad(iterable, size, padding=None):
           return islice(pad_infinite(iterable, padding), size)

        plain = sorted([A for A in self.daily_plannings])
        isPlainEven = len(plain) % 2 == 0
        odds = iter(plain[:(len(plain) if isPlainEven else len(plain)-1)])
        even = iter(plain[1:(len(plain)-1 if isPlainEven else len(plain))])
        odds_iter = pad([(A, next(odds)) for A in odds], floor(len(plain)/2))
        even_iter = pad([(A, next(even)) for A in even], floor(len(plain)/2))

        return [(None, datetime(self.year, self.month, 1))] + [A for A in list(chain.from_iterable(zip(odds_iter, even_iter))) if A is not None]

    def __str__(self):
        return "\n".join([str(self.daily_plannings[daily_planning]) for daily_planning in sorted(self.daily_plannings)])

    # TODO: if all but ConstraintStrategy.NONE are uncommented, preferences are not flawlessly taken into account...
    def __compute__(self):
        self.holidays = dict()
        for x in Database.team():
            self.holidays[x.id] = x.__holidays__(self)  # computing holidays for nephrologists

        for (yesterday, today) in self.iterate():
            if yesterday is not None:
                yesterday_profile = self.daily_plannings[date(yesterday.year, yesterday.month, yesterday.day)].profile
            else:
                yesterday_profile = None

            current_daily_planning = self.daily_plannings[date(today.year, today.month, today.day)]  # the daily planning for the current day

            if current_daily_planning.weekday == 0:
                # recomputing holidays to take obligation recovery into account
                self.holidays = dict()
                for x in Database.team():
                    self.holidays[x.id] = x.__holidays__(self)  # computing holidays for nephrologists

            # if today_date is weekend day or today_date is holiday
            if current_daily_planning.weekday in [4, 5, 6] or not current_daily_planning.is_working_day:
                # allocate all damn day in the same time
                current_daily_planning.__allocate_whole_day__(ConstraintStrategy.ALLOCATE_WEEKEND_DAYS.value, yesterday_profile, self.holidays)
                current_daily_planning.__allocate_whole_day__(ConstraintStrategy.ALLOCATE_HOLIDAYS.value, yesterday_profile, self.holidays)

            # allocate all day's timeslots separately
            for current_timeslot in current_daily_planning.profile:
                if current_daily_planning.weekday in [0, 5, 6]:
                    current_daily_planning.__allocate_timeslot__(ConstraintStrategy.ALLOCATE_MORNING_DIALYSIS.value, yesterday_profile, current_timeslot, self.holidays)
                current_daily_planning.__allocate_timeslot__(ConstraintStrategy.FOCUS_ON_PREFERENCES.value + ConstraintStrategy.DISCARD_COUNTERS.value, yesterday_profile, current_timeslot, self.holidays)
                current_daily_planning.__allocate_timeslot__(ConstraintStrategy.NONE.value, yesterday_profile, current_timeslot, self.holidays)

    def output(self):
        # from xlrd import open_workbook
        from xlwt import Workbook, XFStyle, Borders, Alignment, Font, Pattern, Style, easyxf
        # from xlutils.copy import copy

        '''
        rb = open_workbook(r"Templates\template.xls")
        wb = copy(rb)

        s = wb.get_sheet(0)
        s.write(0, 0, 'A1')
        wb.save(r"C:\Temp\nephro-planner\new.xls")
        '''

        book = Workbook(encoding="utf-8")
        sheet = book.add_sheet(r"Feuille1")

        style_title = XFStyle()
        font_title = Font()
        font_title.name = "Comic Sans MS"
        font_title.height = 280
        style_title.font = font_title
        style_title.alignment.horz = Alignment.HORZ_CENTER
        style_title.alignment.vert = Alignment.VERT_CENTER

        style_cell_bottom = XFStyle()
        borders_cell_bottom  = Borders()
        borders_cell_bottom .bottom = Borders.MEDIUM
        style_cell_bottom.borders = borders_cell_bottom

        style_header = XFStyle()
        font_header = Font()
        font_header.bold = 1
        font_header.name = "Arial Narrow"
        font_header.height = 240
        style_header.font = font_header
        style_header.alignment.horz = Alignment.HORZ_CENTER
        style_header.alignment.vert = Alignment.VERT_CENTER
        borders_header = Borders()
        borders_header.top = Borders.MEDIUM
        borders_header.left = Borders.MEDIUM
        borders_header.bottom = Borders.MEDIUM
        borders_header.right = Borders.MEDIUM
        style_header.borders = borders_header

        style_sub_header = XFStyle()
        font_sub_header = Font()
        font_sub_header.name = "Arial Narrow"
        font_sub_header.height = 240
        style_sub_header.font = font_sub_header
        style_sub_header.alignment.horz = Alignment.HORZ_CENTER
        style_sub_header.alignment.vert = Alignment.VERT_CENTER
        borders_sub_header = Borders()
        borders_sub_header.top = Borders.MEDIUM
        borders_sub_header.left = Borders.MEDIUM
        borders_sub_header.bottom = Borders.MEDIUM
        borders_sub_header.right = Borders.MEDIUM
        style_sub_header.borders = borders_sub_header

        style_date = XFStyle()
        font_date = Font()
        font_date.name = "Arial Narrow"
        font_date.height = 240
        style_date.font = font_date
        style_date.alignment.horz = Alignment.HORZ_RIGHT
        style_date.alignment.vert = Alignment.VERT_CENTER
        borders_date = Borders()
        borders_date.left = Borders.MEDIUM
        style_date.borders = borders_date

        style_date_status = XFStyle()
        font_date_status = Font()
        font_date_status.name = "Arial Narrow"
        font_date_status.height = 240
        style_date_status.font = font_date_status
        style_date_status.alignment.horz = Alignment.HORZ_LEFT
        style_date_status.alignment.vert = Alignment.VERT_CENTER
        borders_date_status = Borders()
        borders_date_status.right = Borders.MEDIUM
        style_date_status.borders = borders_date_status

        style_cell_normal = XFStyle()
        font_cell_normal = Font()
        font_cell_normal.name = "Arial Narrow"
        font_cell_normal.height = 220
        style_cell_normal.font = font_cell_normal
        style_cell_normal.alignment.horz = Alignment.HORZ_CENTER
        style_cell_normal.alignment.vert = Alignment.VERT_CENTER

        style_cell_right = XFStyle()
        font_cell_right = Font()
        font_cell_right.name = "Arial Narrow"
        font_cell_right.height = 220
        style_cell_right.font = font_cell_right
        style_cell_right.alignment.horz = Alignment.HORZ_CENTER
        style_cell_right.alignment.vert = Alignment.VERT_CENTER
        borders_cell_right = Borders()
        borders_cell_right.right = Borders.MEDIUM
        style_cell_right.borders = borders_cell_right

        style_cell_top = XFStyle()
        borders_cell_top = Borders()
        borders_cell_top.top = Borders.MEDIUM
        style_cell_top.borders = borders_cell_top

        column_offset = 1
        date_column_offset = 2
        row_offset = 1
        table_width = 1 + 3 * len(Database.team())

        # build titles
        sheet.write_merge(row_offset, row_offset, column_offset, table_width + 1, "POLE MEDECINE INTERNE", style_title)
        sheet.write_merge(row_offset + 1, row_offset + 1, column_offset, table_width + 1, "Service NEPHROLOGIE – HEMODIALYSE", style_title)
        sheet.write_merge(row_offset + 2, row_offset + 2, column_offset, table_width + 1, "Planning de {0} {1}".format(self.human_readable_months[self.month - 1], self.year), style_title)

        # patch date columns top borders
        sheet.write(row_offset + 5, column_offset, "", style_cell_bottom)
        sheet.write(row_offset + 5, column_offset + 1, "", style_cell_bottom)

        # build header and sub header
        for x in Database.team():
            sheet.write_merge(row_offset + 4, row_offset + 4, column_offset + date_column_offset + 3 * (x.id - 1), column_offset + date_column_offset + 3 * x.id - 1, x.name, style_header)
            sheet.write(row_offset + 5, column_offset + date_column_offset + 3 * (x.id - 1), "M", style_sub_header)
            sheet.write(row_offset + 5, column_offset + date_column_offset + 3 * (x.id - 1) + 1, "AM", style_sub_header)
            sheet.write(row_offset + 5, column_offset + date_column_offset + 3 * (x.id - 1) + 2, "N", style_sub_header)

        '''
        i = 40
        for x in sorted(Style.colour_map):
            style = XFStyle()
            pattern = Pattern()
            pattern.pattern = Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = Style.colour_map[x]
            style.pattern = pattern
            sheet.write(i, 1, x, style)
            i += 1
        '''

        pattern_pale_blue = Pattern()
        pattern_pale_blue.pattern = Pattern.SOLID_PATTERN
        pattern_pale_blue.pattern_fore_colour = Style.colour_map['pale_blue']

        pattern_light_yellow = Pattern()
        pattern_light_yellow.pattern = Pattern.SOLID_PATTERN
        pattern_light_yellow.pattern_fore_colour = Style.colour_map['light_yellow']

        pattern_ice_blue = Pattern()
        pattern_ice_blue.pattern = Pattern.SOLID_PATTERN
        pattern_ice_blue.pattern_fore_colour = Style.colour_map['ice_blue']

        pattern_light_green = Pattern()
        pattern_light_green.pattern = Pattern.SOLID_PATTERN
        pattern_light_green.pattern_fore_colour = Style.colour_map['light_green']

        pattern_ivory = Pattern()
        pattern_ivory.pattern = Pattern.SOLID_PATTERN
        pattern_ivory.pattern_fore_colour = Style.colour_map['ivory']

        pattern_tan = Pattern()
        pattern_tan.pattern = Pattern.SOLID_PATTERN
        pattern_tan.pattern_fore_colour = Style.colour_map['tan']

        pattern_gold = Pattern()
        pattern_gold.pattern = Pattern.SOLID_PATTERN
        pattern_gold.pattern_fore_colour = Style.colour_map['gold']

        def __cell_colouration__(style, current_activity):
            if current_activity is Activity.CONSULTATION:
                style.pattern = pattern_pale_blue
            elif current_activity is Activity.DIALYSIS:
                style.pattern = pattern_ice_blue
            elif current_activity is Activity.NEPHROLOGY:
                style.pattern = pattern_light_green
            elif current_activity is Activity.OTHERS:
                style.pattern = pattern_tan
            elif current_activity is Activity.OBLIGATION:
                style.pattern = pattern_ivory
            elif current_activity is Activity.OBLIGATION_WEEKEND:
                style.pattern = pattern_light_yellow
            elif current_activity is Activity.OBLIGATION_HOLIDAY:
                style.pattern = pattern_gold
            else:
                style.pattern = Pattern()
            return style

        last_day = calendar.monthrange(self.year, self.month)[1]
        for x in range(1, last_day + 1):
            current_date = date(self.year, self.month, x)
            current_daily_planning = self.daily_plannings[current_date]

            # build date and date status columns
            sheet.write(row_offset + 5 + x, column_offset, "{0}. {1}".format(self.human_readable_days[current_daily_planning.weekday][0:3].lower(), x), style_date)
            if current_daily_planning.weekday in [5, 6]:
                sheet.write(row_offset + 5 + x, column_offset + 1, "WK", style_date_status)
            elif not current_daily_planning.is_working_day:
                sheet.write(row_offset + 5 + x, column_offset + 1, "Férié", style_date_status)
            else:
                sheet.write(row_offset + 5 + x, column_offset + 1, "", style_date_status)

            '''
            easyxf(
                 'font: bold 1, name Tahoma, height 160;'
                 'align: vertical center, horizontal center, wrap on;'
                 'borders: left thin, right thin, top thin, bottom thin;'
                 'pattern: pattern solid, pattern_fore_colour green, pattern_back_colour green'
                 )
            '''
            
            # fill in month planning
            for y in Database.team():
                current_activity = current_daily_planning.__get_activity__(TimeSlot.FIRST_SHIFT, y)
                sheet.write(row_offset + 5 + x, column_offset + date_column_offset + 3 * (y.id - 1), self.human_readable_activities[current_activity] if current_activity else "", __cell_colouration__(style_cell_normal, current_activity))
                current_activity = current_daily_planning.__get_activity__(TimeSlot.SECOND_SHIFT, y)
                sheet.write(row_offset + 5 + x, column_offset + date_column_offset + 1 + 3 * (y.id - 1), self.human_readable_activities[current_activity] if current_activity else "", __cell_colouration__(style_cell_normal, current_activity))
                current_activity = current_daily_planning.__get_activity__(TimeSlot.THIRD_SHIFT, y)
                sheet.write(row_offset + 5 + x, column_offset + date_column_offset + 2 + 3 * (y.id - 1), self.human_readable_activities[current_activity] if current_activity else "", __cell_colouration__(style_cell_right, current_activity))

        # patch table bottom border
        for x in range(0, table_width + 1):
            sheet.write(row_offset + 5 + (last_day + 1), column_offset + x, "", style_cell_top)

        book.save(r"C:\Temp\nephro-planner\new.xls")







































