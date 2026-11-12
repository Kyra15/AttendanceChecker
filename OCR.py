import pandas as pd
import numpy as np
import re






text = '''
Thu Nov 5, 2026
Teacher Absence - Unexcused
2
Application Innovation HON
Thu Nov 5, 2026
Activity (Other)
6-8
View Classes
Mon Nov 2, 2026
Excused Absence (Illness)
1-8
View Classes
Thu Oct 29, 2026
Excused Absence
5-8
View Classes
Wed Oct 28, 2026
Excused Absence
1
US Government & Politics AP
Tue Oct 27, 2026
Activity (Acad/College Advising Visit)
5
English Lit & Comp AP
Mon Oct 26, 2026
Activity (Internship)
1-7
View Classes
Mon Oct 19, 2026
Activity (Acad/College Advising Visit)
2
Application Innovation HON
Fri Oct 16, 2026
Activity (In School Activity)
5
English Lit & Comp AP
Thu Oct 15, 2026
Excused Absence
1
US Government & Politics AP
Thu Oct 15, 2026
Tardy - Excused
2
Application Innovation HON
Tue Oct 13, 2026
Activity (Acad/College Advising Visit)
2
Application Innovation HON
Mon Oct 12, 2026
Excused Absence
1-3
View Classes
Fri Oct 9, 2026
Excused Absence
1
US Government & Politics AP
Fri Oct 9, 2026
Tardy - Excused
2
Application Innovation HON
Thu Oct 8, 2026
Excused Absence (Illness)
1-8
View Classes
Wed Oct 7, 2026
Teacher Absence - Unexcused
7
Macroeconomics AP
Mon Oct 5, 2026
Activity (College Visitations)
4
Physics C: Elect & Mag AP
Thu Oct 1, 2026
Teacher Absence - Unexcused
7
Macroeconomics AP
Mon Sep 28, 2026
Activity (College Visitations)
6
Calculus BC Competition AP
Fri Sep 25, 2026
Excused Absence
1-2
View Classes
Fri Sep 25, 2026
Activity (College Visitations)
3
Multivariable Calculus HH
Thu Sep 24, 2026
Activity (In School Activity)
1-3 & 5
View Classes
Fri Sep 18, 2026
Activity (In School Activity)
5
English Lit & Comp AP
Tue Sep 15, 2026
Activity (In School Activity)
1-2
View Classes
Tue Sep 15, 2026
Teacher Absence - Unexcused
3
Multivariable Calculus HH
Mon Sep 14, 2026
Excused Absence
3
Multivariable Calculus HH
Mon Sep 14, 2026
Tardy - Excused
4
Physics C: Elect & Mag AP
Wed Sep 9, 2026
Activity (In School Activity)
7
Macroeconomics AP
Thu Sep 3, 2026
Activity (In School Activity)
1
US Government & Politics AP
Fri Aug 28, 2026
Activity (In School Activity)
3
Multivariable Calculus HH
'''


line_lst = text.split("\n")[1:-1]
# print(line_lst, len(line_lst))

reshaped_data = np.array(line_lst).reshape(-1, 4)
df = pd.DataFrame(reshaped_data, columns=["Date", "Absence", "Period", "Class"])
# print(df.head(7))

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

