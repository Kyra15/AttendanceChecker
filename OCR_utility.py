import pandas as pd
import numpy as np
import re
import io

import pillow_heif
import cohere


# call cohere ocr api with prompt
# text ='''Tue Sep 15, 2026, Activity (In School Activity), 1-2, View Classes\n
# Tue Sep 15, 2026, Teacher Absence - Unexcused, 3, Multivariable Calculus HH\n
# Mon Sep 14, 2026, Excused Absence, 3, Multivariable Calculus HH\n
# Mon Sep 14, 2026, Tardy - Excused, 4, Physics C: Elect & Mag AP\n
# Wed Sep 9, 2026, Activity (In School Activity), 7, Macroeconomics AP\n
# Thu Sep 3, 2026, Activity (In School Activity), 1, US Government & Politics AP\n
# Fri Aug 28, 2026, Activity (In School Activity), 3, Multivariable Calculus HH'''

# maybe split on the year? need to figure out how to read this 
# bc rn its a csv but the commas in the date throw it off
# or i genuinely just ignore the date LMAO

# line_lst = text.split("\n")[1:-1]
# # print(line_lst, len(line_lst))

# reshaped_data = np.array(line_lst).reshape(-1, 4)
# df = pd.DataFrame(reshaped_data, columns=["Date", "Absence", "Period", "Class"])
# # print(df.head(7))


def init_csv(text):

    df = pd.read_csv(io.StringIO(text), names=["Date", "Absence", "Period", "Class"], sep='|')

    filter_df = df[~df["Absence"].astype(str).str.contains("Activity", na=False)]
    filter_df = filter_df[~filter_df["Absence"].astype(str).str.contains("Tardy")]
    filter_df = filter_df.drop(columns=["Date", "Class"])

    return filter_df
# print(filter_df.head(7))


# i need to parse the periods and
# then reorganize so that it’s for period 2, its this count
# so maybe i write out the periods separated by commas and
# then just look for if it includes it yk

def expand_range(match):
    start = int(match.group(1))
    end = int(match.group(2))
    return ", ".join(str(n) for n in range(start, end + 1))


def parse_num(text):
   text_list = text.split("&")
   text = ", ".join(text_list)

   pattern = r"^(\d+)-(\d+)$"
   final = re.sub(pattern, expand_range, text)
   return final


# loop through df, run parse num on every period column, then replace the period column with the final
def count_absences(filter_df):
    filter_df["Parsed_Periods"] = filter_df["Period"].apply(parse_num)

    final_counts = []
    for i in range(7):
        final_counts.append(int(filter_df["Parsed_Periods"].str.count(str(i+1)).sum()))

    return final_counts

