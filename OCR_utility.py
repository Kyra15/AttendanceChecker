import pandas as pd
import numpy as np
import re

import pillow_heif
import cohere


# call cohere ocr api with prompt
text = ''''''

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

