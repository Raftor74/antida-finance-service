from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY

from .base import QueryBuilder
from builders import ServiceBuilder
from models import Transaction
from services.category import Category


class TransactionQueryBuilder(QueryBuilder):
    table_name = Transaction.table

    def set_filter(self, user_id, query_filter: dict):
        self.filter_by_user(user_id) \
            .filter_by_category(query_filter) \
            .filter_by_datetime_range(query_filter) \
            .filter_by_datetime(query_filter)
        return self

    def filter_by_user(self, user_id):
        return self.where('account_id', user_id)

    def filter_by_datetime(self, query_filter: dict):
        datetime_code = query_filter.get('datetime')
        if datetime_code is None:
            return self

        current_date = datetime.today().date()
        current_week_start = current_date - timedelta(days=current_date.weekday() % 7)
        current_week_end = current_week_start + relativedelta(weeks=1)
        current_month_start = current_date + relativedelta(day=1)
        current_month_end = current_month_start + relativedelta(months=1)
        current_year_start = current_date + relativedelta(month=1, day=1)
        current_year_end = current_year_start + relativedelta(years=1)

        current_quarter_start = rrule(
            MONTHLY,
            bymonth=(1, 4, 7, 10),
            bysetpos=-1,
            dtstart=datetime(current_date.year, 1, 1),
            count=8
        )
        current_quarter_first_day = current_quarter_start.before(datetime.now())
        current_quarter_last_day = current_quarter_start.after(datetime.now())
        previous_quarter_first_day = current_quarter_first_day - relativedelta(months=3)

        if datetime_code == 'current_week':
            self.where('date_time', current_week_start, '>=')
            self.where('date_time', current_week_end, '<')
        elif datetime_code == 'last_week':
            last_week_start = current_week_start - timedelta(days=7)
            last_week_end = last_week_start + timedelta(days=7)
            self.where('date_time', last_week_start, '>=')
            self.where('date_time', last_week_end, '<')
        elif datetime_code == 'current_month':
            self.where('date_time', current_month_start, '>=')
            self.where('date_time', current_month_end, '<')
        elif datetime_code == 'last_month':
            last_month_start = current_month_start - relativedelta(months=1)
            self.where('date_time', last_month_start, '>=')
            self.where('date_time', current_month_start, '<')
        elif datetime_code == 'current_quarter':
            self.where('date_time', current_quarter_first_day, '>=')
            self.where('date_time', current_quarter_last_day, '<')
        elif datetime_code == 'previous_quarter':
            self.where('date_time', previous_quarter_first_day, '>=')
            self.where('date_time', current_quarter_first_day, '<')
        elif datetime_code == 'current_year':
            self.where('date_time', current_year_start, '>=')
            self.where('date_time', current_year_end, '<')
        elif datetime_code == 'last_year':
            last_year_start = current_year_start - relativedelta(years=1)
            self.where('date_time', last_year_start, '>=')
            self.where('date_time', current_year_start, '<')

        return self

    def filter_by_category(self, query_filter: dict):
        category_id = query_filter.get('category')
        if category_id is None:
            return self
        category_service = ServiceBuilder(Category).build()
        sub_categories = category_service.get_subcategories(category_id, ['id'])
        categories_pk = [sub_category['id'] for sub_category in sub_categories]
        categories_pk.append(category_id)
        categories_pk = list(map(str, categories_pk))
        placeholder = ','.join(categories_pk)
        value_placeholder = f'({placeholder})'
        return self.where_raw('category_id', value_placeholder, 'IN')

    def filter_by_datetime_range(self, query_filter: dict):
        datetime_from = query_filter.get('datetime_from')
        datetime_to = query_filter.get('datetime_to')
        if datetime_from:
            self.where('date_time', datetime_from, '>=')
        if datetime_to:
            self.where('date_time', datetime_to, '<=')
        return self
