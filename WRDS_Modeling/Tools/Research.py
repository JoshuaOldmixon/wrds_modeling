import pandas as pd
from datetime import date
import wrds as w
from dateutil.relativedelta import relativedelta

class wrdsData:

    def __init__(self,symbol,start):
        
        #               Change Login To Use
        
        wrds = w.Connection(wrds_username=*******)
        
        
        p = {'symbol': symbol, 'start': start}
        ohlc = wrds.raw_sql("""select prcod, prchd, prcld, prccd, tic, datadate
                                    from comp_na_daily_all.secd
                                    where tic = %(symbol)s
                                    and datadate>=%(start)s""",
                                    params=p,
                                    date_cols=['date'])

        df = pd.DataFrame(ohlc).reset_index().drop(columns='index').rename(columns={"prcod": "open", "prchd": "high", "prcld": "low", "prccd": "close"})
        
        self.table = df

        

#               Milisecond data from NYSE

#ms_data = wrds.raw_sql("""select *
#                            from taqm_2022.ctm_2022
#                            where sym_root = %(symbol)s
#                            and date>=%(start)s""",
#                            params=p,
#                            date_cols=['date'])

#               NOT OHLC DATA
