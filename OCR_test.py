import pandas as pd
import numpy as np
import re
import io

import pillow_heif
import cohere


# call cohere ocr api with prompt
text ='''| Mon Nov 16, 2026 | Activity (Internship) | 1-5 | View Classes |\n| Wed Nov 11, 2026 | Excused Absence | 4-5 | View Classes |\n| Thu Nov 5, 2026 | Teacher Absence - Unexcused | 2 | Application Innovation HON |\n| Thu Nov 5, 2026 | Activity (Other) | 6-8 | View Classes |\n| Mon Nov 2, 2026 | Excused Absence (Illness) | 1-8 | View Classes |\n| Thu Oct 29, 2026 | Excused Absence | 5-8 | View Classes |\n| Wed Oct 28, 2026 | Excused Absence | 1 | US Government & Politics AP |\n| Tue Oct 27, 2026 | Activity (Acad/College Advising Visit) | 5 | English Lit & Comp AP |\n| Mon Oct 26, 2026 | Activity (Internship) | 1-7 | View Classes |\n| Mon Oct 19, 2026 | Activity (Acad/College Advising Visit) | 2 | Application Innovation HON |\n| Fri Oct 16, 2026 | Activity (In School Activity) | 5 | English Lit & Comp AP |\n| Thu Oct 15, 2026 | Excused Absence | 1 | US Government & Politics AP |\n| Thu Oct 15, 2026 | Tardy - Excused | 2 | Application Innovation HON |\n| Tue Oct 13, 2026 | Activity (Acad/College Advising Visit) | 2 | Application Innovation HON |\n| Mon Oct 12, 2026 | Excused Absence | 1-3 | View Classes |\n| Fri Oct 9, 2026 | Excused Absence | 1 | US Government & Politics AP |\n| Fri Oct 9, 2026 | Tardy - Excused | 2 | Application Innovation HON |\n| Thu Oct 8, 2026 | Excused Absence (Illness) | 1-8 | View Classes |\n| Wed Oct 7, 2026 | Teacher Absence - Unexcused | 7 | Macroeconomics AP |\n| Mon Oct 5, 2026 | Activity (College Visitations) | 4 | Physics C: Elect & Mag AP |\n| Thu Oct 1, 2026 | Teacher Absence - Unexcused | 7 | Macroeconomics AP |\n| Mon Sep 28, 2026 | Activity (College Visitations) | 6 | Calculus BC Competition AP |\n| Fri Sep 25, 2026 | Excused Absence | 1-2 | View Classes |\n| Fri Sep 25, 2026 | Activity (College Visitations) | 3 | Multivariable Calculus HH |\n| Thu Sep 24, 2026 | Activity (In School Activity) | 1-3 & 5 | View Classes |\n| Fri Sep 18, 2026 | Activity (In School Activity) | 5 | English Lit & Comp AP |'''

# maybe split on the year? need to figure out how to read this 
# bc rn its a csv but the commas in the date throw it off
# or i genuinely just ignore the date LMAO

# line_lst = text.split("\n")[1:-1]
# # print(line_lst, len(line_lst))

# reshaped_data = np.array(line_lst).reshape(-1, 4)
# df = pd.DataFrame(reshaped_data, columns=["Date", "Absence", "Period", "Class"])
# # print(df.head(7))

df = pd.read_csv(io.StringIO(text), names=["Date", "Absence", "Period", "Class"], sep="|")

filter_df = df[~df["Absence"].str.contains("Activity")]
filter_df = filter_df[~filter_df["Absence"].str.contains("Tardy")]
filter_df = filter_df.drop(columns=["Date", "Class"])
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
filter_df["Parsed_Periods"] = filter_df["Period"].apply(parse_num)

final_counts = []
for i in range(7):
    final_counts.append(filter_df["Parsed_Periods"].str.count(str(i+1)).sum())

print(final_counts)

