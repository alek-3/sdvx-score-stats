import csv
import os
import openpyxl
import datetime

class Stats:
    def show_score_stats(self, file_name):
        csv_path = os.path.join("scoresheet", file_name)
        record_date = self.filename_to_date(file_name)
        self.get_play_count(csv_path)
        averages = self.calc_avarage(csv_path)
        self.write_excel(record_date, averages)



    def calc_avarage(self, csv_path):
        """レベルごとの平均点を計算し、出力する"""
        with open(csv_path, "r", encoding="utf-8") as f:
            r = csv.DictReader(f, delimiter=",")
            level_score_dict = {} # 辞書型
            level_list = []
            for row in r:
                music_level = int(row["楽曲レベル"])
                score = int(row["ハイスコア"])
                if music_level not in level_list:
                    level_score_dict[music_level] = {"譜面数": 1, "スコア合計": score}
                    level_list.append(music_level)
                else:
                    target_level_scores = level_score_dict[music_level]
                    target_level_scores["譜面数"] += 1
                    target_level_scores["スコア合計"] += score
                    level_score_dict[music_level] = target_level_scores
            for level, score in level_score_dict.items():
                level_score_dict[level]["平均スコア"] = score["スコア合計"] / score["譜面数"]

            print(sorted(level_score_dict.items()))
            print(sorted(level_score_dict.items())[16][1]['平均スコア'])
            return sorted(level_score_dict.items())



    def get_play_count(self, csv_path):
        """プレーした譜面の合計回数（投入クレジット数ではない）を出力する"""
        with open(csv_path, "r", encoding="utf-8") as f:
            r = csv.DictReader(f, delimiter=",")
            play_count = 0
            for row in r:
                play_count += int(row["プレー回数"])
            print("譜面プレー回数：{play_count}".format(play_count=play_count))

    def write_excel(self, record_date, averages):
        """日付と平均スコアの推移をExcelシートに書きこむ"""
        wb = openpyxl.load_workbook('sdvx_score_averages.xlsx')
        sheet = wb.active

        # 一列目
        sheet.cell(row=file_number + 1, column=1).value = record_date

        # 二行目以降
        # 二列目以降
        level = 1
        for average in averages:
            sheet.cell(row=file_number + 1, column=level + 1).value = average[1]['平均スコア']
            level += 1

        wb.save('sdvx_score_averages.xlsx')

    def write_header(self):
        wb = openpyxl.load_workbook('sdvx_score_averages.xlsx')
        sheet = wb.active
        sheet.cell(row=1, column=1).value = '日付＼レベル'
        sheet.column_dimensions['A'].width = 13
        for col in range(2,22):
            sheet.cell(row=1, column=col).value = col - 1

        wb.save('sdvx_score_averages.xlsx')

    def filename_to_date(self, filename):
        """日付を表す文字列を日付形式に変換する？(例:'score20180616')"""
        date_str = filename[5:13]
        record_date = datetime.datetime.strptime(date_str, '%Y%m%d')
        return record_date.date()






stats = Stats()
files = os.listdir("scoresheet")
files_file = [f for f in files if os.path.isfile(os.path.join("scoresheet", f))]

stats.write_header()

# ファイル番号を行番号として使う
file_number = 1

for file in files_file:
    stats.show_score_stats(file)
    file_number += 1

